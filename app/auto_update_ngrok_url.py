#!/usr/bin/env python3
"""
Автоматическое обновление ngrok URL в проекте
Получает текущий URL от ngrok API и обновляет все файлы
"""

import requests
import json
import os
import re
import time
from pathlib import Path

def get_ngrok_url():
    """Получает публичный URL от ngrok API"""
    try:
        # Пробуем получить URL от локального ngrok API
        response = requests.get('http://localhost:4040/api/tunnels', timeout=5)
        if response.status_code == 200:
            data = response.json()
            
            # Ищем HTTPS туннель
            for tunnel in data.get('tunnels', []):
                if tunnel.get('proto') == 'https':
                    public_url = tunnel.get('public_url')
                    if public_url:
                        print(f"✅ Найден ngrok URL: {public_url}")
                        return public_url
            
            print("❌ HTTPS туннель не найден")
            return None
            
    except requests.exceptions.RequestException as e:
        print(f"❌ Ошибка подключения к ngrok API: {e}")
        return None

def read_file_with_encoding(file_path):
    """Читает файл, пробуя разные кодировки"""
    encodings = ['utf-8', 'utf-8-sig', 'cp1251', 'cp866', 'latin1']
    
    for encoding in encodings:
        try:
            with open(file_path, 'r', encoding=encoding) as f:
                content = f.read()
            return content, encoding
        except (UnicodeDecodeError, UnicodeError):
            continue
    
    # Если все кодировки не работают, используем errors='ignore'
    try:
        with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
            content = f.read()
        return content, 'utf-8'
    except Exception as e:
        raise Exception(f"Не удалось прочитать файл {file_path}: {e}")

def update_env_file(new_url):
    """Обновляет .env файлы с новым URL"""
    env_files = [Path('.env'), Path('bots/.env')]
    
    for env_file in env_files:
        if env_file.exists():
            try:
                content, detected_encoding = read_file_with_encoding(env_file)
                
                # Обновляем или добавляем WEBAPP_URL
                if 'WEBAPP_URL=' in content:
                    content = re.sub(r'WEBAPP_URL=.*', f'WEBAPP_URL={new_url}', content)
                else:
                    content += f'\nWEBAPP_URL={new_url}\n'
                
                # Сохраняем в UTF-8
                with open(env_file, 'w', encoding='utf-8') as f:
                    f.write(content)
                
                print(f"✅ Обновлен {env_file} (было: {detected_encoding})")
                
            except Exception as e:
                print(f"❌ Ошибка обновления {env_file}: {e}")
                # Создаем новый файл
                try:
                    env_file.parent.mkdir(parents=True, exist_ok=True)
                    with open(env_file, 'w', encoding='utf-8') as f:
                        f.write(f'WEBAPP_URL={new_url}\n')
                        f.write('BOT_TOKEN=YOUR_BOT_TOKEN_HERE\n')
                    print(f"✅ Создан новый {env_file}")
                except Exception as create_error:
                    print(f"❌ Не удалось создать {env_file}: {create_error}")
        else:
            # Создаем новый .env файл
            try:
                env_file.parent.mkdir(parents=True, exist_ok=True)
                with open(env_file, 'w', encoding='utf-8') as f:
                    f.write(f'WEBAPP_URL={new_url}\n')
                    f.write('BOT_TOKEN=YOUR_BOT_TOKEN_HERE\n')
                
                print(f"✅ Создан новый {env_file}")
            except Exception as e:
                print(f"❌ Не удалось создать {env_file}: {e}")

def update_bot_files(new_url):
    """Обновляет все bot файлы с новым URL"""
    bot_files = [
        'bots/bot1_simple.py',
        'bots/bot_simple.py'
    ]
    
    old_url_pattern = r'https://[a-zA-Z0-9\-]+\.ngrok-free\.app'
    
    for file_path in bot_files:
        if os.path.exists(file_path):
            try:
                content, detected_encoding = read_file_with_encoding(file_path)
                
                # Заменяем старые ngrok URL на новый
                updated_content = re.sub(old_url_pattern, new_url, content)
                
                # Сохраняем в UTF-8
                with open(file_path, 'w', encoding='utf-8') as f:
                    f.write(updated_content)
                
                print(f"✅ Обновлен файл: {file_path} (было: {detected_encoding})")
                
            except Exception as e:
                print(f"❌ Ошибка обновления {file_path}: {e}")
        else:
            print(f"⚠️  Файл не найден: {file_path}")

def update_frontend_files(new_url):
    """Обновляет frontend файлы с новым URL"""
    frontend_files = [
        'frontend/api.js',
        'frontend/app.js'
    ]
    
    old_url_pattern = r'https://[a-zA-Z0-9\-]+\.ngrok-free\.app'
    
    for file_path in frontend_files:
        if os.path.exists(file_path):
            try:
                content, detected_encoding = read_file_with_encoding(file_path)
                
                # Заменяем старые ngrok URL на новый
                updated_content = re.sub(old_url_pattern, new_url, content)
                
                # Сохраняем в UTF-8
                with open(file_path, 'w', encoding='utf-8') as f:
                    f.write(updated_content)
                
                print(f"✅ Обновлен файл: {file_path} (было: {detected_encoding})")
                
            except Exception as e:
                print(f"❌ Ошибка обновления {file_path}: {e}")
        else:
            print(f"⚠️  Файл не найден: {file_path}")

def wait_for_ngrok(max_attempts=30, delay=2):
    """Ждет запуска ngrok с повторными попытками"""
    print(f"🔄 Ожидание запуска ngrok (максимум {max_attempts} попыток)...")
    
    for attempt in range(max_attempts):
        url = get_ngrok_url()
        if url:
            return url
        
        print(f"⏳ Попытка {attempt + 1}/{max_attempts}... Ждем {delay} сек")
        time.sleep(delay)
    
    print("❌ ngrok не запустился в течение заданного времени")
    return None

def main():
    """Основная функция"""
    print("🚀 Автоматическое обновление ngrok URL")
    print("=" * 40)
    
    # Проверяем, запущен ли ngrok
    ngrok_url = get_ngrok_url()
    
    if not ngrok_url:
        print("🔄 ngrok не найден, ожидаем запуска...")
        ngrok_url = wait_for_ngrok()
    
    if not ngrok_url:
        print("❌ Не удалось получить ngrok URL")
        return False
    
    print(f"🌐 Обновляем проект с URL: {ngrok_url}")
    print("-" * 40)
    
    # Обновляем все файлы
    try:
        update_env_file(ngrok_url)
        update_bot_files(ngrok_url)
        update_frontend_files(ngrok_url)
        
        print("-" * 40)
        print("✅ Все файлы успешно обновлены!")
        print(f"🌐 Текущий URL: {ngrok_url}")
        return True
        
    except Exception as e:
        print(f"❌ Критическая ошибка: {e}")
        return False

if __name__ == "__main__":
    success = main()
    if not success:
        exit(1) 