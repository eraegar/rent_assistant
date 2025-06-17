from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime
from enum import Enum

# User schemas
class UserCreate(BaseModel):
    phone: str
    password: str
    name: str

class UserLogin(BaseModel):
    phone: str
    password: str

class UserOut(BaseModel):
    id: int
    phone: str
    name: str
    
    class Config:
        from_attributes = True

# Task enums for API
class TaskStatusEnum(str, Enum):
    pending = "pending"
    completed = "completed"
    revision = "revision"

class TaskTypeEnum(str, Enum):
    personal = "personal"
    business = "business"

class TaskPriorityEnum(str, Enum):
    low = "low"
    medium = "medium"
    high = "high"

class TaskSpeedEnum(str, Enum):
    standard = "standard"
    fast = "fast"
    urgent = "urgent"

# Task schemas
class TaskCreate(BaseModel):
    title: str
    description: Optional[str] = None
    type: TaskTypeEnum = TaskTypeEnum.personal
    priority: TaskPriorityEnum = TaskPriorityEnum.low
    speed: TaskSpeedEnum = TaskSpeedEnum.standard

class TaskUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    type: Optional[TaskTypeEnum] = None
    priority: Optional[TaskPriorityEnum] = None
    speed: Optional[TaskSpeedEnum] = None
    status: Optional[TaskStatusEnum] = None

class TaskOut(BaseModel):
    id: int
    title: str
    description: Optional[str]
    type: TaskTypeEnum
    status: TaskStatusEnum
    priority: TaskPriorityEnum
    speed: TaskSpeedEnum
    assistant: Optional[str]
    created_at: datetime
    completed_at: Optional[datetime]
    user_id: int
    
    class Config:
        from_attributes = True

class TaskStats(BaseModel):
    total_tasks: int
    completed_tasks: int
    pending_tasks: int
    revision_tasks: int

