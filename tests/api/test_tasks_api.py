"""Tests for tasks API endpoints."""

import pytest

from tests.api.expectations import TaskExpectations
from tests.api.steps import TaskSteps
from tests.test_data.task_data import (
    EMPTY_TITLE,
    WHITESPACE_TITLE,
    PAST_DEADLINE,
    VALID_TASK_FUTURE_DEADLINE,
    VALID_TASK_FULL,
    MISSING_TITLE,
    NON_EXISTENT_TASK_ID,
    INVALID_ID_STRING,
    UPDATE_TITLE_PAYLOAD,
    EXPECTED_TASK_AFTER_TITLE_UPDATE,
    VALID_TASK_MINIMAL,
    UPDATE_ALL_FIELDS_PAYLOAD,
    EXPECTED_TASK_AFTER_ALL_FIELDS_UPDATE,
)


@pytest.fixture
def steps():
    """Fixture for test steps."""
    return TaskSteps()


@pytest.fixture
def expect():
    """Fixture for expectations."""
    return TaskExpectations()


def test_create_task_with_minimal_valid_data(client, steps, expect):
    # When
    response = steps.create_task(client, payload=VALID_TASK_MINIMAL)

    # Then
    expect.assert_status_code(response, expected=201)
    task_data = response.json()
    expect.assert_task_base_fields(task_data)
    expect.assert_task_values(task_data, VALID_TASK_MINIMAL)


def test_create_task_with_full_valid_data(client, steps, expect):
    # When
    response = steps.create_task(client, payload=VALID_TASK_FULL)

    # Then
    expect.assert_status_code(response, expected=201)
    task_data = response.json()
    expect.assert_task_base_fields(task_data)
    expect.assert_task_values(task_data, VALID_TASK_FULL)


def test_create_task_with_empty_title(client, steps, expect):
    # When
    response = steps.create_task(client, payload=EMPTY_TITLE)

    # Then
    expect.assert_status_code(response, expected=400)
    expect.assert_validation_error(response, expected_status=400)


def test_create_task_with_whitespace_title(client, steps, expect):
    # When
    response = steps.create_task(client, payload=WHITESPACE_TITLE)

    # Then
    expect.assert_status_code(response, expected=400)
    expect.assert_validation_error(response, expected_status=400)


def test_create_task_with_past_deadline(client, steps, expect):
    # When
    response = steps.create_task(client, payload=PAST_DEADLINE)

    # Then
    expect.assert_status_code(response, expected=400)
    expect.assert_validation_error(response, expected_status=400)


def test_create_task_with_future_deadline(client, steps, expect):
    # When
    response = steps.create_task(client, payload=VALID_TASK_FUTURE_DEADLINE)

    # Then
    expect.assert_status_code(response, expected=201)
    task_data = response.json()
    expect.assert_task_base_fields(task_data)
    expect.assert_task_values(task_data, VALID_TASK_FUTURE_DEADLINE)


def test_create_task_without_title(client, steps, expect):
    # When
    response = steps.create_task(client, payload=MISSING_TITLE)

    # Then
    expect.assert_status_code(response, expected=422)
    expect.assert_validation_error(response, expected_status=422)


# GET
# -------------------------------------------------------------------------------------------------------------


def test_get_task_by_id_success(client, steps, expect):
    # Given: task is created
    create_task_response = steps.create_task(client, payload=VALID_TASK_MINIMAL)
    task_id = create_task_response.json()["id"]

    # When: task is requested by id
    get_task_response = steps.get_task(client, task_id)

    # Then: task is returned successfully
    expect.assert_status_code(get_task_response, expected=200)

    returned_task_data = get_task_response.json()
    expect.assert_task_base_fields(returned_task_data)
    expect.assert_task_values(returned_task_data, VALID_TASK_MINIMAL)


def test_get_task_by_id_not_found(client, steps, expect):
    # When: task is requested by incorrect id
    get_task_response = steps.get_task(client, NON_EXISTENT_TASK_ID)

    # Then: 404 not found error returned
    expect.assert_status_code(get_task_response, expected=404)
    expect.assert_not_found(get_task_response, expected_status=404)


def test_get_task_by_invalid_uuid(client, steps, expect):
    # When: task is requested by invalid id format
    get_task_response = steps.get_task(client, INVALID_ID_STRING)

    # Then: 422 validation error returned
    expect.assert_status_code(get_task_response, expected=422)
    expect.assert_validation_error(get_task_response, expected_status=422)


# GET ALL
# -------------------------------------------------------------------------------------------------------------


def test_get_all_tasks_returns_empty_list(client, steps, expect):
    # Given: no tasks created

    # When: all tasks are requested
    get_all_response = steps.list_tasks(client)
    # Then: empty list is returned
    expect.assert_status_code(get_all_response, expected=200)
    expect.assert_task_list_response(get_all_response.json(), expected_total=0)


def test_get_all_tasks_returns_single_task(client, steps, expect):
    # Given: one task created
    steps.create_task(client, payload=VALID_TASK_MINIMAL)

    # When: all tasks are requested
    get_all_response = steps.list_tasks(client)

    # Then: single task is returned
    expect.assert_status_code(get_all_response, expected=200)
    expect.assert_task_list_response(get_all_response.json(), expected_total=1)


