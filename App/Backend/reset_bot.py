#!/usr/bin/env python3
"""
Сброс состояния Telegram бота
Удаляет webhook и очищает очередь обновлений
"""

import os
import requests
import time
from dotenv import load_dotenv

load_dotenv()

def reset_bot():
    """Сбрасывает состояние бота"""
    token = os.getenv("BOT_TOKEN")
    
    if not token or token == "YOUR_BOT_TOKEN_HERE":
        print("❌ Токен бота не настроен в .env файле")
        return False
    
    print(f"🤖 Сброс состояния бота...")
    print(f"🔑 Token: {token[:10]}...")
    print("-" * 40)
    
    base_url = f"https://api.telegram.org/bot{token}"
    
    # 1. Удаляем webhook
    try:
        print("🔄 Удаление webhook...")
        response = requests.post(f"{base_url}/deleteWebhook", timeout=10)
        result = response.json()
        if result.get('ok'):
            print("✅ Webhook удален")
        else:
            print(f"⚠️  Webhook: {result.get('description', 'неизвестная ошибка')}")
    except Exception as e:
        print(f"⚠️  Ошибка удаления webhook: {e}")
    
    # 2. Получаем и очищаем все обновления
    try:
        print("🔄 Очистка очереди обновлений...")
        
        # Получаем все накопленные обновления
        response = requests.post(f"{base_url}/getUpdates", 
                               json={"timeout": 1, "limit": 100}, 
                               timeout=15)
        result = response.json()
        
        if result.get('ok'):
            updates = result.get('result', [])
            print(f"📥 Найдено {len(updates)} обновлений")
            
            if updates:
                # Берем ID последнего обновления и делаем offset
                last_update_id = updates[-1]['update_id']
                
                # Подтверждаем все обновления
                response = requests.post(f"{base_url}/getUpdates", 
                                       json={"offset": last_update_id + 1, "timeout": 1}, 
                                       timeout=10)
                print("✅ Очередь обновлений очищена")
            else:
                print("✅ Очередь обновлений пуста")
        else:
            print(f"⚠️  Ошибка получения обновлений: {result.get('description')}")
            
    except Exception as e:
        print(f"⚠️  Ошибка очистки обновлений: {e}")
    
    # 3. Проверяем статус бота
    try:
        print("🔄 Проверка статуса бота...")
        response = requests.post(f"{base_url}/getMe", timeout=10)
        result = response.json()
        
        if result.get('ok'):
            bot_info = result.get('result', {})
            print(f"✅ Бот активен: @{bot_info.get('username')}")
            print(f"📝 Имя: {bot_info.get('first_name')}")
        else:
            print(f"❌ Ошибка статуса: {result.get('description')}")
            return False
            
    except Exception as e:
        print(f"❌ Ошибка проверки статуса: {e}")
        return False
    
    print("-" * 40)
    print("✅ Сброс состояния бота завершен!")
    print("🚀 Теперь можно запускать бота")
    return True

if __name__ == "__main__":
    success = reset_bot()
    if not success:
        print("❌ Сброс не удался")
        exit(1)
    else:
        print("✅ Готово к запуску!") 