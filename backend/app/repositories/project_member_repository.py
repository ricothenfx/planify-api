from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.models.project_member import ProjectMember, MemberRole


class ProjectMemberRepository:
    def __init__(self, db: AsyncSession):
        self.db = db
    
    async def get_member(self, project_id: str, user_id: str) -> ProjectMember | None:
        result = await self.db.execute(
            select(ProjectMember).where(
                ProjectMember.project_id == project_id,
                ProjectMember.user_id == user_id,
            )
        )
        return result.scalar_one_or_none()
    
    async def get_all_members(self, project_id: str) -> list[ProjectMember]:
        result = await self.db.execute(
            select(ProjectMember).where(
                ProjectMember.project_id == project_id
            )
        )
        return list(result.scalars().all())
    
    async def add_member(self, project_id: str, user_id: str, role: MemberRole = MemberRole.MEMBER) -> ProjectMember:
        member = ProjectMember(
            project_id=project_id,
            user_id=user_id,
            role=role,
        )
        self.db.add(member)
        await self.db.flush()
        await self.db.refresh(member)
        return member
    
    async def remove_member(self, member: ProjectMember) -> None:
        await self.db.delete(member)
        await self.db.flush()
    
    async def update_role(self, member: ProjectMember, role: MemberRole) -> ProjectMember:
        member.role = role
        await self.db.flush()
        await self.db.refresh(member)
        return member