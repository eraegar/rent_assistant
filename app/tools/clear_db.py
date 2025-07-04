import os
import sqlite3

# Определяем путь к test.db в корне проекта
script_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.abspath(os.path.join(script_dir, '..', '..'))
DB_PATH = os.path.join(project_root, 'test.db')

if not os.path.exists(DB_PATH):
    print(f"❌ Файл базы не найден: {DB_PATH}")
    exit(1)

# Connect to database
conn = sqlite3.connect(DB_PATH)
cursor = conn.cursor()

print("Clearing database...")

# Получаем список таблиц
cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
tables = [row[0] for row in cursor.fetchall()]

for tbl in tables:
    cursor.execute(f"DELETE FROM {tbl}")

conn.commit()

print("Database cleared!")

# Show counts
for tbl in tables:
    cursor.execute(f"SELECT COUNT(*) FROM {tbl}")
    count = cursor.fetchone()[0]
    print(f"{tbl}: {count} records remaining")

conn.close() 