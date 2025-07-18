#!/usr/bin/env python3
"""
Скрипт для создания менеджера в системе.
"""

import sys
import os

# Добавляем родительскую директорию в path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from database import SessionLocal
import models
import auth
from datetime import datetime

def create_manager():
    """Создать менеджера в системе"""
    db = SessionLocal()
    
    try:
        # Данные менеджера
        manager_data = {
            "name": "Менеджер",
            "phone": "+79999999999",  # Используем стандартный тестовый номер
            "password": "admin123",
            "email": "manager@company.com",
            "department": "Operations"
        }
        
        print("🔧 Создание менеджера...")
        print(f"📝 Имя: {manager_data['name']}")
        print(f"📞 Телефон: {manager_data['phone']}")
        print(f"🔐 Пароль: {manager_data['password']}")
        print(f"📧 Email: {manager_data['email']}")
        print(f"🏢 Отдел: {manager_data['department']}")
        
        # Проверяем, не существует ли уже пользователь с таким номером
        existing_user = db.query(models.User).filter(
            models.User.phone == manager_data["phone"]
        ).first()
        
        if existing_user:
            print(f"⚠️  Пользователь с номером {manager_data['phone']} уже существует!")
            print(f"   Имя: {existing_user.name}")
            print(f"   Роль: {existing_user.role.value}")
            
            if existing_user.role == models.UserRole.manager:
                print("✅ Менеджер уже создан!")
                return
            else:
                print("❌ Номер телефона занят пользователем с другой ролью!")
                return
        
        # Создаем пользователя
        hashed_password = auth.get_password_hash(manager_data["password"])
        db_user = models.User(
            phone=manager_data["phone"],
            name=manager_data["name"],
            password_hash=hashed_password,
            role=models.UserRole.manager,
            created_at=datetime.utcnow()
        )
        db.add(db_user)
        db.flush()
        
        # Создаем профиль менеджера
        manager_profile = models.ManagerProfile(
            user_id=db_user.id,
            email=manager_data["email"],
            department=manager_data["department"]
        )
        db.add(manager_profile)
        
        db.commit()
        db.refresh(db_user)
        
        print("✅ Менеджер успешно создан!")
        print(f"   ID: {db_user.id}")
        print(f"   Имя: {db_user.name}")
        print(f"   Телефон: {db_user.phone}")
        print(f"   Email: {manager_profile.email}")
        print(f"   Отдел: {manager_profile.department}")
        print(f"   Дата создания: {db_user.created_at}")
        
        print("\n🔑 Данные для входа:")
        print(f"   Телефон: {manager_data['phone']}")
        print(f"   Пароль: {manager_data['password']}")
        print(f"   URL: http://localhost:3001 (Manager Dashboard)")
        
    except Exception as e:
        db.rollback()
        print(f"❌ Ошибка при создании менеджера: {e}")
        import traceback
        traceback.print_exc()
    finally:
        db.close()

if __name__ == "__main__":
    create_manager() 