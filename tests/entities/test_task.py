import datetime
from uuid import UUID

import pytest

from src.entities.task import Task
from src.entities.task_status import Priority, TaskStatus
from src.exceptions import ValidationError


def test_create_task_with_all_fields_sets_values_correctly():
    task = Task(title="Test Task", description="Test description", priority=Priority.HIGH)

    assert task.title == "Test Task"
    assert task.description == "Test description"
    assert task.status == TaskStatus.NEW
    assert task.priority == Priority.HIGH
    assert isinstance(task.id, UUID)
    assert isinstance(task.created_at, datetime.datetime)
    assert isinstance(task.updated_at, datetime.datetime)


def test_create_task_with_empty_title_raises_validation_error():
    with pytest.raises(ValidationError, match="Title is required"):
        Task(title="")


def test_create_task_with_whitespace_title_raises_validation_error():
    with pytest.raises(ValidationError, match="Title is required"):
        Task(title="   ")


def test_create_task_with_past_deadline_raises_validation_error(past_date):
    with pytest.raises(ValidationError, match="Deadline cannot be in the past"):
        Task(title="Test", deadline=past_date)


def test_update_task_title_changes_value_and_updates_timestamp():
    task = Task(title="Original")
    old_updated_at = task.updated_at

    task.update(title="New Title")

    assert task.title == "New Title"
    assert task.updated_at > old_updated_at


def test_update_task_with_empty_title_raises_validation_error():
    task = Task(title="Valid")
    with pytest.raises(ValidationError, match="Title is required"):
        task.update(title="")


def test_update_task_multiple_fields_changes_all_values():
    task = Task(title="Original", priority=Priority.LOW)

    task.update(title="Updated", description="New desc", priority=Priority.HIGH)

    assert task.title == "Updated"
    assert task.description == "New desc"
    assert task.priority == Priority.HIGH


def test_mark_task_in_progress_changes_status(sample_task):
    sample_task.mark_in_progress()

    assert sample_task.status == TaskStatus.IN_PROGRESS


def test_mark_task_completed_changes_status(sample_task):
    sample_task.mark_completed()

    assert sample_task.status == TaskStatus.COMPLETED


def test_mark_task_with_same_status_is_idempotent(sample_task):
    sample_task.mark_in_progress()
    sample_task.mark_in_progress()

    assert sample_task.status == TaskStatus.IN_PROGRESS


def test_modify_completed_task_status_raises_validation_error(sample_task):
    sample_task.mark_completed()

    with pytest.raises(ValidationError, match="Cannot modify completed task"):
        sample_task.mark_in_progress()


def test_to_dict_returns_all_fields_with_correct_types():
    task = Task(title="Test", description="Desc", priority=Priority.MEDIUM)

    result = task.to_dict()

    assert result["title"] == "Test"
    assert result["description"] == "Desc"
    assert result["status"] == "new"
    assert result["priority"] == "medium"
    assert "id" in result
    assert "created_at" in result
    assert "updated_at" in result


def test_create_task_with_minimal_data_sets_defaults():
    task = Task(title="Test")

    assert task.title == "Test"
    assert task.description == ""
    assert task.status == TaskStatus.NEW
    assert task.priority == Priority.LOW
    assert task.deadline is None


def test_create_task_with_future_deadline_sets_value(future_date):
    task = Task(title="Test", deadline=future_date)

    assert task.deadline == future_date


def test_update_task_deadline_changes_value(sample_task, future_date):
    sample_task.update(deadline=future_date)

    assert sample_task.deadline == future_date


def test_update_task_with_past_deadline_raises_validation_error(sample_task, past_date):
    with pytest.raises(ValidationError, match="Deadline cannot be in the past"):
        sample_task.update(deadline=past_date)


def test_update_task_with_none_values_keeps_original_fields(sample_task):
    original_title = sample_task.title
    original_description = sample_task.description

    sample_task.update(title=None, description=None)

    assert sample_task.title == original_title
    assert sample_task.description == original_description


def test_mark_task_back_to_new_from_in_progress(sample_task):
    sample_task.mark_in_progress()
    sample_task.mark_new()

    assert sample_task.status == TaskStatus.NEW
