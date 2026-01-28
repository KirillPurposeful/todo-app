import datetime
from dataclasses import asdict, dataclass, field
from uuid import UUID, uuid4

from ..exceptions import ValidationError
from .task_status import Priority, TaskStatus

# todo: создать таск валидатор для соблюдения SRP
# todo: разделить модель домена и модель db ORM надо было бы сделать в норм проекте
#   для разделения логики и данных


@dataclass
class Task:
    title: str
    description: str = ""
    status: TaskStatus = TaskStatus.NEW
    priority: Priority = Priority.LOW
    deadline: datetime.datetime | None = None
    created_at: datetime.datetime = field(default_factory=lambda: datetime.datetime.now(datetime.UTC))
    updated_at: datetime.datetime = field(default_factory=lambda: datetime.datetime.now(datetime.UTC))
    id: UUID = field(default_factory=uuid4)

    def __post_init__(self) -> None:
        self._validate_title(self.title)
        self._validate_deadline(self.deadline)

    @staticmethod
    def _validate_title(title: str) -> None:
        if not title or not title.strip():
            raise ValidationError("Title is required")

    @staticmethod
    def _validate_deadline(deadline: datetime.datetime | None) -> None:
        if deadline is not None and deadline < datetime.datetime.now(datetime.UTC):
            raise ValidationError("Deadline cannot be in the past")

    def _touch(self) -> None:
        self.updated_at = datetime.datetime.now(datetime.UTC)

    def update(
        self,
        title: str | None = None,
        description: str | None = None,
        priority: Priority | None = None,
        deadline: datetime.datetime | None = None,
    ) -> None:
        if title is not None:
            self._validate_title(title)
            self.title = title

        if description is not None:
            self.description = description

        if priority is not None:
            self.priority = priority

        if deadline is not None:
            self._validate_deadline(deadline)
            self.deadline = deadline

        self._touch()

    def _set_status(self, new_status: TaskStatus) -> None:
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

    def to_dict(self) -> dict:
        data = asdict(self)
        data['status'] = self.status.value
        data['priority'] = self.priority.value
        return data

