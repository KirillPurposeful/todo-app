from copy import deepcopy
from uuid import UUID

from src.entities.task import Task
from src.repositories.base import BaseRepository


class InMemoryTaskRepository(BaseRepository[Task]):
    def __init__(self) -> None:
        self._storage: dict[UUID, Task] = {}

    def save(self, entity: Task) -> Task:
        self._storage[entity.id] = entity
        return entity

    def delete(self, id: UUID) -> bool:
        if id in self._storage:
            del self._storage[id]
            return True
        return False

    def get_by_id(self, id: UUID) -> Task | None:
        return deepcopy(self._storage.get(id))

    def get_all(self) -> list[Task]:
        return [deepcopy(task) for task in self._storage.values()]
