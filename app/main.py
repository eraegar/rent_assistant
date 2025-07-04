import os
from fastapi import FastAPI, Depends, HTTPException, status, Header, Request, Query
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from sqlalchemy.orm import Session
from sqlalchemy import func
from fastapi.middleware.cors import CORSMiddleware
import models, schemas, database, auth
import sys
from datetime import datetime, timedelta
from typing import Optional

# Import new API routers
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

try:
    from routers.client_api import router as client_router
    print("✅ Client API router loaded successfully")
except ImportError as e:
    print(f"⚠️ Client API router not found, creating placeholder. Error: {e}")
    from fastapi import APIRouter
    client_router = APIRouter(prefix="/api/v1/clients", tags=["clients"])

try:
    from routers.assistant_api import router as assistant_router
    print("✅ Assistant API router loaded successfully")
except ImportError as e:
    print(f"⚠️ Assistant API router not found, creating placeholder. Error: {e}")
    from fastapi import APIRouter
    assistant_router = APIRouter(prefix="/api/v1/assistants", tags=["assistants"])

try:
    from routers.management_api import router as management_router
    print("✅ Management API router loaded successfully")
except ImportError as e:
    print(f"⚠️ Management API router not found, creating placeholder. Error: {e}")
from fastapi import APIRouter
    management_router = APIRouter(prefix="/api/v1/management", tags=["management"])

# Create database tables
print("Creating database tables...")
models.Base.metadata.create_all(bind=database.engine)
print("Database tables created successfully!")

app = FastAPI(
    title="Assistant-for-Rent API", 
    version="2.0.0",
    description="Multi-service API for Client, Assistant, and Management interfaces"
)

# Background task lifecycle events
@app.on_event("startup")
async def startup_event():
    """Initialize application services"""
    print("🚀 Application starting up...")
    print("✅ Application startup complete")

@app.on_event("shutdown")
async def shutdown_event():
    """Cleanup application services"""
    print("🛑 Application shutting down...")
    print("✅ Application shutdown complete")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify your domains
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

def get_db():
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()

# =============================================================================
# INCLUDE NEW API ROUTERS
# =============================================================================

# Include the new service-specific routers
app.include_router(client_router)
app.include_router(assistant_router)
app.include_router(management_router)

# =============================================================================
# LEGACY ENDPOINTS (for backward compatibility)
# =============================================================================

from fastapi import APIRouter
auth_router = APIRouter(prefix="/auth", tags=["legacy-auth"])

@auth_router.post("/register", response_model=schemas.UserOut)
def legacy_register(user: schemas.UserCreate, db: Session = Depends(get_db)):
    """Legacy registration endpoint - redirects to client registration"""
    print(f"🔥 Legacy registration attempt - redirecting to client API")
    
    # For now, assume all legacy registrations are clients
    if user.role == models.UserRole.client:
        # Redirect to client registration logic
        existing_user = db.query(models.User).filter(models.User.phone == user.phone).first()
        if existing_user:
            raise HTTPException(status_code=400, detail="Phone already registered")
        
        hashed = auth.get_password_hash(user.password)
        db_user = models.User(
            phone=user.phone, 
            password_hash=hashed, 
            name=user.name,
            role=user.role,
            telegram_username=user.telegram_username
        )
        
        db.add(db_user)
        db.flush()
        
        # Create appropriate profile based on role
        if user.role == models.UserRole.client:
            client_profile = models.ClientProfile(user_id=db_user.id)
            db.add(client_profile)
        
        db.commit()
        db.refresh(db_user)
        
        return db_user
    else:
        raise HTTPException(status_code=400, detail="Use role-specific registration endpoints")

@auth_router.post("/login")
def legacy_login(user: schemas.UserLogin, db: Session = Depends(get_db)):
    """Legacy login endpoint"""
    print(f"🔑 Legacy login attempt: {user.phone}")
    db_user = db.query(models.User).filter(models.User.phone == user.phone).first()
    if not db_user or not auth.verify_password(user.password, db_user.password_hash):
        raise HTTPException(status_code=400, detail="Incorrect phone or password")
    
    token = auth.create_access_token({
        "user_id": db_user.id, 
        "role": db_user.role.value
    })
    return {"access_token": token, "token_type": "bearer"}

@auth_router.get("/me", response_model=schemas.UserOut)
def get_me(current_user: models.User = Depends(auth.get_current_user)):
    return current_user

# Include legacy auth router
app.include_router(auth_router)

# Include legacy tasks router for backward compatibility
try:
    from routers import tasks as legacy_tasks
    app.include_router(legacy_tasks.router, prefix="/legacy")
    print("✅ Legacy tasks router loaded successfully")
except ImportError as e:
    print(f"⚠️ Legacy tasks router not found. Error: {e}")

# =============================================================================
# STATIC FILES & FRONTEND
# =============================================================================

# Mount static files - commented out since we use separate React apps now
# frontend_dir = os.path.join(os.path.dirname(__file__), "frontend")
# app.mount("/static", StaticFiles(directory=frontend_dir), name="static")

