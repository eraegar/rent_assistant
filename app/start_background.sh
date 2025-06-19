#!/bin/bash

# Telegram Assistant - Background Service Launcher
# For Ubuntu 22.04 production deployment

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
CYAN='\033[0;36m'
NC='\033[0m' # No Color

# Configuration
PROJECT_DIR=$(pwd)
LOG_DIR="$PROJECT_DIR/logs"
PID_DIR="$PROJECT_DIR/pids"

# Create necessary directories
mkdir -p "$LOG_DIR" "$PID_DIR"

print_header() {
    echo -e "${CYAN}"
    echo "🐧 TELEGRAM ASSISTANT - BACKGROUND MODE 🐧"
    echo "========================================="
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

# Function to check if service is running
check_service() {
    local pidfile="$1"
    local name="$2"
    
    if [ -f "$pidfile" ]; then
        local pid=$(cat "$pidfile")
        if kill -0 "$pid" 2>/dev/null; then
            print_success "$name is running (PID: $pid)"
            return 0
        else
            print_warning "$name PID file exists but process is dead"
            rm -f "$pidfile"
            return 1
        fi
    else
        print_warning "$name is not running"
        return 1
    fi
}

# Function to stop service
stop_service() {
    local pidfile="$1"
    local name="$2"
    
    if [ -f "$pidfile" ]; then
        local pid=$(cat "$pidfile")
        if kill -0 "$pid" 2>/dev/null; then
            print_step "Stopping $name (PID: $pid)..."
            kill "$pid"
            sleep 2
            if kill -0 "$pid" 2>/dev/null; then
                print_warning "Force killing $name..."
                kill -9 "$pid"
            fi
            rm -f "$pidfile"
            print_success "$name stopped"
        else
            rm -f "$pidfile"
        fi
    fi
}

# Function to start FastAPI
start_fastapi() {
    print_step "🌐 Starting FastAPI server..."
    
    cd "$PROJECT_DIR"
    nohup python3 -m uvicorn main:app --host 0.0.0.0 --port 8001 --reload \
        > "$LOG_DIR/fastapi.log" 2>&1 &
    
    echo $! > "$PID_DIR/fastapi.pid"
    local pid=$(cat "$PID_DIR/fastapi.pid")
    
    print_success "FastAPI started (PID: $pid)"
    print_warning "Log: $LOG_DIR/fastapi.log"
    
    # Wait for startup
    echo "⏳ Waiting for FastAPI startup..."
    sleep 10
    
    # Check if started successfully
    if curl -s http://localhost:8001 > /dev/null; then
        print_success "FastAPI server responding"
    else
        print_error "FastAPI server not responding"
        return 1
    fi
}

# Function to start ngrok
start_ngrok() {
    print_step "🌍 Starting ngrok tunnel..."
    
    # Check ngrok binary
    if command -v ngrok &> /dev/null; then
        ngrok_cmd="ngrok"
    elif [ -f "$PROJECT_DIR/ngrok" ]; then
        chmod +x "$PROJECT_DIR/ngrok"
        ngrok_cmd="$PROJECT_DIR/ngrok"
    else
        print_error "ngrok not found!"
        return 1
    fi
    
    cd "$PROJECT_DIR"
    nohup $ngrok_cmd http 8001 --log=stdout \
        > "$LOG_DIR/ngrok.log" 2>&1 &
    
    echo $! > "$PID_DIR/ngrok.pid"
    local pid=$(cat "$PID_DIR/ngrok.pid")
    
    print_success "ngrok started (PID: $pid)"
    print_warning "Log: $LOG_DIR/ngrok.log"
    
    # Wait for tunnel establishment
    echo "⏳ Waiting for ngrok tunnel..."
    sleep 15
}

# Function to update ngrok URL
update_ngrok_url() {
    print_step "🔄 Updating ngrok URL..."
    
    cd "$PROJECT_DIR"
    if [ -f "auto_update_ngrok_url.py" ]; then
        python3 auto_update_ngrok_url.py
        if [ $? -eq 0 ]; then
            print_success "ngrok URL updated"
        else
            print_error "Failed to update ngrok URL"
            return 1
        fi
    else
        print_warning "auto_update_ngrok_url.py not found, skipping URL update"
    fi
}

# Function to start Telegram bot
start_bot() {
    print_step "🤖 Starting Telegram bot..."
    
    cd "$PROJECT_DIR"
    if [ -f "bots/bot1_simple.py" ]; then
        nohup python3 bots/bot1_simple.py \
            > "$LOG_DIR/bot.log" 2>&1 &
        
        echo $! > "$PID_DIR/bot.pid"
        local pid=$(cat "$PID_DIR/bot.pid")
        
        print_success "Telegram bot started (PID: $pid)"
        print_warning "Log: $LOG_DIR/bot.log"
    else
        print_error "bot1_simple.py not found!"
        return 1
    fi
}

# Function to show status
show_status() {
    print_header
    echo "📊 SERVICE STATUS:"
    echo "=================="
    
    check_service "$PID_DIR/fastapi.pid" "FastAPI"
    check_service "$PID_DIR/ngrok.pid" "ngrok"
    check_service "$PID_DIR/bot.pid" "Telegram Bot"
    
    echo
    echo "📁 LOG FILES:"
    echo "============="
    echo "FastAPI: $LOG_DIR/fastapi.log"
    echo "ngrok:   $LOG_DIR/ngrok.log"
    echo "Bot:     $LOG_DIR/bot.log"
    
    echo
    echo "🔧 MANAGEMENT:"
    echo "=============="
    echo "Start:   ./start_background.sh start"
    echo "Stop:    ./start_background.sh stop"
    echo "Restart: ./start_background.sh restart"
    echo "Status:  ./start_background.sh status"
    echo "Logs:    ./start_background.sh logs"
}

# Function to stop all services
stop_all() {
    print_step "🛑 Stopping all services..."
    
    stop_service "$PID_DIR/bot.pid" "Telegram Bot"
    stop_service "$PID_DIR/ngrok.pid" "ngrok"
    stop_service "$PID_DIR/fastapi.pid" "FastAPI"
    
    print_success "All services stopped"
}

# Function to start all services
start_all() {
    print_header
    
    # Pre-checks
    if [ ! -f ".env" ]; then
        print_error ".env file not found!"
        echo "Create .env file first with BOT_TOKEN"
        exit 1
    fi
    
    if grep -q "BOT_TOKEN=YOUR_BOT_TOKEN_HERE" .env; then
        print_error "BOT_TOKEN not configured in .env!"
        exit 1
    fi
    
    # Start services
    start_fastapi || exit 1
    sleep 5
    
    start_ngrok || exit 1
    sleep 10
    
    update_ngrok_url
    sleep 5
    
    start_bot || exit 1
    
    print_success "All services started successfully!"
    echo
    show_status
}

# Function to show logs
show_logs() {
    echo "📋 SELECT LOG TO VIEW:"
    echo "====================="
    echo "1. FastAPI"
    echo "2. ngrok"
    echo "3. Telegram Bot"
    echo "4. All logs (tail -f)"
    echo
    read -p "Select (1-4): " choice
    
    case $choice in
        1) tail -f "$LOG_DIR/fastapi.log" ;;
        2) tail -f "$LOG_DIR/ngrok.log" ;;
        3) tail -f "$LOG_DIR/bot.log" ;;
        4) tail -f "$LOG_DIR"/*.log ;;
        *) echo "Invalid choice" ;;
    esac
}

# Main script logic
case "${1:-status}" in
    "start")
        start_all
        ;;
    "stop")
        stop_all
        ;;
    "restart")
        stop_all
        sleep 5
        start_all
        ;;
    "status")
        show_status
        ;;
    "logs")
        show_logs
        ;;
    *)
        echo "Usage: $0 {start|stop|restart|status|logs}"
        echo
        show_status
        ;;
esac 