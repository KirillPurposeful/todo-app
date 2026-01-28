from fastapi import FastAPI

from src.api.handlers.exception_handlers import (
    task_not_found_handler,
    validation_error_handler,
)
from src.api.routers.tasks import router
from src.exceptions import TaskNotFoundError, ValidationError

app = FastAPI(
    title="TODO App",
    description="Simple TODO application with clean architecture",
    version="1.0.0",
    docs_url="/docs",
)

app.include_router(router)
app.add_exception_handler(ValidationError, validation_error_handler)
app.add_exception_handler(TaskNotFoundError, task_not_found_handler)
