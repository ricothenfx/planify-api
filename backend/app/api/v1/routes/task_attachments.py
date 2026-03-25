from fastapi import APIRouter, Depends, UploadFile, File
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.database import get_db
from app.core.dependencies import get_current_user
from app.models.user import User
from app.schemas.task_attachment import AttachmentResponse
from app.services.task_attachment_service import TaskAttachmentService

router = APIRouter(
    prefix="/projects/{project_id}/tasks/{task_id}/attachments",
    tags=["Task Attachments"],
)


@router.post("", response_model=AttachmentResponse, status_code=201)
async def upload_attachment(
    project_id: str,
    task_id: str,
    file: UploadFile = File(...),
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    service = TaskAttachmentService(db)
    return await service.upload(project_id=project_id, task_id=task_id, file=file, user_id=current_user.id)


@router.get("", response_model=list[AttachmentResponse])
async def get_attachments(
    project_id: str,
    task_id: str,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    service = TaskAttachmentService(db)
    return await service.get_all(project_id=project_id, task_id=task_id)


@router.delete("/{attachment_id}", status_code=204)
async def delete_attachment(
    project_id: str,
    task_id: str,
    attachment_id: str,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    service = TaskAttachmentService(db)
    await service.delete(project_id=project_id, task_id=task_id, attachment_id=attachment_id, user_id=current_user.id)