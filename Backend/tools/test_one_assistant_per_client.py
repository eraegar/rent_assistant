#!/usr/bin/env python3
"""
Тест для проверки ограничения "один ассистент на клиента"
"""
import sqlite3
import os
import requests
import json

# Connect to database
current_dir = os.path.dirname(os.path.abspath(__file__))
db_path = os.path.abspath(os.path.join(current_dir, '..', 'test.db'))

print("=== ТЕСТ: ОДИН АССИСТЕНТ НА КЛИЕНТА ===")
print()

# 1. Проверить текущие назначения
conn = sqlite3.connect(db_path)
cursor = conn.cursor()

print("1. Текущие назначения клиентов:")
cursor.execute("""
    SELECT 
        ca.client_id,
        u_client.name as client_name,
        ca.assistant_id,
        u_assistant.name as assistant_name,
        ca.status
    FROM client_assistant_assignments ca
    JOIN client_profiles cp ON ca.client_id = cp.id
    JOIN users u_client ON cp.user_id = u_client.id
    JOIN assistant_profiles ap ON ca.assistant_id = ap.id
    JOIN users u_assistant ON ap.user_id = u_assistant.id
    WHERE ca.status = 'active'
    ORDER BY ca.client_id
""")

assignments = cursor.fetchall()
for assignment in assignments:
    client_id, client_name, assistant_id, assistant_name, status = assignment
    print(f"  Клиент {client_id} ({client_name}) → Ассистент {assistant_id} ({assistant_name})")

print()

# 2. Проверить нарушения правила (клиенты с несколькими ассистентами)
print("2. Проверка нарушений (клиенты с несколькими ассистентами):")
cursor.execute("""
    SELECT 
        client_id,
        COUNT(*) as assistant_count
    FROM client_assistant_assignments 
    WHERE status = 'active'
    GROUP BY client_id
    HAVING COUNT(*) > 1
""")

violations = cursor.fetchall()
if violations:
    print("  ❌ НАЙДЕНЫ НАРУШЕНИЯ:")
    for violation in violations:
        client_id, count = violation
        print(f"    Клиент {client_id} имеет {count} ассистентов!")
else:
    print("  ✅ Нарушений не найдено - у каждого клиента максимум 1 ассистент")

print()

# 3. Проверить API эндпоинт (симуляция)
print("3. Проверка логики назначения:")

# Найдем клиента без ассистента
cursor.execute("""
    SELECT cp.id, u.name
    FROM client_profiles cp
    JOIN users u ON cp.user_id = u.id
    LEFT JOIN client_assistant_assignments caa ON cp.id = caa.client_id AND caa.status = 'active'
    WHERE caa.id IS NULL
    LIMIT 1
""")

unassigned_client = cursor.fetchone()

# Найдем клиента с ассистентом
cursor.execute("""
    SELECT cp.id, u.name
    FROM client_profiles cp
    JOIN users u ON cp.user_id = u.id
    JOIN client_assistant_assignments caa ON cp.id = caa.client_id AND caa.status = 'active'
    LIMIT 1
""")

assigned_client = cursor.fetchone()

if unassigned_client:
    client_id, client_name = unassigned_client
    print(f"  ✅ Клиент без ассистента: {client_id} ({client_name}) - можно назначить")

if assigned_client:
    client_id, client_name = assigned_client
    print(f"  ⚠️  Клиент с ассистентом: {client_id} ({client_name}) - должен заблокировать повторное назначение")

print()

# 4. Статистика
print("4. Статистика:")
cursor.execute("SELECT COUNT(*) FROM client_profiles")
total_clients = cursor.fetchone()[0]

cursor.execute("SELECT COUNT(DISTINCT client_id) FROM client_assistant_assignments WHERE status = 'active'")
assigned_clients = cursor.fetchone()[0]

print(f"  Всего клиентов: {total_clients}")
print(f"  Клиентов с ассистентами: {assigned_clients}")
print(f"  Клиентов без ассистентов: {total_clients - assigned_clients}")

conn.close()

print()
print("=== РЕЗУЛЬТАТ ТЕСТА ===")
if violations:
    print("❌ ТЕСТ НЕ ПРОЙДЕН: Найдены клиенты с несколькими ассистентами")
    print("   Необходимо исправить данные в базе")
else:
    print("✅ ТЕСТ ПРОЙДЕН: Ограничение соблюдается")
    print("   Каждый клиент имеет максимум одного ассистента")

print()
print("💡 Для проверки API эндпоинта запустите backend:")
print("   cd app && python main.py")
print()
print("   Затем попробуйте назначить ассистента на клиента через manager-app") 