from src.repositories.memory import InMemoryTaskRepository

_repository_instance: InMemoryTaskRepository | None = None


def get_task_repository() -> InMemoryTaskRepository:
    global _repository_instance
    if _repository_instance is None:
        _repository_instance = InMemoryTaskRepository()
    return _repository_instance
