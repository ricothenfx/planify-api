from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.models.task import Task


class TaskRepository:
    def __init__(self, db: AsyncSession):
        self.db = db
    
    async def get_by_id(self, task_id: str) -> Taks | None:
        result = await self.db.execute(select(Task).where(Task.id == task_id))
        return result.scalar_one_or_none()
    
    async def get_all_by_project(self, project_id: str) -> list[Task]:
        result = await self.db.execute(select(Task).where(Task.project_id == project_id))
        return list(result.scalars().all())
    
    async def create(self, project_id: str, data: dict) -> Task:
        task = Task(project_id=project_id, **data)
        self.db.add(task)
        await self.db.flush()
        await self.db.refresh(task)
        return task
    
    async def update(self, task: Task, data: dict) -> Task:
        for key, value in data.items():
            setattr(task, key, value)
        await self.db.flush()
        await self.db.refresh(task)
        return task
    
    async def delete(self, task: Task) -> None:
        await self.db.delete(task)
        await self.db.flush()