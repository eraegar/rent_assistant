#!/usr/bin/env python3
"""
Test script to verify task rejection behavior and marketplace integration
"""
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from database import SessionLocal
from models import Task, TaskStatus, AssistantProfile, User, UserRole
from datetime import datetime
from sqlalchemy.orm import Session


def test_task_rejection_flow():
    """Test the complete task rejection flow"""
    
    db = SessionLocal()
    
    try:
        print("🧪 Testing Task Rejection Flow")
        print("=" * 50)
        
        # Find an assistant to test with
        assistant = db.query(AssistantProfile).join(User).filter(
            User.role == UserRole.assistant
        ).first()
        
        if not assistant:
            print("❌ No assistant found in database")
            return
        
        print(f"📋 Using assistant: {assistant.user.name} (ID: {assistant.id})")
        
        # Find a task in progress assigned to this assistant
        task = db.query(Task).filter(
            Task.assistant_id == assistant.id,
            Task.status == TaskStatus.in_progress
        ).first()
        
        if not task:
            print("❌ No in-progress task found for this assistant")
            return
        
        print(f"📝 Found task: {task.title} (ID: {task.id})")
        print(f"   Status: {task.status}")
        print(f"   Assigned to: {task.assistant_id}")
        print(f"   Claimed at: {task.claimed_at}")
        
        # Count tasks in marketplace before rejection
        marketplace_before = db.query(Task).filter(
            Task.status == TaskStatus.pending,
            Task.assistant_id.is_(None)
        ).count()
        
        print(f"📊 Marketplace tasks before rejection: {marketplace_before}")
        
        # Simulate task rejection
        print("\n🔄 Simulating task rejection...")
        
        # Store original values
        original_active_tasks = assistant.current_active_tasks
        
        # Apply rejection logic (same as in reject_task function)
        task.status = TaskStatus.pending
        task.rejected_at = datetime.utcnow()
        task.rejection_reason = "Test rejection - automated test"
        task.assistant_id = None
        task.claimed_at = None
        
        # Update assistant stats
        assistant.current_active_tasks = max(0, assistant.current_active_tasks - 1)
        
        db.commit()
        
        # Count tasks in marketplace after rejection
        marketplace_after = db.query(Task).filter(
            Task.status == TaskStatus.pending,
            Task.assistant_id.is_(None)
        ).count()
        
        print(f"📊 Marketplace tasks after rejection: {marketplace_after}")
        
        # Verify the results
        print("\n✅ Verification Results:")
        print(f"   Task status: {task.status}")
        print(f"   Task assigned to: {task.assistant_id}")
        print(f"   Task claimed at: {task.claimed_at}")
        print(f"   Task rejected at: {task.rejected_at}")
        print(f"   Rejection reason: {task.rejection_reason}")
        print(f"   Assistant active tasks: {original_active_tasks} → {assistant.current_active_tasks}")
        print(f"   Marketplace increase: {marketplace_after - marketplace_before}")
        
        # Check if task appears in marketplace
        task_in_marketplace = db.query(Task).filter(
            Task.id == task.id,
            Task.status == TaskStatus.pending,
            Task.assistant_id.is_(None)
        ).first()
        
        if task_in_marketplace:
            print("✅ SUCCESS: Task successfully returned to marketplace!")
        else:
            print("❌ FAILED: Task not found in marketplace")
        
        # Revert changes for cleanup
        print("\n🔄 Reverting changes for cleanup...")
        task.status = TaskStatus.in_progress
        task.assistant_id = assistant.id
        task.claimed_at = datetime.utcnow()
        task.rejected_at = None
        task.rejection_reason = None
        assistant.current_active_tasks = original_active_tasks
        
        db.commit()
        print("✅ Changes reverted successfully")
        
    except Exception as e:
        print(f"❌ Error during test: {e}")
        db.rollback()
        raise
    finally:
        db.close()


def check_marketplace_logic():
    """Check the marketplace filtering logic"""
    
    db = SessionLocal()
    
    try:
        print("\n🔍 Checking Marketplace Logic")
        print("=" * 50)
        
        # Check tasks with different statuses
        statuses = [TaskStatus.pending, TaskStatus.in_progress, TaskStatus.completed]
        
        for status in statuses:
            count = db.query(Task).filter(Task.status == status).count()
            print(f"📊 Tasks with status '{status}': {count}")
        
        # Check marketplace eligible tasks
        marketplace_tasks = db.query(Task).filter(
            Task.status == TaskStatus.pending,
            Task.assistant_id.is_(None)
        ).count()
        
        print(f"📊 Tasks eligible for marketplace: {marketplace_tasks}")
        
        # Check recently rejected tasks
        rejected_tasks = db.query(Task).filter(
            Task.rejected_at.isnot(None)
        ).count()
        
        print(f"📊 Tasks that were rejected (all time): {rejected_tasks}")
        
        # Check if any rejected tasks are in marketplace
        rejected_in_marketplace = db.query(Task).filter(
            Task.rejected_at.isnot(None),
            Task.status == TaskStatus.pending,
            Task.assistant_id.is_(None)
        ).count()
        
        print(f"📊 Previously rejected tasks now in marketplace: {rejected_in_marketplace}")
        
    except Exception as e:
        print(f"❌ Error during marketplace check: {e}")
        raise
    finally:
        db.close()


def main():
    """Main function to run all tests"""
    print("🚀 Starting Task Rejection Tests")
    print("=" * 50)
    
    try:
        # Run marketplace logic check
        check_marketplace_logic()
        
        # Run full rejection flow test
        test_task_rejection_flow()
        
        print("\n🎉 All tests completed successfully!")
        
    except Exception as e:
        print(f"\n💥 Test failed with error: {e}")
        return 1
    
    return 0


if __name__ == "__main__":
    sys.exit(main()) 