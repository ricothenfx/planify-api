from datetime import datetime
from pydantic import BaseModel
from app.models.project_member import MemberRole


class AddMemberRequest(BaseModel):
    user_id: str
    role: MemberRole = MemberRole.MEMBER


class UpdateMemberRoleRequest(BaseModel):
    role: MemberRole


class ProjectMemberResponse(BaseModel):
    id: str
    project_id: str
    user_id: str
    role: MemberRole
    joined_at: datetime

    model_config = {"from_attributes": True}