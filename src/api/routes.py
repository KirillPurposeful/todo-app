from typing import Annotated
from uuid import UUID

from fastapi import APIRouter, Depends, status


from src.api.dependencies import get_task_service
from src.api.schemas.task_schema import TaskResponse, TaskCreate
from src.entities.task import Task
from src.repositories.memory import InMemoryTaskRepository

router = APIRouter(prefix="/api/v1/tasks", tags=["tasks"])


@router.get("/", response_model=list[TaskResponse])
async def list_tasks(
    service: Annotated[InMemoryTaskRepository, Depends(get_task_service)],
) -> list[TaskResponse]:
    tasks = service.get_all()
    return [TaskResponse(**task.to_dict()) for task in tasks]

@router.post(
    "/",
    response_model=str,
    status_code=status.HTTP_201_CREATED,
)
async def create_product(
    data: TaskCreate,
    service: Annotated[InMemoryTaskRepository, Depends(get_task_service)],
) -> str:
    product = service.save(Task(title=data.title))
    return str(product.id)

@router.get("/{task_id}", response_model=TaskResponse)
async def get_product(
    task_id: str,
    service: Annotated[InMemoryTaskRepository, Depends(get_task_service)]
) -> TaskResponse:
    task = service.get_by_id(UUID(task_id))
    return TaskResponse(**task.to_dict())


@router.delete("/{task_id}", response_model=bool)
async def delete_product(
    task_id: str,
    service: Annotated[InMemoryTaskRepository, Depends(get_task_service)]
) -> bool:
    service.delete(UUID(task_id))
    return True