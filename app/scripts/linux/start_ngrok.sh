#!/bin/bash

echo "🔗 Starting ngrok tunnel..."
echo "========================="

# Check ngrok
ngrok_cmd=""
if command -v ngrok &> /dev/null; then
    ngrok_cmd="ngrok"
    echo "✅ ngrok found in system"
elif [ -f "./ngrok" ]; then
    ngrok_cmd="./ngrok"
    chmod +x ./ngrok
    echo "✅ ngrok found in project folder"
else
    echo "❌ ngrok not found!"
    echo "Install ngrok:"
    echo "  sudo snap install ngrok"
    echo "  or download: https://ngrok.com/download"
    exit 1
fi

echo "🚀 Starting ngrok on port 8001..."
echo "📡 Dashboard: http://localhost:4040"
echo "🔄 After startup there will be auto URL update..."
echo ""
echo "❌ To stop press Ctrl+C"
echo ""

# Start ngrok in background for auto URL update
$ngrok_cmd http 8001 &
ngrok_pid=$!

# Wait for ngrok startup
echo "⏳ Waiting for ngrok startup (15 sec)..."
sleep 15

# Auto URL update
if [ -f "auto_update_ngrok_url.py" ]; then
    echo "🔄 Auto updating ngrok URL..."
    
    if command -v python3 &> /dev/null; then
        python3 auto_update_ngrok_url.py
    elif command -v python &> /dev/null; then
        python auto_update_ngrok_url.py
    else
        echo "⚠️  Python not found, skipping auto update"
    fi
fi

echo ""
echo "✅ ngrok started! PID: $ngrok_pid"
echo "🌐 Check new URL at: http://localhost:4040"

# Return ngrok control to main thread
wait $ngrok_pid 