from datetime import datetime
from pydantic import BaseModel, Field
from app.models.task import TaskStatus, TaskPriority


class TaskBase(BaseModel):
    title: str = Field(min_length=1, max_length=255)
    description: str | None = None
    status: TaskStatus = TaskStatus.TODO
    priority: TaskPriority = TaskPriority.MEDIUM
    assignee_id: str | None = None
    due_date: datetime | None = None


class TaskCreate(TaskBase):
    pass    


class TaskUpdate(BaseModel):
    title: str | None = Field(None, min_length=1, max_length=255)
    description: str | None = None
    status: TaskStatus | None = None
    priority: TaskPriority | None = None
    assignee_id: str | None = None
    due_date: datetime | None = None


class TaskResponse(TaskBase):
    id: str
    project_id: str
    created_at: datetime
    updated_at: datetime

    model_config = {"from_attributes": True}