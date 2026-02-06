"""API test steps - actions performed in tests."""

from starlette.responses import Response
from starlette.testclient import TestClient


class TaskSteps:

    BASE_URL = "/api/v1/tasks"

    def create_task(self, client: TestClient, payload: dict) -> Response:
        return client.post(f"{self.BASE_URL}/", json=payload)

    def get_task(self, client: TestClient, task_id: str) -> Response:
        return client.get(f"{self.BASE_URL}/{task_id}")

    def list_tasks(self, client: TestClient) -> Response:
        return client.get(f"{self.BASE_URL}/")

    def update_task(self, client: TestClient, task_id: str, payload: dict) -> Response:
        return client.put(f"{self.BASE_URL}/{task_id}", json=payload)

    def delete_task(self, client: TestClient, task_id: str) -> Response:
        return client.delete(f"{self.BASE_URL}/{task_id}")

    def complete_task(self, client: TestClient, task_id: str) -> Response:
        return client.post(f"{self.BASE_URL}/{task_id}/complete")
