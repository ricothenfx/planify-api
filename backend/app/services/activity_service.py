from sqlalchemy.ext.asyncio import AsyncSession
from app.repositories.activity_repository import ActivityRepository
from app.models.activity import Activity


class ActivityService:
    def __init__(self, db: AsyncSession):
        self.repo = ActivityRepository(db)
    
    async def log(
        self,
        user_id: str,
        project_id: str,
        entity_type: str,
        entity_id: str,
        action: str,
        extra_data: dict | None = None,
    ) -> Activity:
        return await self.repo.create(
            user_id=user_id,
            project_id=project_id,
            entity_type=entity_type,
            entity_id=entity_id,
            action=action,
            extra_data=extra_data,
        )
    
    async def get_project_activities(self, project_id: str) -> list[Activity]:
        return await self.repo.get_by_project(project_id=project_id)