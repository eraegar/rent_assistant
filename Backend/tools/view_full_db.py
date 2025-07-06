import sqlite3
import os


def main():
    # Нахождение файла test.db в корне проекта
    script_dir = os.path.dirname(os.path.abspath(__file__))
    project_root = os.path.abspath(os.path.join(script_dir, '..', '..'))
    db_path = os.path.join(project_root, 'test.db')

    if not os.path.exists(db_path):
        print(f"❌ Файл базы данных не найден по пути: {db_path}")
        return

    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    # Список таблиц
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
    tables = [row[0] for row in cursor.fetchall()]

    if not tables:
        print("📂 Таблицы не найдены.")
    else:
        print(f"📊 Найдено таблиц: {len(tables)}")
        for table in tables:
            print(f"\n=== Таблица: {table} ===")
            # Структура таблицы
            cursor.execute(f"PRAGMA table_info({table});")
            cols = cursor.fetchall()
            col_names = [col[1] for col in cols]
            print(f"Столбцы: {col_names}")

            # Данные таблицы
            cursor.execute(f"SELECT * FROM {table};")
            rows = cursor.fetchall()
            print(f"Записей: {len(rows)}")
            for idx, row in enumerate(rows, 1):
                record = dict(zip(col_names, row))
                print(f"  {idx}. {record}")

    conn.close()


if __name__ == '__main__':
    main() 