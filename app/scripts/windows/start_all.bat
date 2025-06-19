@echo off
title Telegram Assistant - Full Startup
color 0A

REM Navigate to project root directory
cd /d "%~dp0\..\.."

echo.
echo 🚀 TELEGRAM ASSISTANT - FULL STARTUP 🚀
echo ========================================
echo.

echo 📋 Startup stages:
echo   1️⃣  FastAPI server
echo   2️⃣  ngrok tunnel  
echo   3️⃣  Auto URL update
echo   4️⃣  Telegram bot
echo.

echo ⚠️  WARNING: Make sure BOT_TOKEN is set in .env file
echo.

pause

echo.
echo 1️⃣  STARTING FASTAPI SERVER...
echo ============================
start "FastAPI Server" cmd /c "call scripts\windows\start_fastapi.bat"

echo ⏳ Waiting for FastAPI startup (10 sec)...
timeout /t 10 /nobreak > nul

echo.
echo 2️⃣  STARTING NGROK TUNNEL...
echo ==========================
if exist "ngrok.exe" (
    start "ngrok tunnel" ngrok.exe http 8001
) else (
    echo ❌ ngrok.exe not found!
    echo 🛠️  Make sure ngrok.exe is in project root
    pause
    exit /b 1
)

echo ⏳ Waiting for ngrok startup (15 sec)...
timeout /t 15 /nobreak > nul

echo.
echo 3️⃣  AUTO URL UPDATE...
echo ========================
if exist "auto_update_ngrok_url.py" (
    python auto_update_ngrok_url.py
    if %ERRORLEVEL% NEQ 0 (
        echo ❌ URL update error!
        echo 🛠️  Try running scripts\windows\update_url.bat manually
        pause
        exit /b 1
    )
) else (
    echo ❌ auto_update_ngrok_url.py not found!
    pause
    exit /b 1
)

echo.
echo 4️⃣  STARTING TELEGRAM BOT...
echo ==========================
echo ⚠️  Make sure BOT_TOKEN is configured in .env file!
pause

start "Telegram Bot" cmd /c "call scripts\windows\start_bot.bat"

echo.
echo ✅ ALL SERVICES STARTED!
echo ========================
echo 🌐 FastAPI: http://localhost:8001
echo 🔗 ngrok: check ngrok window
echo 🤖 Telegram Bot: running
echo.
echo 📊 For monitoring open Task Manager
echo 🛑 To stop - close corresponding windows
echo.

pause 