@echo off
title Telegram Assistant - Create .env File
color 0B

echo.
echo 📝 CREATING .ENV FILE
echo ======================
echo.

REM Navigate to project root directory
cd /d "%~dp0\..\.."

if exist ".env" (
    echo ✅ .env file already exists
    echo.
    choice /C YN /M "Do you want to recreate .env file? (Y/N)"
    if errorlevel 2 goto :end
    echo 🔄 Recreating .env file...
) else (
    echo 📋 .env file not found. Creating from template...
)

if exist "env_template.txt" (
    copy "env_template.txt" ".env" > nul
    echo ✅ .env file created from template
) else (
    echo 🔄 Creating basic .env file...
    (
        echo # Telegram Bot Configuration
        echo BOT_TOKEN=YOUR_BOT_TOKEN_HERE
        echo.
        echo # Database Configuration  
        echo DATABASE_URL=sqlite:///test.db
        echo.
        echo # API Configuration
        echo API_HOST=0.0.0.0
        echo API_PORT=8001
        echo.
        echo # ngrok Configuration (will be automatically updated^)
        echo NGROK_URL=https://your-ngrok-url.ngrok.io
        echo.
        echo # Security
        echo SECRET_KEY=your-secret-key-here
        echo.
        echo # Development
        echo DEBUG=True
    ) > .env
    echo ✅ Created basic .env file
)

echo.
echo ⚠️  IMPORTANT: Edit .env file and specify:
echo    • Real BOT_TOKEN from @BotFather
echo    • Secure SECRET_KEY
echo.
echo 🛠️  To setup bot token use:
echo    scripts\windows\setup_bot_token.bat
echo.

:end
pause 