def test_get_all_tasks_returns_multiple_tasks(client, steps, expect):
    # Given: multiple tasks created
    steps.create_task(client, payload=VALID_TASK_MINIMAL)
    steps.create_task(client, payload=VALID_TASK_MINIMAL)

    # When: all tasks are requested
    get_all_response = steps.list_tasks(client)

    # Then: multiple tasks are returned
    expect.assert_status_code(get_all_response, expected=200)
    expect.assert_task_list_response(get_all_response.json(), expected_total=2)


# UPDATE
# -------------------------------------------------------------------------------------------------------------


def test_update_task_single_field(client, steps, expect):
    # Given: task created
    create_task_response = steps.create_task(client, payload=VALID_TASK_MINIMAL)
    task_id = create_task_response.json()["id"]

    # When: task updated
    update_response = steps.update_task(client, task_id, payload=UPDATE_TITLE_PAYLOAD)

    # Then: task is updated
    expect.assert_status_code(update_response, expected=200)
    expect.assert_task_base_fields(update_response.json())
    expect.assert_task_values(update_response.json(), EXPECTED_TASK_AFTER_TITLE_UPDATE)


def test_update_task_multiple_fields(client, steps, expect):
    # Given: task created
    create_task_response = steps.create_task(client, payload=VALID_TASK_MINIMAL)
    task_id = create_task_response.json()["id"]

    # When: task updated
    update_response = steps.update_task(client, task_id, payload=UPDATE_ALL_FIELDS_PAYLOAD)

    # Then: task is updated
    expect.assert_status_code(update_response, expected=200)
    expect.assert_task_base_fields(update_response.json())
    expect.assert_task_values(update_response.json(), EXPECTED_TASK_AFTER_ALL_FIELDS_UPDATE)


def test_update_task_invalid_uuid(client, steps, expect):
    # When: task updated with invalid id
    update_response = steps.update_task(client, INVALID_ID_STRING, payload=UPDATE_TITLE_PAYLOAD)

    # Then: validation error returned
    expect.assert_status_code(update_response, expected=422)
    expect.assert_validation_error(update_response, expected_status=422)


def test_update_task_not_found(client, steps, expect):
    # When: task is updated with a non-existent id
    update_response = steps.update_task(client, NON_EXISTENT_TASK_ID, payload=UPDATE_TITLE_PAYLOAD)

    # Then: not found error returned
    expect.assert_status_code(update_response, expected=404)
    expect.assert_not_found(update_response, expected_status=404)


def test_delete_task_success(client, steps, expect):
    # Given: task created
    create_task_response = steps.create_task(client, payload=VALID_TASK_MINIMAL)
    task_id = create_task_response.json()["id"]

    # When: task deleted
    delete_response = steps.delete_task(client, task_id)

    # Then: task is deleted and cannot be retrieved
    expect.assert_status_code(delete_response, expected=204)

    get_task_response = steps.get_task(client, task_id)
    expect.assert_not_found(get_task_response, expected_status=404)


def test_delete_task_not_found(client, steps, expect):
    # When: deleting a non-existent task
    delete_response = steps.delete_task(client, NON_EXISTENT_TASK_ID)

    # Then: not found error is returned
    expect.assert_status_code(delete_response, expected=404)
    expect.assert_not_found(delete_response, expected_status=404)


def test_delete_task_with_invalid_uuid(client, steps, expect):
    # When: deleting a task with invalid id format
    delete_response = steps.delete_task(client, INVALID_ID_STRING)

    # Then: validation error is returned
    expect.assert_status_code(delete_response, expected=422)
    expect.assert_validation_error(delete_response, expected_status=422)


# CHANGE TASK STATUS
#-------------------------------------------------------------------------------------------------------------
def test_complete_task_success(client, steps, expect):
    # Given: task created
    create_task_response = steps.create_task(client, payload=VALID_TASK_MINIMAL)
    task_id = create_task_response.json()["id"]

    # When: task is completed
    complete_response = steps.complete_task(client, task_id)

    # Then: the task status is completed
    expect.assert_status_code(complete_response, expected=200)
    expect.assert_task_base_fields(complete_response.json())
    expect.assert_task_values(complete_response.json(), {"status": "completed"})

def test_complete_task_not_found(client, steps, expect):
    # When: completing not-existing task
    complete_response = steps.complete_task(client, NON_EXISTENT_TASK_ID)

    # Then: not found error is returned
    expect.assert_status_code(complete_response, expected=404)
    expect.assert_not_found(complete_response, expected_status=404)

def test_complete_task_with_invalid_uuid(client, steps, expect):

    # When: completing a task with invalid id format
    complete_response = steps.complete_task(client, INVALID_ID_STRING)

    # Then: validation error is returned
    expect.assert_status_code(complete_response, expected=422)
    expect.assert_validation_error(complete_response, expected_status=422)

def test_complete_task_is_idempotent(client, steps, expect):
    # Given: task is created and completed
    create_task_response = steps.create_task(client, payload=VALID_TASK_MINIMAL)
    task_id = create_task_response.json()["id"]
    steps.complete_task(client, task_id)

    # When: the task is completed again
    complete_again_response = steps.complete_task(client, task_id)

    # Then: the task status remains completed
    expect.assert_status_code(complete_again_response, expected=200)
    expect.assert_task_base_fields(complete_again_response.json())
    expect.assert_task_values(complete_again_response.json(), {"status": "completed"})
