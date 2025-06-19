# 🚀 Быстрый старт на Ubuntu 22.04

## ⚡ Одной командой

```bash
# Подготовка (выполнить один раз)
sudo apt update && sudo apt install python3 python3-pip curl -y && pip3 install -r requirements.txt && chmod +x start_background.sh && chmod +x monitor.sh

# Настройка токена (выполнить один раз)
nano .env
# Добавить: BOT_TOKEN=ваш_токен_от_BotFather

# Запуск в фоне
./start_background.sh start
```

## 🔧 Основные команды

```bash
# Управление сервисами
./start_background.sh start    # Запуск всех сервисов
./start_background.sh stop     # Остановка всех сервисов
./start_background.sh restart  # Перезапуск
./start_background.sh status   # Проверка статуса

# Мониторинг
./monitor.sh                   # Живой мониторинг (обновляется каждые 30 сек)
./monitor.sh once              # Разовая проверка статуса

# Логи
./start_background.sh logs     # Просмотр логов (интерактивно)
tail -f logs/bot.log          # Логи бота
tail -f logs/fastapi.log      # Логи API
tail -f logs/ngrok.log        # Логи ngrok
```

## 📊 Что запускается

1. **FastAPI** (порт 8001) - веб-интерфейс
2. **ngrok** - публичный туннель
3. **Telegram Bot** - обработка сообщений
4. **Auto URL update** - синхронизация ngrok URL

## 🎯 Проверка работы

```bash
# Проверить статус
./start_background.sh status

# Проверить порты
netstat -tlnp | grep :8001

# Проверить процессы
ps aux | grep python3
```

## 🔄 Автозапуск при загрузке

```bash
# Настроить пути в файле
sudo nano telegram-assistant.service

# Установить сервис
sudo cp telegram-assistant.service /etc/systemd/system/
sudo systemctl daemon-reload
sudo systemctl enable telegram-assistant
sudo systemctl start telegram-assistant

# Проверить
sudo systemctl status telegram-assistant
```

## 🛠️ Решение проблем

```bash
# Остановить все процессы
./start_background.sh stop
pkill -f "python3.*bot"
pkill -f "uvicorn"
pkill -f "ngrok"

# Очистить PID файлы
rm -rf pids/ logs/

# Перезапустить
./start_background.sh start
```

## 📱 Результат

После запуска:
- ✅ Telegram бот отвечает на `/start`
- ✅ Веб-интерфейс доступен через ngrok URL
- ✅ Все логи сохраняются в `logs/`
- ✅ Процессы отслеживаются через PID файлы

🎉 **Готово! Telegram Assistant работает в фоне на Ubuntu.** 