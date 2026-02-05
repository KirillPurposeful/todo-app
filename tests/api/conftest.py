import pytest
from fastapi.testclient import TestClient

from src.api.app import app
from src.api.dependencies import get_task_repository


@pytest.fixture
def client():
    """FastAPI test client for API testing."""
    return TestClient(app)



@pytest.fixture(autouse=True)
def reset_repo():
    get_task_repository().clear()