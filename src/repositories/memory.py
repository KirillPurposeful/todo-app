from copy import deepcopy
from uuid import UUID

from src.entities.task import Task
from src.entities.task_status import TaskStatus
from src.repositories.base import BaseRepository


class InMemoryTaskRepository(BaseRepository[Task]):
    def __init__(self) -> None:
        self._storage: dict[UUID, Task] = {}

    def save(self, entity: Task) -> Task:
        self._storage[entity.id] = entity
        return entity

    def get_by_id(self, id: UUID) -> Task | None:
        return deepcopy(self._storage.get(id))

    def get_all(self) -> list[Task]:
        return [deepcopy(task) for task in self._storage.values()]

    def get_by_status(self, status: TaskStatus) -> list[Task]:
        return [deepcopy(task) for task in self._storage.values() if task.status == status]

    def delete(self, id: UUID) -> bool:
        return self._storage.pop(id, None) is not None
