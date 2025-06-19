#!/bin/bash

# Telegram Assistant - Real-time Monitor
# For Ubuntu 22.04

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
CYAN='\033[0;36m'
NC='\033[0m'

PROJECT_DIR=$(pwd)
LOG_DIR="$PROJECT_DIR/logs"
PID_DIR="$PROJECT_DIR/pids"

print_header() {
    clear
    echo -e "${CYAN}"
    echo "📊 TELEGRAM ASSISTANT - LIVE MONITOR"
    echo "====================================="
    echo -e "${NC}"
    echo "📅 $(date)"
    echo "🖥️  $(hostname)"
    echo
}

get_service_status() {
    local pidfile="$1"
    local name="$2"
    
    if [ -f "$pidfile" ]; then
        local pid=$(cat "$pidfile")
        if kill -0 "$pid" 2>/dev/null; then
            # Get CPU and memory usage
            local cpu=$(ps -p "$pid" -o %cpu --no-headers 2>/dev/null | tr -d ' ')
            local mem=$(ps -p "$pid" -o %mem --no-headers 2>/dev/null | tr -d ' ')
            local rss=$(ps -p "$pid" -o rss --no-headers 2>/dev/null | tr -d ' ')
            
            if [ -n "$cpu" ]; then
                echo -e "${GREEN}🟢 $name${NC} (PID: $pid) CPU: ${cpu}% MEM: ${mem}% (${rss}KB)"
            else
                echo -e "${RED}🔴 $name${NC} (PID: $pid) - Process info unavailable"
            fi
        else
            echo -e "${RED}🔴 $name${NC} - Dead process (PID file exists)"
        fi
    else
        echo -e "${YELLOW}⭕ $name${NC} - Not running"
    fi
}

show_ports() {
    echo -e "${BLUE}🌐 PORT STATUS:${NC}"
    echo "==============="
    
    # Check FastAPI port
    if netstat -tln 2>/dev/null | grep -q ":8001 "; then
        echo -e "${GREEN}✅ Port 8001 (FastAPI)${NC} - Listening"
    else
        echo -e "${RED}❌ Port 8001 (FastAPI)${NC} - Not listening"
    fi
    
    # Check ngrok API port
    if netstat -tln 2>/dev/null | grep -q ":4040 "; then
        echo -e "${GREEN}✅ Port 4040 (ngrok API)${NC} - Listening"
    else
        echo -e "${YELLOW}⚠️  Port 4040 (ngrok API)${NC} - Not listening"
    fi
}

show_disk_usage() {
    echo -e "${BLUE}💾 DISK USAGE:${NC}"
    echo "==============="
    
    df -h "$PROJECT_DIR" | tail -1 | awk '{print "Project: " $3 "/" $2 " (" $5 " used)"}'
    
    if [ -d "$LOG_DIR" ]; then
        local log_size=$(du -sh "$LOG_DIR" 2>/dev/null | cut -f1)
        echo "Logs: $log_size"
    fi
}

show_network() {
    echo -e "${BLUE}🌍 NETWORK:${NC}"
    echo "==========="
    
    # Check internet connection
    if ping -c 1 8.8.8.8 &> /dev/null; then
        echo -e "${GREEN}✅ Internet${NC} - Connected"
    else
        echo -e "${RED}❌ Internet${NC} - No connection"
    fi
    
    # Get ngrok URL if available
    if curl -s http://localhost:4040/api/tunnels 2>/dev/null | grep -q "public_url"; then
        local ngrok_url=$(curl -s http://localhost:4040/api/tunnels 2>/dev/null | python3 -c "
import sys, json
try:
    data = json.load(sys.stdin)
    tunnels = data.get('tunnels', [])
    for tunnel in tunnels:
        if tunnel.get('proto') == 'https':
            print(tunnel.get('public_url', 'Unknown'))
            break
except:
    print('Error parsing ngrok data')
" 2>/dev/null)
        if [ -n "$ngrok_url" ] && [ "$ngrok_url" != "Error parsing ngrok data" ]; then
            echo -e "${GREEN}✅ ngrok URL${NC}: $ngrok_url"
        else
            echo -e "${YELLOW}⚠️  ngrok URL${NC}: Could not retrieve"
        fi
    else
        echo -e "${YELLOW}⚠️  ngrok${NC}: API not responding"
    fi
}

show_logs_tail() {
    echo -e "${BLUE}📋 RECENT LOGS:${NC}"
    echo "==============="
    
    if [ -d "$LOG_DIR" ]; then
        for logfile in "$LOG_DIR"/*.log; do
            if [ -f "$logfile" ]; then
                local filename=$(basename "$logfile")
                echo -e "${CYAN}📄 $filename:${NC}"
                tail -3 "$logfile" 2>/dev/null | sed 's/^/  /'
                echo
            fi
        done
    else
        echo "No log directory found"
    fi
}

show_system_info() {
    echo -e "${BLUE}🖥️  SYSTEM:${NC}"
    echo "=========="
    
    # CPU Load
    local load=$(uptime | awk -F'load average:' '{print $2}' | tr -d ' ')
    echo "Load: $load"
    
    # Memory
    if command -v free &> /dev/null; then
        local mem_info=$(free -h | grep '^Mem:')
        local mem_used=$(echo $mem_info | awk '{print $3}')
        local mem_total=$(echo $mem_info | awk '{print $2}')
        echo "Memory: $mem_used / $mem_total"
    fi
    
    # Uptime
    local uptime_info=$(uptime -p 2>/dev/null || uptime)
    echo "Uptime: $uptime_info"
}

# Main monitoring loop
monitor_loop() {
    while true; do
        print_header
        
        echo -e "${BLUE}🔧 SERVICES:${NC}"
        echo "============"
        get_service_status "$PID_DIR/fastapi.pid" "FastAPI Server"
        get_service_status "$PID_DIR/ngrok.pid" "ngrok Tunnel"
        get_service_status "$PID_DIR/bot.pid" "Telegram Bot"
        echo
        
        show_ports
        echo
        
        show_network
        echo
        
        show_system_info
        echo
        
        show_disk_usage
        echo
        
        show_logs_tail
        
        echo -e "${CYAN}🔄 Updating in 30 seconds... (Ctrl+C to exit)${NC}"
        
        # Wait 30 seconds or until interrupted
        for i in {30..1}; do
            echo -ne "\r⏱️  Next update in: ${i}s "
            sleep 1
        done
        echo
    done
}

# Handle Ctrl+C gracefully
trap 'echo -e "\n\n${YELLOW}👋 Monitor stopped${NC}"; exit 0' INT

case "${1:-live}" in
    "live"|"monitor"|"watch")
        monitor_loop
        ;;
    "once"|"status")
        print_header
        get_service_status "$PID_DIR/fastapi.pid" "FastAPI Server"
        get_service_status "$PID_DIR/ngrok.pid" "ngrok Tunnel"
        get_service_status "$PID_DIR/bot.pid" "Telegram Bot"
        echo
        show_ports
        echo
        show_network
        ;;
    *)
        echo "Usage: $0 {live|once|status}"
        echo
        echo "  live   - Continuous monitoring (default)"
        echo "  once   - Single status check"
        echo "  status - Same as once"
        ;;
esac 