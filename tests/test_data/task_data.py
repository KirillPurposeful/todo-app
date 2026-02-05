"""Test data for task API testing."""

# VALID DATA

VALID_TASK_MINIMAL = {"title": "Test task"}

VALID_TASK_FULL = {
    "title": "Test task",
    "description": "Test Description",
    "priority": "high",
    "deadline": "2099-01-01T12:00:00Z",
}

VALID_TASK_FUTURE_DEADLINE = {"title": "Test task", "deadline": "2035-01-01T00:00:00Z"}

# INVALID TITLE CASES

EMPTY_TITLE = {"title": ""}
WHITESPACE_TITLE = {"title": "   "}
TOO_LONG_TITLE = {"title": "a" * 256}
MISSING_TITLE = {}

INVALID_TITLE_CASES = [
    EMPTY_TITLE,
    WHITESPACE_TITLE,
    TOO_LONG_TITLE,
    MISSING_TITLE,
]


# INVALID DESCRIPTION CASES

TOO_LONG_DESCRIPTION = {"title": "Valid title", "description": "a" * 1001}

INVALID_DESCRIPTION_CASES = [
    TOO_LONG_DESCRIPTION,
]

# INVALID PRIORITY CASES

INVALID_PRIORITY_STRING = {"title": "Valid title", "priority": "invalid"}

INVALID_PRIORITY_NUMBER = {"title": "Valid title", "priority": 999}

INVALID_PRIORITY_CASES = [
    INVALID_PRIORITY_STRING,
    INVALID_PRIORITY_NUMBER,
]

# INVALID DEADLINE CASES

PAST_DEADLINE = {"title": "Valid title", "deadline": "2020-01-01T00:00:00Z"}

INVALID_DEADLINE_FORMAT = {"title": "Valid title", "deadline": "not-a-date"}

INVALID_DEADLINE_CASES = [
    PAST_DEADLINE,
    INVALID_DEADLINE_FORMAT,
]

# INVALID ID FORMAT
INVALID_ID_STRING = "invalid_id"

# NON-EXISTENT ID
NON_EXISTENT_TASK_ID = "123e4567-e89b-12d3-a456-426614174000"

# UPDATE CASES
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
