from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.models.task_attachment import TaskAttachment


class TaskAttachmentRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_by_id(self, attachment_id: str) -> TaskAttachment | None:
        result = await self.db.execute(
            select(TaskAttachment).where(TaskAttachment.id == attachment_id)
        )
        return result.scalar_one_or_none()

    async def get_all_by_task(self, task_id: str) -> list[TaskAttachment]:
        result = await self.db.execute(
            select(TaskAttachment)
            .where(TaskAttachment.task_id == task_id)
            .order_by(TaskAttachment.created_at.desc())
        )
        return list(result.scalars().all())

    async def create(
        self,
        task_id: str,
        user_id: str,
        filename: str,
        file_url: str,
        public_id: str,
        file_size: int,
        mime_type: str,
    ) -> TaskAttachment:
        attachment = TaskAttachment(
            task_id=task_id,
            user_id=user_id,
            filename=filename,
            file_url=file_url,
            public_id=public_id,
            file_size=file_size,
            mime_type=mime_type,
        )
        self.db.add(attachment)
        await self.db.flush()
        await self.db.refresh(attachment)
        return attachment

    async def delete(self, attachment: TaskAttachment) -> None:
        await self.db.delete(attachment)
        await self.db.flush()