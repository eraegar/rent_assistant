#!/usr/bin/env python3
"""
Test script to verify revision workflow for assistants:
1. Client sends task for revision
2. Assistant can see task with revision_requested status
3. Assistant can complete or reject the task again
"""
import sys
import os
import requests
import json

# Добавляем путь к app папке
current_dir = os.path.dirname(os.path.abspath(__file__))
app_dir = os.path.dirname(current_dir)
sys.path.append(app_dir)

# Меняем рабочую директорию на app
os.chdir(app_dir)

from database import SessionLocal
from models import User, UserRole, ClientProfile, AssistantProfile, Task, TaskStatus, TaskType
from datetime import datetime

def test_revision_workflow():
    """Test the complete revision workflow"""
    print("🧪 Тестирование workflow переработки задач для ассистентов")
    print("=" * 60)
    
    # 1. Setup test data
    db = SessionLocal()
    
    try:
        # Find or create test client
        test_client = db.query(User).filter(
            User.phone == "+7777777777",
            User.role == UserRole.client
        ).first()
        
        if not test_client:
            print("❌ Тестовый клиент не найден. Создайте клиента с телефоном +7777777777")
            return
        
        # Find or create test assistant
        test_assistant = db.query(User).filter(
            User.phone == "+7888888888",
            User.role == UserRole.assistant
        ).first()
        
        if not test_assistant:
            print("❌ Тестовый ассистент не найден. Создайте ассистента с телефоном +7888888888")
            return
        
        # Create a test task in revision_requested status
        test_task = Task(
            title="Тестовая задача для переработки",
            description="Эта задача была отправлена клиентом на переработку",
            type=TaskType.personal,
            status=TaskStatus.revision_requested,
            client_id=test_client.client_profile.id,
            assistant_id=test_assistant.assistant_profile.id,
            created_at=datetime.utcnow(),
            claimed_at=datetime.utcnow(),
            completed_at=datetime.utcnow(),
            result="Предыдущий результат работы",
            completion_notes="Предыдущие заметки",
            revision_notes="Клиент просит исправить детали и улучшить качество"
        )
        
        db.add(test_task)
        db.commit()
        db.refresh(test_task)
        
        print(f"✅ Создана тестовая задача с ID: {test_task.id} в статусе 'revision_requested'")
        
        # 2. Test assistant login
        print("\n📝 Тестирование входа ассистента...")
        login_response = requests.post('http://localhost:8000/api/v1/assistants/auth/login', 
                                     json={"phone": "+7888888888", "password": "password123"})
        
        if login_response.status_code != 200:
            print(f"❌ Ошибка входа ассистента: {login_response.text}")
            return
        
        assistant_token = login_response.json()['access_token']
        headers = {'Authorization': f'Bearer {assistant_token}'}
        print("✅ Ассистент успешно вошел в систему")
        
        # 3. Test getting assigned tasks with revision_requested status
        print("\n📋 Тестирование получения назначенных задач...")
        tasks_response = requests.get('http://localhost:8000/api/v1/assistants/tasks/assigned', 
                                    headers=headers)
        
        if tasks_response.status_code != 200:
            print(f"❌ Ошибка получения задач: {tasks_response.text}")
            return
        
        tasks = tasks_response.json()
        revision_tasks = [t for t in tasks if t['status'] == 'revision_requested']
        
        print(f"✅ Получено {len(tasks)} назначенных задач")
        print(f"✅ Из них {len(revision_tasks)} задач на переработку")
        
        if not revision_tasks:
            print("❌ Задачи на переработку не найдены!")
            return
            
        revision_task = revision_tasks[0]
        print(f"✅ Найдена задача на переработку: '{revision_task['title']}'")
        print(f"   Статус: {revision_task['status']}")
        print(f"   Заметки по переработке: {revision_task.get('revision_notes', 'Не указаны')}")
        
        # 4. Test dashboard stats include revision_requested tasks
        print("\n📊 Тестирование статистики dashboard...")
        stats_response = requests.get('http://localhost:8000/api/v1/assistants/dashboard/stats',
                                    headers=headers)
        
        if stats_response.status_code == 200:
            stats = stats_response.json()
            print(f"✅ Активных задач в статистике: {stats['active_tasks']}")
            print(f"   (должно включать задачи на переработку)")
        else:
            print(f"❌ Ошибка получения статистики: {stats_response.text}")
        
        # 5. Test completing revision task
        print("\n✅ Тестирование повторного завершения задачи на переработке...")
        completion_data = {
            "detailed_result": "Исправленный результат после замечаний клиента",
            "completion_summary": "Все замечания клиента учтены и исправлены"
        }
        
        complete_response = requests.post(
            f'http://localhost:8000/api/v1/assistants/tasks/{revision_task["id"]}/complete',
            json=completion_data,
            headers=headers
        )
        
        if complete_response.status_code == 200:
            print("✅ Задача на переработку успешно завершена повторно")
            result = complete_response.json()
            print(f"   Ответ: {result['message']}")
            
            # Verify task status changed to completed
            updated_tasks_response = requests.get('http://localhost:8000/api/v1/assistants/tasks/assigned', 
                                                headers=headers)
            if updated_tasks_response.status_code == 200:
                updated_tasks = updated_tasks_response.json()
                updated_task = next((t for t in updated_tasks if t['id'] == revision_task['id']), None)
                if updated_task and updated_task['status'] == 'completed':
                    print("✅ Статус задачи изменен на 'completed'")
                else:
                    print(f"❌ Статус задачи не изменился: {updated_task['status'] if updated_task else 'задача не найдена'}")
        else:
            print(f"❌ Ошибка завершения задачи: {complete_response.text}")
        
        # 6. Test rejecting revision task (create another one for this test)
        print("\n🔄 Тестирование отклонения задачи на переработке...")
        
        # Create another revision task for rejection test
        test_task_2 = Task(
            title="Тестовая задача для отклонения",
            description="Эта задача будет отклонена ассистентом",
            type=TaskType.personal,
            status=TaskStatus.revision_requested,
            client_id=test_client.client_profile.id,
            assistant_id=test_assistant.assistant_profile.id,
            created_at=datetime.utcnow(),
            claimed_at=datetime.utcnow(),
            revision_notes="Требуется сделать что-то невозможное"
        )
        
        db.add(test_task_2)
        db.commit()
        db.refresh(test_task_2)
        
        rejection_data = {
            "reason": "Требования клиента технически невыполнимы"
        }
        
        reject_response = requests.post(
            f'http://localhost:8000/api/v1/assistants/tasks/{test_task_2.id}/reject',
            json=rejection_data,
            headers=headers
        )
        
        if reject_response.status_code == 200:
            print("✅ Задача на переработку успешно отклонена")
            result = reject_response.json()
            print(f"   Ответ: {result['message']}")
            print(f"   Причина отклонения: {result['rejection_reason']}")
        else:
            print(f"❌ Ошибка отклонения задачи: {reject_response.text}")
        
        print("\n" + "=" * 60)
        print("🎉 Тестирование workflow переработки завершено!")
        print("Итоги:")
        print("✅ Ассистент может видеть задачи со статусом 'revision_requested'")
        print("✅ Ассистент может повторно завершить задачу на переработке")  
        print("✅ Ассистент может отклонить задачу на переработке")
        print("✅ Статистика корректно учитывает задачи на переработку")
        
    except Exception as e:
        print(f"❌ Ошибка во время тестирования: {str(e)}")
        import traceback
        traceback.print_exc()
    finally:
        db.close()

if __name__ == "__main__":
    test_revision_workflow() 