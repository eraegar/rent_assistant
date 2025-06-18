#!/bin/bash

# Скрипт для запуска всех сервисов Telegram Assistant

echo "🚀 Запуск Telegram Assistant сервисов..."
echo "======================================="

# Активация виртуального окружения
source venv/bin/activate

# Функция для остановки всех процессов при выходе
cleanup() {
    echo "🛑 Остановка сервисов..."
    kill $FASTAPI_PID $NGROK_PID $BOT_PID 2>/dev/null
    exit 0
}

trap cleanup SIGINT SIGTERM

# Запуск FastAPI сервера
echo "🌐 Запуск FastAPI сервера..."
python -m uvicorn main:app --host 0.0.0.0 --port 8000 &
FASTAPI_PID=$!
echo "✅ FastAPI запущен (PID: $FASTAPI_PID)"

# Ожидание запуска сервера
sleep 3

# Запуск ngrok
echo "🔗 Запуск ngrok..."
ngrok http 8000 --log=stdout &
NGROK_PID=$!
echo "✅ ngrok запущен (PID: $NGROK_PID)"

# Ожидание получения URL от ngrok
echo "⏳ Ожидание URL от ngrok..."
sleep 5

# Получение ngrok URL
NGROK_URL=$(curl -s http://localhost:4040/api/tunnels | python3 -c "
import sys, json
try:
    data = json.load(sys.stdin)
    for tunnel in data['tunnels']:
        if tunnel['config']['addr'] == 'http://localhost:8000':
            print(tunnel['public_url'])
            break
except:
    pass
")

if [ -n "$NGROK_URL" ]; then
    echo "🎉 ngrok URL: $NGROK_URL"
    
    # Обновление .env файла
    if [ -f .env ]; then
        sed -i "s|WEBAPP_URL=.*|WEBAPP_URL=$NGROK_URL|" .env
        echo "✅ .env файл обновлен"
    fi
else
    echo "❌ Не удалось получить ngrok URL"
fi

# Запуск Telegram бота
echo "🤖 Запуск Telegram бота..."
python bots/bot1_simple.py &
BOT_PID=$!
echo "✅ Бот запущен (PID: $BOT_PID)"

echo ""
echo "🎯 Все сервисы запущены!"
echo "📱 Протестируйте бота в Telegram"
echo "🌐 Веб-приложение: $NGROK_URL"
echo "📊 API документация: $NGROK_URL/docs"
echo ""
echo "🛑 Для остановки нажмите Ctrl+C"

# Ожидание
wait 