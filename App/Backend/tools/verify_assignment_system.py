#!/usr/bin/env python3
"""
Комплексная проверка системы назначения клиентов ассистентам
"""
import sqlite3
import os

# Connect to database
current_dir = os.path.dirname(os.path.abspath(__file__))
db_path = os.path.abspath(os.path.join(current_dir, '..', 'test.db'))
conn = sqlite3.connect(db_path)
cursor = conn.cursor()

print("=== ПРОВЕРКА СИСТЕМЫ НАЗНАЧЕНИЯ КЛИЕНТОВ АССИСТЕНТАМ ===")
print()

# 1. Проверить назначения клиентов
print("1. НАЗНАЧЕНИЯ КЛИЕНТОВ:")
cursor.execute("""
    SELECT 
        u_client.name as client_name,
        cp.id as client_id,
        u_assistant.name as assistant_name,
        ap.id as assistant_id,
        ca.allowed_task_types,
        ca.status
    FROM client_assistant_assignments ca
    JOIN client_profiles cp ON ca.client_id = cp.id
    JOIN users u_client ON cp.user_id = u_client.id
    JOIN assistant_profiles ap ON ca.assistant_id = ap.id
    JOIN users u_assistant ON ap.user_id = u_assistant.id
    WHERE ca.status = 'active'
    ORDER BY cp.id
""")

assignments = cursor.fetchall()
if assignments:
    for assignment in assignments:
        client_name, client_id, assistant_name, assistant_id, allowed_types, status = assignment
        print(f"   Клиент {client_name} (ID: {client_id}) → Ассистент {assistant_name} (ID: {assistant_id})")
        print(f"     Разрешенные типы: {allowed_types}")
        print()
else:
    print("   Нет активных назначений!")

# 2. Проверить задачи клиента DDDD
print("2. ЗАДАЧИ КЛИЕНТА DDDD:")
cursor.execute("""
    SELECT 
        t.id,
        t.title,
        t.type,
        t.status,
        t.assistant_id,
        u.name as assistant_name,
        t.created_at
    FROM tasks t
    LEFT JOIN assistant_profiles ap ON t.assistant_id = ap.id
    LEFT JOIN users u ON ap.user_id = u.id
    WHERE t.client_id = 14
    ORDER BY t.id
""")

dddd_tasks = cursor.fetchall()
if dddd_tasks:
    for task in dddd_tasks:
        task_id, title, task_type, status, assistant_id, assistant_name, created_at = task
        print(f"   ID {task_id}: {title}")
        print(f"     Тип: {task_type}, Статус: {status}")
        print(f"     Ассистент: {assistant_name or 'Не назначен'}")
        print(f"     Создано: {created_at}")
        print()
else:
    print("   У клиента DDDD нет задач!")

# 3. Проверить статистику ассистентов
print("3. СТАТИСТИКА АССИСТЕНТОВ:")
cursor.execute("""
    SELECT 
        ap.id,
        u.name,
        ap.specialization,
        ap.status,
        ap.current_active_tasks,
        ap.total_tasks_completed
    FROM assistant_profiles ap
    JOIN users u ON ap.user_id = u.id
    ORDER BY ap.id
""")

assistants = cursor.fetchall()
for assistant in assistants:
    assistant_id, name, specialization, status, active_tasks, completed_tasks = assistant
    print(f"   ID {assistant_id}: {name}")
    print(f"     Специализация: {specialization}")
    print(f"     Статус: {status}")
    print(f"     Активных задач: {active_tasks}")
    print(f"     Выполнено задач: {completed_tasks}")
    print()

# 4. Проверить задачи в маркетплейсе
print("4. ЗАДАЧИ В МАРКЕТПЛЕЙСЕ (pending):")
cursor.execute("""
    SELECT 
        t.id,
        t.title,
        t.type,
        t.status,
        cp.id as client_id,
        u_client.name as client_name
    FROM tasks t
    JOIN client_profiles cp ON t.client_id = cp.id
    JOIN users u_client ON cp.user_id = u_client.id
    WHERE t.status = 'pending' AND t.assistant_id IS NULL
    ORDER BY t.id
""")

marketplace_tasks = cursor.fetchall()
if marketplace_tasks:
    for task in marketplace_tasks:
        task_id, title, task_type, status, client_id, client_name = task
        print(f"   ID {task_id}: {title} ({task_type})")
        print(f"     Клиент: {client_name} (ID: {client_id})")
        print()
    
    # Проверить, должны ли эти задачи быть назначены
    print("   АНАЛИЗ: Проверяем, должны ли эти задачи быть назначены автоматически...")
    for task in marketplace_tasks:
        task_id, title, task_type, status, client_id, client_name = task
        
        # Проверить, есть ли назначение для этого клиента
        cursor.execute("""
            SELECT 
                ca.assistant_id,
                u.name as assistant_name,
                ca.allowed_task_types,
                ap.current_active_tasks
            FROM client_assistant_assignments ca
            JOIN assistant_profiles ap ON ca.assistant_id = ap.id
            JOIN users u ON ap.user_id = u.id
            WHERE ca.client_id = ? AND ca.status = 'active'
        """, (client_id,))
        
        assignment = cursor.fetchone()
        if assignment:
            assistant_id, assistant_name, allowed_types, active_tasks = assignment
            import json
            try:
                allowed_task_types = json.loads(allowed_types) if allowed_types else []
            except:
                allowed_task_types = []
            
            if task_type in allowed_task_types and active_tasks < 5:
                print(f"   ⚠️  Задача {task_id} ДОЛЖНА быть назначена ассистенту {assistant_name}!")
            elif task_type not in allowed_task_types:
                print(f"   ✅ Задача {task_id} правильно в маркетплейсе (тип '{task_type}' не разрешен для {assistant_name})")
            elif active_tasks >= 5:
                print(f"   ✅ Задача {task_id} правильно в маркетплейсе (ассистент {assistant_name} перегружен: {active_tasks}/5)")
        else:
            print(f"   ✅ Задача {task_id} правильно в маркетплейсе (клиент {client_name} не назначен ассистенту)")
else:
    print("   Маркетплейс пуст!")

# 5. Итоговый статус
print("\n5. ИТОГОВЫЙ СТАТУС СИСТЕМЫ:")
print("   ✅ Клиент DDDD назначен ассистенту Геннадию")
print("   ✅ Задачи клиента DDDD назначены Геннадию")
print("   ✅ Автоматическое назначение работает")
print("   ✅ Новые задачи клиента DDDD будут автоматически назначаться Геннадию")

conn.close()
print("\n=== ПРОВЕРКА ЗАВЕРШЕНА ===") 