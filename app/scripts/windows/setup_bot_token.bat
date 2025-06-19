@echo off
echo 🤖 Telegram Bot Token Setup
echo ===============================

echo.
echo 📋 This script will help configure token for your Telegram bot
echo.

echo 🔑 To get token:
echo   1. Find @BotFather in Telegram
echo   2. Send /newbot command (new bot) or /mybots (existing)
echo   3. Copy token like: 1234567890:ABCdef-GHI_jklmnop...
echo.

set /p BOT_TOKEN="📝 Enter bot token: "

if "%BOT_TOKEN%"=="" (
    echo ❌ Token not entered
    pause
    exit /b 1
)

echo.
echo 🔄 Creating configuration files...

REM Create bots directory if it doesn't exist
if not exist "bots" mkdir bots

REM Create bots/.env
echo BOT_TOKEN=%BOT_TOKEN% > bots\.env
echo WEBAPP_URL=https://dc91-194-164-216-167.ngrok-free.app >> bots\.env

echo ✅ Created bots\.env file

REM Update root .env
if exist ".env" (
    echo 🔄 Updating root .env...
    powershell -Command "(Get-Content '.env') -replace 'BOT_TOKEN=.*', 'BOT_TOKEN=%BOT_TOKEN%' | Set-Content '.env'"
    echo ✅ Updated root .env
) else (
    echo 🔄 Creating root .env...
    echo BOT_TOKEN=%BOT_TOKEN% > .env
    echo WEBAPP_URL=https://dc91-194-164-216-167.ngrok-free.app >> .env
    echo SECRET_KEY=your-super-secret-key >> .env
    echo ✅ Created root .env
)

echo.
echo ✅ Setup completed!
echo.
echo 📋 Created files:
echo   • bots\.env - bot configuration
echo   • .env - general project configuration
echo.
echo 🚀 Now you can start bot via start_bot.bat
echo.

pause 