@echo off
echo 🚀 Starting ngrok for Telegram Assistant
echo =====================================

echo.
echo 📁 Navigating to application directory...
cd /d "%~dp0..\.."
echo 📍 Current directory: %CD%

echo.
echo 📋 Checking ngrok...
if not exist "ngrok.exe" (
    echo ❌ ngrok.exe not found in current folder
    echo 📥 Download ngrok.exe and place it in project folder
    pause
    exit /b 1
)

echo ✅ ngrok.exe found

echo.
echo 🔗 Starting ngrok on port 8001...
echo 📍 Your FastAPI should be running on http://localhost:8001
echo.
echo 🤖 URL will be automatically updated in all files!
echo.

start "ngrok tunnel" .\ngrok.exe http 8001

echo ⏳ Waiting for ngrok startup...
timeout /t 10 /nobreak > nul

echo 🔄 Automatic URL update...
python auto_update_ngrok_url.py

echo.
echo ✅ Done! ngrok started and URL updated in all files
echo 🌐 Check logs above for new URL
echo.

pause 