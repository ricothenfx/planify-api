from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.database import get_db
from app.core.dependencies import get_current_user
from app.models.user import User
from app.schemas.project_member import (
    AddMemberRequest,
    UpdateMemberRoleRequest,
    ProjectMemberResponse,
)
from app.services.project_member_service import ProjectMemberService


router = APIRouter(
    prefix="/projects/{project_id}/members",
    tags=["Project Members"],
)


@router.post("", response_model=ProjectMemberResponse, status_code=201)
async def add_member(
    project_id: str,
    data: AddMemberRequest,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    service = ProjectMemberService(db)
    return await service.add_member(project_id=project_id, data=data, current_user_id=current_user.id)


@router.get("", response_model=list[ProjectMemberResponse])
async def get_members(
    project_id: str,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    service = ProjectMemberService(db)
    return await service.get_members(project_id=project_id, current_user_id=current_user.id)


@router.patch("/{user_id}", response_model=ProjectMemberResponse)
async def update_member_role(
    project_id: str,
    user_id: str,
    data: UpdateMemberRoleRequest,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    service = ProjectMemberService(db)
    return await service.update_role(project_id=project_id, user_id=user_id, data=data, current_user_id=current_user.id)


@router.delete("/{user_id}", status_code=204)
async def remove_member(
    project_id: str,
    user_id: str,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    service = ProjectMemberService(db)
    await service.remove_member(project_id, user_id, current_user.id)