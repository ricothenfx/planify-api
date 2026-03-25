from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import HTTPException, status
from app.repositories.task_comment_repository import TaskCommentRepository
from app.repositories.task_repository import TaskRepository
from app.repositories.project_repository import ProjectRepository
from app.schemas.task_comment import CommentCreate, CommentUpdate, CommentResponse
from app.services.activity_service import ActivityService
from app.core.websocket_manager import ws_manager


class TaskCommentService:
    def __init__(self, db: AsyncSession):
        self.comment_repo = TaskCommentRepository(db)
        self.task_repo = TaskRepository(db)
        self.project_repo = ProjectRepository(db)
        self.activity = ActivityService(db)

    async def create(
        self,
        project_id: str,
        task_id: str,
        data: CommentCreate,
        user_id: str,
    ) -> CommentResponse:
        await self._verify_task(project_id, task_id)
        comment = await self.comment_repo.create(
            task_id=task_id,
            user_id=user_id,
            content=data.content,
        )
        await self.activity.log(
            user_id=user_id,
            project_id=project_id,
            entity_type="comment",
            entity_id=comment.id,
            action="created",
            extra_data={"task_id": task_id},
        )
        await ws_manager.broadcast_to_project(project_id, {
            "type": "comment_created",
            "task_id": task_id,
            "comment_id": comment.id,
            "by_user": user_id,
        })
        return CommentResponse.model_validate(comment)

    async def get_all(
        self,
        project_id: str,
        task_id: str,
    ) -> list[CommentResponse]:
        await self._verify_task(project_id, task_id)
        comments = await self.comment_repo.get_all_by_task(task_id)
        return [CommentResponse.model_validate(c) for c in comments]

    async def update(
        self,
        project_id: str,
        task_id: str,
        comment_id: str,
        data: CommentUpdate,
        user_id: str,
    ) -> CommentResponse:
        await self._verify_task(project_id, task_id)
        # Check if user is owner of this comment
        comment = await self._get_and_verify_author(comment_id, user_id)
        comment = await self.comment_repo.update(comment, data.content)
        return CommentResponse.model_validate(comment)

    async def delete(
        self,
        project_id: str,
        task_id: str,
        comment_id: str,
        user_id: str,
    ) -> None:
        await self._verify_task(project_id, task_id)
        # Check if user is owner of this comment
        comment = await self._get_and_verify_author(comment_id, user_id)
        await self.comment_repo.delete(comment)

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

    async def _get_and_verify_author(self, comment_id: str, user_id: str):
        comment = await self.comment_repo.get_by_id(comment_id)
        if not comment:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Comment not found",
            )
        if comment.user_id != user_id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Not authorized to modify this comment",
            )
        return comment