# 🚀 Telegram Assistant - Настройка с ngrok

## 📋 Быстрый старт

### 1. Подготовка ngrok

1. **Скачайте ngrok**: https://ngrok.com/download
2. **Распакуйте** в любую папку
3. **Зарегистрируйтесь** на https://ngrok.com и получите authtoken
4. **Настройте authtoken**:
   ```bash
   ngrok config add-authtoken ваш_токен
   ```

### 2. Создание Telegram бота

1. Найдите **@BotFather** в Telegram
2. Отправьте `/newbot`
3. Введите название и username бота
4. **Сохраните токен** (понадобится в шаге 4)

### 3. Запуск ngrok

Откройте командную строку и запустите:
```bash
ngrok http 8000
```

**Оставьте это окно открытым!** ngrok должен работать постоянно.

### 4. Настройка приложения

1. **Создайте файл `.env`** в папке проекта:
   ```
   BOT_TOKEN=ваш_токен_от_botfather
   WEBAPP_URL=будет_обновлен_автоматически
   SECRET_KEY=любая_длинная_строка
   ```

2. **Запустите автонастройку**:
   ```bash
   python setup_ngrok.py
   ```

### 5. Запуск всех сервисов

**Вариант A - Автоматически (Windows):**
```bash
start_telegram_app.bat
```

**Вариант B - Вручную:**

1. **Запустите FastAPI сервер**:
   ```bash
   uvicorn main:main --reload --host 0.0.0.0 --port 8000
   ```

2. **Запустите Telegram бота** (в новом терминале):
   ```bash
   python bots/bot1.py
   ```

### 6. Настройка WebApp в BotFather

1. Найдите **@BotFather** в Telegram
2. Выберите вашего бота
3. **Bot Settings** → **Menu Button** → **Configure Menu Button**
4. **Button text**: `Открыть приложение`
5. **URL**: скопируйте HTTPS URL из ngrok (например: `https://abc123.ngrok.io`)

### 7. Тестирование

1. Найдите вашего бота в Telegram
2. Отправьте `/start`
3. Нажмите кнопку **"🚀 Открыть приложение"**
4. Должно открыться ваше веб-приложение!

## 🔧 Решение проблем

### ngrok не запускается
- Проверьте, что порт 8000 свободен
- Убедитесь, что authtoken настроен правильно

### Бот не отвечает
- Проверьте токен в `.env` файле
- Убедитесь, что FastAPI сервер запущен на порту 8000

### WebApp не открывается
- Убедитесь, что URL в BotFather начинается с `https://`
- Проверьте, что ngrok туннель активен
- Перезапустите `python setup_ngrok.py`

### Ошибка "Module not found"
```bash
pip install requests python-dotenv
```

## 📱 Структура проекта

```
telegram-assistant/app/
├── bots/
│   ├── bot1.py              # Основной бот с WebApp
│   └── bot_simple.py        # Простая версия без WebApp
├── frontend/
│   ├── index.html           # Веб-интерфейс
│   ├── api.js              # API клиент
│   ├── app.js              # Логика приложения
│   └── telegram-webapp.js   # Telegram WebApp интеграция
├── main.py                  # FastAPI сервер
├── setup_ngrok.py          # Автонастройка ngrok
├── start_telegram_app.bat  # Автозапуск (Windows)
└── .env                    # Конфигурация
```

## 🌐 Альтернативы ngrok

Если ngrok не подходит, можете использовать:
- **localtunnel**: `npm install -g localtunnel && lt --port 8000`
- **serveo**: `ssh -R 80:localhost:8000 serveo.net`
- **Heroku/Railway** для постоянного размещения

## 📞 Поддержка

Если что-то не работает:
1. Проверьте все шаги еще раз
2. Убедитесь, что все сервисы запущены
3. Посмотрите логи в командной строке
4. Перезапустите все с начала 