# Serve a simple API info page instead of HTML frontend
@app.get("/")
def read_root():
    """API information root endpoint"""
    print("🏠 Serving API info")
    return {
        "message": "Telegram Assistant API v2.0.0",
        "services": {
            "client_app": "http://localhost:3000",
            "manager_app": "http://localhost:3001",
            "api_docs": "http://localhost:8000/docs"
        },
        "status": "running"
    }

# =============================================================================
# ASSISTANT API ENDPOINTS (Direct implementation)
# =============================================================================

@app.post("/api/v1/assistants/auth/register")
async def register_assistant_direct(request: Request, db: Session = Depends(get_db)):
    """Direct assistant registration endpoint"""
    try:
        print("📝 Assistant registration attempt")
        data = await request.json()
        print(f"Data: {data}")
        
        required_fields = ["name", "phone", "password", "email"]
        for field in required_fields:
            if field not in data or not data[field]:
                raise HTTPException(status_code=400, detail=f"Missing required field: {field}")
        print("✅ Required fields validated")
        
        # Check if phone already exists
        existing_user = db.query(models.User).filter(models.User.phone == data["phone"]).first()
        if existing_user:
            raise HTTPException(status_code=400, detail="Phone number already registered")
        print("✅ Phone number is available")
        
        # Create user
        hashed_password = auth.get_password_hash(data["password"])
        print("✅ Password hashed")
        
        db_user = models.User(
            phone=data["phone"],
            name=data["name"],
            password_hash=hashed_password,
            role=models.UserRole.assistant,
            telegram_username=data.get("telegram_username")
        )
        print("✅ User object created")
        
        db.add(db_user)
        db.flush()
        print(f"✅ User added to DB, ID: {db_user.id}")
        
        # Create assistant profile
        specialization = data.get("specialization", "personal_only")
        if specialization not in [spec.value for spec in models.AssistantSpecialization]:
            specialization = "personal_only"
        
        assistant_profile = models.AssistantProfile(
            user_id=db_user.id,
            email=data["email"],
            specialization=getattr(models.AssistantSpecialization, specialization),
            status="offline"
        )
        print("✅ Assistant profile created")
        
        db.add(assistant_profile)
        db.commit()
        print("✅ Changes committed to DB")
        
        db.refresh(db_user)
        print("✅ User refreshed from DB")
        
        response = {
            "id": db_user.id,
            "name": db_user.name,
            "email": assistant_profile.email,
            "telegram_username": db_user.telegram_username,
            "specialization": assistant_profile.specialization.value,
            "status": assistant_profile.status,
            "current_active_tasks": 0,
            "total_tasks_completed": 0,
            "average_rating": 0.0
        }
        print(f"✅ Assistant registration successful: {response}")
        return response
        
    except HTTPException:
        raise
    except Exception as e:
        print(f"❌ Assistant registration error: {str(e)}")
        import traceback
        traceback.print_exc()
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")

@app.post("/api/v1/assistants/auth/login")
async def login_assistant_direct(request: Request, db: Session = Depends(get_db)):
    """Direct assistant login endpoint"""
    try:
        print("🔐 Assistant login attempt")
        data = await request.json()
        print(f"Login data: {data}")
        
        user = db.query(models.User).filter(
            models.User.phone == data["phone"],
            models.User.role == models.UserRole.assistant
        ).first()
        
        if not user:
            print("❌ Assistant not found")
            raise HTTPException(status_code=400, detail="Incorrect phone or password")
        
        if not auth.verify_password(data["password"], user.password_hash):
            print("❌ Password verification failed")
            raise HTTPException(status_code=400, detail="Incorrect phone or password")
        
        token = auth.create_access_token({"user_id": user.id, "role": "assistant"})
        print(f"✅ Assistant login successful for user: {user.id}")
        
        return {"access_token": token, "token_type": "bearer"}
        
    except HTTPException:
        raise
    except Exception as e:
        print(f"❌ Assistant login error: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")

@app.get("/api/v1/assistants/profile")
async def get_assistant_profile_direct(current_user: models.User = Depends(auth.get_current_user), db: Session = Depends(get_db)):
    """Direct assistant profile endpoint"""
    try:
        print(f"👤 Assistant profile request for user: {current_user.id}")
        
        # Reload user from DB to get relationships
        user = db.query(models.User).filter(models.User.id == current_user.id).first()
        if not user or user.role != models.UserRole.assistant:
            raise HTTPException(status_code=403, detail="Access denied. Assistant role required.")
        
        if not user.assistant_profile:
            raise HTTPException(status_code=404, detail="Assistant profile not found")
        
        profile = user.assistant_profile
        
        response = {
            "id": user.id,
            "name": user.name,
            "email": profile.email,
            "telegram_username": user.telegram_username,
            "specialization": profile.specialization.value,
            "status": profile.status,
            "current_active_tasks": profile.current_active_tasks,
            "total_tasks_completed": profile.total_tasks_completed,
            "average_rating": profile.average_rating
        }
        print(f"✅ Assistant profile response: {response}")
        return response
        
    except HTTPException:
        raise
    except Exception as e:
        print(f"❌ Assistant profile error: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")

