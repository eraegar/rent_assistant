#!/bin/bash

# 🚀 Автоматический деплой Telegram Assistant на Ubuntu 22.04
# Использование: ./deploy.sh [domain]

set -e

DOMAIN=${1:-"rent-assistant.ru"}
USER="telegram-assistant"
PROJECT_DIR="/home/$USER/telegram-assistant"

echo "🚀 Начинаем деплой Telegram Assistant..."
echo "📍 Домен: $DOMAIN"

# Проверка прав sudo
if [[ $EUID -eq 0 ]]; then
   echo "❌ Не запускайте этот скрипт от root. Используйте обычного пользователя с sudo."
   exit 1
fi

# Функция для вывода статуса
print_status() {
    echo "📋 $1"
}

# 1. Обновление системы
print_status "Обновление системы..."
sudo apt update && sudo apt upgrade -y

# 2. Установка зависимостей
print_status "Установка зависимостей..."
sudo apt install python3 python3-pip python3-venv git curl wget unzip htop nginx -y

# Установка Node.js 18
if ! command -v node &> /dev/null; then
    print_status "Установка Node.js..."
    curl -fsSL https://deb.nodesource.com/setup_18.x | sudo -E bash -
    sudo apt-get install -y nodejs
fi

# Установка PM2
if ! command -v pm2 &> /dev/null; then
    print_status "Установка PM2..."
    sudo npm install -g pm2 serve
fi

# 3. Создание пользователя (если не существует)
if ! id "$USER" &>/dev/null; then
    print_status "Создание пользователя $USER..."
    sudo useradd -m -s /bin/bash $USER
    sudo usermod -aG sudo $USER
fi

# 4. Настройка проекта
print_status "Настройка Backend..."
cd $PROJECT_DIR/Backend

# Создание виртуального окружения
if [ ! -d "venv" ]; then
    python3 -m venv venv
fi

source venv/bin/activate
pip install -r requirements.txt

# Создание .env файла (если не существует)
if [ ! -f ".env" ]; then
    cat > .env << EOF
DATABASE_URL=sqlite:///./telegram_assistant.db
SECRET_KEY=$(openssl rand -hex 32)
BOT_TOKEN=REPLACE_WITH_YOUR_BOT_TOKEN
CLIENT_WEBAPP_URL=https://$DOMAIN
MANAGER_WEBAPP_URL=https://manager.$DOMAIN
ASSISTANT_WEBAPP_URL=https://assistant.$DOMAIN
CORS_ORIGINS=["https://$DOMAIN","https://client.$DOMAIN","https://manager.$DOMAIN","https://assistant.$DOMAIN"]
EOF
    echo "⚠️  Не забудьте обновить BOT_TOKEN в Backend/.env"
fi

# Инициализация БД
if [ ! -f "telegram_assistant.db" ]; then
    python init_db.py
fi

# 5. Сборка Frontend приложений
print_status "Сборка Frontend приложений..."

# Client App
cd $PROJECT_DIR/Frontend/client-app
sed -i "s|http://127.0.0.1:8000/api/v1|https://api.$DOMAIN/api/v1|g" src/services/api.ts
npm install
npm run build

# Manager App
cd ../manager-app
sed -i "s|http://localhost:8000|https://api.$DOMAIN|g" src/stores/useManagerStore.ts
npm install
npm run build

# Assistant App
cd ../assistant-app
sed -i "s|http://localhost:8000|https://api.$DOMAIN|g" src/stores/useAssistantStore.ts
npm install
npm run build

# 6. Создание PM2 конфигурации
print_status "Настройка PM2..."
cd $PROJECT_DIR

cat > ecosystem.config.js << EOF
module.exports = {
  apps: [
    {
      name: 'telegram-assistant-backend',
      script: 'venv/bin/python',
      args: 'main.py',
      cwd: '$PROJECT_DIR/Backend',
      env: {
        PORT: 8000,
        NODE_ENV: 'production'
      },
      instances: 1,
      autorestart: true,
      watch: false,
      max_memory_restart: '1G'
    },
    {
      name: 'telegram-assistant-client',
      script: 'npx',
      args: 'serve -s build -l 3000',
      cwd: '$PROJECT_DIR/Frontend/client-app',
      env: { PORT: 3000 },
      instances: 1,
      autorestart: true,
      watch: false
    },
    {
      name: 'telegram-assistant-manager',
      script: 'npx',
      args: 'serve -s build -l 3001',
      cwd: '$PROJECT_DIR/Frontend/manager-app',
      env: { PORT: 3001 },
      instances: 1,
      autorestart: true,
      watch: false
    },
    {
      name: 'telegram-assistant-assistant',
      script: 'npx',
      args: 'serve -s build -l 3002',
      cwd: '$PROJECT_DIR/Frontend/assistant-app',
      env: { PORT: 3002 },
      instances: 1,
      autorestart: true,
      watch: false
    },
    {
      name: 'telegram-bot',
      script: 'venv/bin/python',
      args: 'bots/bot1_simple.py',
      cwd: '$PROJECT_DIR/TelegramBot',
      env: {
        PYTHONPATH: '$PROJECT_DIR/Backend'
      },
      instances: 1,
      autorestart: true,
      watch: false
    }
  ]
};
EOF

