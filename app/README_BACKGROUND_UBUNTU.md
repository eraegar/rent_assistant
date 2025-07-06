# 🐧 Запуск Telegram Assistant в фоновом режиме на Ubuntu 22.04

## 🚀 Быстрый старт

### 1. Подготовка системы
```bash
# Обновление системы
sudo apt update && sudo apt upgrade -y

# Установка зависимостей
sudo apt install python3 python3-pip python3-venv curl git -y

# Установка ngrok (если не установлен)
sudo snap install ngrok
# или скачать в папку проекта: https://ngrok.com/download
```

### 2. Настройка проекта
```bash
# Переход в папку проекта
cd /path/to/your/telegram-assistant/app

# Создание виртуального окружения (опционально)
python3 -m venv venv
source venv/bin/activate

# Установка зависимостей
pip3 install -r requirements.txt

# Настройка токена бота
./scripts/linux/setup_bot_token.sh
# или создать .env файл вручную
```

### 3. Запуск в фоновом режиме
```bash
# Сделать скрипт исполняемым
chmod +x start_background.sh

# Запустить все сервисы в фоне
./start_background.sh start
```

## 🔧 Управление сервисами

### Основные команды:
```bash
# Запуск всех сервисов
./start_background.sh start

# Остановка всех сервисов  
./start_background.sh stop

# Перезапуск всех сервисов
./start_background.sh restart

# Проверка статуса
./start_background.sh status

# Просмотр логов
./start_background.sh logs
```

### Что запускается:
1. **FastAPI сервер** - веб-интерфейс на порту 8001
2. **ngrok туннель** - публичный доступ к серверу
3. **Telegram бот** - обработка сообщений
4. **Автообновление URL** - синхронизация ngrok URL

## 📊 Мониторинг

### Проверка статуса:
```bash
./start_background.sh status
```

### Просмотр логов:
```bash
# Логи FastAPI
tail -f logs/fastapi.log

# Логи ngrok
tail -f logs/ngrok.log

# Логи бота
tail -f logs/bot.log

# Все логи сразу
tail -f logs/*.log
```

### Файлы процессов:
- PID файлы: `pids/`
- Логи: `logs/`

## 🔄 Автозапуск при загрузке (systemd)

### 1. Настройка сервиса:
```bash
# Редактировать пути в файле сервиса
sudo nano telegram-assistant.service

# Скопировать в systemd
sudo cp telegram-assistant.service /etc/systemd/system/

# Перезагрузить systemd
sudo systemctl daemon-reload

# Включить автозапуск
sudo systemctl enable telegram-assistant

# Запустить сервис
sudo systemctl start telegram-assistant
```

### 2. Управление systemd сервисом:
```bash
# Статус сервиса
sudo systemctl status telegram-assistant

# Логи сервиса
sudo journalctl -u telegram-assistant -f

# Перезапуск сервиса
sudo systemctl restart telegram-assistant

# Остановка сервиса
sudo systemctl stop telegram-assistant

# Отключение автозапуска
sudo systemctl disable telegram-assistant
```

## 🔧 Настройка для продакшена

### 1. Отредактировать systemd сервис:
```bash
# Заменить пути на реальные
sudo nano /etc/systemd/system/telegram-assistant.service

# Пример:
# WorkingDirectory=/home/ubuntu/telegram-assistant/app
# ExecStart=/home/ubuntu/telegram-assistant/app/start_background.sh start
```

### 2. Настроить пользователя:
```bash
# Создать пользователя для сервиса (опционально)
sudo useradd -r -s /bin/false telegram-assistant

# Или использовать существующего пользователя
# Заменить User=ubuntu на нужного пользователя
```

### 3. Права доступа:
```bash
# Сделать владельцем папки проекта
sudo chown -R ubuntu:ubuntu /path/to/telegram-assistant/

# Права на исполнение
chmod +x start_background.sh
chmod +x scripts/linux/*.sh
```

## 🛠️ Устранение неполадок

### Проблемы с запуском:
```bash
# Проверить статус
./start_background.sh status

# Проверить логи
./start_background.sh logs

# Проверить порты
sudo netstat -tlnp | grep :8001

# Проверить процессы
ps aux | grep python3
```

### Очистка:
```bash
# Остановить все сервисы
./start_background.sh stop

# Удалить PID и логи
rm -rf pids/ logs/

# Очистить webhook (если нужно)
python3 clear_webhook.py
```

### Переустановка зависимостей:
```bash
# Обновить requirements
pip3 install -r requirements.txt --upgrade

# Перезапустить сервисы
./start_background.sh restart
```

## 📋 Checklist перед запуском

- [ ] Python 3.8+ установлен
- [ ] pip3 установлен  
- [ ] ngrok установлен или скачан
- [ ] requirements.txt установлены
- [ ] .env файл создан с BOT_TOKEN
- [ ] start_background.sh имеет права на исполнение
- [ ] Порт 8001 свободен
- [ ] Интернет соединение работает

## 🎯 Результат

После успешного запуска у вас будет:

✅ **FastAPI сервер** - http://localhost:8001  
✅ **ngrok туннель** - https://xxx.ngrok.io  
✅ **Telegram бот** - работает в фоне  
✅ **Автообновление** - URL синхронизируется  
✅ **Логирование** - все логи сохраняются  
✅ **Мониторинг** - статус сервисов  

🎉 **Ваш Telegram Assistant работает в фоновом режиме!** 