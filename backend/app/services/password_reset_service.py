from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import HTTPException, status
from datetime import datetime, timezone
from app.repositories.password_reset_repository import PasswordResetRepository
from app.repositories.user_repository import UserRepository
from app.services.email_service import EmailService
from app.core.security import hash_password
from app.core.config import settings


class PasswordResetService:
    def __init__(self, db: AsyncSession):
        self.reset_repo = PasswordResetRepository(db)
        self.user_repo = UserRepository(db)
        self.email_service = EmailService()

    async def request_reset(self, email: str) -> None:
        user = await self.user_repo.get_by_email(email)

        # Always return success even email not exist: prevent user enumeration
        if not user:
            return

        reset = await self.reset_repo.create(user_id=user.id)
        reset_url = f"{settings.FRONTEND_URL}/reset-password?token={reset.token}"

        await self.email_service.send_password_reset(
            email=user.email,
            reset_url=reset_url,
        )

    async def reset_password(self, token: str, new_password: str) -> None:
        reset = await self.reset_repo.get_by_token(token)

        # Check if token exists
        if not reset:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Invalid or expired reset token",
            )

        # Check if token already used before
        if reset.is_used:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Reset token has already been used",
            )

        # Check if token has been expired
        expires_at = reset.expires_at
        if expires_at.tzinfo is None:
            expires_at = expires_at.replace(tzinfo=timezone.utc)
        if expires_at < datetime.now(timezone.utc):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Reset token has expired",
            )

        # Check if user exists
        user = await self.user_repo.get_by_id(reset.user_id)
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found",
            )

        # Update password
        user.hashed_password = hash_password(new_password)
        await self.reset_repo.mark_as_used(reset)