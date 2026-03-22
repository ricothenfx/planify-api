from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.database import get_db
from app.core.dependencies import get_current_user
from app.models.user import User
from app.schemas.task import TaskCreate, TaskUpdate, TaskResponse
from app.services.task_service import TaskService


router = APIRouter(
    prefix="/projects/{project_id}/tasks",
    tags=["Tasks"],
)


@router.post("", response_model=TaskResponse, status_code=201)
async def create_task(
    project_id: str,
    data: TaskCreate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    service = TaskService(db)
    return await service.create(project_id=project_id, data=data, owner_id=current_user.id)


@router.get("", response_model=list[TaskResponse])
async def get_tasks(
    project_id: str,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    service = TaskService(db)
    return await service.get_all(project_id=project_id, owner_id=current_user.id)


@router.get("/{task_id}", response_model=TaskResponse)
async def get_task(
    project_id: str,
    task_id: str,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    service = TaskService(db)
    return await service.get_by_id(project_id=project_id, task_id=task_id, owner_id=current_user.id)


@router.patch("/{task_id}", response_model=TaskResponse)
async def update_task(
    project_id: str,
    task_id: str,
    data: TaskUpdate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    service = TaskService(db)
    return await service.update(project_id=project_id, task_id=task_id, data=data, owner_id=current_user.id)


@router.delete("/{task_id}", status_code=204)
async def delete_task(
    project_id: str,
    task_id: str,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    service = TaskService(db)
    return await service.delete(project_id=project_id, task_id=task_id, owner_id=current_user.id)