from datetime import datetime
from pydantic import BaseModel


class AttachmentResponse(BaseModel):
    id: str
    task_id: str
    user_id: str
    filename: str
    file_url: str
    file_size: int
    mime_type: str
    created_at: datetime

    model_config = {"from_attributes": True}