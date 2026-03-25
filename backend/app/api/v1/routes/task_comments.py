from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.database import get_db
from app.core.dependencies import get_current_user
from app.models.user import User
from app.schemas.task_comment import CommentCreate, CommentUpdate, CommentResponse
from app.services.task_comment_service import TaskCommentService

router = APIRouter(
    prefix="/projects/{project_id}/tasks/{task_id}/comments",
    tags=["Task Comments"],
)


@router.post("", response_model=CommentResponse, status_code=201)
async def create_comment(
    project_id: str,
    task_id: str,
    data: CommentCreate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    service = TaskCommentService(db)
    return await service.create(project_id=project_id, task_id=task_id, data=data, user_id=current_user.id)


@router.get("", response_model=list[CommentResponse])
async def get_comments(
    project_id: str,
    task_id: str,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    service = TaskCommentService(db)
    return await service.get_all(project_id=project_id, task_id=task_id)


@router.patch("/{comment_id}", response_model=CommentResponse)
async def update_comment(
    project_id: str,
    task_id: str,
    comment_id: str,
    data: CommentUpdate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    service = TaskCommentService(db)
    return await service.update(project_id=project_id, task_id=task_id, comment_id=comment_id, data=data, user_id=current_user.id)


@router.delete("/{comment_id}", status_code=204)
async def delete_comment(
    project_id: str,
    task_id: str,
    comment_id: str,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    service = TaskCommentService(db)
    await service.delete(project_id=project_id, task_id=task_id, comment_id=comment_id, user_id=current_user.id)