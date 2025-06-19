#!/bin/bash

echo "🐧 LINUX TELEGRAM ASSISTANT LAUNCHER"
echo "====================================="
echo ""
echo "📋 Available actions:"
echo "  1️⃣  Full startup (all services)"
echo "  2️⃣  Setup bot token"
echo "  3️⃣  FastAPI server only"
echo "  4️⃣  ngrok tunnel only"
echo "  5️⃣  Telegram bot only"
echo "  6️⃣  Quick URL update"
echo "  7️⃣  Create .env file"
echo "  0️⃣  Exit"
echo ""
read -p "Select action (0-7): " choice

case $choice in
    0) 
        echo "👋 Goodbye!"
        exit 0
        ;;
    1) 
        echo "1️⃣  STARTING ALL SERVICES..."
        if [ -f "scripts/linux/start_all.sh" ]; then
            ./scripts/linux/start_all.sh
        else
            echo "❌ File scripts/linux/start_all.sh not found!"
        fi
        ;;
    2) 
        echo "2️⃣  TOKEN SETUP..."
        if [ -f "scripts/linux/setup_bot_token.sh" ]; then
            ./scripts/linux/setup_bot_token.sh
        else
            echo "❌ File scripts/linux/setup_bot_token.sh not found!"
        fi
        ;;
    3) 
        echo "3️⃣  STARTING FASTAPI..."
        if [ -f "scripts/linux/start_fastapi.sh" ]; then
            ./scripts/linux/start_fastapi.sh
        else
            echo "❌ File scripts/linux/start_fastapi.sh not found!"
        fi
        ;;
    4) 
        echo "4️⃣  STARTING NGROK..."
        if [ -f "scripts/linux/start_ngrok.sh" ]; then
            ./scripts/linux/start_ngrok.sh
        else
            echo "❌ File scripts/linux/start_ngrok.sh not found!"
        fi
        ;;
    5) 
        echo "5️⃣  STARTING BOT..."
        if [ -f "scripts/linux/start_bot.sh" ]; then
            ./scripts/linux/start_bot.sh
        else
            echo "❌ File scripts/linux/start_bot.sh not found!"
        fi
        ;;
    6) 
        echo "6️⃣  QUICK URL UPDATE..."
        if [ -f "scripts/linux/quick_update_url.sh" ]; then
            ./scripts/linux/quick_update_url.sh
        else
            echo "❌ File scripts/linux/quick_update_url.sh not found!"
        fi
        ;;
    7)
        echo "7️⃣  CREATING .ENV FILE..."
        if [ -f "scripts/linux/create_env.sh" ]; then
            ./scripts/linux/create_env.sh
        else
            echo "❌ File scripts/linux/create_env.sh not found!"
            echo "Creating basic .env file..."
            if [ -f "env_template.txt" ]; then
                cp env_template.txt .env
                echo "✅ .env file created from template"
            else
                cat > .env << EOF
# Telegram Bot Configuration
BOT_TOKEN=YOUR_BOT_TOKEN_HERE

# Database Configuration  
DATABASE_URL=sqlite:///test.db

# API Configuration
API_HOST=0.0.0.0
API_PORT=8001

# ngrok Configuration (will be automatically updated)
NGROK_URL=https://your-ngrok-url.ngrok.io

# Security
SECRET_KEY=your-secret-key-here

# Development
DEBUG=True
EOF
                echo "✅ Created basic .env file"
            fi
            echo "⚠️  IMPORTANT: Edit .env file and specify:"
            echo "   • Real BOT_TOKEN from @BotFather"
            echo "   • Secure SECRET_KEY"
        fi
        ;;
    *) 
        echo "❌ Invalid choice! Please try again."
        ;;
esac

echo ""
read -p "Press Enter to exit..." 