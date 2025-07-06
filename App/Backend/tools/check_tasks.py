#!/usr/bin/env python3
"""
Проверка задач в базе данных
"""
import sqlite3
import os

# Connect to database
current_dir = os.path.dirname(os.path.abspath(__file__))
db_path = os.path.abspath(os.path.join(current_dir, '..', 'test.db'))
conn = sqlite3.connect(db_path)
cursor = conn.cursor()

print("=== ЗАДАЧИ В БАЗЕ ДАННЫХ ===")

# Get tasks
cursor.execute("SELECT id, title, type, status, assistant_id, client_id, created_at FROM tasks ORDER BY id")
tasks = cursor.fetchall()

print(f"Всего задач: {len(tasks)}")
print()

for task in tasks:
    task_id, title, task_type, status, assistant_id, client_id, created_at = task
    print(f"ID {task_id}: {title}")
    print(f"  Тип: {task_type}")
    print(f"  Статус: {status}")
    print(f"  Ассистент: {assistant_id if assistant_id else 'Не назначен'}")
    print(f"  Клиент: {client_id}")
    print(f"  Создано: {created_at}")
    print()

# Check marketplace tasks
cursor.execute("SELECT COUNT(*) FROM tasks WHERE status = 'pending' AND assistant_id IS NULL")
marketplace_count = cursor.fetchone()[0]

print(f"📊 Задач в маркетплейсе (pending + не назначенные): {marketplace_count}")

conn.close() 