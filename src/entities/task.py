import datetime
from uuid import uuid4

from .task_status import Priority, TaskStatus


class Task:
    def __init__(
        self,
        *,
        title: str = "",
        description: str = "",
        priority: Priority = Priority.LOW,
        deadline: datetime.datetime | None = None,
    ):
        self.id = str(uuid4())
        self.title = title
        self.description = description
        self.status = TaskStatus.NEW
        self.priority = priority
        self.deadline = deadline
        self.created_at = datetime.datetime.now()
        self.updated_at = datetime.datetime.now()

    def mark_in_progress(self) -> None:
        if self.status == TaskStatus.COMPLETED:
            raise ValueError("Cannot restart completed task")
        if self.status == TaskStatus.IN_PROGRESS:
            return
        self.status = TaskStatus.IN_PROGRESS
        self.updated_at = datetime.datetime.now()

    def mark_completed(self) -> None:
        if self.status == TaskStatus.COMPLETED:
            raise ValueError("Task already completed")
        self.status = TaskStatus.COMPLETED
        self.updated_at = datetime.datetime.now()

    def set_priority(self, priority: Priority) -> None:
        self.priority = priority
        self.updated_at = datetime.datetime.now()

    def update_deadline(self, deadline: datetime.datetime) -> None:
        self.deadline = deadline
        self.updated_at = datetime.datetime.now()

    def __repr__(self) -> str:
        return f"Task(title='{self.title}', status={self.status.value})"

