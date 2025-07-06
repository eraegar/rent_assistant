#!/usr/bin/env python3
"""
Переназначение клиента DDDD ассистенту Геннадию
"""
import sqlite3
import os
from datetime import datetime

# Connect to database
current_dir = os.path.dirname(os.path.abspath(__file__))
db_path = os.path.abspath(os.path.join(current_dir, '..', 'test.db'))
conn = sqlite3.connect(db_path)
cursor = conn.cursor()

print("=== ПЕРЕНАЗНАЧЕНИЕ КЛИЕНТА DDDD АССИСТЕНТУ ГЕННАДИЮ ===")

# First, check current assignment
cursor.execute("""
    SELECT ca.id, ca.assistant_id, u_assistant.name
    FROM client_assistant_assignments ca
    JOIN assistant_profiles ap ON ca.assistant_id = ap.id
    JOIN users u_assistant ON ap.user_id = u_assistant.id
    WHERE ca.client_id = 14 AND ca.status = 'active'
""")

current_assignment = cursor.fetchone()
if current_assignment:
    assignment_id, current_assistant_id, current_assistant_name = current_assignment
    print(f"Текущее назначение: Ассистент {current_assistant_name} (ID: {current_assistant_id})")
else:
    print("Клиент DDDD не назначен!")
    exit(1)

# Find Gennady's ID
cursor.execute("""
    SELECT ap.id, u.name
    FROM assistant_profiles ap
    JOIN users u ON ap.user_id = u.id
    WHERE u.name = 'Геннадий'
""")

gennady = cursor.fetchone()
if not gennady:
    print("Ассистент Геннадий не найден!")
    exit(1)

gennady_id, gennady_name = gennady
print(f"Найден ассистент: {gennady_name} (ID: {gennady_id})")

# Update the assignment
try:
    # Update the existing assignment
    cursor.execute("""
        UPDATE client_assistant_assignments 
        SET assistant_id = ?, updated_at = ?
        WHERE id = ?
    """, (gennady_id, datetime.utcnow().isoformat(), assignment_id))
    
    print(f"✅ Назначение обновлено: Клиент DDDD теперь назначен Геннадию")
    
    # Get all tasks from client 14 that are currently assigned to the old assistant
    cursor.execute("""
        SELECT id, title, type, status, assistant_id
        FROM tasks 
        WHERE client_id = 14 AND assistant_id = ?
    """, (current_assistant_id,))
    
    tasks_to_reassign = cursor.fetchall()
    print(f"Найдено {len(tasks_to_reassign)} задач для переназначения:")
    
    for task in tasks_to_reassign:
        task_id, title, task_type, status, old_assistant_id = task
        print(f"  - Задача {task_id}: {title} ({task_type}, {status})")
    
    if tasks_to_reassign:
        # Reassign all tasks to Gennady
        task_ids = [str(task[0]) for task in tasks_to_reassign]
        placeholders = ','.join(['?' for _ in task_ids])
        
        cursor.execute(f"""
            UPDATE tasks 
            SET assistant_id = ?, claimed_at = ?
            WHERE id IN ({placeholders}) AND client_id = 14
        """, [gennady_id, datetime.utcnow().isoformat()] + [int(tid) for tid in task_ids])
        
        # Update old assistant task count (decrease)
        cursor.execute("""
            UPDATE assistant_profiles 
            SET current_active_tasks = current_active_tasks - ?
            WHERE id = ?
        """, (len(tasks_to_reassign), current_assistant_id))
        
        # Update Gennady's task count (increase)
        cursor.execute("""
            UPDATE assistant_profiles 
            SET current_active_tasks = current_active_tasks + ?
            WHERE id = ?
        """, (len(tasks_to_reassign), gennady_id))
        
        print(f"✅ Переназначено {len(tasks_to_reassign)} задач Геннадию")
    
    # Commit all changes
    conn.commit()
    print("✅ Все изменения сохранены в базе данных")
    
except Exception as e:
    print(f"❌ Ошибка: {e}")
    conn.rollback()
finally:
    conn.close()

print("\n=== ПРОВЕРКА РЕЗУЛЬТАТА ===")
# Reconnect and verify
conn = sqlite3.connect(db_path)
cursor = conn.cursor()

# Check new assignment
cursor.execute("""
    SELECT 
        u_client.name as client_name,
        u_assistant.name as assistant_name,
        ca.status,
        ca.allowed_task_types
    FROM client_assistant_assignments ca
    JOIN client_profiles cp ON ca.client_id = cp.id
    JOIN users u_client ON cp.user_id = u_client.id
    JOIN assistant_profiles ap ON ca.assistant_id = ap.id
    JOIN users u_assistant ON ap.user_id = u_assistant.id
    WHERE ca.client_id = 14 AND ca.status = 'active'
""")

new_assignment = cursor.fetchone()
if new_assignment:
    client_name, assistant_name, status, allowed_types = new_assignment
    print(f"Клиент: {client_name}")
    print(f"Назначен ассистенту: {assistant_name}")
    print(f"Статус: {status}")
    print(f"Разрешенные типы задач: {allowed_types}")

# Check reassigned tasks
cursor.execute("""
    SELECT t.id, t.title, t.type, t.status, u.name as assistant_name
    FROM tasks t
    JOIN assistant_profiles ap ON t.assistant_id = ap.id
    JOIN users u ON ap.user_id = u.id
    WHERE t.client_id = 14
    ORDER BY t.id
""")

reassigned_tasks = cursor.fetchall()
print(f"\nЗадачи клиента DDDD:")
for task in reassigned_tasks:
    task_id, title, task_type, status, assistant_name = task
    print(f"  ID {task_id}: {title} - {task_type} - {status} - Ассистент: {assistant_name}")

conn.close() 