from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.database import get_db
from app.core.dependencies import get_current_user
from app.models.user import User
from app.schemas.activity import ActivityResponse
from app.services.activity_service import ActivityService
from app.services.project_service import ProjectService


router = APIRouter(
    prefix="/projects/{project_id}/activities",
    tags=["Activities"],
)


@router.get("", response_model=list[ActivityResponse])
async def get_activities(
    project_id: str,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    await ProjectService(db).get_by_id(project_id=project_id, owner_id=current_user.id)
    return await ActivityService(db).get_project_activities(project_id=project_id)