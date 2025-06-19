@echo off
echo 🤖 Starting Telegram Bot
echo ========================

echo.
echo 📁 Navigating to application directory...
cd /d "%~dp0..\.."
echo 📍 Current directory: %CD%

echo.
echo 📋 Checking dependencies...
python -c "import telegram" 2>nul
if %errorlevel% neq 0 (
    echo ❌ python-telegram-bot not installed. Installing dependencies...
    pip install -r requirements.txt
    if %errorlevel% neq 0 (
        echo ❌ Error installing dependencies
        pause
        exit /b 1
    )
)

echo ✅ Dependencies ready

echo.
echo 📋 Checking configuration...
if not exist ".env" (
    echo ❌ .env file not found
    echo 📝 Run update_url.bat to create configuration
    pause
    exit /b 1
)

REM Check bot token
findstr /C:"BOT_TOKEN=YOUR_BOT_TOKEN_HERE" .env >nul
if %errorlevel% equ 0 (
    echo ❌ Bot token not configured
    echo 📝 Edit .env file and specify real bot token
    pause
    exit /b 1
)

echo ✅ Configuration ready

echo.
echo 🚀 Starting Telegram bot...
echo.
echo ⚠️  Make sure that:
echo    • FastAPI server is running (start_fastapi.bat)
echo    • ngrok is working (start_ngrok.bat)  
echo    • URL is updated (update_url.bat)
echo.
echo 🛑 To stop press Ctrl+C
echo.

python bots/bot1_simple.py

pause 