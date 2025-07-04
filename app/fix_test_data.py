#!/usr/bin/env python3

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

import models
import database

def fix_assistant_specializations():
    """Fix existing assistant specializations to use correct enum values"""
    
    print("🔧 Fixing assistant specializations...")
    
    db = database.SessionLocal()
    try:
        # Get all assistants
        assistants = db.query(models.AssistantProfile).all()
        
        for assistant in assistants:
            print(f"Assistant {assistant.user.name}: {assistant.specialization}")
            
            # Update old enum values
            if str(assistant.specialization) == 'AssistantSpecialization.business':
                assistant.specialization = models.AssistantSpecialization.full_access
                print(f"  → Updated to: {assistant.specialization}")
        
        db.commit()
        print("✅ All assistant specializations updated!")
        
    except Exception as e:
        print(f"❌ Error: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    fix_assistant_specializations() 