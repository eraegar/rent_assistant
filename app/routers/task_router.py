from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from ..schemas import TaskCreate, TaskResponse
from ..database import SessionLocal
from ..services.task_service import (
    create_task as svc_create_task,
    get_tasks_by_user,
    update_task_status as svc_update_task_status,
    delete_task as svc_delete_task
)
from ..auth import decode_jwt

router = APIRouter(prefix="/tasks", tags=["tasks"])

# Security scheme for Swagger UI integration
bearer_scheme = HTTPBearer()

# Dependency: get DB session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Dependency: extract user_id from Bearer token
def get_user_id(credentials: HTTPAuthorizationCredentials = Depends(bearer_scheme)) -> str:
    token = credentials.credentials
    payload = decode_jwt(token)
    return payload.get("user_id")

@router.post("/", response_model=TaskResponse)
def create(
    task: TaskCreate,
    user_id: str = Depends(get_user_id),
    db: Session = Depends(get_db)
):
    return svc_create_task(db, task, user_id)

@router.get("/", response_model=List[TaskResponse])
def read_all(
    user_id: str = Depends(get_user_id),
    db: Session = Depends(get_db)
):
    return get_tasks_by_user(db, user_id)

@router.put("/{task_id}", response_model=TaskResponse)
def update_status(
    task_id: int,
    status: str,
    user_id: str = Depends(get_user_id),
    db: Session = Depends(get_db)
):
    task = svc_update_task_status(db, task_id, status, user_id)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    return task

@router.delete("/{task_id}")
def delete(
    task_id: int,
    user_id: str = Depends(get_user_id),
    db: Session = Depends(get_db)
):
    success = delete_task(db, task_id, user_id)
    if not success:
        raise HTTPException(status_code=404, detail="Task not found")
    return {"message": "Deleted"}
