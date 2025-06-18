#!/bin/bash

# Скрипт для развертывания Telegram Assistant на сервере

echo "🚀 Развертывание Telegram Assistant..."
echo "====================================="

# Обновление системы
echo "📦 Обновление системы..."
sudo apt update && sudo apt upgrade -y

# Установка Python и pip
echo "🐍 Установка Python..."
sudo apt install -y python3 python3-pip python3-venv git curl

# Клонирование репозитория (замените URL на ваш)
echo "📥 Клонирование репозитория..."
if [ -d "telegram-assistant" ]; then
    cd telegram-assistant
    git pull
else
    git clone YOUR_REPO_URL telegram-assistant
    cd telegram-assistant/app
fi

# Создание виртуального окружения
echo "🔧 Создание виртуального окружения..."
python3 -m venv venv
source venv/bin/activate

# Установка зависимостей
echo "📚 Установка зависимостей..."
pip install -r requirements.txt

# Создание .env файла
echo "⚙️ Настройка окружения..."
if [ ! -f .env ]; then
    cp .env.example .env
    echo "❗ Отредактируйте файл .env с вашими токенами"
    echo "   BOT_TOKEN=ваш_токен_бота"
    echo "   SECRET_KEY=ваш_секретный_ключ"
fi

# Инициализация базы данных
echo "🗄️ Инициализация базы данных..."
python init_db.py

# Установка ngrok
echo "🌐 Установка ngrok..."
if ! command -v ngrok &> /dev/null; then
    curl -s https://ngrok-agent.s3.amazonaws.com/ngrok.asc | sudo tee /etc/apt/trusted.gpg.d/ngrok.asc >/dev/null
    echo "deb https://ngrok-agent.s3.amazonaws.com buster main" | sudo tee /etc/apt/sources.list.d/ngrok.list
    sudo apt update && sudo apt install ngrok
fi

echo "✅ Развертывание завершено!"
echo ""
echo "📋 Следующие шаги:"
echo "1. Отредактируйте .env файл: nano .env"
echo "2. Настройте ngrok: ngrok config add-authtoken YOUR_TOKEN"
echo "3. Запустите сервисы: ./start_server.sh" 