@app.put("/api/v1/assistants/profile/status")
async def update_assistant_status_direct(request: Request, current_user: models.User = Depends(auth.get_current_user), db: Session = Depends(get_db)):
    """Direct assistant status update endpoint"""
    try:
        print(f"🔄 Assistant status update for user: {current_user.id}")
        data = await request.json()
        
        # Reload user from DB
        user = db.query(models.User).filter(models.User.id == current_user.id).first()
        if not user or user.role != models.UserRole.assistant:
            raise HTTPException(status_code=403, detail="Access denied. Assistant role required.")
        
        new_status = data.get("status", "offline")
        if new_status not in ["online", "offline"]:
            raise HTTPException(status_code=400, detail="Status must be 'online' or 'offline'")
        
        user.assistant_profile.status = new_status
        user.last_active = datetime.utcnow()
        
        db.commit()
        print(f"✅ Assistant status updated to: {new_status}")
        
        return {"success": True, "message": f"Status updated to {new_status}"}
        
    except HTTPException:
        raise
    except Exception as e:
        print(f"❌ Assistant status update error: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")

@app.get("/api/v1/assistants/tasks/marketplace")
async def get_marketplace_tasks_direct(
    skip: int = Query(0, ge=0),
    limit: int = Query(20, ge=1, le=100),
    task_type: Optional[str] = None,
    current_user: models.User = Depends(auth.get_current_user),
    db: Session = Depends(get_db)
):
    """Direct marketplace tasks endpoint"""
    try:
        print(f"🛒 Marketplace tasks request for assistant: {current_user.id}")
        
        # Reload user from DB
        user = db.query(models.User).filter(models.User.id == current_user.id).first()
        if not user or user.role != models.UserRole.assistant:
            raise HTTPException(status_code=403, detail="Access denied. Assistant role required.")
        
        # Get available tasks
        query = db.query(models.Task).filter(
            models.Task.status == models.TaskStatus.pending,
            models.Task.assistant_id.is_(None)  # Unclaimed tasks
        )
        
        # Filter by assistant specialization
        assistant_spec = user.assistant_profile.specialization
        if assistant_spec == models.AssistantSpecialization.personal_only:
            query = query.filter(models.Task.type == models.TaskType.personal)
        
        if task_type:
            query = query.filter(models.Task.type == task_type)
        
        tasks = query.order_by(models.Task.created_at.asc()).offset(skip).limit(limit).all()
        
        marketplace_tasks = []
        for task in tasks:
            # Calculate time remaining
            if task.deadline:
                time_remaining = task.deadline - datetime.utcnow()
                if time_remaining.total_seconds() > 0:
                    hours = int(time_remaining.total_seconds() // 3600)
                    minutes = int((time_remaining.total_seconds() % 3600) // 60)
                    time_remaining_str = f"{hours}ч {minutes}м"
                else:
                    time_remaining_str = "Просрочено"
            else:
                time_remaining_str = "Без дедлайна"
            
            marketplace_tasks.append({
                "id": task.id,
                "title": task.title,
                "description": task.description,
                "type": task.type.value,
                "client_name": task.client.user.name.split()[0],  # First name only
                "created_at": task.created_at.isoformat(),
                "deadline": task.deadline.isoformat() if task.deadline else None,
                "time_remaining": time_remaining_str
            })
        
        print(f"✅ Found {len(marketplace_tasks)} marketplace tasks")
        return marketplace_tasks
        
    except HTTPException:
        raise
    except Exception as e:
        print(f"❌ Marketplace tasks error: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")

@app.post("/api/v1/assistants/tasks/{task_id}/claim")
async def claim_task_direct(task_id: int, current_user: models.User = Depends(auth.get_current_user), db: Session = Depends(get_db)):
    """Direct task claim endpoint"""
    try:
        print(f"🎯 Task claim attempt: {task_id} by assistant: {current_user.id}")
        
        # Reload user from DB
        user = db.query(models.User).filter(models.User.id == current_user.id).first()
        if not user or user.role != models.UserRole.assistant:
            raise HTTPException(status_code=403, detail="Access denied. Assistant role required.")
        
        task = db.query(models.Task).filter(
            models.Task.id == task_id,
            models.Task.status == models.TaskStatus.pending,
            models.Task.assistant_id.is_(None)
        ).first()
        
        if not task:
            raise HTTPException(status_code=404, detail="Task not found or already claimed")
        
        # Check if assistant can handle this task type
        assistant_spec = user.assistant_profile.specialization
        if (assistant_spec == models.AssistantSpecialization.personal_only and 
            task.type == models.TaskType.business):
            raise HTTPException(
                status_code=403, 
                detail="Personal assistants cannot claim business tasks"
            )
        
        # Claim the task
        task.assistant_id = user.assistant_profile.id
        task.status = models.TaskStatus.in_progress
        task.claimed_at = datetime.utcnow()
        
        # Update assistant stats
        user.assistant_profile.current_active_tasks += 1
        
        db.commit()
        print(f"✅ Task {task_id} claimed successfully")
        
        return {"success": True, "message": "Task claimed successfully"}
        
    except HTTPException:
        raise
    except Exception as e:
        print(f"❌ Task claim error: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")

@app.get("/api/v1/assistants/dashboard/stats")
async def get_assistant_dashboard_stats_direct(current_user: models.User = Depends(auth.get_current_user), db: Session = Depends(get_db)):
    """Direct assistant dashboard stats endpoint"""
    try:
        print(f"📊 Dashboard stats request for assistant: {current_user.id}")
        
        # Reload user from DB
        user = db.query(models.User).filter(models.User.id == current_user.id).first()
        if not user or user.role != models.UserRole.assistant:
            raise HTTPException(status_code=403, detail="Access denied. Assistant role required.")
        
        assistant_id = user.assistant_profile.id
        
        # Task statistics
        total_tasks = db.query(models.Task).filter(
            models.Task.assistant_id == assistant_id
        ).count()
        
        active_tasks = db.query(models.Task).filter(
            models.Task.assistant_id == assistant_id,
            models.Task.status == models.TaskStatus.in_progress
        ).count()
        
        completed_tasks = db.query(models.Task).filter(
            models.Task.assistant_id == assistant_id,
            models.Task.status.in_([models.TaskStatus.completed, models.TaskStatus.approved])
        ).count()
        
        # Average rating
        avg_rating = db.query(models.Task.client_rating).filter(
            models.Task.assistant_id == assistant_id,
            models.Task.client_rating.isnot(None)
        ).all()
        
        average_rating = sum([rating[0] for rating in avg_rating]) / len(avg_rating) if avg_rating else 0.0
        
        # Available tasks in marketplace
        available_tasks = db.query(models.Task).filter(
            models.Task.status == models.TaskStatus.pending,
            models.Task.assistant_id.is_(None)
        ).count()
        
        stats = {
            "total_tasks": total_tasks,
            "active_tasks": active_tasks,
            "completed_tasks": completed_tasks,
            "average_rating": round(average_rating, 1),
            "available_marketplace_tasks": available_tasks,
            "status": user.assistant_profile.status,
            "specialization": user.assistant_profile.specialization.value
        }
        
        print(f"✅ Dashboard stats: {stats}")
        return stats
        
    except HTTPException:
        raise
    except Exception as e:
        print(f"❌ Dashboard stats error: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")

# =============================================================================
# ASSISTANT TASKS MANAGEMENT
# =============================================================================

@app.get("/api/v1/assistants/tasks/assigned")
async def get_assigned_tasks_direct(
    skip: int = Query(0, ge=0),
    limit: int = Query(20, ge=1, le=100),
    status: Optional[str] = None,
    current_user: models.User = Depends(auth.get_current_user),
    db: Session = Depends(get_db)
):
    """Direct assigned tasks endpoint"""
    try:
        print(f"📋 Assigned tasks request for assistant: {current_user.id}")
        
        # Reload user from DB
        user = db.query(models.User).filter(models.User.id == current_user.id).first()
        if not user or user.role != models.UserRole.assistant:
            raise HTTPException(status_code=403, detail="Access denied. Assistant role required.")
        
        query = db.query(models.Task).filter(
            models.Task.assistant_id == user.assistant_profile.id
        )
        
        if status:
            query = query.filter(models.Task.status == status)
        
        tasks = query.order_by(models.Task.claimed_at.desc()).offset(skip).limit(limit).all()
        
        task_list = []
        for task in tasks:
            task_list.append({
                "id": task.id,
                "title": task.title,
                "description": task.description,
                "type": task.type.value,
                "status": task.status.value,
                "created_at": task.created_at.isoformat(),
                "deadline": task.deadline.isoformat() if task.deadline else None,
                "claimed_at": task.claimed_at.isoformat() if task.claimed_at else None,
                "completed_at": task.completed_at.isoformat() if task.completed_at else None,
                "result": task.result,
                "completion_notes": task.completion_notes,
                "client_rating": task.client_rating,
                "client_feedback": task.client_feedback,
                "client_id": task.client_id
            })
        
        print(f"✅ Found {len(task_list)} assigned tasks")
        return task_list
        
    except HTTPException:
        raise
    except Exception as e:
        print(f"❌ Assigned tasks error: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")

@app.post("/api/v1/assistants/tasks/{task_id}/complete")
async def complete_task_direct(task_id: int, request: Request, current_user: models.User = Depends(auth.get_current_user), db: Session = Depends(get_db)):
    """Direct task completion endpoint"""
    try:
        print(f"✅ Task completion attempt: {task_id} by assistant: {current_user.id}")
        data = await request.json()
        
        # Reload user from DB
        user = db.query(models.User).filter(models.User.id == current_user.id).first()
        if not user or user.role != models.UserRole.assistant:
            raise HTTPException(status_code=403, detail="Access denied. Assistant role required.")
        
        task = db.query(models.Task).filter(
            models.Task.id == task_id,
            models.Task.assistant_id == user.assistant_profile.id,
            models.Task.status == models.TaskStatus.in_progress
        ).first()
        
        if not task:
            raise HTTPException(status_code=404, detail="Task not found or not in progress")
        
        # Update task with completion data
        task.status = models.TaskStatus.completed
        task.completed_at = datetime.utcnow()
        task.result = data.get("detailed_result", "")
        task.completion_notes = data.get("completion_summary", "")
        
        # Update assistant stats
        user.assistant_profile.current_active_tasks -= 1
        user.assistant_profile.total_tasks_completed += 1
        
        db.commit()
        print(f"✅ Task {task_id} completed successfully")
        
        return {"success": True, "message": "Task completed successfully"}
        
    except HTTPException:
        raise
    except Exception as e:
        print(f"❌ Task completion error: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")

# =============================================================================
# MANAGER API ENDPOINTS (Direct implementation)
# =============================================================================

@app.post("/api/v1/management/auth/register")
async def register_manager_direct(request: Request, db: Session = Depends(get_db)):
    """Direct manager registration endpoint"""
    try:
        print("📝 Manager registration attempt")
        data = await request.json()
        print(f"Data: {data}")
        
        required_fields = ["name", "phone", "password", "email"]
        for field in required_fields:
            if field not in data or not data[field]:
                raise HTTPException(status_code=400, detail=f"Missing required field: {field}")
        print("✅ Required fields validated")
        
        # Check if phone already exists
        existing_user = db.query(models.User).filter(models.User.phone == data["phone"]).first()
        if existing_user:
            raise HTTPException(status_code=400, detail="Phone number already registered")
        print("✅ Phone number is available")
        
        # Create user
        hashed_password = auth.get_password_hash(data["password"])
        print("✅ Password hashed")
        
        db_user = models.User(
            phone=data["phone"],
            name=data["name"],
            password_hash=hashed_password,
            role=models.UserRole.manager,
            telegram_username=data.get("telegram_username")
        )
        print("✅ User object created")
        
        db.add(db_user)
        db.flush()
        print(f"✅ User added to DB, ID: {db_user.id}")
        
        # Create manager profile
        manager_profile = models.ManagerProfile(
            user_id=db_user.id,
            email=data["email"],
            department=data.get("department", "Operations")
        )
        print("✅ Manager profile created")
        
        db.add(manager_profile)
        db.commit()
        print("✅ Changes committed to DB")
        
        db.refresh(db_user)
        print("✅ User refreshed from DB")
        
        response = {
            "id": db_user.id,
            "name": db_user.name,
            "email": manager_profile.email,
            "department": manager_profile.department
        }
        print(f"✅ Manager registration successful: {response}")
        return response
        
    except HTTPException:
        raise
    except Exception as e:
        print(f"❌ Manager registration error: {str(e)}")
        import traceback
        traceback.print_exc()
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")

@app.post("/api/v1/management/auth/login")
async def login_manager_direct(request: Request, db: Session = Depends(get_db)):
    """Direct manager login endpoint"""
    try:
        print("🔐 Manager login attempt")
        data = await request.json()
        print(f"Login data: {data}")
        
        user = db.query(models.User).filter(
            models.User.phone == data["phone"],
            models.User.role == models.UserRole.manager
        ).first()
        
        if not user:
            print("❌ Manager not found")
            raise HTTPException(status_code=400, detail="Incorrect phone or password")
        
        if not auth.verify_password(data["password"], user.password_hash):
            print("❌ Password verification failed")
            raise HTTPException(status_code=400, detail="Incorrect phone or password")
        
        token = auth.create_access_token({"user_id": user.id, "role": "manager"})
        print(f"✅ Manager login successful for user: {user.id}")
        
        return {"access_token": token, "token_type": "bearer"}
        
    except HTTPException:
        raise
    except Exception as e:
        print(f"❌ Manager login error: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")

@app.get("/api/v1/management/profile")
async def get_manager_profile_direct(current_user: models.User = Depends(auth.get_current_user), db: Session = Depends(get_db)):
    """Direct manager profile endpoint"""
    try:
        print(f"👤 Manager profile request for user: {current_user.id}")
        
        # Reload user from DB to get relationships
        user = db.query(models.User).filter(models.User.id == current_user.id).first()
        if not user or user.role != models.UserRole.manager:
            raise HTTPException(status_code=403, detail="Access denied. Manager role required.")
        
        if not user.manager_profile:
            raise HTTPException(status_code=404, detail="Manager profile not found")
        
        profile = user.manager_profile
        
        response = {
            "id": user.id,
            "name": user.name,
            "email": profile.email,
            "department": profile.department
        }
        print(f"✅ Manager profile response: {response}")
        return response
        
    except HTTPException:
        raise
    except Exception as e:
        print(f"❌ Manager profile error: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")

@app.get("/api/v1/management/dashboard/overview")
async def get_overview_analytics_direct(current_user: models.User = Depends(auth.get_current_user), db: Session = Depends(get_db)):
    """Direct overview analytics endpoint"""
    try:
        print(f"📊 Overview analytics request for manager: {current_user.id}")
        
        # Reload user from DB
        user = db.query(models.User).filter(models.User.id == current_user.id).first()
        if not user or user.role != models.UserRole.manager:
            raise HTTPException(status_code=403, detail="Access denied. Manager role required.")
        
        # Get real statistics from database
        total_tasks = db.query(models.Task).count()
        pending_tasks = db.query(models.Task).filter(models.Task.status == models.TaskStatus.pending).count()
        in_progress_tasks = db.query(models.Task).filter(models.Task.status == models.TaskStatus.in_progress).count()
        completed_tasks = db.query(models.Task).filter(
            models.Task.status.in_([models.TaskStatus.completed, models.TaskStatus.approved])
        ).count()
        
        # Tasks created this week
        week_ago = datetime.utcnow() - timedelta(days=7)
        new_tasks_week = db.query(models.Task).filter(models.Task.created_at >= week_ago).count()
        
        # Assistant statistics
        total_assistants = db.query(models.AssistantProfile).count()
        online_assistants = db.query(models.AssistantProfile).filter(
            models.AssistantProfile.status == "online"
        ).count()
        assistants_with_tasks = db.query(models.AssistantProfile).filter(
            models.AssistantProfile.current_active_tasks > 0
        ).count()
        
        avg_tasks_per_assistant = (
            db.query(func.avg(models.AssistantProfile.current_active_tasks)).scalar() or 0
        )
        
        # Client statistics
        total_clients = db.query(models.ClientProfile).count()
        active_subscribers = db.query(models.Subscription).filter(
            models.Subscription.status == models.SubscriptionStatus.active
        ).count()
        
        # New clients this week
        new_clients_week = db.query(models.User).filter(
            models.User.role == models.UserRole.client,
            models.User.created_at >= week_ago
        ).count()
        
        # Subscription distribution
        subscription_query = db.query(
            models.Subscription.plan, 
            func.count(models.Subscription.id)
        ).filter(
            models.Subscription.status == models.SubscriptionStatus.active
        ).group_by(models.Subscription.plan).all()
        
        subscription_distribution = {
            plan.value: count for plan, count in subscription_query
        }
        
        # Performance metrics
        task_completion_rate = (
            (completed_tasks / total_tasks * 100) if total_tasks > 0 else 0
        )
        
        assistant_utilization = (
            (online_assistants / total_assistants * 100) if total_assistants > 0 else 0
        )
        
        # Revenue metrics (все подписчики платят, конверсия не нужна)
        total_revenue = 0
        for plan, count in subscription_query:
            if plan == models.SubscriptionPlan.personal_2h:
                total_revenue += count * 15000  # 15,000 рублей
            elif plan == models.SubscriptionPlan.personal_5h:
                total_revenue += count * 30000  # 30,000 рублей
            elif plan == models.SubscriptionPlan.personal_8h:
                total_revenue += count * 50000  # 50,000 рублей
            elif plan == models.SubscriptionPlan.business_2h:
                total_revenue += count * 30000  # 30,000 рублей
            elif plan == models.SubscriptionPlan.business_5h:
                total_revenue += count * 60000  # 60,000 рублей
            elif plan == models.SubscriptionPlan.business_8h:
                total_revenue += count * 80000  # 80,000 рублей
            elif plan == models.SubscriptionPlan.full_2h:
                total_revenue += count * 40000  # 40,000 рублей
            elif plan == models.SubscriptionPlan.full_5h:
                total_revenue += count * 80000  # 80,000 рублей
            elif plan == models.SubscriptionPlan.full_8h:
                total_revenue += count * 100000  # 100,000 рублей
        
        overview = {
            "tasks": {
                "total": total_tasks,
                "pending": pending_tasks,
                "in_progress": in_progress_tasks,
                "completed": completed_tasks,
                "new_this_week": new_tasks_week
            },
            "assistants": {
                "total_active": total_assistants,
                "online_now": online_assistants,
                "with_active_tasks": assistants_with_tasks,
                "avg_tasks_per_assistant": round(avg_tasks_per_assistant, 1)
            },
            "clients": {
                "total_active": total_clients,
                "active_subscribers": active_subscribers,
                "new_this_week": new_clients_week,
                "subscription_distribution": subscription_distribution
            },
            "performance": {
                "task_completion_rate": round(task_completion_rate, 1),
                "assistant_utilization": round(assistant_utilization, 1),
                "monthly_revenue": total_revenue
            }
        }
        
        print(f"✅ Overview analytics: {overview}")
        return overview
        
    except HTTPException:
        raise
    except Exception as e:
        print(f"❌ Overview analytics error: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")

@app.get("/api/v1/management/tasks")
async def get_all_tasks_direct(
    skip: int = Query(0, ge=0),
    limit: int = Query(50, ge=1, le=100),
    status: Optional[str] = None,
    task_type: Optional[str] = None,
    current_user: models.User = Depends(auth.get_current_user),
    db: Session = Depends(get_db)
):
    """Direct get all tasks endpoint"""
    try:
        print(f"📋 All tasks request for manager: {current_user.id}")
        
        # Reload user from DB
        user = db.query(models.User).filter(models.User.id == current_user.id).first()
        if not user or user.role != models.UserRole.manager:
            raise HTTPException(status_code=403, detail="Access denied. Manager role required.")
        
        query = db.query(models.Task)
        
        # Apply filters
        if status:
            query = query.filter(models.Task.status == status)
        
        if task_type:
            query = query.filter(models.Task.type == task_type)
        
        # Get total count for pagination
        total_count = query.count()
        
        # Apply pagination and ordering
        tasks = query.order_by(models.Task.created_at.desc()).offset(skip).limit(limit).all()
        
        # Format response
        task_list = []
        for task in tasks:
            task_data = {
                "id": task.id,
                "title": task.title,
                "description": task.description,
                "type": task.type.value,
                "status": task.status.value,
                "created_at": task.created_at.isoformat(),
                "deadline": task.deadline.isoformat() if task.deadline else None,
                "claimed_at": task.claimed_at.isoformat() if task.claimed_at else None,
                "completed_at": task.completed_at.isoformat() if task.completed_at else None,
                "result": task.result,
                "completion_notes": task.completion_notes,
                "client_rating": task.client_rating,
                "client_feedback": task.client_feedback,
                "client": {
                    "id": task.client.id,
                    "name": task.client.user.name,
                    "phone": task.client.user.phone
                }
            }
            
            if task.assistant:
                task_data["assistant"] = {
                    "id": task.assistant.id,
                    "name": task.assistant.user.name,
                    "specialization": task.assistant.specialization.value
                }
            else:
                task_data["assistant"] = None
                
            task_list.append(task_data)
        
        result = {
            "tasks": task_list,
            "pagination": {
                "total": total_count,
                "limit": limit,
                "offset": skip,
                "has_more": skip + limit < total_count
            }
        }
        
        print(f"✅ Found {len(task_list)} tasks")
        return result
        
    except HTTPException:
        raise
    except Exception as e:
        print(f"❌ All tasks error: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")

@app.get("/api/v1/management/assistants")
async def get_all_assistants_direct(
    skip: int = Query(0, ge=0),
    limit: int = Query(50, ge=1, le=100),
    status: Optional[str] = None,
    current_user: models.User = Depends(auth.get_current_user),
    db: Session = Depends(get_db)
):
    """Direct get all assistants endpoint"""
    try:
        print(f"👥 All assistants request for manager: {current_user.id}")
        
        # Reload user from DB
        user = db.query(models.User).filter(models.User.id == current_user.id).first()
        if not user or user.role != models.UserRole.manager:
            raise HTTPException(status_code=403, detail="Access denied. Manager role required.")
        
        query = db.query(models.AssistantProfile)
        
        if status:
            query = query.filter(models.AssistantProfile.status == status)
        
        total_count = query.count()
        assistants = query.offset(skip).limit(limit).all()
        
        assistant_list = []
        for assistant in assistants:
            # Get recent task statistics
            week_ago = datetime.utcnow() - timedelta(days=7)
            recent_tasks = db.query(models.Task).filter(
                models.Task.assistant_id == assistant.id,
                models.Task.claimed_at >= week_ago
            ).count()
            
            assistant_data = {
                "id": assistant.id,
                "name": assistant.user.name,
                "email": assistant.email,
                "phone": assistant.user.phone,
                "telegram_username": assistant.user.telegram_username,
                "specialization": assistant.specialization.value,
                "status": assistant.status,
                "current_active_tasks": assistant.current_active_tasks,
                "total_tasks_completed": assistant.total_tasks_completed,
                "average_rating": assistant.average_rating,
                "recent_tasks_week": recent_tasks,
                "last_active": assistant.user.last_active.isoformat() if assistant.user.last_active else None,
                "created_at": assistant.user.created_at.isoformat()
            }
            assistant_list.append(assistant_data)
        
        result = {
            "assistants": assistant_list,
            "pagination": {
                "total": total_count,
                "limit": limit,
                "offset": skip,
                "has_more": skip + limit < total_count
            }
        }
        
        print(f"✅ Found {len(assistant_list)} assistants")
        return result
        
    except HTTPException:
        raise
    except Exception as e:
        print(f"❌ All assistants error: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")

@app.get("/api/v1/management/clients")
async def get_all_clients_direct(
    skip: int = Query(0, ge=0),
    limit: int = Query(50, ge=1, le=100),
    subscription_status: Optional[str] = None,
    current_user: models.User = Depends(auth.get_current_user),
    db: Session = Depends(get_db)
):
    """Direct get all clients endpoint"""
    try:
        print(f"👤 All clients request for manager: {current_user.id}")
        
        # Reload user from DB
        user = db.query(models.User).filter(models.User.id == current_user.id).first()
        if not user or user.role != models.UserRole.manager:
            raise HTTPException(status_code=403, detail="Access denied. Manager role required.")
        
        # Get clients from database
        query = db.query(models.ClientProfile).join(models.User).filter(
            models.User.role == models.UserRole.client
        )
        
        # Filter by subscription status if provided
        if subscription_status:
            query = query.join(models.Subscription).filter(
                models.Subscription.status == subscription_status
            )
        
        total_count = query.count()
        clients = query.offset(skip).limit(limit).all()
        
        client_list = []
        for client in clients:
            # Get task statistics
            total_tasks = db.query(models.Task).filter(
                models.Task.client_id == client.id
            ).count()
            
            active_tasks = db.query(models.Task).filter(
                models.Task.client_id == client.id,
                models.Task.status.in_([models.TaskStatus.pending, models.TaskStatus.in_progress])
            ).count()
            
            # Get subscription info
            subscription_data = None
            if client.subscription:
                subscription_data = {
                    "id": client.subscription.id,
                    "plan": client.subscription.plan.value,
                    "status": client.subscription.status.value,
                    "started_at": client.subscription.started_at.isoformat(),
                    "expires_at": client.subscription.expires_at.isoformat() if client.subscription.expires_at else None,
                    "auto_renew": client.subscription.auto_renew
                }
            
            client_data = {
                "id": client.id,
                "name": client.user.name,
                "email": client.email,
                "phone": client.user.phone,
                "telegram_username": client.user.telegram_username,
                "total_tasks": total_tasks,
                "active_tasks": active_tasks,
                "created_at": client.user.created_at.isoformat(),
                "subscription": subscription_data
            }
            client_list.append(client_data)
        
        result = {
            "clients": client_list,
            "pagination": {
                "total": total_count,
                "limit": limit,
                "offset": skip,
                "has_more": skip + limit < total_count
            }
        }
        
        print(f"✅ Found {len(client_list)} clients")
        return result
        
    except HTTPException:
        raise
    except Exception as e:
        print(f"❌ All clients error: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")

@app.get("/api/v1/management/marketplace/stats")
async def get_marketplace_stats_direct(
    current_user: models.User = Depends(auth.get_current_user),
    db: Session = Depends(get_db)
):
    """Get marketplace statistics for management dashboard"""
    try:
        print(f"📊 Marketplace stats request for manager: {current_user.id}")
        
        # Reload user from DB
        user = db.query(models.User).filter(models.User.id == current_user.id).first()
        if not user or user.role != models.UserRole.manager:
            raise HTTPException(status_code=403, detail="Access denied. Manager role required.")
        
        # Get marketplace statistics directly from database
        # Task statistics
        total_pending_tasks = db.query(models.Task).filter(
            models.Task.status == models.TaskStatus.pending
        ).count()
        
        total_in_progress_tasks = db.query(models.Task).filter(
            models.Task.status == models.TaskStatus.in_progress
        ).count()
        
        total_completed_tasks = db.query(models.Task).filter(
            models.Task.status.in_([models.TaskStatus.completed, models.TaskStatus.approved])
        ).count()
        
        # Check for overdue tasks
        overdue_tasks = db.query(models.Task).filter(
            models.Task.status == models.TaskStatus.pending,
            models.Task.deadline < datetime.utcnow()
        ).count()
        
        # Assistant statistics
        total_assistants = db.query(models.AssistantProfile).count()
        online_assistants = db.query(models.AssistantProfile).filter(
            models.AssistantProfile.status == "online"
        ).count()
        
        # Tasks that need assignment
        assignment_needed = total_pending_tasks > 0
        
        # Recent task creation statistics
        week_ago = datetime.utcnow() - timedelta(days=7)
        recent_tasks = db.query(models.Task).filter(
            models.Task.created_at >= week_ago
        ).count()
        
        stats = {
            "total_pending_tasks": total_pending_tasks,
            "total_in_progress_tasks": total_in_progress_tasks,
            "total_completed_tasks": total_completed_tasks,
            "overdue_tasks": overdue_tasks,
            "assignment_needed": assignment_needed,
            "total_assistants": total_assistants,
            "online_assistants": online_assistants,
            "recent_tasks_week": recent_tasks,
            "system_health": "healthy" if not assignment_needed and overdue_tasks == 0 else "warning",
            "last_updated": datetime.utcnow().isoformat(),
            "recommendations": []
        }
        
        # Add recommendations based on stats
        if overdue_tasks > 0:
            stats["recommendations"].append("Some tasks are overdue for assignment")
        
        if total_pending_tasks > 10:
            stats["recommendations"].append("High number of pending tasks - consider adding more assistants")
            
        if online_assistants < 3:
            stats["recommendations"].append("Low number of online assistants")
        
        print(f"✅ Marketplace stats: {stats}")
        return stats
        
    except HTTPException:
        raise
    except Exception as e:
        print(f"❌ Marketplace stats error: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")