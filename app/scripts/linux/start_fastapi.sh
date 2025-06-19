#!/bin/bash

echo "🌐 Starting FastAPI Server..."
echo "============================"

# Check Python
if command -v python3 &> /dev/null; then
    python_cmd="python3"
elif command -v python &> /dev/null; then
    python_cmd="python"
else
    echo "❌ Python not found!"
    exit 1
fi

# Check main.py
if [ ! -f "main.py" ]; then
    echo "❌ main.py not found!"
    exit 1
fi

# Check dependencies
if [ -f "requirements.txt" ]; then
    echo "🔄 Checking dependencies..."
    pip3 install -q -r requirements.txt
fi

echo "🚀 Starting FastAPI on port 8001..."
echo "📡 Server will be available at: http://localhost:8001"
echo "⚡ Auto-reload enabled"
echo ""
echo "❌ To stop press Ctrl+C"
echo ""

$python_cmd -m uvicorn main:app --host 0.0.0.0 --port 8001 --reload 