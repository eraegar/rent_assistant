import requests

# Используем полный токен
TOKEN = "8143892418:AAG1KiaAA7zZigMNTyeV1ZDdgyBlBD0rW90"

print(f"🔍 Очищаем webhook для бота...")
print(f"🔑 Token: {TOKEN[:10]}...")

# Удаляем webhook
url = f"https://api.telegram.org/bot{TOKEN}/deleteWebhook"
response = requests.get(url)

if response.status_code == 200:
    print("✅ Webhook удален успешно!")
    print(f"📋 Ответ: {response.json()}")
else:
    print(f"❌ Ошибка удаления webhook: {response.text}")

# Проверяем информацию о webhook
url = f"https://api.telegram.org/bot{TOKEN}/getWebhookInfo"
response = requests.get(url)

if response.status_code == 200:
    info = response.json()
    print("📋 Информация о webhook:")
    print(f"   URL: {info['result'].get('url', 'Не установлен')}")
    print(f"   Pending updates: {info['result'].get('pending_update_count', 0)}")
else:
    print(f"❌ Ошибка получения информации: {response.text}")

print("🚀 Теперь можно запускать бота!") 