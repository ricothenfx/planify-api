from datetime import datetime
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.models.user import User


class UserRepository:
    def __init__(self, db: AsyncSession):
        self.db = db
    
    async def get_by_id(self, user_id: str) -> User | None:
        result = await self.db.execute(select(User).where(User.id == user_id))
        return result.scalar_one_or_none()
    
    async def get_by_email(self, email: str) -> User | None:
        result = await self.db.execute(select(User).where(User.email == email))
        return result.scalar_one_or_none()
    
    async def get_by_username(self, username: str) -> User | None:
        result = await self.db.execute(select(User).where(User.username == username))
        return result.scalar_one_or_none()
    
    async def create(self, email: str, username: str, hashed_password: str) -> User:
        user = User(
            email=email,
            username=username,
            hashed_password=hashed_password,
        )
        self.db.add(user)
        await self.db.flush()
        await self.db.refresh(user)
        return user
    
    async def update_password(self, user_id: str, hashed_password: str) -> None:
        user = await self.get_by_id(user_id)
        if user:
            user.hashed_password = hashed_password
            await self.db.flush()
    
    async def increment_failed_attempts(self, user_id: str) -> int:
        user = await self.get_by_id(user_id)
        user.failed_login_attempts += 1
        await self.db.flush()
        return user.failed_login_attempts

    async def lock_account(self, user_id: str, until: datetime) -> None:
        user = await self.get_by_id(user_id)
        user.locked_until = until
        await self.db.flush()

    async def reset_login_attempts(self, user_id: str) -> None:
        user = await self.get_by_id(user_id)
        user.failed_login_attempts = 0
        user.locked_until = None
        await self.db.flush()