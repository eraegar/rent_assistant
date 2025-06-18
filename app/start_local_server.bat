@echo off
echo 🚀 Запуск локального FastAPI сервера на порту 8000
echo ===============================================

echo.
echo 📋 Проверка зависимостей...
python -c "import uvicorn" 2>nul
if %errorlevel% neq 0 (
    echo ❌ uvicorn не установлен. Устанавливаю зависимости...
    pip install -r requirements.txt
    if %errorlevel% neq 0 (
        echo ❌ Ошибка установки зависимостей
        pause
        exit /b 1
    )
)

echo.
echo ✅ Зависимости готовы
echo.
echo 🚀 Запуск FastAPI сервера...
echo 📍 Адрес: http://localhost:8000
echo 🔗 Swagger UI: http://localhost:8000/docs
echo.
echo ⚠️  Для остановки нажмите Ctrl+C
echo.

python -m uvicorn main:app --reload --host 0.0.0.0 --port 8000 