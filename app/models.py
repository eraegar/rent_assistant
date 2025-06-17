from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey, Enum
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from datetime import datetime
import enum

Base = declarative_base()

class User(Base):
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True)
    phone = Column(String, unique=True, index=True)
    name = Column(String)
    password_hash = Column(String)
    
    # Relationship with tasks
    tasks = relationship("Task", back_populates="user")

class TaskStatus(enum.Enum):
    pending = "pending"
    completed = "completed"
    revision = "revision"

class TaskType(enum.Enum):
    personal = "personal"
    business = "business"

class TaskPriority(enum.Enum):
    low = "low"
    medium = "medium"
    high = "high"

class TaskSpeed(enum.Enum):
    standard = "standard"
    fast = "fast"
    urgent = "urgent"

class Task(Base):
    __tablename__ = "tasks"
    
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    description = Column(Text)
    type = Column(Enum(TaskType), default=TaskType.personal)
    status = Column(Enum(TaskStatus), default=TaskStatus.pending)
    priority = Column(Enum(TaskPriority), default=TaskPriority.low)
    speed = Column(Enum(TaskSpeed), default=TaskSpeed.standard)
    assistant = Column(String)  # Assigned assistant name
    created_at = Column(DateTime, default=datetime.utcnow)
    completed_at = Column(DateTime, nullable=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    
    # Relationship with user
    user = relationship("User", back_populates="tasks")