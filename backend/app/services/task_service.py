from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import HTTPException, status
from app.repositories.task_repository import TaskRepository
from app.repositories.project_repository import ProjectRepository
from app.schemas.task import TaskCreate, TaskUpdate, TaskResponse
from app.schemas.pagination import PaginatedResponse
from app.services.activity_service import ActivityService
from app.services.ai_service import AIService
from app.core.websocket_manager import ws_manager
from app.models.task import TaskStatus, TaskPriority


class TaskService:
    def __init__(self, db: AsyncSession):
        self.task_repo = TaskRepository(db)
        self.project_repo = ProjectRepository(db)
        self.activity = ActivityService(db)
    
    async def create(self, project_id: str, data: TaskCreate, owner_id: str) -> TaskResponse:
        await self._verify_project_owner(project_id, owner_id)
        task_data = data.model_dump()
        task = await self.task_repo.create(project_id=project_id, data=task_data)
        await self.activity.log(
            user_id=owner_id,
            project_id=project_id,
            entity_type="task",
            entity_id=task.id,
            action="created",
            extra_data={"title": task.title},
        )
        await ws_manager.broadcast_to_project(
            project_id=project_id,
            message={
                "type": "task_created",
                "task_id": task.id,
                "title": task.title,
                "by_user": owner_id,
            }
        )
        return TaskResponse.model_validate(task)
    
    async def get_all(
        self,
        project_id: str,
        owner_id: str,
        page: int = 1,
        limit: int = 10,
        status: TaskStatus | None = None,
        priority: TaskPriority | None = None,
        assignee_id: str | None = None,
        sort: str = "created_at",
        order: str = "desc",
    ):
        await self._verify_project_owner(project_id, owner_id)
        tasks, total = await self.task_repo.get_all_by_project(
            project_id=project_id,
            page=page,
            limit=limit,
            status=status,
            priority=priority,
            assignee_id=assignee_id,
            sort=sort,
            order=order,
        )
        return PaginatedResponse.create(
            items=[TaskResponse.model_validate(t) for t in tasks],
            total=total,
            page=page,
            limit=limit,
        )
    
    async def get_by_id(self, project_id: str, task_id: str, owner_id: str) -> TaskResponse:
        await self._verify_project_owner(project_id, owner_id)
        task = await self._get_task_in_project(task_id, project_id)
        return TaskResponse.model_validate(task)
    
    async def update(self, project_id: str, task_id: str, data: TaskUpdate, owner_id: str) -> dict:
        project = await self._verify_project_owner(project_id, owner_id)
        task = await self._get_task_in_project(task_id, project_id)
        old_status = task.status
        update_data = data.model_dump(exclude_none=True)
        task = await self.task_repo.update(task, update_data)
        extra = update_data.copy()
        if "status" in update_data:
            extra["old_status"] = old_status
        await self.activity.log(
            user_id=owner_id,
            project_id=project_id,
            entity_type="task",
            entity_id=task.id,
            action="updated",
            extra_data=extra,
        )
        await ws_manager.broadcast_to_project(
            project_id=project_id,
            message={
                "type": "task_updated",
                "task_id": task.id,
                "title": task.title,
                "changes": update_data,
                "by_user": owner_id,
            }
        )

        # Generate AI suggestions if status changed
        suggestions = []
        if "status" in update_data:
            try:
                ai_service = AIService()
                suggestions = await ai_service.suggest_next_actions(
                    task_title=task.title,
                    task_description=task.description,
                    new_status=task.status.value,
                    project_name=project.name,
                )
            except Exception:
                suggestions = []
        
        return {
            "task": TaskResponse.model_validate(task),
            "suggestions": suggestions,
        }
    
    async def delete(self, project_id: str, task_id: str, owner_id: str) -> None:
        await self._verify_project_owner(project_id, owner_id)
        task = await self._get_task_in_project(task_id, project_id)
        await self.activity.log(
            user_id=owner_id,
            project_id=project_id,
            entity_type="task",
            entity_id=task.id,
            action="deleted",
            extra_data={"title": task.title},
        )
        await ws_manager.broadcast_to_project(
            project_id=project_id,
            message={
                "type": "task_deleted",
                "task_id": task.id,
                "title": task.title,
                "by_user": owner_id,
            }
        )
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
    
    async def generate_ai_tasks(self, project_id: str, owner_id: str) -> list[TaskResponse]:
        project = await self._verify_project_owner(project_id, owner_id)

        ai_service = AIService()
        generated_tasks = await ai_service.generate_tasks(
            project_name=project.name,
            project_description=project.description,
        )

        created_tasks = []
        for task_data in generated_tasks:
            task = await self.task_repo.create(
                project_id=project_id,
                data={
                    "title": task_data["title"],
                    "description": task_data.get("description"),
                    "priority": task_data.get("priority", "medium"),
                },
            )
            await self.activity.log(
                user_id=owner_id,
                project_id=project_id,
                entity_type="task",
                entity_id=task.id,
                action="ai_generated",
                extra_data={"title": task.title},
            )
            created_tasks.append(TaskResponse.model_validate(task))
        
        await ws_manager.broadcast_to_project(
            project_id=project_id,
            message={
                "type": "ai_tasks_generated",
                "count": len(created_tasks),
                "by_user": owner_id,
            }
        )        
        return created_tasks