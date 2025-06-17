#!/usr/bin/env python3
"""
Скрипт для автоматического получения ngrok URL и обновления конфигурации бота
"""
import requests
import json
import time
import os
from dotenv import load_dotenv, set_key

load_dotenv()

def get_ngrok_url():
    """Получаем публичный URL от ngrok"""
    try:
        # ngrok API endpoint (локальный)
        response = requests.get("http://127.0.0.1:4040/api/tunnels")
        if response.status_code == 200:
            tunnels = response.json()["tunnels"]
            for tunnel in tunnels:
                if tunnel["config"]["addr"] == "http://localhost:8000":
                    public_url = tunnel["public_url"]
                    if public_url.startswith("https://"):
                        return public_url
        return None
    except Exception as e:
        print(f"❌ Ошибка получения ngrok URL: {e}")
        return None

def update_env_file(webapp_url):
    """Обновляем .env файл с новым URL"""
    try:
        # Обновляем WEBAPP_URL в .env файле
        if os.path.exists('.env'):
            set_key('.env', 'WEBAPP_URL', webapp_url)
        else:
            # Создаем .env файл если его нет
            with open('.env', 'w') as f:
                f.write(f"BOT_TOKEN=YOUR_BOT_TOKEN_HERE\n")
                f.write(f"WEBAPP_URL={webapp_url}\n")
                f.write(f"SECRET_KEY=your-secret-key-here\n")
        
        print(f"✅ Обновлен .env файл: WEBAPP_URL={webapp_url}")
        return True
    except Exception as e:
        print(f"❌ Ошибка обновления .env: {e}")
        return False

def wait_for_ngrok():
    """Ждем запуска ngrok"""
    print("⏳ Ожидаем запуска ngrok...")
    for i in range(30):  # Ждем до 30 секунд
        url = get_ngrok_url()
        if url:
            return url
        time.sleep(1)
        print(f"   Попытка {i+1}/30...")
    return None

def main():
    print("🚀 Настройка ngrok для Telegram WebApp")
    print("=" * 50)
    
    # Проверяем, запущен ли ngrok
    ngrok_url = get_ngrok_url()
    
    if not ngrok_url:
        print("❌ ngrok не запущен или не найден туннель на порт 8000")
        print("\n📋 Инструкции по запуску:")
        print("1. Скачайте ngrok: https://ngrok.com/download")
        print("2. Зарегистрируйтесь и получите authtoken")
        print("3. Запустите: ngrok http 8000")
        print("4. Запустите этот скрипт снова")
        
        # Пытаемся дождаться ngrok
        ngrok_url = wait_for_ngrok()
        
        if not ngrok_url:
            print("❌ Время ожидания истекло. Запустите ngrok и попробуйте снова.")
            return False
    
    print(f"✅ Найден ngrok URL: {ngrok_url}")
    
    # Обновляем конфигурацию
    if update_env_file(ngrok_url):
        print(f"\n🎉 Настройка завершена!")
        print(f"🌐 Ваш WebApp URL: {ngrok_url}")
        print(f"\n📋 Следующие шаги:")
        print(f"1. Обновите токен бота в .env файле")
        print(f"2. Запустите FastAPI сервер: uvicorn main:main --reload --host 0.0.0.0 --port 8000")
        print(f"3. Запустите бота: python bots/bot1.py")
        print(f"4. В @BotFather установите WebApp URL: {ngrok_url}")
        
        return True
    
    return False

if __name__ == "__main__":
    main() 