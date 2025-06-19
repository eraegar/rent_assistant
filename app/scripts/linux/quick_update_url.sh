#!/bin/bash

echo "🔄 Quick ngrok URL update..."
echo "================================="

# Check Python
if command -v python3 &> /dev/null; then
    python_cmd="python3"
elif command -v python &> /dev/null; then
    python_cmd="python"
else
    echo "❌ Python not found!"
    exit 1
fi

# Check that ngrok is running
if ! curl -s http://localhost:4040/api/tunnels > /dev/null; then
    echo "❌ ngrok not running or unavailable!"
    echo "Start ngrok: ./start_ngrok.sh"
    exit 1
fi

echo "✅ ngrok found on localhost:4040"

# Run auto update
if [ -f "auto_update_ngrok_url.py" ]; then
    echo "🔄 Updating URL in all files..."
    
    if $python_cmd auto_update_ngrok_url.py; then
        echo "✅ URL successfully updated!"
        
        # Show new URL
        new_url=$(curl -s http://localhost:4040/api/tunnels | $python_cmd -c "
import sys, json
try:
    data = json.load(sys.stdin)
    for tunnel in data.get('tunnels', []):
        if tunnel.get('config', {}).get('addr') == 'localhost:8001':
            print(tunnel['public_url'])
            break
except:
    pass
" 2>/dev/null)
        
        if [ -n "$new_url" ]; then
            echo "🌐 New URL: $new_url"
        fi
        
    else
        echo "❌ Error updating URL!"
        exit 1
    fi
else
    echo "❌ auto_update_ngrok_url.py not found!"
    exit 1
fi 