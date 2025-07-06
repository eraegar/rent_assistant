#!/usr/bin/env python3
"""
Создание тестовых задач для проверки маркетплейса
"""
import sys
import os
from datetime import datetime, timedelta

# Добавляем путь к папке app для импорта моделей
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import models
import database
from sqlalchemy.orm import Session
from sqlalchemy import create_engine

# Настраиваем правильный путь к базе данных
db_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'test.db')
engine = create_engine(f"sqlite:///{db_path}", connect_args={"check_same_thread": False})
SessionLocal = database.sessionmaker(autocommit=False, autoflush=False, bind=engine)

def create_test_tasks():
    """Создать тестовые задачи без автоматического назначения"""
    db = SessionLocal()
    
    try:
        # Проверяем, есть ли клиенты
        clients = db.query(models.ClientProfile).limit(5).all()
        if not clients:
            print("❌ Нет клиентов в базе данных!")
            return
        
        print(f"✅ Найдено {len(clients)} клиентов")
        
        # Создаем тестовые задачи
        test_tasks = [
            {
                "title": "Организовать встречу с командой",
                "description": "Нужно забронировать переговорную на 10 человек в центре города, подготовить презентацию и разослать приглашения всем участникам.",
                "type": models.TaskType.business,
                "client_id": clients[0].id if len(clients) > 0 else 1
            },
            {
                "title": "Купить подарок на день рождения",
                "description": "Найти и купить оригинальный подарок для мамы на день рождения. Бюджет до 5000 рублей. Она любит чтение и цветы.",
                "type": models.TaskType.personal,
                "client_id": clients[1].id if len(clients) > 1 else 1
            },
            {
                "title": "Исследование рынка конкурентов",
                "description": "Провести анализ конкурентов в сфере IT-услуг. Составить таблицу с ценами, услугами и ключевыми преимуществами топ-10 компаний.",
                "type": models.TaskType.business,
                "client_id": clients[2].id if len(clients) > 2 else 1
            },
            {
                "title": "Записаться к врачу",
                "description": "Найти хорошего стоматолога в районе метро Сокольники, записаться на прием на ближайшую неделю.",
                "type": models.TaskType.personal,
                "client_id": clients[3].id if len(clients) > 3 else 1
            },
            {
                "title": "Подготовить отчет по продажам",
                "description": "Собрать данные по продажам за последний квартал, создать презентацию с графиками и рекомендациями для руководства.",
                "type": models.TaskType.business,
                "client_id": clients[0].id if len(clients) > 0 else 1
            },
            {
                "title": "Организовать переезд",
                "description": "Найти надежную транспортную компанию для переезда квартиры. Нужно упаковать вещи и перевезти в новую квартиру в выходные.",
                "type": models.TaskType.personal,
                "client_id": clients[1].id if len(clients) > 1 else 1
            }
        ]
        
        created_count = 0
        for task_data in test_tasks:
            # Создаем задачу напрямую в базе с статусом pending
            task = models.Task(
                title=task_data["title"],
                description=task_data["description"],
                type=task_data["type"],
                client_id=task_data["client_id"],
                status=models.TaskStatus.pending,  # Важно: pending статус
                assistant_id=None,  # Важно: без ассистента
                deadline=datetime.utcnow() + timedelta(hours=48),  # 48 часов на выполнение
                created_at=datetime.utcnow()
            )
            
            db.add(task)
            created_count += 1
        
        db.commit()
        print(f"✅ Создано {created_count} тестовых задач в маркетплейсе!")
        
        # Покажем статистику задач
        pending_tasks = db.query(models.Task).filter(
            models.Task.status == models.TaskStatus.pending,
            models.Task.assistant_id.is_(None)
        ).count()
        
        total_tasks = db.query(models.Task).count()
        
        print(f"📊 Статистика задач:")
        print(f"   - Всего задач: {total_tasks}")
        print(f"   - В маркетплейсе (pending, не назначенные): {pending_tasks}")
        
    except Exception as e:
        print(f"❌ Ошибка при создании задач: {str(e)}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    print("🚀 Создание тестовых задач для маркетплейса...")
    create_test_tasks()
    print("✅ Готово!") 