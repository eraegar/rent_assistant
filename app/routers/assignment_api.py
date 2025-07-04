from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session
from typing import List, Optional
from datetime import datetime
import json

import models, database

router = APIRouter(prefix="/api/v1/management/assignments", tags=["assignments"])

def get_db():
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()

def get_current_manager(
    current_user: models.User = Depends(models.auth.get_current_user),
    db: Session = Depends(get_db)
):
    """Ensure the current user is a manager"""
    user = db.query(models.User).filter(models.User.id == current_user.id).first()
    if not user or user.role != models.UserRole.manager:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Access denied. Manager role required."
        )
    return user

# =============================================================================
# CLIENT-ASSISTANT PERMANENT ASSIGNMENTS
# =============================================================================

@router.get("/")
def get_all_assignments(
    skip: int = Query(0, ge=0),
    limit: int = Query(50, ge=1, le=100),
    client_id: Optional[int] = None,
    assistant_id: Optional[int] = None,
    status: Optional[str] = None,
    current_manager: models.User = Depends(get_current_manager),
    db: Session = Depends(get_db)
):
    """Get all permanent client-assistant assignments"""
    
    query = db.query(models.ClientAssistantAssignment)
    
    if client_id:
        query = query.filter(models.ClientAssistantAssignment.client_id == client_id)
    if assistant_id:
        query = query.filter(models.ClientAssistantAssignment.assistant_id == assistant_id)
    if status:
        query = query.filter(models.ClientAssistantAssignment.status == status)
    
    total_count = query.count()
    assignments = query.offset(skip).limit(limit).all()
    
    assignment_list = []
    for assignment in assignments:
        allowed_types = []
        if assignment.allowed_task_types:
            try:
                allowed_types = json.loads(assignment.allowed_task_types)
            except:
                allowed_types = []
        
        assignment_data = {
            "id": assignment.id,
            "client": {
                "id": assignment.client.id,
                "name": assignment.client.user.name,
                "phone": assignment.client.user.phone
            },
            "assistant": {
                "id": assignment.assistant.id,
                "name": assignment.assistant.user.name,
                "specialization": assignment.assistant.specialization.value,
                "current_active_tasks": assignment.assistant.current_active_tasks
            },
            "status": assignment.status.value,
            "allowed_task_types": allowed_types,
            "created_at": assignment.created_at.isoformat(),
            "updated_at": assignment.updated_at.isoformat(),
            "created_by_manager": assignment.created_by_manager.user.name if assignment.created_by_manager else None
        }
        assignment_list.append(assignment_data)
    
    return {
        "assignments": assignment_list,
        "pagination": {
            "total": total_count,
            "limit": limit,
            "offset": skip,
            "has_more": skip + limit < total_count
        }
    }

@router.post("/create")
def create_assignment(
    assignment_data: dict,
    current_manager: models.User = Depends(get_current_manager),
    db: Session = Depends(get_db)
):
    """Create a new permanent client-assistant assignment"""
    
    client_id = assignment_data.get("client_id")
    assistant_id = assignment_data.get("assistant_id")
    allowed_task_types = assignment_data.get("allowed_task_types", [])
    
    if not client_id or not assistant_id:
        raise HTTPException(status_code=400, detail="Client ID and Assistant ID are required")
    
    # Find client and assistant
    client = db.query(models.ClientProfile).filter(models.ClientProfile.id == client_id).first()
    if not client:
        raise HTTPException(status_code=404, detail="Client not found")
    
    assistant = db.query(models.AssistantProfile).filter(models.AssistantProfile.id == assistant_id).first()
    if not assistant:
        raise HTTPException(status_code=404, detail="Assistant not found")
    
    # Check if assignment already exists
    existing = db.query(models.ClientAssistantAssignment).filter(
        models.ClientAssistantAssignment.client_id == client_id,
        models.ClientAssistantAssignment.assistant_id == assistant_id,
        models.ClientAssistantAssignment.status == models.AssignmentStatus.active
    ).first()
    
    if existing:
        raise HTTPException(status_code=400, detail="Active assignment already exists between this client and assistant")
    
    # Create assignment
    assignment = models.ClientAssistantAssignment(
        client_id=client_id,
        assistant_id=assistant_id,
        status=models.AssignmentStatus.active,
        created_by=current_manager.manager_profile.id,
        allowed_task_types=json.dumps(allowed_task_types) if allowed_task_types else None
    )
    
    db.add(assignment)
    db.commit()
    db.refresh(assignment)
    
    return {
        "success": True,
        "message": f"Assignment created between {client.user.name} and {assistant.user.name}",
        "assignment_id": assignment.id,
        "allowed_task_types": allowed_task_types
    }

@router.put("/{assignment_id}/deactivate")
def deactivate_assignment(
    assignment_id: int,
    current_manager: models.User = Depends(get_current_manager),
    db: Session = Depends(get_db)
):
    """Deactivate a permanent client-assistant assignment"""
    
    assignment = db.query(models.ClientAssistantAssignment).filter(
        models.ClientAssistantAssignment.id == assignment_id
    ).first()
    
    if not assignment:
        raise HTTPException(status_code=404, detail="Assignment not found")
    
    if assignment.status != models.AssignmentStatus.active:
        raise HTTPException(status_code=400, detail="Assignment is not active")
    
    assignment.status = models.AssignmentStatus.inactive
    assignment.updated_at = datetime.utcnow()
    
    db.commit()
    
    return {
        "success": True,
        "message": f"Assignment between {assignment.client.user.name} and {assignment.assistant.user.name} has been deactivated"
    }

@router.put("/{assignment_id}/reactivate")
def reactivate_assignment(
    assignment_id: int,
    current_manager: models.User = Depends(get_current_manager),
    db: Session = Depends(get_db)
):
    """Reactivate a permanent client-assistant assignment"""
    
    assignment = db.query(models.ClientAssistantAssignment).filter(
        models.ClientAssistantAssignment.id == assignment_id
    ).first()
    
    if not assignment:
        raise HTTPException(status_code=404, detail="Assignment not found")
    
    if assignment.status != models.AssignmentStatus.inactive:
        raise HTTPException(status_code=400, detail="Assignment is not inactive")
    
    # Check if assistant is not overloaded
    if assignment.assistant.current_active_tasks >= 5:
        raise HTTPException(status_code=400, detail="Assistant is at maximum capacity")
    
    assignment.status = models.AssignmentStatus.active
    assignment.updated_at = datetime.utcnow()
    
    db.commit()
    
    return {
        "success": True,
        "message": f"Assignment between {assignment.client.user.name} and {assignment.assistant.user.name} has been reactivated"
    } 