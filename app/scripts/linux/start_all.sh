#!/bin/bash

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
PURPLE='\033[0;35m'
CYAN='\033[0;36m'
NC='\033[0m' # No Color

# Function for beautiful output
print_header() {
    echo -e "${CYAN}"
    echo "🚀 TELEGRAM ASSISTANT - FULL STARTUP 🚀"
    echo "========================================"
    echo -e "${NC}"
}

print_step() {
    echo -e "${BLUE}$1${NC}"
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

# Function to check command
check_command() {
    if command -v "$1" &> /dev/null; then
        return 0
    else
        return 1
    fi
}

# Function to check file
check_file() {
    if [ -f "$1" ]; then
        return 0
    else
        return 1
    fi
}

# Function to check port
check_port() {
    if lsof -Pi :$1 -sTCP:LISTEN -t >/dev/null ; then
        return 0
    else
        return 1
    fi
}

# Main function
main() {
    clear
    print_header
    
    echo "📋 Startup stages:"
    echo "  1️⃣  System check"
    echo "  2️⃣  FastAPI server"
    echo "  3️⃣  ngrok tunnel"
    echo "  4️⃣  Auto URL update"
    echo "  5️⃣  Telegram bot"
    echo
    
    print_warning "WARNING: Make sure BOT_TOKEN is set in .env file"
    echo
    
    read -p "Press Enter to continue or Ctrl+C to cancel..."
    
    # 1. System check
    print_step "1️⃣  SYSTEM CHECK..."
    echo "============================"
    
    # Check Python
    if check_command python3; then
        python_version=$(python3 --version 2>&1)
        print_success "Python found: $python_version"
    elif check_command python; then
        python_version=$(python --version 2>&1)
        print_success "Python found: $python_version"
        alias python3=python
    else
        print_error "Python not found! Install Python 3.8+"
        exit 1
    fi
    
    # Check pip
    if check_command pip3; then
        print_success "pip3 found"
    elif check_command pip; then
        print_success "pip found"
        alias pip3=pip
    else
        print_error "pip not found! Install pip"
        exit 1
    fi
    
    # Check dependencies
    if check_file "requirements.txt"; then
        print_success "requirements.txt found"
        echo "🔄 Checking dependencies..."
        pip3 install -q -r requirements.txt
        print_success "Dependencies installed"
    else
        print_warning "requirements.txt not found, skipping dependency installation"
    fi
    
    # Check ngrok
    ngrok_found=false
    if check_command ngrok; then
        print_success "ngrok found in system"
        ngrok_cmd="ngrok"
        ngrok_found=true
    elif check_file "./ngrok"; then
        print_success "ngrok found in project folder"
        chmod +x ./ngrok
        ngrok_cmd="./ngrok"
        ngrok_found=true
    else
        print_error "ngrok not found!"
        echo "Install ngrok:"
        echo "  sudo snap install ngrok"
        echo "  or download to project folder: https://ngrok.com/download"
        exit 1
    fi
    
    # Check bot token
    if check_file ".env"; then
        if grep -q "BOT_TOKEN=YOUR_BOT_TOKEN_HERE" .env || ! grep -q "BOT_TOKEN=" .env; then
            print_error "Bot token not configured!"
            echo "Run: ./setup_bot_token.sh"
            exit 1
        else
            print_success "Bot token configured"
        fi
    else
        print_error ".env file not found!"
        echo "Run: ./setup_bot_token.sh"
        exit 1
    fi
    
    # Check ports
    if check_port 8001; then
        print_error "Port 8001 already in use!"
        echo "Kill process: lsof -ti:8001 | xargs kill -9"
        exit 1
    else
        print_success "Port 8001 is free"
    fi
    
    echo
    sleep 2
    
    # 2. Start FastAPI server
    print_step "2️⃣  STARTING FASTAPI SERVER..."
    echo "============================"
    
    if check_file "main.py"; then
        echo "🚀 Starting FastAPI server on port 8001..."
        gnome-terminal --title="FastAPI Server" -- bash -c "
            echo '🌐 FastAPI server starting...';
            python3 -m uvicorn main:app --host 0.0.0.0 --port 8001 --reload;
            read -p 'Press Enter to close...'
        " 2>/dev/null || \
        xterm -title "FastAPI Server" -e "
            echo '🌐 FastAPI server starting...';
            python3 -m uvicorn main:app --host 0.0.0.0 --port 8001 --reload;
            read -p 'Press Enter to close...'
        " 2>/dev/null || \
        {
            echo "🔄 Starting in background (terminal not found)..."
            nohup python3 -m uvicorn main:app --host 0.0.0.0 --port 8001 --reload > fastapi.log 2>&1 &
            fastapi_pid=$!
            echo "FastAPI PID: $fastapi_pid"
        }
        
        print_success "FastAPI server started"
    else
        print_error "main.py not found!"
        exit 1
    fi
    
    echo "⏳ Waiting for FastAPI startup (10 sec)..."
    sleep 10
    
    # Check that FastAPI started
    if curl -s http://localhost:8001 > /dev/null; then
        print_success "FastAPI server responding"
    else
        print_warning "FastAPI server not responding, continuing..."
    fi
    
    echo
    sleep 2
    
    # 3. Start ngrok tunnel
    print_step "3️⃣  STARTING NGROK TUNNEL..."
    echo "============================"
    
    echo "🔗 Starting ngrok on port 8001..."
    gnome-terminal --title="ngrok tunnel" -- bash -c "
        echo '🔗 ngrok tunnel starting...';
        $ngrok_cmd http 8001;
        read -p 'Press Enter to close...'
    " 2>/dev/null || \
    xterm -title "ngrok tunnel" -e "
        echo '🔗 ngrok tunnel starting...';
        $ngrok_cmd http 8001;
        read -p 'Press Enter to close...'
    " 2>/dev/null || \
    {
        echo "🔄 Starting in background (terminal not found)..."
        nohup $ngrok_cmd http 8001 > ngrok.log 2>&1 &
        ngrok_pid=$!
        echo "ngrok PID: $ngrok_pid"
    }
    
    print_success "ngrok tunnel started"
    
    echo "⏳ Waiting for ngrok startup (15 sec)..."
    sleep 15
    
    # 4. Auto URL update
    print_step "4️⃣  AUTO URL UPDATE..."
    echo "========================"
    
    if check_file "auto_update_ngrok_url.py"; then
        echo "🔄 Automatic URL update..."
        python3 auto_update_ngrok_url.py
        
        if [ $? -eq 0 ]; then
            print_success "URL successfully updated in all files"
        else
            print_error "URL update error!"
            echo "🛠️  Try running scripts/linux/quick_update_url.sh manually"
            read -p "Continue anyway? (y/N): " continue_anyway
            if [[ ! $continue_anyway =~ ^[Yy]$ ]]; then
                exit 1
            fi
        fi
    else
        print_error "auto_update_ngrok_url.py not found!"
        exit 1
    fi
    
    echo
    sleep 2
    
    # 5. Start Telegram bot
    print_step "5️⃣  STARTING TELEGRAM BOT..."
    echo "============================"
    print_warning "Make sure BOT_TOKEN is configured in .env file!"
    read -p "Press Enter to continue..."
    
        if check_file "bots/bot1_simple.py"; then
        echo "🤖 Starting Telegram bot..."
            gnome-terminal --title="Telegram Bot" -- bash -c "
            echo '🤖 Telegram bot starting...';
            python3 bots/bot1_simple.py;
            read -p 'Press Enter to close...'
            " 2>/dev/null || \
            xterm -title "Telegram Bot" -e "
            echo '🤖 Telegram bot starting...';
            python3 bots/bot1_simple.py;
            read -p 'Press Enter to close...'
            " 2>/dev/null || \
            {
            echo "🔄 Starting in background (terminal not found)..."
            nohup python3 bots/bot1_simple.py > bot.log 2>&1 &
                bot_pid=$!
                echo "Bot PID: $bot_pid"
            }
            
        print_success "Telegram bot started"
    else
        print_error "bots/bot1_simple.py not found!"
        exit 1
    fi
    
    echo
    sleep 2
    
    # Final summary
    echo
    print_header
    print_success "ALL SERVICES STARTED!"
    echo "========================"
    echo "🌐 FastAPI: http://localhost:8001"
    echo "🔗 ngrok: check ngrok window"
    echo "🤖 Telegram Bot: running"
    echo
    echo "📊 For monitoring use:"
    echo "  ps aux | grep python"
    echo "  ps aux | grep ngrok"
    echo
    echo "🛑 To stop services:"
    echo "  pkill -f uvicorn"
    echo "  pkill -f ngrok"
    echo "  pkill -f bot1_simple"
    echo
    
    # Show process info if available
    if [[ -n $fastapi_pid ]]; then
        echo "FastAPI PID: $fastapi_pid"
    fi
    if [[ -n $ngrok_pid ]]; then
        echo "ngrok PID: $ngrok_pid"
    fi
    if [[ -n $bot_pid ]]; then
        echo "Bot PID: $bot_pid"
    fi
    
    echo
    read -p "Press Enter to exit..."
}

# Run main function
    main "$@"