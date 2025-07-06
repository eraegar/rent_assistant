#!/usr/bin/env python3
"""
Исправление множественных назначений ассистентов на клиентов
"""
import sqlite3
import os
from datetime import datetime

# Connect to database
current_dir = os.path.dirname(os.path.abspath(__file__))
db_path = os.path.abspath(os.path.join(current_dir, '..', 'test.db'))

print("=== ИСПРАВЛЕНИЕ МНОЖЕСТВЕННЫХ НАЗНАЧЕНИЙ ===")
print()

conn = sqlite3.connect(db_path)
cursor = conn.cursor()

# 1. Найти всех клиентов с множественными назначениями
print("1. Поиск клиентов с множественными ассистентами:")
cursor.execute("""
    SELECT 
        ca.client_id,
        u_client.name as client_name,
        COUNT(*) as assistant_count
    FROM client_assistant_assignments ca
    JOIN client_profiles cp ON ca.client_id = cp.id
    JOIN users u_client ON cp.user_id = u_client.id
    WHERE ca.status = 'active'
    GROUP BY ca.client_id, u_client.name
    HAVING COUNT(*) > 1
""")

violating_clients = cursor.fetchall()

if not violating_clients:
    print("  ✅ Множественных назначений не найдено")
    conn.close()
    exit()

for client_id, client_name, count in violating_clients:
    print(f"  ❌ Клиент {client_id} ({client_name}) имеет {count} ассистентов")

print()

# 2. Для каждого клиента оставить только последнее назначение
print("2. Исправление назначений:")

for client_id, client_name, count in violating_clients:
    print(f"  Обработка клиента {client_id} ({client_name}):")
    
    # Получить все назначения этого клиента, отсортированные по дате создания
    cursor.execute("""
        SELECT 
            ca.id,
            ca.assistant_id,
            u_assistant.name as assistant_name,
            ca.created_at
        FROM client_assistant_assignments ca
        JOIN assistant_profiles ap ON ca.assistant_id = ap.id
        JOIN users u_assistant ON ap.user_id = u_assistant.id
        WHERE ca.client_id = ? AND ca.status = 'active'
        ORDER BY ca.created_at DESC
    """, (client_id,))
    
    assignments = cursor.fetchall()
    
    # Оставляем первое (самое новое) назначение активным
    latest_assignment = assignments[0]
    latest_id, latest_assistant_id, latest_assistant_name, latest_created_at = latest_assignment
    print(f"    ✅ Оставляем: Ассистент {latest_assistant_id} ({latest_assistant_name}) - {latest_created_at}")
    
    # Деактивируем остальные назначения
    for assignment in assignments[1:]:
        assignment_id, assistant_id, assistant_name, created_at = assignment
        print(f"    🔄 Деактивируем: Ассистент {assistant_id} ({assistant_name}) - {created_at}")
        
        cursor.execute("""
            UPDATE client_assistant_assignments 
            SET status = 'deactivated'
            WHERE id = ?
        """, (assignment_id,))
        
        # Возвращаем задачи этого ассистента в маркетплейс (если они были назначены через это назначение)
        cursor.execute("""
            UPDATE tasks 
            SET assistant_id = NULL, status = 'pending', claimed_at = NULL
            WHERE client_id = ? AND assistant_id = ? AND status = 'in_progress'
        """, (client_id, assistant_id))
        
        # Обновляем счетчик активных задач у ассистента
        cursor.execute("""
            UPDATE assistant_profiles 
            SET current_active_tasks = (
                SELECT COUNT(*) 
                FROM tasks 
                WHERE assistant_id = ? AND status = 'in_progress'
            )
            WHERE id = ?
        """, (assistant_id, assistant_id))

print()

# 3. Commit изменения
print("3. Сохранение изменений...")
conn.commit()
print("  ✅ Изменения сохранены")

print()

# 4. Проверка результата
print("4. Проверка после исправления:")
cursor.execute("""
    SELECT 
        client_id,
        COUNT(*) as assistant_count
    FROM client_assistant_assignments 
    WHERE status = 'active'
    GROUP BY client_id
    HAVING COUNT(*) > 1
""")

remaining_violations = cursor.fetchall()

if remaining_violations:
    print("  ❌ Еще остались нарушения:")
    for client_id, count in remaining_violations:
        print(f"    Клиент {client_id} имеет {count} ассистентов")
else:
    print("  ✅ Все исправлено - у каждого клиента максимум 1 ассистент")

# 5. Итоговая статистика
print()
print("5. Итоговая статистика:")
cursor.execute("SELECT COUNT(*) FROM client_profiles")
total_clients = cursor.fetchone()[0]

cursor.execute("SELECT COUNT(DISTINCT client_id) FROM client_assistant_assignments WHERE status = 'active'")
assigned_clients = cursor.fetchone()[0]

cursor.execute("SELECT COUNT(*) FROM tasks WHERE status = 'pending' AND assistant_id IS NULL")
marketplace_tasks = cursor.fetchone()[0]

print(f"  Всего клиентов: {total_clients}")
print(f"  Клиентов с ассистентами: {assigned_clients}")
print(f"  Клиентов без ассистентов: {total_clients - assigned_clients}")
print(f"  Задач в маркетплейсе: {marketplace_tasks}")

conn.close()

print()
print("=== ИСПРАВЛЕНИЕ ЗАВЕРШЕНО ===")
print("✅ Теперь каждый клиент имеет максимум одного ассистента")
print()
print("💡 Запустите тест снова для проверки:")
print("   python test_one_assistant_per_client.py") 