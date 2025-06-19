#!/bin/bash

echo "🤖 Starting Telegram Bot..."
echo "=========================="

# Check Python
if command -v python3 &> /dev/null; then
    python_cmd="python3"
elif command -v python &> /dev/null; then
    python_cmd="python"
else
    echo "❌ Python not found!"
    exit 1
fi

# Check bot file
if [ ! -f "bots/bot1_simple.py" ]; then
    echo "❌ bots/bot1_simple.py not found!"
    exit 1
fi

# Check token
if [ -f ".env" ] && grep -q "BOT_TOKEN=" .env; then
    token=$(grep "BOT_TOKEN=" .env | cut -d '=' -f2)
    if [ "$token" == "YOUR_BOT_TOKEN_HERE" ] || [ -z "$token" ]; then
        echo "❌ Bot token not configured!"
        echo "Run: ./setup_bot_token.sh"
        exit 1
    fi
else
    echo "❌ .env file not found or token not configured!"
    echo "Run: ./setup_bot_token.sh"
    exit 1
fi

echo "✅ Bot token found: ${token:0:10}..."

# Check dependencies
if [ -f "requirements.txt" ]; then
    echo "🔄 Checking dependencies..."
    pip3 install -q -r requirements.txt
fi

echo ""
echo "🚀 Starting Telegram bot..."
echo "📱 Bot will run in foreground"
echo ""
echo "⚠️  WARNING:"
echo "   • Make sure ngrok is running and URL is updated"
echo "   • If 'Conflict' error occurs, stop other bot instances"
echo ""
echo "❌ To stop press Ctrl+C"
echo ""

cd bots
$python_cmd bot1_simple.py 