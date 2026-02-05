import datetime
from uuid import UUID

import pytest

from src.entities.task import Task
from src.entities.task_status import Priority, TaskStatus
from src.exceptions import ValidationError


@pytest.fixture
def sample_task():
    return Task(title="Test Task")


@pytest.fixture
def past_date():
    return datetime.datetime.now(datetime.UTC) - datetime.timedelta(days=1)


@pytest.fixture
def future_date():
    return datetime.datetime.now(datetime.UTC) + datetime.timedelta(days=7)


def test_create_task_with_valid_data():
    task = Task(title="Test Task", description="Test description", priority=Priority.HIGH)

    assert task.title == "Test Task"
    assert task.description == "Test description"
    assert task.status == TaskStatus.NEW
    assert task.priority == Priority.HIGH
    assert isinstance(task.id, UUID)
    assert isinstance(task.created_at, datetime.datetime)
    assert isinstance(task.updated_at, datetime.datetime)


def test_create_task_with_empty_title_raises_error():
    with pytest.raises(ValidationError, match="Title is required"):
        Task(title="")


def test_create_task_with_whitespace_title_raises_error():
    with pytest.raises(ValidationError, match="Title is required"):
        Task(title="   ")


def test_create_task_with_past_deadline_raises_error(past_date):
    with pytest.raises(ValidationError, match="Deadline cannot be in the past"):
        Task(title="Test", deadline=past_date)


def test_update_task_title():
    task = Task(title="Original")
    old_updated_at = task.updated_at

    task.update(title="New Title")

    assert task.title == "New Title"
    assert task.updated_at > old_updated_at


def test_update_task_with_invalid_title_raises_error():
    task = Task(title="Valid")
    with pytest.raises(ValidationError, match="Title is required"):
        task.update(title="")


def test_update_task_multiple_fields():
    task = Task(title="Original", priority=Priority.LOW)

    task.update(title="Updated", description="New desc", priority=Priority.HIGH)

    assert task.title == "Updated"
    assert task.description == "New desc"
    assert task.priority == Priority.HIGH


def test_mark_task_in_progress(sample_task):
    sample_task.mark_in_progress()

    assert sample_task.status == TaskStatus.IN_PROGRESS


def test_mark_task_completed(sample_task):
    sample_task.mark_completed()

    assert sample_task.status == TaskStatus.COMPLETED


def test_status_change_is_idempotent(sample_task):
    sample_task.mark_in_progress()
    sample_task.mark_in_progress()

    assert sample_task.status == TaskStatus.IN_PROGRESS


def test_cannot_modify_completed_task_status(sample_task):
    sample_task.mark_completed()

    with pytest.raises(ValidationError, match="Cannot modify completed task"):
        sample_task.mark_in_progress()


def test_to_dict_returns_correct_structure():
    task = Task(title="Test", description="Desc", priority=Priority.MEDIUM)

    result = task.to_dict()

    assert result["title"] == "Test"
    assert result["description"] == "Desc"
    assert result["status"] == "new"
    assert result["priority"] == "medium"
    assert "id" in result
    assert "created_at" in result
    assert "updated_at" in result
