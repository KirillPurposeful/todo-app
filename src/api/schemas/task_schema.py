import datetime
from uuid import UUID

from pydantic import BaseModel

from src.entities.task_status import Priority, TaskStatus


class TaskResponse(BaseModel):
    model_config = {"from_attributes": True}

    id: UUID
    title: str
    description: str | None
    status: TaskStatus
    priority: Priority
    deadline: datetime.datetime | None
    created_at: datetime.datetime
    updated_at: datetime.datetime


class TaskCreate(BaseModel):
    title: str
    description: str = ""
    priority: Priority = Priority.LOW
    deadline: datetime.datetime | None = None


class TaskUpdate(BaseModel):
    title: str | None = None
    description: str | None = None
    priority: Priority | None = None
    deadline: datetime.datetime | None = None


class TaskListResponse(BaseModel):
    tasks: list[TaskResponse]
    total: int


class ErrorResponse(BaseModel):
    detail: str
