@echo off
echo 🌐 Starting FastAPI Server
echo =========================

echo.
echo 📁 Navigating to application directory...
cd /d "%~dp0..\.."
echo 📍 Current directory: %CD%

echo.
echo 📋 Checking dependencies...
python -c "import uvicorn" 2>nul
if %errorlevel% neq 0 (
    echo ❌ uvicorn not installed. Installing dependencies...
    pip install -r requirements.txt
    if %errorlevel% neq 0 (
        echo ❌ Error installing dependencies
        pause
        exit /b 1
    )
)

echo ✅ Dependencies ready

echo.
echo 🚀 Starting FastAPI server on port 8001...
echo 📍 Address: http://localhost:8001
echo 🔗 API documentation: http://localhost:8001/docs
echo.
echo ⚠️  To stop press Ctrl+C
echo ⚠️  After startup open start_ngrok.bat in another window
echo.

python -m uvicorn main:app --reload --host 0.0.0.0 --port 8001

pause 