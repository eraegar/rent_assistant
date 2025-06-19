@echo off
echo 🔄 Automatic ngrok URL update
echo =====================================

echo.
echo 📁 Navigating to application directory...
cd /d "%~dp0..\.."
echo 📍 Current directory: %CD%

echo.
echo 📡 Getting current ngrok URL...
python auto_update_ngrok_url.py

if %ERRORLEVEL% EQU 0 (
    echo.
    echo ✅ URL successfully updated in all files!
    echo 🔄 Restart bot to apply changes
) else (
    echo.
    echo ❌ URL update error
    echo 🛠️  Check that:
    echo    • ngrok is running
    echo    • Can access http://localhost:4040
    echo    • Project files are writable
)

echo.
pause 