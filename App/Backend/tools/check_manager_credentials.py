#!/usr/bin/env python3
"""
Check manager credentials in database
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
from models import User, UserRole
import auth

def check_manager_credentials():
    """Check manager credentials in database"""
    
    db = SessionLocal()
    
    try:
        print("🔍 Checking manager credentials...")
        print("=" * 50)
        
        # Find all managers
        managers = db.query(User).filter(User.role == UserRole.manager).all()
        print(f"📊 Found {len(managers)} managers:")
        
        for manager in managers:
            print(f"  ID: {manager.id}")
            print(f"  Name: {manager.name}")
            print(f"  Phone: {manager.phone}")
            print(f"  Password hash: {manager.password_hash}")
            print(f"  Created: {manager.created_at}")
            print()
            
            # Test password verification
            test_passwords = ["manager123", "admin", "password", "123456"]
            print("  Testing common passwords:")
            for pwd in test_passwords:
                if auth.verify_password(pwd, manager.password_hash):
                    print(f"    ✅ Password '{pwd}' - MATCH!")
                else:
                    print(f"    ❌ Password '{pwd}' - no match")
            print("-" * 30)
        
        # Create test manager if none exists
        if not managers:
            print("📝 Creating test manager...")
            
            test_manager = User(
                phone="+7900000001",
                name="Test Manager",
                password_hash=auth.get_password_hash("manager123"),
                role=UserRole.manager
            )
            
            db.add(test_manager)
            db.commit()
            db.refresh(test_manager)
            
            print(f"✅ Test manager created:")
            print(f"  Phone: {test_manager.phone}")
            print(f"  Password: manager123")
            print(f"  ID: {test_manager.id}")
        
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()
    finally:
        db.close()

if __name__ == "__main__":
    check_manager_credentials() 