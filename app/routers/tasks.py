from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from datetime import datetime
import random

import models, schemas, database, auth

router = APIRouter(prefix="/tasks", tags=["tasks"])

def get_db():
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()

# List of assistant names for random assignment
ASSISTANTS = [
    "Анна Петрова", "Максим Иванов", "Елена Сидорова", 
    "Дмитрий Козлов", "Мария Волкова", "Александр Морозов"
]

@router.get("/", response_model=List[schemas.TaskOut])
def get_tasks(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=100),
    status: Optional[schemas.TaskStatusEnum] = None,
    type: Optional[schemas.TaskTypeEnum] = None,
    current_user: models.User = Depends(auth.get_current_user),
    db: Session = Depends(get_db)
):
    """Get user's tasks with optional filtering"""
    query = db.query(models.Task).filter(models.Task.user_id == current_user.id)
    
    if status:
        query = query.filter(models.Task.status == status)
    if type:
        query = query.filter(models.Task.type == type)
    
    tasks = query.order_by(models.Task.created_at.desc()).offset(skip).limit(limit).all()
    return tasks

@router.post("/", response_model=schemas.TaskOut)
def create_task(
    task: schemas.TaskCreate,
    current_user: models.User = Depends(auth.get_current_user),
    db: Session = Depends(get_db)
):
    """Create a new task"""
    # Assign random assistant
    assistant = random.choice(ASSISTANTS)
    
    db_task = models.Task(
        title=task.title,
        description=task.description,
        type=task.type,
        priority=task.priority,
        speed=task.speed,
        assistant=assistant,
        user_id=current_user.id
    )
    
    db.add(db_task)
    db.commit()
    db.refresh(db_task)
    return db_task

@router.get("/{task_id}", response_model=schemas.TaskOut)
def get_task(
    task_id: int,
    current_user: models.User = Depends(auth.get_current_user),
    db: Session = Depends(get_db)
):
    """Get a specific task"""
    task = db.query(models.Task).filter(
        models.Task.id == task_id,
        models.Task.user_id == current_user.id
    ).first()
    
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    
    return task

@router.put("/{task_id}", response_model=schemas.TaskOut)
def update_task(
    task_id: int,
    task_update: schemas.TaskUpdate,
    current_user: models.User = Depends(auth.get_current_user),
    db: Session = Depends(get_db)
):
    """Update a task"""
    task = db.query(models.Task).filter(
        models.Task.id == task_id,
        models.Task.user_id == current_user.id
    ).first()
    
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    
    # Update fields that are provided
    update_data = task_update.dict(exclude_unset=True)
    for field, value in update_data.items():
        setattr(task, field, value)
    
    # If status is being changed to completed, set completion time
    if task_update.status == schemas.TaskStatusEnum.completed and task.status != models.TaskStatus.completed:
        task.completed_at = datetime.utcnow()
    
    db.commit()
    db.refresh(task)
    return task

@router.delete("/{task_id}")
def delete_task(
    task_id: int,
    current_user: models.User = Depends(auth.get_current_user),
    db: Session = Depends(get_db)
):
    """Delete a task"""
    task = db.query(models.Task).filter(
        models.Task.id == task_id,
        models.Task.user_id == current_user.id
    ).first()
    
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    
    db.delete(task)
    db.commit()
    return {"message": "Task deleted successfully"}

@router.get("/stats/overview", response_model=schemas.TaskStats)
def get_task_stats(
    current_user: models.User = Depends(auth.get_current_user),
    db: Session = Depends(get_db)
):
    """Get task statistics for the current user"""
    tasks = db.query(models.Task).filter(models.Task.user_id == current_user.id).all()
    
    total_tasks = len(tasks)
    completed_tasks = len([t for t in tasks if t.status == models.TaskStatus.completed])
    pending_tasks = len([t for t in tasks if t.status == models.TaskStatus.pending])
    revision_tasks = len([t for t in tasks if t.status == models.TaskStatus.revision])
    
    return schemas.TaskStats(
        total_tasks=total_tasks,
        completed_tasks=completed_tasks,
        pending_tasks=pending_tasks,
        revision_tasks=revision_tasks
    )

@router.get("/analytics/monthly")
def get_monthly_analytics(
    current_user: models.User = Depends(auth.get_current_user),
    db: Session = Depends(get_db)
):
    """Get monthly task completion analytics"""
    # This is a simplified version - you might want to implement 
    # more sophisticated analytics based on actual dates
    completed_tasks = db.query(models.Task).filter(
        models.Task.user_id == current_user.id,
        models.Task.status == models.TaskStatus.completed
    ).all()
    
    # Mock weekly data for now
    weekly_data = [3, 5, 4, 6]  # You can replace this with real calculation
    
    return {
        "labels": ["Нед 1", "Нед 2", "Нед 3", "Нед 4"],
        "data": weekly_data
    }

@router.get("/analytics/types")
def get_task_type_analytics(
    current_user: models.User = Depends(auth.get_current_user),
    db: Session = Depends(get_db)
):
    """Get task type distribution analytics"""
    tasks = db.query(models.Task).filter(models.Task.user_id == current_user.id).all()
    
    business_count = len([t for t in tasks if t.type == models.TaskType.business])
    personal_count = len([t for t in tasks if t.type == models.TaskType.personal])
    
    return {
        "labels": ["Бизнес-задачи", "Личные задачи"],
        "data": [business_count, personal_count]
    } 