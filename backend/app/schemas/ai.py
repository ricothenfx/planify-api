from pydantic import BaseModel
from app.schemas.task import TaskResponse


class GenerateTasksRequest(BaseModel):
    project_id: str


class GenerateTasksResponse(BaseModel):
    generated: int
    tasks: list[TaskResponse]