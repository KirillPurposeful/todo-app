from fastapi import FastAPI

from src.api.routes import router

app = FastAPI(
    title="TODO App",
    description="Simple TODO application with clean architecture",
    version="1.0.0",
    docs_url="/docs",  #
)

app.include_router(router)
