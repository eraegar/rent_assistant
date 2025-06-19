@echo off
title Telegram Assistant - Windows Launcher
color 0A

echo.
echo 🪟 WINDOWS TELEGRAM ASSISTANT LAUNCHER
echo =====================================
echo.
echo 📋 Available actions:
echo   1️⃣  Full startup (all services)
echo   2️⃣  Setup bot token
echo   3️⃣  FastAPI server only
echo   4️⃣  ngrok tunnel only  
echo   5️⃣  Telegram bot only
echo   6️⃣  Quick URL update
echo   7️⃣  Create .env file
echo   0️⃣  Exit
echo.
set /p choice="Select action (0-7): "

if "%choice%"=="0" goto :exit
if "%choice%"=="1" goto :start_all
if "%choice%"=="2" goto :setup_token
if "%choice%"=="3" goto :start_fastapi
if "%choice%"=="4" goto :start_ngrok
if "%choice%"=="5" goto :start_bot
if "%choice%"=="6" goto :quick_update
if "%choice%"=="7" goto :create_env

echo ❌ Invalid choice! Please try again.
pause
exit /b 1

:start_all
echo.
echo 1️⃣  STARTING ALL SERVICES...
cd /d "%~dp0"
if exist "scripts\windows\start_all.bat" (
    call "scripts\windows\start_all.bat"
) else (
    echo ❌ File scripts\windows\start_all.bat not found!
    pause
)
goto :exit

:setup_token
echo.
echo 2️⃣  TOKEN SETUP...
cd /d "%~dp0"
if exist "scripts\windows\setup_bot_token.bat" (
    call "scripts\windows\setup_bot_token.bat"
) else (
    echo ❌ File scripts\windows\setup_bot_token.bat not found!
    pause
)
goto :exit

:start_fastapi
echo.
echo 3️⃣  STARTING FASTAPI...
cd /d "%~dp0"
if exist "scripts\windows\start_fastapi.bat" (
    call "scripts\windows\start_fastapi.bat"
) else (
    echo ❌ File scripts\windows\start_fastapi.bat not found!
    pause
)
goto :exit

:start_ngrok
echo.
echo 4️⃣  STARTING NGROK...
cd /d "%~dp0"
if exist "scripts\windows\start_ngrok.bat" (
    call "scripts\windows\start_ngrok.bat"
) else (
    echo ❌ File scripts\windows\start_ngrok.bat not found!
    pause
)
goto :exit

:start_bot
echo.
echo 5️⃣  STARTING BOT...
cd /d "%~dp0"
if exist "scripts\windows\start_bot.bat" (
    call "scripts\windows\start_bot.bat"
) else (
    echo ❌ File scripts\windows\start_bot.bat not found!
    pause
)
goto :exit

:quick_update
echo.
echo 6️⃣  QUICK URL UPDATE...
cd /d "%~dp0"
if exist "scripts\windows\quick_update_url.bat" (
    call "scripts\windows\quick_update_url.bat"
) else (
    echo ❌ File scripts\windows\quick_update_url.bat not found!
    pause
)
goto :exit

:create_env
echo.
echo 7️⃣  CREATING .ENV FILE...
cd /d "%~dp0"
if exist "scripts\windows\create_env.bat" (
    call "scripts\windows\create_env.bat"
) else (
    echo ❌ File scripts\windows\create_env.bat not found!
    pause
)
goto :exit

:exit
echo.
echo �� Goodbye!
exit /b 0 