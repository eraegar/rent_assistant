#!/usr/bin/env python3
"""
Script to create test data for the Assistant-for-Rent API
Run this after setting up the new database schema
"""

import sys
import os
from datetime import datetime, timedelta

# Add the app directory to the path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

import models, database, auth

def create_test_data():
    """Create test users and data for all three roles"""
    
    # Create database tables
    models.Base.metadata.create_all(bind=database.engine)
    
    db = database.SessionLocal()
    
    try:
        print("🚀 Creating test data...")
        
        # =============================================================================
        # CREATE TEST CLIENTS
        # =============================================================================
        
        print("👤 Creating test clients...")
        
        # Client 1
        client1_user = models.User(
            phone="+7900123456",
            name="Иван Петров",
            password_hash=auth.get_password_hash("password123"),
            role=models.UserRole.client,
            telegram_username="@ivan_petrov"
        )
        db.add(client1_user)
        db.flush()
        
        client1_profile = models.ClientProfile(
            user_id=client1_user.id,
            email="ivan@example.com"
        )
        db.add(client1_profile)
        db.flush()
        
        # Client 1 subscription
        client1_subscription = models.Subscription(
            client_id=client1_profile.id,
            plan=models.SubscriptionPlan.full_8h,
            status=models.SubscriptionStatus.active,
            started_at=datetime.utcnow(),
            expires_at=datetime.utcnow() + timedelta(days=30),
            auto_renew=True
        )
        db.add(client1_subscription)
        
        # Client 2
        client2_user = models.User(
            phone="+7900654321",
            name="Мария Сидорова",
            password_hash=auth.get_password_hash("password123"),
            role=models.UserRole.client,
            telegram_username="@maria_sidorova"
        )
        db.add(client2_user)
        db.flush()
        
        client2_profile = models.ClientProfile(
            user_id=client2_user.id,
            email="maria@example.com"
        )
        db.add(client2_profile)
        db.flush()
        
        # Client 2 subscription
        client2_subscription = models.Subscription(
            client_id=client2_profile.id,
            plan=models.SubscriptionPlan.personal_5h,
            status=models.SubscriptionStatus.active,
            started_at=datetime.utcnow(),
            expires_at=datetime.utcnow() + timedelta(days=30),
            auto_renew=True
        )
        db.add(client2_subscription)
        
        # =============================================================================
        # CREATE TEST ASSISTANTS
        # =============================================================================
        
        print("🤝 Creating test assistants...")
        
        # Assistant 1 - Business specialist
        assistant1_user = models.User(
            phone="+7900111111",
            name="Анна Козлова",
            password_hash=auth.get_password_hash("assistant123"),
            role=models.UserRole.assistant,
            telegram_username="@anna_assistant"
        )
        db.add(assistant1_user)
        db.flush()
        
        assistant1_profile = models.AssistantProfile(
            user_id=assistant1_user.id,
            email="anna.assistant@example.com",
            specialization=models.AssistantSpecialization.full_access,
            status="online",
            current_active_tasks=0,
            total_tasks_completed=25,
            average_rating=4.8
        )
        db.add(assistant1_profile)
        
        # Assistant 2 - Personal only
        assistant2_user = models.User(
            phone="+7900222222",
            name="Дмитрий Волков",
            password_hash=auth.get_password_hash("assistant123"),
            role=models.UserRole.assistant,
            telegram_username="@dmitry_assistant"
        )
        db.add(assistant2_user)
        db.flush()
        
        assistant2_profile = models.AssistantProfile(
            user_id=assistant2_user.id,
            email="dmitry.assistant@example.com",
            specialization=models.AssistantSpecialization.personal_only,
            status="online",
            current_active_tasks=1,
            total_tasks_completed=15,
            average_rating=4.5
        )
        db.add(assistant2_profile)
        
        # Assistant 3 - Offline
        assistant3_user = models.User(
            phone="+7900333333",
            name="Елена Морозова",
            password_hash=auth.get_password_hash("assistant123"),
            role=models.UserRole.assistant,
            telegram_username="@elena_assistant"
        )
        db.add(assistant3_user)
        db.flush()
        
        assistant3_profile = models.AssistantProfile(
            user_id=assistant3_user.id,
            email="elena.assistant@example.com",
            specialization=models.AssistantSpecialization.business_only,
            status="offline",
            current_active_tasks=0,
            total_tasks_completed=30,
            average_rating=4.9
        )
        db.add(assistant3_profile)
        
        # =============================================================================
        # CREATE TEST MANAGERS
        # =============================================================================
        
        print("👔 Creating test managers...")
        
        # Manager 1
        manager1_user = models.User(
            phone="+7900999999",
            name="Александр Руководитель",
            password_hash=auth.get_password_hash("manager123"),
            role=models.UserRole.manager,
            telegram_username="@alex_manager"
        )
        db.add(manager1_user)
        db.flush()
        
        manager1_profile = models.ManagerProfile(
            user_id=manager1_user.id,
            email="alex.manager@example.com",
            department="Operations"
        )
        db.add(manager1_profile)
        
        # =============================================================================
        # CREATE TEST TASKS
        # =============================================================================
        
        print("📋 Creating test tasks...")
        
        # Flush to get IDs
        db.flush()
        
        # Task 1 - Pending personal task
        task1 = models.Task(
            title="Найти няню на выходные",
            description="Нужно найти проверенную няню для ребенка 5 лет на субботу и воскресенье",
            type=models.TaskType.personal,
            status=models.TaskStatus.pending,
            client_id=client2_profile.id,
            deadline=datetime.utcnow() + timedelta(hours=20)
        )
        db.add(task1)
        
        # Task 2 - In progress business task
        task2 = models.Task(
            title="Исследование рынка конкурентов",
            description="Провести анализ 5 основных конкурентов в сфере IT-услуг",
            type=models.TaskType.business,
            status=models.TaskStatus.in_progress,
            client_id=client1_profile.id,
            assistant_id=assistant1_profile.id,
            deadline=datetime.utcnow() + timedelta(hours=15),
            claimed_at=datetime.utcnow() - timedelta(hours=2)
        )
        db.add(task2)
        
        # Task 3 - Completed task
        task3 = models.Task(
            title="Забронировать ресторан",
            description="Забронировать столик в хорошем ресторане на 4 человека на пятницу вечером",
            type=models.TaskType.personal,
            status=models.TaskStatus.completed,
            client_id=client1_profile.id,
            assistant_id=assistant2_profile.id,
            deadline=datetime.utcnow() + timedelta(hours=10),
            claimed_at=datetime.utcnow() - timedelta(hours=4),
            completed_at=datetime.utcnow() - timedelta(hours=1),
            result="Забронирован столик в ресторане 'Пушкин' на пятницу в 19:00",
            completion_notes="Столик на 4 человека, подтверждение бронирования отправлено на телефон"
        )
        db.add(task3)
        
        # Task 4 - Approved task with rating
        task4 = models.Task(
            title="Купить подарок",
            description="Выбрать и купить подарок для мамы на день рождения, бюджет до 5000 рублей",
            type=models.TaskType.personal,
            status=models.TaskStatus.approved,
            client_id=client2_profile.id,
            assistant_id=assistant2_profile.id,
            deadline=datetime.utcnow() - timedelta(hours=5),
            claimed_at=datetime.utcnow() - timedelta(hours=8),
            completed_at=datetime.utcnow() - timedelta(hours=3),
            approved_at=datetime.utcnow() - timedelta(hours=1),
            result="Купил красивый набор косметики Dior в подарочной упаковке",
            completion_notes="Выбрал набор с учетом предпочтений, получен чек и гарантия",
            client_rating=5,
            client_feedback="Отличный выбор! Маме очень понравился подарок. Спасибо!"
        )
        db.add(task4)
        
        # Task 5 - Overdue unclaimed task
        task5 = models.Task(
            title="Поиск офиса для аренды",
            description="Найти офисное помещение 50-70 кв.м в центре города, бюджет до 80000 в месяц",
            type=models.TaskType.business,
            status=models.TaskStatus.pending,
            client_id=client1_profile.id,
            deadline=datetime.utcnow() - timedelta(hours=2),  # Overdue
            created_at=datetime.utcnow() - timedelta(hours=8)  # Created 8 hours ago
        )
        db.add(task5)
        
        # =============================================================================
        # CREATE SAMPLE MESSAGES
        # =============================================================================
        
        print("💬 Creating sample messages...")
        
        # Messages for task 2 (in progress)
        message1 = models.Message(
            task_id=task2.id,
            sender_id=client1_user.id,
            content="Добавлю, что особенно интересует ценовая политика конкурентов"
        )
        db.add(message1)
        
        message2 = models.Message(
            task_id=task2.id,
            sender_id=assistant1_user.id,
            content="Понял, учту это в анализе. Уже собрал информацию по 3 компаниям, завтра закончу остальные 2"
        )
        db.add(message2)
        
        # Commit all changes
        db.commit()
        
        print("✅ Test data created successfully!")
        print("\n📊 Created:")
        print("  - 2 Clients (Ivan with Full plan, Maria with Personal plan)")
        print("  - 3 Assistants (Anna & Elena - business, Dmitry - personal only)")
        print("  - 1 Manager (Alexander)")
        print("  - 5 Tasks (various statuses)")
        print("  - 2 Messages")
        
        print("\n🔑 Test credentials:")
        print("  Clients:")
        print("    +7900123456 / password123 (Ivan - Full subscription)")
        print("    +7900654321 / password123 (Maria - Personal subscription)")
        print("  Assistants:")
        print("    anna.assistant@example.com / assistant123 (Business specialist)")
        print("    dmitry.assistant@example.com / assistant123 (Personal only)")
        print("    elena.assistant@example.com / assistant123 (Business, offline)")
        print("  Manager:")
        print("    alex.manager@example.com / manager123")
        
    except Exception as e:
        print(f"❌ Error creating test data: {e}")
        db.rollback()
        raise
    finally:
        db.close()

if __name__ == "__main__":
    create_test_data() 