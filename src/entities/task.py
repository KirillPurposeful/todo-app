import datetime
from dataclasses import dataclass, field
from uuid import UUID, uuid4

from ..exceptions import ValidationError
from .task_status import Priority, TaskStatus


@dataclass
class Task:
    title: str
    description: str = ""
    status: TaskStatus = TaskStatus.NEW
    priority: Priority = Priority.LOW
    deadline: datetime.datetime | None = None
    created_at: datetime.datetime = field(default_factory=datetime.datetime.now)
    updated_at: datetime.datetime = field(default_factory=datetime.datetime.now)
    id: UUID = field(default_factory=uuid4)

    def __post_init__(self) -> None:
        self.__validate_title(self.title)
        self.__validate_deadline(self.deadline)

    @staticmethod
    def __validate_title(title: str) -> None:
        if not title or not title.strip():
            raise ValidationError("Title is required")

    @staticmethod
    def __validate_deadline(deadline: datetime.datetime | None) -> None:
        if deadline is not None and deadline < datetime.datetime.now():
            raise ValidationError("Deadline cannot be in the past")

    def _touch(self) -> None:
        """Update the updated_at timestamp."""
        self.updated_at = datetime.datetime.now()

    def update(
        self,
        title: str | None = None,
        description: str | None = None,
        priority: Priority | None = None,
        deadline: datetime.datetime | None = None,
    ) -> None:
        if title is not None:
            self.__validate_title(title)
            self.title = title

        if description is not None:
            self.description = description

        if priority is not None:
            self.priority = priority

        if deadline is not None:
            self.__validate_deadline(deadline)
            self.deadline = deadline

        self._touch()

    def _set_status(self, new_status: TaskStatus) -> None:
        """Change task status with validation."""
        if self.status == new_status:
            return

        if self.status == TaskStatus.COMPLETED:
            raise ValidationError("Cannot modify completed task")

        self.status = new_status
        self._touch()

    def mark_new(self) -> None:
        self._set_status(TaskStatus.NEW)

    def mark_in_progress(self) -> None:
        self._set_status(TaskStatus.IN_PROGRESS)

    def mark_completed(self) -> None:
        self._set_status(TaskStatus.COMPLETED)

    def __repr__(self) -> str:
        return f"Task(title='{self.title}', status={self.status.value})"
