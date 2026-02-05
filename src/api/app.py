from fastapi import FastAPI

from src.api.routers.tasks import task_router

app = FastAPI(
    title="TODO App",
    description="Simple TODO application with clean architecture",
    version="1.0.0",
    docs_url="/docs",
)

app.include_router(task_router)
