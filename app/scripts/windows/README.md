# 🪟 Windows Batch Scripts

Эта папка содержит `.bat` скрипты для управления **Telegram Assistant** в Windows.

## 🚀 Быстрый старт

```cmd
# Из корневой папки проекта (telegram-assistant\app\)

# 1. Настройка токена (только первый раз)
scripts\windows\setup_bot_token.bat

# 2. Запуск всех сервисов
scripts\windows\start_all.bat
```

## 📋 Все скрипты

### 🔧 Основные команды

#### `start_all.bat` - Полный автозапуск
```cmd
scripts\windows\start_all.bat
```
**Что делает:**
- ✅ Проверяет все зависимости (Python, ngrok, токен)
- 🌐 Запускает FastAPI сервер (порт 8001)
- 🔗 Запускает ngrok туннель
- 🔄 Автоматически обновляет URL во всех файлах
- 🤖 Запускает Telegram бота

#### `setup_bot_token.bat` - Настройка токена
```cmd
scripts\windows\setup_bot_token.bat
```
**Что делает:**
- 🔑 Запрашивает токен от @BotFather
- ✅ Проверяет валидность токена
- 📄 Обновляет .env файлы (корневой и bots/.env)
- 🧪 Тестирует подключение к Telegram API

### 🎯 Отдельные компоненты

#### `start_fastapi.bat` - Только веб-сервер
```cmd
scripts\windows\start_fastapi.bat
```
- Запускает FastAPI на http://localhost:8001
- Включена автоперезагрузка при изменениях

#### `start_ngrok.bat` - Только туннель
```cmd
scripts\windows\start_ngrok.bat
```
- Создает публичный HTTPS туннель
- Автоматически обновляет URL в файлах
- Панель управления: http://localhost:4040

#### `start_bot.bat` - Только бот
```cmd
scripts\windows\start_bot.bat
```
- Запускает Telegram бота
- Проверяет наличие токена

### ⚡ Утилиты

#### `quick_update_url.bat` - Быстрое обновление URL
```cmd
scripts\windows\quick_update_url.bat
```
- Получает текущий ngrok URL
- Обновляет все конфигурационные файлы
- Не перезапускает сервисы

#### `update_url.bat` - Полное обновление URL (старая версия)
```cmd
scripts\windows\update_url.bat
```
- Использует auto_update_ngrok_url.py

#### `reset_bot.bat` - Сброс состояния бота
```cmd
scripts\windows\reset_bot.bat
```
- Завершает все процессы Python
- Сбрасывает webhook'и бота

## 🎨 Особенности Windows скриптов

### ✨ Цветной вывод
Скрипты используют PowerShell для красивого цветного вывода:
- 🟢 Зеленый - успешные операции
- 🔴 Красный - ошибки
- 🟡 Желтый - предупреждения
- 🔵 Синий - информация

### 🪟 Автоматические окна
- Каждый сервис запускается в отдельном окне
- Заголовки окон указывают на тип сервиса
- Легко отслеживать статус каждого компонента

### 🔧 Проверки зависимостей
- Автоматическая проверка Python, pip, ngrok
- Проверка портов на занятость
- Валидация токена бота

## 📁 Структура файлов проекта

После запуска скриптов:
```
telegram-assistant\app\
├── .env                          # Основная конфигурация
├── bots\
│   ├── .env                      # Конфигурация бота
│   └── bot1_simple.py           # Код бота
├── scripts\
│   └── windows\                 # Эта папка
│       ├── start_all.bat        # Главный скрипт
│       ├── setup_bot_token.bat  # Настройка токена
│       └── ...                  # Остальные скрипты
├── ngrok.exe                    # ngrok для Windows
├── main.py                      # FastAPI приложение
└── auto_update_ngrok_url.py    # Автообновление URL
```

## 🛠️ Требования

### Системные требования
- **Windows 10/11**
- **PowerShell 5.0+** (встроен в Windows)
- **Python 3.8+**
- **pip** (обычно идет с Python)

### Необходимые файлы
- `ngrok.exe` в корне проекта
- `requirements.txt` с зависимостями Python
- Токен от @BotFather

### Python пакеты
```txt
fastapi
uvicorn
python-telegram-bot
python-dotenv
requests
```

## 🚨 Устранение неполадок

### "Python не найден"
```cmd
# Установите Python с официального сайта
# https://python.org/downloads/
# Убедитесь что отмечена опция "Add to PATH"
```

### "ngrok.exe не найден"
```cmd
# Скачайте ngrok.exe с сайта https://ngrok.com/download
# Поместите файл в папку telegram-assistant\app\
```

### "Токен не настроен"
```cmd
# Запустите настройку токена
scripts\windows\setup_bot_token.bat
```

### "Порт 8001 уже занят"
```cmd
# Найдите процесс
netstat -ano | findstr :8001

# Завершите процесс (замените PID на реальный)
taskkill /PID 1234 /F
```

### "Conflict: terminated by other getUpdates request"
```cmd
# Завершите все процессы Python
taskkill /f /im python.exe

# Запустите сброс бота
scripts\windows\reset_bot.bat
```

## 📖 Пример полного запуска

1. **Первоначальная настройка:**
   ```cmd
   cd telegram-assistant\app
   scripts\windows\setup_bot_token.bat
   ```

2. **Запуск всех сервисов:**
   ```cmd
   scripts\windows\start_all.bat
   ```

3. **Проверка работы:**
   - FastAPI: http://localhost:8001
   - ngrok панель: http://localhost:4040
   - Telegram: найдите своего бота и отправьте /start

4. **Остановка (в каждом окне сервиса):**
   ```
   Ctrl+C
   ```

## 💡 Советы

- **Всегда запускайте из корня проекта** (`telegram-assistant\app\`)
- **Используйте `start_all.bat` для полного запуска** - это самый простой способ
- **Оставляйте окна сервисов открытыми** для мониторинга логов
- **При изменении кода** FastAPI автоматически перезагрузится
- **Новый ngrok URL** каждый раз при перезапуске - это нормально

---

**🔗 Полная документация:** [README_START_ALL.md](../../README_START_ALL.md) 