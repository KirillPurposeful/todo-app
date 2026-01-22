import datetime
from uuid import UUID

from src.entities.task import Task
from src.entities.task_status import Priority, TaskStatus
from src.exceptions import TaskNotFoundError, ValidationError
from src.repositories.base import BaseRepository


class TaskService:
    def __init__(self, repository: BaseRepository[Task]) -> None:
        self._repository = repository

    def create_task(
        self,
        title: str,
        description: str,
        priority: Priority = Priority.LOW,
        deadline: datetime.datetime | None = None,
    ) -> Task:
        if not title or not title.strip():
            raise ValidationError("Title is required")

        if deadline is not None and deadline < datetime.datetime.now():
            raise ValidationError("Deadline cannot be in the past")

        task = Task(
            title=title.strip(),
            description=description,
            priority=priority,
            deadline=deadline,
        )

        self._repository.save(task)
        return task

    def get_task_by_id(self, task_id: UUID) -> Task:
        task = self._repository.get_by_id(task_id)
        if task is None:
            raise TaskNotFoundError(f"Task with id {task_id} not found")
        return task

    def get_all_tasks(self) -> list[Task]:
        return self._repository.get_all()

    def update_task(
        self,
        task_id: UUID,
        title: str | None = None,
        description: str | None = None,
        priority: Priority | None = None,
        deadline: datetime.datetime | None = None,
    ) -> Task:
        task = self.get_task_by_id(task_id)

        if title is not None and not title.strip():
            raise ValidationError("Title cannot be empty")

        if deadline is not None and deadline < datetime.datetime.now():
            raise ValidationError("Deadline cannot be in the past")

        task.update(
            title=title.strip() if title else None,
            description=description,
            priority=priority,
            deadline=deadline,
        )

        self._repository.save(task)
        return task

    def change_task_status(self, task_id: UUID, status: TaskStatus) -> Task:
        task = self.get_task_by_id(task_id)

        if status == TaskStatus.NEW:
            task.status = TaskStatus.NEW
            task.updated_at = datetime.datetime.now()
        elif status == TaskStatus.IN_PROGRESS:
            task.mark_in_progress()
        elif status == TaskStatus.COMPLETED:
            task.mark_completed()

        self._repository.save(task)
        return task

    def delete_task(self, task_id: UUID) -> None:
        deleted = self._repository.delete(task_id)
        if not deleted:
            raise TaskNotFoundError(f"Task with id {task_id} not found")

    def get_tasks_by_status(self, status: TaskStatus) -> list[Task]:
        return self._repository.get_by_status(status)
