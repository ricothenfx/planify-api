from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.models.project import Project

class ProjectRepository:
    def __init__(self, db: AsyncSession):
        self.db = db
    
    async def get_by_id(self, project_id: str) -> Project | None:
        result = await self.db.execute(select(Project).where(Project.id == project_id))
        return result.scalar_one_or_none()
    
    async def get_all_by_owner(self, owner_id: str) -> list[Project]:
        result = await self.db.execute(select(Project).where(Project.owner_id == owner_id))
        return list(result.scalars().all())
    
    async def create(self, name: str, description: str | None, owner_id: str) -> Project:
        project = Project(
            name=name,
            description=description,
            owner_id=owner_id,
        )
        self.db.add(project)
        await self.db.flush()
        await self.db.refresh(project)
        return project
    
    async def update(self, project: Project, data: dict) -> Project:
        for key, value in data.items():
            setattr(project, key, value)
        await self.db.flush()
        await self.db.refresh(project)
        return project
    
    async def delete(self, project: Project) -> None:
        await self.db.delete(project)
        await self.db.flush()