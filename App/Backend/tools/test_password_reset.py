#!/usr/bin/env python3
"""
Test script to verify password reset functionality for assistants
"""
import sys
import os

# Добавляем путь к app папке
current_dir = os.path.dirname(os.path.abspath(__file__))
app_dir = os.path.dirname(current_dir)
sys.path.append(app_dir)

# Меняем рабочую директорию на app
os.chdir(app_dir)

from database import SessionLocal
from models import User, UserRole, AssistantProfile
import auth

def test_password_reset():
    """Test password reset functionality"""
    
    db = SessionLocal()
    
    try:
        print("🧪 Testing Password Reset Functionality")
        print("=" * 50)
        print(f"📂 Working directory: {os.getcwd()}")
        print(f"📂 Database should be at: {os.path.join(os.getcwd(), 'test.db')}")
        print(f"📂 Database exists: {os.path.exists('test.db')}")
        
        # Find all assistants first
        all_assistants = db.query(User).filter(
            User.role == UserRole.assistant
        ).all()
        
        print(f"📋 Found {len(all_assistants)} assistants:")
        for assistant in all_assistants:
            profile = db.query(AssistantProfile).filter(
                AssistantProfile.user_id == assistant.id
            ).first()
            print(f"  ID: {assistant.id}, Name: {assistant.name}, Phone: {assistant.phone}")
            if profile:
                print(f"      Profile ID: {profile.id}, Email: {profile.email}")
        
        # Find Геннадий by name (not just ID 5)
        gennady = db.query(User).filter(
            User.role == UserRole.assistant,
            User.name.like('%Геннадий%')
        ).first()
        
        if not gennady:
            print("❌ Геннадий не найден, попробуем найти по ID 5...")
            gennady = db.query(User).filter(
                User.id == 5,
                User.role == UserRole.assistant
            ).first()
        
        if not gennady:
            print("❌ Геннадий не найден ни по имени, ни по ID 5")
            return
        
        print(f"📋 Found Геннадий:")
        print(f"    ID: {gennady.id}")
        print(f"    Name: {gennady.name}")
        print(f"    Phone: {gennady.phone}")
        print(f"    Current password hash: {gennady.password_hash[:50]}...")
        
        # Test current password
        print(f"\n🔐 Testing current password verification:")
        current_passwords_to_try = ['qwqwqw', 'assistant123', 'password', '123456']
        
        for pwd in current_passwords_to_try:
            if auth.verify_password(pwd, gennady.password_hash):
                print(f"✅ Current password is: '{pwd}'")
                break
            else:
                print(f"❌ Password '{pwd}' is incorrect")
        else:
            print("❌ None of the tested passwords work")
        
        # Test password reset
        print(f"\n🔄 Testing password reset...")
        
        # Generate new password (same logic as in API)
        import secrets
        import string
        new_password = ''.join(secrets.choice(string.ascii_letters + string.digits) for _ in range(8))
        print(f"Generated new password: {new_password}")
        
        # Update password
        new_hashed = auth.get_password_hash(new_password)
        old_hash = gennady.password_hash
        gennady.password_hash = new_hashed
        
        db.commit()
        db.refresh(gennady)
        
        print(f"Old hash: {old_hash[:50]}...")
        print(f"New hash: {gennady.password_hash[:50]}...")
        
        # Verify new password works
        if auth.verify_password(new_password, gennady.password_hash):
            print(f"✅ New password '{new_password}' works correctly!")
        else:
            print(f"❌ New password '{new_password}' verification failed!")
        
        # Restore original password for testing
        print(f"\n🔙 Restoring original password 'qwqwqw'...")
        original_hash = auth.get_password_hash('qwqwqw')
        gennady.password_hash = original_hash
        db.commit()
        
        if auth.verify_password('qwqwqw', gennady.password_hash):
            print(f"✅ Original password 'qwqwqw' restored successfully!")
        else:
            print(f"❌ Failed to restore original password!")
        
    except Exception as e:
        print(f"❌ Error during password test: {e}")
        import traceback
        traceback.print_exc()
    finally:
        db.close()

if __name__ == "__main__":
    test_password_reset() 