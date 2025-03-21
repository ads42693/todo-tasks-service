from fastapi import APIRouter, Depends, HTTPException, status
from typing import List
from app.core.auth import get_current_user
from app.models.user import User
from app.schemas.task import TaskCreate, TaskUpdate, TaskResponse
from app.services.task_service import TaskService
from app.core.database import get_db

router = APIRouter()

@router.get("/tasks", response_model=List[TaskResponse])
async def get_tasks(
    current_user: User = Depends(get_current_user),
    db = Depends(get_db),
    skip: int = 0,
    limit: int = 100
):
    """Get all tasks for the current user"""
    service = TaskService(db)
    tasks = await service.get_tasks(current_user.id, skip, limit)
    return tasks

@router.post("/tasks", response_model=TaskResponse, status_code=status.HTTP_201_CREATED)
async def create_task(
    task: TaskCreate,
    current_user: User = Depends(get_current_user),
    db = Depends(get_db)
):
    """Create a new task for the current user"""
    service = TaskService(db)
    return await service.create_task(task, current_user.id)

@router.get("/tasks/{task_id}", response_model=TaskResponse)
async def get_task(
    task_id: int,
    current_user: User = Depends(get_current_user),
    db = Depends(get_db)
):
    """Get a specific task by ID"""
    service = TaskService(db)
    task = await service.get_task(task_id, current_user.id)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    return task

@router.put("/tasks/{task_id}", response_model=TaskResponse)
async def update_task(
    task_id: int,
    task_update: TaskUpdate,
    current_user: User = Depends(get_current_user),
    db = Depends(get_db)
):
    """Update a task"""
    service = TaskService(db)
    task = await service.get_task(task_id, current_user.id)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    
    updated_task = await service.update_task(task_id, task_update)
    return updated_task

@router.delete("/tasks/{task_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_task(
    task_id: int,
    current_user: User = Depends(get_current_user),
    db = Depends(get_db)
):
    """Delete a task"""
    service = TaskService(db)
    task = await service.get_task(task_id, current_user.id)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    
    await service.delete_task(task_id)
    return None