from sqlalchemy.orm import Session
from ..models import Task
from ..schemas import TaskCreate

def create_task(db: Session, task_data: TaskCreate, user_id: str) -> Task:
    task = Task(
        title=task_data.title,
        description=task_data.description,
        type=task_data.type,
        priority=task_data.priority,
        user_id=int(user_id),
    )
    db.add(task)
    db.commit()
    db.refresh(task)
    return task

def get_tasks_by_user(db:Session, user_id:str):
    return db.query(Task).filter(Task.user_id == int(user_id)).all()

def update_task_status(db:Session, task_id: int, status: str, user_id : str):
    task = db.query(Task).filter(
        Task.id == task_id,
        Task.user_id == int(user_id)
    ).first()
    if not task:
        return None
    task.status = status
    db.commit()
    db.refresh(task)
    return task

def delete_task(db:Session, task_id: int, user_id: str) -> bool:
    task = db.query(Task).filter(
        Task.id == task_id,
        Task.user_id == int(user_id)
    ).first()
    if not task:
        return False
    db.delete(task)
    db.commit()
    return True
