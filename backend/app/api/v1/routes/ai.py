from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.database import get_db
from app.core.dependencies import get_current_user
from app.models.user import User
from app.schemas.ai import GenerateTasksResponse
from app.services.task_service import TaskService


router = APIRouter(
    prefix="/ai",
    tags=["AI"],
)


@router.post("/projects/{project_id}/generate-tasks", response_model=GenerateTasksResponse)
async def generate_tasks(
    project_id: str,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user), 
):
    service = TaskService(db)
    tasks = await service.generate_ai_tasks(
        project_id=project_id,
        owner_id=current_user.id,
    )
    return GenerateTasksResponse(generated=len(tasks), tasks=tasks)