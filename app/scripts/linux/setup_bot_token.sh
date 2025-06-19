#!/bin/bash

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
CYAN='\033[0;36m'
NC='\033[0m' # No Color

print_header() {
    echo -e "${CYAN}"
    echo "🤖 TELEGRAM BOT TOKEN SETUP 🤖"
    echo "=============================="
    echo -e "${NC}"
}

print_success() {
    echo -e "${GREEN}✅ $1${NC}"
}

print_warning() {
    echo -e "${YELLOW}⚠️  $1${NC}"
}

print_error() {
    echo -e "${RED}❌ $1${NC}"
}

print_info() {
    echo -e "${BLUE}ℹ️  $1${NC}"
}

main() {
    clear
    print_header
    
    echo "📱 This script will help you configure your Telegram bot token"
    echo
    print_info "If you don't have a bot yet, follow these steps:"
    echo "  1. Find @BotFather in Telegram"
    echo "  2. Send /newbot command"
    echo "  3. Follow instructions and get your token"
    echo "  4. Token looks like: 1234567890:ABCdef-GHI_jklmnop..."
    echo
    
    # Check existing token
    if [ -f ".env" ] && grep -q "BOT_TOKEN=" .env; then
        current_token=$(grep "BOT_TOKEN=" .env | cut -d '=' -f2)
        if [ "$current_token" != "YOUR_BOT_TOKEN_HERE" ] && [ -n "$current_token" ]; then
            echo -e "${YELLOW}🔍 Found existing token:${NC}"
            echo "   BOT_TOKEN=${current_token:0:10}..."
            echo
            read -p "Do you want to replace existing token? (y/N): " replace_choice
            if [[ ! $replace_choice =~ ^[Yy]$ ]]; then
                print_info "Token setup cancelled"
                exit 0
            fi
        fi
    fi
    
    # Input new token
    echo -e "${CYAN}🔑 Enter your bot token:${NC}"
    read -s bot_token
    echo
    
    # Check token format
    if [[ ! $bot_token =~ ^[0-9]+:[A-Za-z0-9_-]+$ ]]; then
        print_error "Invalid token format!"
        echo "Token should have format: 1234567890:ABCdef-GHI_jklmnop..."
        exit 1
    fi
    
    # Create/update root .env file
    echo "📄 Updating root .env file..."
    
    # Create basic .env if it doesn't exist
    if [ ! -f ".env" ]; then
        cat > .env << EOF
# Telegram Bot Configuration
BOT_TOKEN=$bot_token

# Web Application URL (will be automatically updated by ngrok)
WEBAPP_URL=https://example.ngrok-free.app

# FastAPI Configuration
SECRET_KEY=your-secret-key-here
DATABASE_URL=sqlite:///./test.db

# Server Configuration
HOST=0.0.0.0
PORT=8001
EOF
    else
        # Update existing file
        if grep -q "BOT_TOKEN=" .env; then
            sed -i "s/BOT_TOKEN=.*/BOT_TOKEN=$bot_token/" .env
        else
            echo "BOT_TOKEN=$bot_token" >> .env
        fi
    fi
    
    print_success "Root .env file updated"
    
    # Create bots directory if it doesn't exist
    if [ ! -d "bots" ]; then
        mkdir -p bots
        print_success "Created bots/ directory"
    fi
    
    # Create/update bots/.env file
    echo "📄 Updating bots/.env file..."
    
    if [ ! -f "bots/.env" ]; then
        cat > bots/.env << EOF
# Telegram Bot Configuration for bots directory
BOT_TOKEN=$bot_token

# Web Application URL (will be automatically updated by ngrok)
WEBAPP_URL=https://example.ngrok-free.app
EOF
    else
        # Update existing file
        if grep -q "BOT_TOKEN=" bots/.env; then
            sed -i "s/BOT_TOKEN=.*/BOT_TOKEN=$bot_token/" bots/.env
        else
            echo "BOT_TOKEN=$bot_token" >> bots/.env
        fi
        
        if ! grep -q "WEBAPP_URL=" bots/.env; then
            echo "WEBAPP_URL=https://example.ngrok-free.app" >> bots/.env
        fi
    fi
    
    print_success "bots/.env file updated"
    
    # Check if Python is available
    if command -v python3 &> /dev/null; then
        python_cmd="python3"
    elif command -v python &> /dev/null; then
        python_cmd="python"
    else
        print_warning "Python not found, skipping token test"
        python_cmd=""
    fi
    
    # Test token
    if [ -n "$python_cmd" ]; then
        echo "🧪 Testing token..."
        
        test_result=$($python_cmd -c "
import requests
import sys
try:
    response = requests.get('https://api.telegram.org/bot$bot_token/getMe', timeout=10)
    if response.status_code == 200:
        data = response.json()
        if data['ok']:
            bot_info = data['result']
            print(f'SUCCESS:{bot_info[\"first_name\"]}:{bot_info[\"username\"]}')
        else:
            print('ERROR:Invalid token')
    else:
        print('ERROR:HTTP error')
except Exception as e:
    print(f'ERROR:{str(e)}')
" 2>/dev/null)
        
        if [[ $test_result == SUCCESS:* ]]; then
            bot_name=$(echo $test_result | cut -d':' -f2)
            bot_username=$(echo $test_result | cut -d':' -f3)
            print_success "Token is valid!"
            echo "   🤖 Bot name: $bot_name"
            echo "   📍 Username: @$bot_username"
        else
            print_error "Error checking token!"
            echo "   Possible causes:"
            echo "   • Invalid token"
            echo "   • No internet connection"
            echo "   • Telegram API issues"
            
            read -p "Continue despite error? (y/N): " continue_choice
            if [[ ! $continue_choice =~ ^[Yy]$ ]]; then
                print_error "Setup cancelled"
                exit 1
            fi
        fi
    fi
    
    echo
    print_success "✅ SETUP COMPLETED!"
    echo "========================"
    echo "📁 Updated files:"
    echo "   • .env (root)"
    echo "   • bots/.env"
    echo
    echo "🚀 Now you can start the project:"
    echo "   ./start_all.sh"
    echo
    echo "🔧 Additional commands:"
    echo "   ./start_fastapi.sh  - Start FastAPI only"
    echo "   ./start_ngrok.sh    - Start ngrok only"
    echo "   ./start_bot.sh      - Start bot only"
    echo
    echo "📱 Your bot commands:"
    if [[ $test_result == SUCCESS:* ]]; then
        bot_username=$(echo $test_result | cut -d':' -f3)
        echo "   Send /start to @$bot_username"
    else
        echo "   Send /start to your bot"
    fi
    echo
    echo "🛠️  If you need to change token later:"
    echo "   Run this script again: ./setup_bot_token.sh"
    echo
}

# Check if running directly
if [[ "${BASH_SOURCE[0]}" == "${0}" ]]; then
    main "$@"
fi 