from typing import Iterable

class TaskExpectations:
    # ---- HTTP ----

    def assert_status_code(self, response, expected: int) -> None:
        assert response.status_code == expected, (
            f"Expected status code {expected}, "
            f"got {response.status_code}. "
            f"Response body: {response.text}"
        )

    # ---- Task response ----

    def assert_task_base_fields(self, data: dict) -> None:
        for field in ("id", "title", "status", "created_at", "updated_at"):
            assert field in data, f"Missing field '{field}' in task response. Full response: {data}"

    def assert_task_status(self, data: dict, expected_status: str) -> None:
        assert "status" in data, f"Missing 'status' field in task response. Full response: {data}"
        assert data["status"] == expected_status, (
            f"Expected task status '{expected_status}', got '{data['status']}'. Full response: {data}"
        )

    def assert_task_values(self, data: dict, expected: dict) -> None:
        for key, value in expected.items():
            actual = data.get(key)
            assert actual == value, (
                f"Field '{key}' mismatch. Expected: {value!r}, got: {actual!r}. Full response: {data}"
            )

    # ---- List response ----

    def assert_task_list_response(self, data: dict, expected_total: int) -> None:
        assert "tasks" in data and isinstance(data["tasks"], list), (
            f"'tasks' must be a list. Got: {data}"
        )
        assert "total" in data and isinstance(data["total"], int), (
            f"'total' must be int. Got: {data}"
        )
        assert data["total"] == expected_total, (
            f"Expected total {expected_total}, got {data['total']}"
        )
        assert len(data["tasks"]) == expected_total, (
            f"Tasks list length {len(data['tasks'])} does not match expected total {expected_total}. "
            f"Full response: {data}"
        )

    # ---- Errors ----

    def assert_validation_error(self, response, expected_status: int = 400) -> None:
        assert response.status_code == expected_status, (
            f"Expected validation status {expected_status}, "
            f"got {response.status_code}. "
            f"Response body: {response.text}"
        )
        body = response.json()
        assert "detail" in body, f"Expected 'detail' in validation error response. Got: {body}"
        assert body["detail"], f"'detail' must not be empty. Full response: {body}"

    def assert_not_found(self, response, expected_status: int = 404) -> None:
        assert response.status_code == expected_status, (
            f"Expected HTTP {expected_status} (not found), "
            f"got {response.status_code}. "
            f"Response body: {response.text}"
        )
