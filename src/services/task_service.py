import datetime
from uuid import UUID

from src.entities.task import Task
from src.entities.task_status import Priority, TaskStatus
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
            raise ValueError("Title is required")

        if deadline is not None and deadline < datetime.datetime.now():
            raise ValueError("Deadline cannot be in the past")

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
            raise ValueError(f"Task with id {task_id} not found")
        return task

    def get_all_tasks(self) -> list[Task]:
        return self._repository.get_all()

    def update_task(
        self,
        task_id: UUID,
        title: str | None = None,
        description: str | None = None,
    ) -> Task:
        task = self.get_task_by_id(task_id)

        if title is not None:
            if not title.strip():
                raise ValueError("Title cannot be empty")
            task.title = title.strip()

        if description is not None:
            task.description = description

        task.updated_at = datetime.datetime.now()
        self._repository.save(task)
        return task

    def change_task_status(self, task_id: UUID, status: TaskStatus) -> Task:
        task = self.get_task_by_id(task_id)

        if status == TaskStatus.IN_PROGRESS:
            task.mark_in_progress()
        elif status == TaskStatus.COMPLETED:
            task.mark_completed()
        else:
            raise ValueError(f"Unsupported status: {status}")

        self._repository.save(task)
        return task

    def delete_task(self, task_id: UUID) -> bool:
        deleted = self._repository.delete(task_id)
        if not deleted:
            raise ValueError(f"Task with id {task_id} not found")
        return True

    def get_tasks_by_status(self, status: TaskStatus) -> list[Task]:
        tasks = self._repository.get_all()
        return [task for task in tasks if task.status == status]
