from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.models.activity import Activity


class ActivityRepository:
    def __init__(self, db: AsyncSession):
        self.db = db
    
    async def create(
        self,
        user_id: str,
        project_id: str,
        entity_type: str,
        entity_id: str,
        action: str,
        extra_data: dict | None = None,
    ) -> Activity:
        activity = Activity(
            user_id=user_id,
            project_id=project_id,
            entity_type=entity_type,
            entity_id=entity_id,
            action=action,
            extra_data=extra_data,
        )
        self.db.add(activity)
        await self.db.flush()
        await self.db.refresh(activity)
        return activity
    
    async def get_by_project(self, project_id: str) -> list[Activity]:
        result = await self.db.execute(
            select(Activity)
            .where(Activity.project_id == project_id)
            .order_by(Activity.created_at.desc())
        )
        return list(result.scalars().all())