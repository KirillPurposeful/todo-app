import datetime
from uuid import UUID

from pydantic import BaseModel

from src.entities.task_status import Priority, TaskStatus


class TaskResponse(BaseModel):
    id: UUID
    title: str
    description: str | None
    status: TaskStatus
    priority: Priority
    deadline: datetime.datetime | None
    created_at: datetime.datetime
    updated_at: datetime.datetime

    class Config:
        from_attributes = True

class TaskCreate(BaseModel):
    title: str