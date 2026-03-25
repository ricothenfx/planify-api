from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import HTTPException, UploadFile, status
from app.repositories.task_attachment_repository import TaskAttachmentRepository
from app.repositories.task_repository import TaskRepository
from app.repositories.project_repository import ProjectRepository
from app.schemas.task_attachment import AttachmentResponse
from app.services.cloudinary_service import CloudinaryService
from app.services.activity_service import ActivityService


class TaskAttachmentService:
    def __init__(self, db: AsyncSession):
        self.attachment_repo = TaskAttachmentRepository(db)
        self.task_repo = TaskRepository(db)
        self.project_repo = ProjectRepository(db)
        self.cloudinary = CloudinaryService()
        self.activity = ActivityService(db)

    async def upload(
        self,
        project_id: str,
        task_id: str,
        file: UploadFile,
        user_id: str,
    ) -> AttachmentResponse:
        await self._verify_task(project_id, task_id)

        upload_result = await self.cloudinary.upload(file)

        attachment = await self.attachment_repo.create(
            task_id=task_id,
            user_id=user_id,
            filename=file.filename,
            file_url=upload_result["file_url"],
            public_id=upload_result["public_id"],
            file_size=upload_result["file_size"],
            mime_type=file.content_type,
        )

        await self.activity.log(
            user_id=user_id,
            project_id=project_id,
            entity_type="attachment",
            entity_id=attachment.id,
            action="uploaded",
            extra_data={"filename": file.filename, "task_id": task_id},
        )

        return AttachmentResponse.model_validate(attachment)

    async def get_all(
        self,
        project_id: str,
        task_id: str,
    ) -> list[AttachmentResponse]:
        await self._verify_task(project_id, task_id)
        attachments = await self.attachment_repo.get_all_by_task(task_id)
        return [AttachmentResponse.model_validate(a) for a in attachments]

    async def delete(
        self,
        project_id: str,
        task_id: str,
        attachment_id: str,
        user_id: str,
    ) -> None:
        await self._verify_task(project_id, task_id)
        attachment = await self.attachment_repo.get_by_id(attachment_id)

        # Check if attachment exists
        if not attachment:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Attachment not found",
            )

        # Check if user is the owner
        if attachment.user_id != user_id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Not authorized to delete this attachment",
            )

        await self.cloudinary.delete(attachment.public_id)
        await self.attachment_repo.delete(attachment)

    async def _verify_task(self, project_id: str, task_id: str):
        project = await self.project_repo.get_by_id(project_id)
        if not project:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Project not found",
            )
        task = await self.task_repo.get_by_id(task_id)
        if not task or task.project_id != project_id:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Task not found",
            )
        return task