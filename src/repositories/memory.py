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

    def get_by_id(self, entity_id: UUID) -> Task | None:
        return self._storage.get(entity_id)

    def get_all(self) -> list[Task]:
        return list(self._storage.values())

    def get_by_status(self, status: TaskStatus) -> list[Task]:
        return [task for task in self._storage.values() if task.status == status]

    def delete(self, entity_id: UUID) -> bool:
        return self._storage.pop(entity_id, None) is not None
