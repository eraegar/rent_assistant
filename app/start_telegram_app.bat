@echo off
echo 🚀 Запуск Telegram Assistant для аренды помощников
echo ================================================

echo.
echo 📋 Шаг 1: Проверка ngrok...
python setup_ngrok.py

if %errorlevel% neq 0 (
    echo ❌ Ошибка настройки ngrok
    pause
    exit /b 1
)

echo.
echo 📋 Шаг 2: Запуск FastAPI сервера...
start "FastAPI Server" cmd /k "uvicorn main:app --reload --host 0.0.0.0 --port 8000"

echo.
echo ⏳ Ждем запуска сервера...
timeout /t 3 /nobreak >nul

echo.
echo 📋 Шаг 3: Запуск Telegram бота...
start "Telegram Bot" cmd /k "python bots/bot1.py"

echo.
echo ✅ Все сервисы запущены!
echo.
echo 📱 Инструкции:
echo 1. Откройте @BotFather в Telegram
echo 2. Выберите вашего бота
echo 3. Bot Settings → Menu Button → Configure Menu Button
echo 4. Скопируйте URL из setup_ngrok.py
echo 5. Протестируйте бота командой /start
echo.
pause 