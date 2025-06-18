# Развертывание Telegram Assistant на сервере

## Быстрый старт

### 1. Подготовка сервера

```bash
# Скачайте и запустите скрипт развертывания
wget https://raw.githubusercontent.com/YOUR_USERNAME/YOUR_REPO/main/deploy.sh
chmod +x deploy.sh
./deploy.sh
```

### 2. Настройка

```bash
cd telegram-assistant/app

# Скопируйте пример конфигурации
cp env_example.txt .env

# Отредактируйте настройки
nano .env
```

Обязательно укажите:
- `BOT_TOKEN` - токен вашего бота от @BotFather
- `SECRET_KEY` - секретный ключ для JWT

### 3. Настройка ngrok

```bash
# Зарегистрируйтесь на ngrok.com и получите authtoken
ngrok config add-authtoken YOUR_NGROK_TOKEN
```

### 4. Запуск

```bash
# Сделайте скрипт исполняемым
chmod +x start_server.sh

# Запустите все сервисы
./start_server.sh
```

## Что происходит при запуске

1. **FastAPI сервер** запускается на порту 8000
2. **ngrok** создает туннель и получает публичный URL
3. **.env файл** автоматически обновляется с новым URL
4. **Telegram бот** запускается и использует новый URL

## Управление сервисами

```bash
# Просмотр логов
tail -f nohup.out

# Остановка всех сервисов
pkill -f "uvicorn\|ngrok\|bot1_simple"

# Перезапуск
./start_server.sh
```

## Структура проекта

```
telegram-assistant/
├── app/
│   ├── main.py              # FastAPI приложение
│   ├── bots/
│   │   └── bot1_simple.py   # Telegram бот
│   ├── frontend/            # Веб-интерфейс
│   ├── requirements.txt     # Зависимости Python
│   ├── .env                 # Настройки (создается автоматически)
│   ├── deploy.sh           # Скрипт развертывания
│   └── start_server.sh     # Скрипт запуска
```

## Полезные команды

```bash
# Проверка статуса портов
netstat -tlnp | grep :8000
netstat -tlnp | grep :4040

# Проверка процессов
ps aux | grep -E "(uvicorn|ngrok|python.*bot)"

# Просмотр ngrok URL
curl -s http://localhost:4040/api/tunnels | jq '.tunnels[0].public_url'
```

## Автозапуск (systemd)

Создайте systemd сервис для автозапуска:

```bash
sudo nano /etc/systemd/system/telegram-assistant.service
```

```ini
[Unit]
Description=Telegram Assistant
After=network.target

[Service]
Type=forking
User=your_username
WorkingDirectory=/path/to/telegram-assistant/app
ExecStart=/path/to/telegram-assistant/app/start_server.sh
Restart=always

[Install]
WantedBy=multi-user.target
```

```bash
sudo systemctl enable telegram-assistant
sudo systemctl start telegram-assistant
``` 