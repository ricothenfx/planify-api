from datetime import datetime
from pydantic import BaseModel


class ActivityResponse(BaseModel):
    id: str
    user_id: str
    project_id: str
    entity_type: str
    entity_id: str
    action: str
    extra_data: dict | None = None
    created_at: datetime

    model_config = {"from_attributes": True}