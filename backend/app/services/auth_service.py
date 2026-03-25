from datetime import datetime, timezone, timedelta
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import HTTPException, status
from jose import JWTError
from app.repositories.user_repository import UserRepository
from app.schemas.auth import LoginRequest, TokenResponse, RefreshTokenRequest
from app.core.security import (
    verify_password,
    create_access_token,
    create_refresh_token,
    decode_access_token,
    hash_password,
)
from app.core.config import settings


class AuthService:
    def __init__(self, db: AsyncSession):
        self.repo = UserRepository(db)
        self.db = db
    
    async def login(self, data: LoginRequest) -> TokenResponse:
        user = await self.repo.get_by_email(data.email)

        # Check if user registered
        if not user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid email or password",
                headers={"WWW-Authenticate": "Bearer"},
            )
        
        # Check if user locked
        if user.locked_until:
            locked_until = user.locked_until
            if locked_until.tzinfo is None:
                locked_until = locked_until.replace(tzinfo=timezone.utc)
            
            now = datetime.now(timezone.utc)
            if locked_until > now:
                remaining_seconds = int((locked_until - now).total_seconds())
                remaining_minutes = remaining_seconds // 60
                remaining_secs = remaining_seconds % 60
                raise HTTPException(
                    status_code=status.HTTP_403_FORBIDDEN,
                    detail=f"Account locked. Try again in {remaining_minutes} minutes {remaining_secs} seconds",
                )
            else:
                # Lock expired — reset automatically
                await self.repo.reset_login_attempts(user.id)
                await self.db.commit()
        
        # Check the password
        if not verify_password(data.password, user.hashed_password):
            attempts = await self.repo.increment_failed_attempts(user.id)

            # Commit first before raise exception
            await self.db.commit()

            # If user's attempt hit max
            if attempts >= settings.MAX_LOGIN_ATTEMPTS:
                lock_until = datetime.now(timezone.utc) + timedelta(
                    minutes=settings.LOCKOUT_DURATION_MINUTES
                )
                await self.repo.lock_account(user.id, lock_until)
                await self.db.commit()
                raise HTTPException(
                    status_code=status.HTTP_403_FORBIDDEN,
                    detail=f"Account locked due to too many failed attempts. Try again in {settings.LOCKOUT_DURATION_MINUTES} minutes",
                )

            # If user's attempt not hit max yet
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail=f"Invalid email or password. {settings.MAX_LOGIN_ATTEMPTS - attempts} attempts remaining",
                headers={"WWW-Authenticate": "Bearer"},
            )
        
        # Check if user inactive
        if not user.is_active:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Account is inactive",
            )
        
        # Login success — reset failed attempts
        await self.repo.reset_login_attempts(user.id)
        
        access_token = create_access_token(data={"sub": str(user.id)})
        refresh_token = create_refresh_token(data={"sub": str(user.id)})

        return TokenResponse(
            access_token=access_token,
            refresh_token=refresh_token,
        )
    
    async def refresh(self, data: RefreshTokenRequest) -> TokenResponse:
        credentials_exception = HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired refresh token",
            headers={"WWW-Authenticate": "Bearer"},
        )

        try:
            payload = decode_access_token(data.refresh_token)
            user_id: str = payload.get("sub")
            token_type: str = payload.get("type")

            if user_id is None or token_type != "refresh":
                raise credentials_exception
        
        except JWTError:
            raise credentials_exception
        
        user = await self.repo.get_by_id(user_id=user_id)
        if not user or not user.is_active:
            raise credentials_exception
        
        access_token = create_access_token(data={"sub": str(user.id)})
        refresh_token = create_refresh_token(data={"sub": str(user.id)})

        return TokenResponse(
            access_token=access_token,
            refresh_token=refresh_token,
        )
    
    async def change_password(
        self,
        user_id: str,
        current_password: str,
        new_password: str,
    ) -> None:
        user = await self.repo.get_by_id(user_id)

        # Check if old password correct
        if not verify_password(current_password, user.hashed_password):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Current password is incorrect",
            )

        # New password must be different of old password
        if current_password == new_password:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="New password must be different from current password",
            )

        await self.repo.update_password(user_id, hash_password(new_password))