from abc import ABC, abstractmethod
from typing import Generic, TypeVar
from uuid import UUID

T = TypeVar("T")


class BaseRepository(ABC, Generic[T]):
    @abstractmethod
    def save(self, entity: T) -> T:
        pass

    @abstractmethod
    def delete(self, entity_id: UUID) -> bool:
        pass

    @abstractmethod
    def get_by_id(self, entity_id: UUID) -> T | None:
        pass

    @abstractmethod
    def get_all(self) -> list[T]:
        pass
