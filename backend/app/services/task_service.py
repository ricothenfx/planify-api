from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import HTTPException, status
from app.repositories.task_repository import TaskRepository
from app.repositories.project_repository import ProjectRepository
from app.schemas.task import TaskCreate, TaskUpdate, TaskResponse


class TaskService:
    def __init__(self, db: AsyncSession):
        self.task_repo = TaskRepository(db)
        self.project_repo = ProjectRepository(db)
    
    async def create(self, project_id: str, data: TaskCreate, owner_id: str) -> TaskResponse:
        await self._verify_project_owner(project_id, owner_id)
        task_data = data.model_dump()
        task = await self.task_repo.create(project_id=project_id, data=task_data)
        return TaskResponse.model_validate(task)
    
    async def get_all(self, project_id: str, owner_id: str) -> list[TaskResponse]:
        await self._verify_project_owner(project_id, owner_id)
        tasks = await self.task_repo.get_all_by_project(project_id)
        return [TaskResponse.model_validate(t) for t in tasks]
    
    async def get_by_id(self, project_id: str, task_id: str, owner_id: str) -> TaskResponse:
        await self._verify_project_owner(project_id, owner_id)
        task = await self._get_task_in_project(task_id, project_id)
        return TaskResponse.model_validate(task)
    
    async def update(self, project_id: str, task_id: str, data: TaskUpdate, owner_id: str) -> TaskResponse:
        await self._verify_project_owner(project_id, owner_id)
        task = await self._get_task_in_project(task_id, project_id)
        update_data = data.model_dump(exclude_none=True)
        task = await self.task_repo.update(task, update_data)
        return TaskResponse.model_validate(task)
    
    async def delete(self, project_id: str, task_id: str, owner_id: str) -> None:
        await self._verify_project_owner(project_id, owner_id)
        task = await self._get_task_in_project(task_id, project_id)
        await self.task_repo.delete(task)
    
    async def _verify_project_owner(self, project_id: str, owner_id: str):
        project = await self.project_repo.get_by_id(project_id)
        if not project:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Project not found",
            )
        if project.owner_id != owner_id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Not authorized to access this project",
            )
        return project
    
    async def _get_task_in_project(self, task_id: str, project_id: str):
        task = await self.task_repo.get_by_id(task_id)
        if not task or task.project_id != project_id:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Task not found",
            )
        return task