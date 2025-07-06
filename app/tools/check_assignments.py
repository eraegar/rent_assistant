#!/usr/bin/env python3
"""
Проверка назначений клиентов ассистентам
"""
import sqlite3
import os

# Connect to database
current_dir = os.path.dirname(os.path.abspath(__file__))
db_path = os.path.abspath(os.path.join(current_dir, '..', 'test.db'))
conn = sqlite3.connect(db_path)
cursor = conn.cursor()

print("=== НАЗНАЧЕНИЯ КЛИЕНТОВ АССИСТЕНТАМ ===")

# Get all assignments
cursor.execute("""
    SELECT 
        ca.id as assignment_id,
        ca.client_id,
        u_client.name as client_name,
        ca.assistant_id,
        u_assistant.name as assistant_name,
        ca.status,
        ca.allowed_task_types,
        ca.created_at
    FROM client_assistant_assignments ca
    JOIN client_profiles cp ON ca.client_id = cp.id
    JOIN users u_client ON cp.user_id = u_client.id
    JOIN assistant_profiles ap ON ca.assistant_id = ap.id
    JOIN users u_assistant ON ap.user_id = u_assistant.id
    ORDER BY ca.created_at DESC
""")

assignments = cursor.fetchall()

print(f"Всего назначений: {len(assignments)}")
print()

for assignment in assignments:
    assignment_id, client_id, client_name, assistant_id, assistant_name, status, allowed_task_types, created_at = assignment
    print(f"Назначение #{assignment_id}:")
    print(f"  Клиент: {client_name} (ID: {client_id})")
    print(f"  Ассистент: {assistant_name} (ID: {assistant_id})")
    print(f"  Статус: {status}")
    print(f"  Разрешенные типы задач: {allowed_task_types}")
    print(f"  Создано: {created_at}")
    print()

# Check for client 14 specifically
print("=== ПРОВЕРКА КЛИЕНТА 14 (DDDD) ===")
cursor.execute("""
    SELECT 
        u.name as client_name,
        ca.assistant_id,
        u_assistant.name as assistant_name,
        ca.status,
        ca.allowed_task_types
    FROM client_profiles cp
    JOIN users u ON cp.user_id = u.id
    LEFT JOIN client_assistant_assignments ca ON cp.id = ca.client_id AND ca.status = 'active'
    LEFT JOIN assistant_profiles ap ON ca.assistant_id = ap.id
    LEFT JOIN users u_assistant ON ap.user_id = u_assistant.id
    WHERE cp.id = 14
""")

client_14 = cursor.fetchone()
if client_14:
    client_name, assistant_id, assistant_name, status, allowed_types = client_14
    print(f"Клиент: {client_name}")
    if assistant_id:
        print(f"Назначен ассистенту: {assistant_name} (ID: {assistant_id})")
        print(f"Статус назначения: {status}")
        print(f"Разрешенные типы задач: {allowed_types}")
    else:
        print("НЕ НАЗНАЧЕН ни одному ассистенту!")
else:
    print("Клиент 14 не найден!")

print()

# Check which assistant is Gennady
print("=== АССИСТЕНТЫ ===")
cursor.execute("""
    SELECT 
        ap.id,
        u.name,
        ap.specialization,
        ap.status,
        ap.current_active_tasks
    FROM assistant_profiles ap
    JOIN users u ON ap.user_id = u.id
    ORDER BY ap.id
""")

assistants = cursor.fetchall()
for assistant in assistants:
    assistant_id, name, specialization, status, active_tasks = assistant
    print(f"ID {assistant_id}: {name} - {specialization} - {status} - {active_tasks} активных задач")

conn.close() 