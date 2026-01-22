import datetime
from uuid import UUID, uuid4

from ..exceptions import ValidationError
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
        self.id: UUID = uuid4()
        self.title = title
        self.description = description
        self.status = TaskStatus.NEW
        self.priority = priority
        self.deadline = deadline
        self.created_at = datetime.datetime.now()
        self.updated_at = datetime.datetime.now()

    def update(
        self,
        title: str | None = None,
        description: str | None = None,
        priority: Priority | None = None,
        deadline: datetime.datetime | None = None,
    ) -> None:
        updates = {
            "title": title,
            "description": description,
            "priority": priority,
            "deadline": deadline,
        }
        for field, value in updates.items():
            if value is not None:
                setattr(self, field, value)
        self.updated_at = datetime.datetime.now()

    def set_priority(self, priority: Priority) -> None:
        self.priority = priority
        self.updated_at = datetime.datetime.now()

    def mark_in_progress(self) -> None:
        if self.status == TaskStatus.COMPLETED:
            raise ValidationError("Cannot restart completed task")
        if self.status == TaskStatus.IN_PROGRESS:
            return
        self.status = TaskStatus.IN_PROGRESS
        self.updated_at = datetime.datetime.now()

    def mark_completed(self) -> None:
        if self.status == TaskStatus.COMPLETED:
            raise ValidationError("Task already completed")
        self.status = TaskStatus.COMPLETED
        self.updated_at = datetime.datetime.now()

    def __repr__(self) -> str:
        return f"Task(title='{self.title}', status={self.status.value})"
