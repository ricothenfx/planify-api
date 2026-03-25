from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import HTTPException, status
from app.repositories.project_member_repository import ProjectMemberRepository
from app.repositories.project_repository import ProjectRepository
from app.repositories.user_repository import UserRepository
from app.schemas.project_member import AddMemberRequest, UpdateMemberRoleRequest, ProjectMemberResponse
from app.models.project_member import MemberRole
from app.services.activity_service import ActivityService


class ProjectMemberService:
    def __init__(self, db: AsyncSession):
        self.member_repo = ProjectMemberRepository(db)
        self.project_repo = ProjectRepository(db)
        self.user_repo = UserRepository(db)
        self.activity = ActivityService(db)
    
    async def add_member(
        self,
        project_id: str,
        data: AddMemberRequest,
        current_user_id: str,
    ) -> ProjectMemberResponse:
        await self._verify_owner(project_id, current_user_id)

        # Check if user exists
        user =  await self.user_repo.get_by_id(data.user_id)
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found",
            )
        
        # Check if user already a member or not
        existing = await self.member_repo.get_member(project_id, data.user_id)
        if existing:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="User is already a member of this project",
            )
        
        member = await self.member_repo.add_member(
            project_id=project_id,
            user_id=data.user_id,
            role=data.role,
        )
        await self.activity.log(
            user_id=current_user_id,
            project_id=project_id,
            entity_type="project_member",
            entity_id=member.id,
            action="member_added",
            extra_data={"user_id": data.user_id, "role": data.role},
        )
        return ProjectMemberResponse.model_validate(member)
    
    async def get_members(self, project_id: str, current_user_id: str) -> list[ProjectMemberResponse]:
        await self._verify_member(project_id, current_user_id)
        members = await self.member_repo.get_all_members(project_id)
        return [ProjectMemberResponse.model_validate(m) for m in members]
    
    async def remove_member(
        self, project_id: str, user_id: str, current_user_id: str
    ) -> None:
        await self._verify_owner(project_id, current_user_id)

        # Owner cannot remove ownself
        if user_id == current_user_id:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Owner cannot remove themselves from the project",
            )

        # Check if user really a member of this project
        member = await self.member_repo.get_member(project_id, user_id)
        if not member:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Member not found",
            )

        await self.activity.log(
            user_id=current_user_id,
            project_id=project_id,
            entity_type="project_member",
            entity_id=member.id,
            action="member_removed",
            extra_data={"user_id": user_id},
        )
        await self.member_repo.remove_member(member)
    
    async def update_role(
        self,
        project_id: str,
        user_id: str,
        data: UpdateMemberRoleRequest,
        current_user_id: str,
    ) -> ProjectMemberResponse:
        await self._verify_owner(project_id, current_user_id)

        # Check if user really a member of this project
        member = await self.member_repo.get_member(project_id, user_id)
        if not member:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Member not found",
            )

        member = await self.member_repo.update_role(member, data.role)
        return ProjectMemberResponse.model_validate(member)
    
    async def _verify_owner(self, project_id: str, user_id: str):
        project = await self.project_repo.get_by_id(project_id)
        if not project:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Project not found",
            )
        if project.owner_id != user_id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Only project owner can perform this action",
            )
        return project
    
    async def _verify_member(self, project_id: str, user_id: str):
        project = await self.project_repo.get_by_id(project_id)
        if not project:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Project not found",
            )
        # Check if user is the owner of this project
        if project.owner_id == user_id:
            return project
        member = await self.member_repo.get_member(project_id, user_id)
        if not member:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Not a member of this project",
            )
        return project