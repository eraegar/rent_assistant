#!/usr/bin/env python3
"""
watch_root_db.py – простой монитор для базы test.db в корне проекта.
Каждые 5 секунд показывает список таблиц и количество записей.
Остановить — Ctrl+C.
"""
import sqlite3
import os
import time
from datetime import datetime

# Путь к базе: два уровня выше папки app/tools
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.abspath(os.path.join(SCRIPT_DIR, '..', '..', 'test.db'))

REFRESH_SECONDS = 5


def get_tables(cursor):
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
    return [row[0] for row in cursor.fetchall()]


def print_stats():
    if not os.path.exists(DB_PATH):
        print(f"❌ Файл базы не найден: {DB_PATH}")
        return

    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()

    tables = get_tables(cur)

    ts = datetime.now().strftime('%H:%M:%S')
    print("=" * 60)
    print(f"⏰ {ts}   |  Обзор базы {os.path.basename(DB_PATH)}")
    print("=" * 60)

    if not tables:
        print("📂 Нет таблиц.")
    else:
        for tbl in tables:
            cur.execute(f"SELECT COUNT(*) FROM {tbl};")
            count = cur.fetchone()[0]
            print(f"{tbl:<20} → {count} записей")

    conn.close()


def main():
    try:
        while True:
            os.system('cls' if os.name == 'nt' else 'clear')
            print_stats()
            time.sleep(REFRESH_SECONDS)
    except KeyboardInterrupt:
        print("\n🚪 Выход из watch_root_db.")


if __name__ == '__main__':
    main() 