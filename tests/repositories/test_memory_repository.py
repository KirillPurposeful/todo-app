from uuid import uuid4

import pytest

from src.entities.task import Task
from src.entities.task_status import TaskStatus
from src.repositories.memory import InMemoryTaskRepository


@pytest.fixture
def repository():
    return InMemoryTaskRepository()


def test_save_task_stores_and_returns_task(repository, sample_task):
    result = repository.save(sample_task)

    assert result == sample_task
    assert repository.get_by_id(sample_task.id) == sample_task


def test_get_by_id_returns_existing_task(repository, sample_task):
    repository.save(sample_task)

    result = repository.get_by_id(sample_task.id)

    assert result == sample_task


def test_get_by_id_returns_none_for_non_existent_task(repository):
    from uuid import uuid4

    result = repository.get_by_id(uuid4())

    assert result is None


def test_get_all_returns_empty_list_when_no_tasks(repository):
    result = repository.get_all()

    assert result == []


def test_get_all_returns_all_stored_tasks(repository):
    task1 = Task(title="Task 1")
    task2 = Task(title="Task 2")
    repository.save(task1)
    repository.save(task2)

    result = repository.get_all()

    assert len(result) == 2
    assert task1 in result
    assert task2 in result


def test_get_by_status_returns_tasks_with_matching_status(repository):
    task1 = Task(title="Task 1")
    task2 = Task(title="Task 2")
    task2.mark_completed()
    repository.save(task1)
    repository.save(task2)

    result = repository.get_by_status(TaskStatus.NEW)

    assert len(result) == 1
    assert task1 in result
    assert task2 not in result


def test_get_by_status_returns_empty_list_when_no_matches(repository, sample_task):
    repository.save(sample_task)

    result = repository.get_by_status(TaskStatus.COMPLETED)

    assert result == []


def test_delete_existing_task_returns_true(repository, sample_task):
    repository.save(sample_task)

    result = repository.delete(sample_task.id)

    assert result is True
    assert repository.get_by_id(sample_task.id) is None


def test_delete_non_existent_task_returns_false(repository):
    result = repository.delete(uuid4())

    assert result is False


def test_clear_removes_all_tasks(repository):
    task1 = Task(title="Task 1")
    task2 = Task(title="Task 2")
    repository.save(task1)
    repository.save(task2)

    repository.clear()

    assert repository.get_all() == []


def test_save_updates_existing_task(repository, sample_task):
    repository.save(sample_task)
    sample_task.update(title="Updated Title")

    repository.save(sample_task)

    result = repository.get_by_id(sample_task.id)
    assert result.title == "Updated Title"
