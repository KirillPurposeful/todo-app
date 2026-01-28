from fastapi import Request, status
from fastapi.responses import JSONResponse


def validation_error_handler(request: Request, exc: Exception) -> JSONResponse:  # noqa: ARG001
    return JSONResponse(
        status_code=status.HTTP_400_BAD_REQUEST,
        content={"error": "ValidationError", "message": str(exc)},
    )


def task_not_found_handler(request: Request, exc: Exception) -> JSONResponse:  # noqa: ARG001
    return JSONResponse(
        status_code=status.HTTP_404_NOT_FOUND,
        content={"error": "TaskNotFoundError", "message": str(exc)},
    )
