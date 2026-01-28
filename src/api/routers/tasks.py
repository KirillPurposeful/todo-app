from typing import Annotated
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, status

from src.api.dependencies import get_task_repository
from src.api.schemas.task_schema import TaskCreate, TaskListResponse, TaskResponse, TaskUpdate
from src.entities.task import Task
from src.repositories.memory import InMemoryTaskRepository

router = APIRouter(prefix="/api/v1/tasks", tags=["tasks"])


def to_response(task: Task) -> TaskResponse:
    return TaskResponse(**task.to_dict())


def get_task_or_404(task_id: UUID, repository: InMemoryTaskRepository) -> Task:
    task = repository.get_by_id(task_id)
    if task is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=f"Task {task_id} not found"
        )
    return task


@router.get("/", response_model=TaskListResponse)
async def get_list_tasks(
    repository: Annotated[InMemoryTaskRepository, Depends(get_task_repository)],
) -> TaskListResponse:
    tasks = repository.get_all()
    total = len(tasks)
    task_responses = [to_response(task) for task in tasks]
    return TaskListResponse(tasks=task_responses, total=total)


@router.post(
    "/",
    response_model=TaskResponse,
    status_code=status.HTTP_201_CREATED,
)
async def create_task(
    data: TaskCreate,
    repository: Annotated[InMemoryTaskRepository, Depends(get_task_repository)],
) -> TaskResponse:
    task = repository.save(
        Task(
            title=data.title,
            description=data.description,
            priority=data.priority,
            deadline=data.deadline,
        )
    )
    return to_response(task)


@router.get("/{task_id}", response_model=TaskResponse)
async def get_task(
    task_id: UUID, repository: Annotated[InMemoryTaskRepository, Depends(get_task_repository)]
) -> TaskResponse:
    task = get_task_or_404(task_id, repository)
    return to_response(task)


@router.delete("/{task_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_task(
    task_id: UUID, repository: Annotated[InMemoryTaskRepository, Depends(get_task_repository)]
) -> None:
    result = repository.delete(task_id)
    if not result:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=f"Task {task_id} not found"
        )


@router.put("/{task_id}", response_model=TaskResponse)
async def update_task(
    task_id: UUID,
    data: TaskUpdate,
    repository: Annotated[InMemoryTaskRepository, Depends(get_task_repository)],
) -> TaskResponse:
    task = get_task_or_404(task_id, repository)

    task.update(
        title=data.title,
        description=data.description,
        priority=data.priority,
        deadline=data.deadline,
    )

    updated_task = repository.save(task)
    return to_response(updated_task)


@router.post("/{task_id}/complete", response_model=TaskResponse)
async def complete_task(
    task_id: UUID,
    repository: Annotated[InMemoryTaskRepository, Depends(get_task_repository)],
) -> TaskResponse:
    task = get_task_or_404(task_id, repository)
    task.mark_completed()
    updated_task = repository.save(task)
    return to_response(updated_task)

