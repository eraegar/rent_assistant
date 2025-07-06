#!/usr/bin/env python3
"""
Создание тестовой задачи для клиента DDDD
"""
import sqlite3
import os
from datetime import datetime, timedelta

# Connect to database
current_dir = os.path.dirname(os.path.abspath(__file__))
db_path = os.path.abspath(os.path.join(current_dir, '..', 'test.db'))
conn = sqlite3.connect(db_path)
cursor = conn.cursor()

print("=== СОЗДАНИЕ ТЕСТОВОЙ ЗАДАЧИ ДЛЯ КЛИЕНТА DDDD ===")

# Create a new personal task for client 14 (DDDD)
try:
    task_title = "Тестовая задача для Геннадия"
    task_description = "Это тестовая личная задача, которая должна автоматически назначиться Геннадию"
    task_type = "personal"
    client_id = 14
    deadline = (datetime.utcnow() + timedelta(hours=24)).isoformat()
    
    cursor.execute("""
        INSERT INTO tasks (title, description, type, client_id, status, created_at, deadline)
        VALUES (?, ?, ?, ?, 'pending', ?, ?)
    """, (task_title, task_description, task_type, client_id, datetime.utcnow().isoformat(), deadline))
    
    task_id = cursor.lastrowid
    print(f"✅ Создана задача ID {task_id}: {task_title}")
    print(f"   Тип: {task_type}")
    print(f"   Клиент: {client_id} (DDDD)")
    print(f"   Статус: pending")
    print(f"   Дедлайн: {deadline}")
    
    # Now simulate the automatic assignment logic
    print("\n=== СИМУЛЯЦИЯ АВТОМАТИЧЕСКОГО НАЗНАЧЕНИЯ ===")
    
    # Find assigned assistant for client 14
    cursor.execute("""
        SELECT ca.assistant_id, u.name, ca.allowed_task_types
        FROM client_assistant_assignments ca
        JOIN assistant_profiles ap ON ca.assistant_id = ap.id
        JOIN users u ON ap.user_id = u.id
        WHERE ca.client_id = ? AND ca.status = 'active'
    """, (client_id,))
    
    assignment = cursor.fetchone()
    if assignment:
        assistant_id, assistant_name, allowed_types = assignment
        print(f"Найдено назначение: {assistant_name} (ID: {assistant_id})")
        print(f"Разрешенные типы: {allowed_types}")
        
        # Check if task type is allowed
        import json
        try:
            allowed_task_types = json.loads(allowed_types) if allowed_types else []
        except:
            allowed_task_types = []
        
        if task_type in allowed_task_types:
            print(f"✅ Тип задачи '{task_type}' разрешен для ассистента")
            
            # Assign the task
            cursor.execute("""
                UPDATE tasks 
                SET assistant_id = ?, status = 'in_progress', claimed_at = ?
                WHERE id = ?
            """, (assistant_id, datetime.utcnow().isoformat(), task_id))
            
            # Update assistant's active task count
            cursor.execute("""
                UPDATE assistant_profiles 
                SET current_active_tasks = current_active_tasks + 1
                WHERE id = ?
            """, (assistant_id,))
            
            print(f"✅ Задача автоматически назначена ассистенту {assistant_name}")
        else:
            print(f"❌ Тип задачи '{task_type}' НЕ разрешен для ассистента")
    else:
        print(f"❌ Не найдено активного назначения для клиента {client_id}")
    
    # Commit changes
    conn.commit()
    print("✅ Изменения сохранены в базе данных")
    
except Exception as e:
    print(f"❌ Ошибка: {e}")
    conn.rollback()
finally:
    conn.close()

# Verify the result
print("\n=== ПРОВЕРКА РЕЗУЛЬТАТА ===")
conn = sqlite3.connect(db_path)
cursor = conn.cursor()

cursor.execute("""
    SELECT 
        t.id,
        t.title,
        t.type,
        t.status,
        t.assistant_id,
        u.name as assistant_name,
        t.created_at,
        t.claimed_at
    FROM tasks t
    LEFT JOIN assistant_profiles ap ON t.assistant_id = ap.id
    LEFT JOIN users u ON ap.user_id = u.id
    WHERE t.client_id = 14
    ORDER BY t.id DESC
    LIMIT 3
""")

recent_tasks = cursor.fetchall()
print("Последние задачи клиента DDDD:")
for task in recent_tasks:
    task_id, title, task_type, status, assistant_id, assistant_name, created_at, claimed_at = task
    print(f"  ID {task_id}: {title}")
    print(f"    Тип: {task_type}, Статус: {status}")
    print(f"    Ассистент: {assistant_name or 'Не назначен'} (ID: {assistant_id or 'N/A'})")
    print(f"    Создано: {created_at}")
    print(f"    Взято в работу: {claimed_at or 'N/A'}")
    print()

conn.close() 