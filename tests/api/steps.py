"""API test steps - actions performed in tests."""

from starlette.testclient import TestClient
from starlette.responses import Response


class TaskSteps:
    """Steps for task API testing."""

    BASE_URL = "/api/v1/tasks"

    def create_task(self, client: TestClient, payload: dict) -> Response:
        """Create a new task via POST /api/v1/tasks."""
        return client.post(f"{self.BASE_URL}/", json=payload)

    def get_task(self, client: TestClient, task_id: str) -> Response:
        """Get task by ID via GET /api/v1/tasks/{task_id}."""
        return client.get(f"{self.BASE_URL}/{task_id}")

    def list_tasks(self, client: TestClient) -> Response:
        """Get all tasks via GET /api/v1/tasks."""
        return client.get(f"{self.BASE_URL}/")

    def update_task(self, client: TestClient, task_id: str, payload: dict) -> Response:
        """Update task via PUT /api/v1/tasks/{task_id}."""
        return client.put(f"{self.BASE_URL}/{task_id}", json=payload)

    def delete_task(self, client: TestClient, task_id: str) -> Response:
        """Delete task via DELETE /api/v1/tasks/{task_id}."""
        return client.delete(f"{self.BASE_URL}/{task_id}")

    def complete_task(self, client: TestClient, task_id: str) -> Response:
        """Complete task via POST /api/v1/tasks/{task_id}/complete."""
        return client.post(f"{self.BASE_URL}/{task_id}/complete")
