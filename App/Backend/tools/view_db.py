#!/usr/bin/env python3
"""
Скрипт для просмотра содержимого базы данных SQLite
"""
import sqlite3
import json
from datetime import datetime

def view_database():
    try:
        # Подключаемся к базе данных
        conn = sqlite3.connect('test.db')
        cursor = conn.cursor()
        
        print("=" * 60)
        print("📊 СОДЕРЖИМОЕ БАЗЫ ДАННЫХ")
        print("=" * 60)
        
        # Получаем список таблиц
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
        tables = cursor.fetchall()
        
        print(f"\n🗂️  Найдено таблиц: {len(tables)}")
        for table in tables:
            print(f"   - {table[0]}")
        
        # Просматриваем каждую таблицу
        for table_name in [t[0] for t in tables]:
            print(f"\n" + "=" * 60)
            print(f"📋 ТАБЛИЦА: {table_name.upper()}")
            print("=" * 60)
            
            # Получаем структуру таблицы
            cursor.execute(f"PRAGMA table_info({table_name})")
            columns = cursor.fetchall()
            
            print("\n🏗️  Структура таблицы:")
            for col in columns:
                print(f"   {col[1]} ({col[2]}) {'- PRIMARY KEY' if col[5] else ''}")
            
            # Получаем данные
            cursor.execute(f"SELECT * FROM {table_name}")
            rows = cursor.fetchall()
            
            print(f"\n📊 Записей в таблице: {len(rows)}")
            
            if rows:
                print("\n📄 Данные:")
                column_names = [col[1] for col in columns]
                
                for i, row in enumerate(rows, 1):
                    print(f"\n   🔢 Запись #{i}:")
                    for j, value in enumerate(row):
                        col_name = column_names[j]
                        # Обрабатываем специальные поля
                        if col_name in ['password_hash']:
                            print(f"      {col_name}: [ЗАШИФРОВАН]")
                        elif col_name in ['created_at', 'updated_at'] and value:
                            try:
                                # Попытка парсинга даты
                                print(f"      {col_name}: {value}")
                            except:
                                print(f"      {col_name}: {value}")
                        else:
                            print(f"      {col_name}: {value}")
            else:
                print("   📭 Таблица пустая")
        
        conn.close()
        print(f"\n" + "=" * 60)
        print("✅ Просмотр завершен!")
        print("=" * 60)
        
    except Exception as e:
        print(f"❌ Ошибка при просмотре базы данных: {e}")

if __name__ == "__main__":
    view_database() 