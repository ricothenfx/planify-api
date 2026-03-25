from datetime import datetime, timezone, timedelta
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.models.password_reset import PasswordReset
import secrets


class PasswordResetRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def create(self, user_id: str) -> PasswordReset:
        # Expires in 1 hour
        expires_at = datetime.now(timezone.utc) + timedelta(hours=1)
        token = secrets.token_urlsafe(32)

        reset = PasswordReset(
            user_id=user_id,
            token=token,
            expires_at=expires_at,
        )
        self.db.add(reset)
        await self.db.flush()
        await self.db.refresh(reset)
        return reset

    async def get_by_token(self, token: str) -> PasswordReset | None:
        result = await self.db.execute(
            select(PasswordReset).where(PasswordReset.token == token)
        )
        return result.scalar_one_or_none()

    async def mark_as_used(self, reset: PasswordReset) -> None:
        reset.is_used = True
        await self.db.flush()