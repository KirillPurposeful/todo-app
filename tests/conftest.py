import datetime

import pytest

from src.entities.task import Task


@pytest.fixture
def sample_task():
    return Task(title="Test Task")


@pytest.fixture
def past_date():
    return datetime.datetime.now(datetime.UTC) - datetime.timedelta(days=1)


@pytest.fixture
def future_date():
    return datetime.datetime.now(datetime.UTC) + datetime.timedelta(days=7)
