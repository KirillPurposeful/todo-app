"""Test data for task API testing."""

# Valid data
VALID_TASK_MINIMAL = {"title": "Test task"}

VALID_TASK_FULL = {
    "title": "Test task",
    "description": "Test Description",
    "priority": "high",
    "deadline": "2099-01-01T12:00:00Z",
}

VALID_TASK_FUTURE_DEADLINE = {"title": "Test task", "deadline": "2035-01-01T00:00:00Z"}

# Invalid title
EMPTY_TITLE = {"title": ""}
WHITESPACE_TITLE = {"title": "   "}
MISSING_TITLE = {}

# Invalid deadline
PAST_DEADLINE = {"title": "Valid title", "deadline": "2020-01-01T00:00:00Z"}

# Invalid ID
INVALID_ID_STRING = "invalid_id"
NON_EXISTENT_TASK_ID = "123e4567-e89b-12d3-a456-426614174000"

# Update payloads
UPDATE_TITLE_PAYLOAD = {"title": "Updated title"}

EXPECTED_TASK_AFTER_TITLE_UPDATE = {
    "title": "Updated title",
    "description": "",
    "priority": "low",
    "deadline": None,
    "status": "new",
}

UPDATE_ALL_FIELDS_PAYLOAD = {
    "title": "Updated title",
    "description": "Updated description",
    "priority": "high",
    "deadline": "2099-01-01T12:00:00Z",
}

EXPECTED_TASK_AFTER_ALL_FIELDS_UPDATE = {
    "title": "Updated title",
    "description": "Updated description",
    "priority": "high",
    "deadline": "2099-01-01T12:00:00Z",
    "status": "new",
}
