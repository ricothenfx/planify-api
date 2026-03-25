from pydantic import BaseModel
from app.schemas.task import TaskResponse


class GenerateTasksRequest(BaseModel):
    project_id: str


class GenerateTasksResponse(BaseModel):
    generated: int
    tasks: list[TaskResponse]


class TaskSuggestionsResponse(BaseModel):
    task_id: str
    status: str
    suggestions: list[str]