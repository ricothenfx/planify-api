from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.models.task_comment import TaskComment


class TaskCommentRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_by_id(self, comment_id: str) -> TaskComment | None:
        result = await self.db.execute(
            select(TaskComment).where(TaskComment.id == comment_id)
        )
        return result.scalar_one_or_none()

    async def get_all_by_task(self, task_id: str) -> list[TaskComment]:
        result = await self.db.execute(
            select(TaskComment)
            .where(TaskComment.task_id == task_id)
            .order_by(TaskComment.created_at.asc())
        )
        return list(result.scalars().all())

    async def create(self, task_id: str, user_id: str, content: str) -> TaskComment:
        comment = TaskComment(
            task_id=task_id,
            user_id=user_id,
            content=content,
        )
        self.db.add(comment)
        await self.db.flush()
        await self.db.refresh(comment)
        return comment

    async def update(self, comment: TaskComment, content: str) -> TaskComment:
        comment.content = content
        await self.db.flush()
        await self.db.refresh(comment)
        return comment

    async def delete(self, comment: TaskComment) -> None:
        await self.db.delete(comment)
        await self.db.flush()