# 7. Создание директории для логов
sudo mkdir -p /var/log/telegram-assistant
sudo chown $USER:$USER /var/log/telegram-assistant

# 8. Установка Cloudflared
print_status "Установка Cloudflare Tunnel..."
if ! command -v cloudflared &> /dev/null; then
    wget -q https://github.com/cloudflare/cloudflared/releases/latest/download/cloudflared-linux-amd64.deb
    sudo dpkg -i cloudflared-linux-amd64.deb
    rm cloudflared-linux-amd64.deb
fi

# 9. Создание конфигурации туннеля
mkdir -p ~/.cloudflared
cat > ~/.cloudflared/config.yml << EOF
# Замените TUNNEL_NAME на имя вашего туннеля
tunnel: telegram-assistant-tunnel
credentials-file: /home/$USER/.cloudflared/TUNNEL_ID.json

ingress:
  # Client App (основное приложение)
  - hostname: $DOMAIN
    service: http://localhost:3000
  - hostname: client.$DOMAIN
    service: http://localhost:3000
    
  # Manager App (скрытое)
  - hostname: manager.$DOMAIN
    service: http://localhost:3001
    
  # Assistant App (скрытое)
  - hostname: assistant.$DOMAIN
    service: http://localhost:3002
    
  # API Backend
  - hostname: api.$DOMAIN
    service: http://localhost:8000
    
  # Catch-all
  - service: http://localhost:3000
EOF

# 10. Настройка файрвола
print_status "Настройка файрвола..."
sudo ufw --force enable
sudo ufw allow ssh
sudo ufw allow 80
sudo ufw allow 443

# 11. Создание скрипта бэкапа
print_status "Настройка автоматических бэкапов..."
cat > /home/$USER/backup.sh << 'EOF'
#!/bin/bash
DATE=$(date +%Y%m%d_%H%M%S)
BACKUP_DIR="/home/telegram-assistant/backups"
mkdir -p $BACKUP_DIR

# Бэкап базы данных
cp /home/telegram-assistant/telegram-assistant/Backend/telegram_assistant.db $BACKUP_DIR/db_backup_$DATE.db

# Удаление старых бэкапов (старше 7 дней)
find $BACKUP_DIR -name "db_backup_*.db" -mtime +7 -delete
EOF

chmod +x /home/$USER/backup.sh

# Добавление в crontab
(crontab -l 2>/dev/null; echo "0 2 * * * /home/$USER/backup.sh") | crontab -

# 12. Запуск сервисов
print_status "Запуск сервисов..."
pm2 start ecosystem.config.js
pm2 save
pm2 startup

echo ""
echo "🎉 Деплой завершен!"
echo ""
echo "📋 Следующие шаги:"
echo "1. Обновите BOT_TOKEN в Backend/.env"
echo "2. Выполните: cloudflared tunnel login"
echo "3. Выполните: cloudflared tunnel create telegram-assistant-tunnel"
echo "4. Обновите TUNNEL_ID в ~/.cloudflared/config.yml"
echo "5. Создайте DNS записи:"
echo "   cloudflared tunnel route dns telegram-assistant-tunnel $DOMAIN"
echo "   cloudflared tunnel route dns telegram-assistant-tunnel client.$DOMAIN"
echo "   cloudflared tunnel route dns telegram-assistant-tunnel manager.$DOMAIN"
echo "   cloudflared tunnel route dns telegram-assistant-tunnel assistant.$DOMAIN"
echo "   cloudflared tunnel route dns telegram-assistant-tunnel api.$DOMAIN"
echo "6. Запустите туннель: sudo cloudflared service install && sudo systemctl start cloudflared"
echo ""
echo "🔧 Полезные команды:"
echo "pm2 status          - статус сервисов"
echo "pm2 logs            - логи всех сервисов"
echo "pm2 restart all     - перезапуск всех сервисов"
echo ""
echo "🌐 После настройки туннеля ваши приложения будут доступны по адресам:"
echo "https://$DOMAIN - Клиентское приложение"
echo "https://manager.$DOMAIN - Панель менеджера"
echo "https://assistant.$DOMAIN - Панель ассистента"
echo "https://api.$DOMAIN - Backend API" 