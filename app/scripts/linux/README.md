# 🐧 Linux/macOS Scripts

This directory contains shell scripts for Linux and macOS systems.

## 🚀 Quick Start

### 1. Make scripts executable:
```bash
chmod +x start_linux.sh scripts/linux/*.sh
```

### 2. Run main launcher:
```bash
./start_linux.sh
```

## 📋 Available Scripts

### 🎯 Main Launcher
- **`../start_linux.sh`** - Main menu launcher
  - Interactive menu with all options
  - Automatically checks for missing files
  - User-friendly interface

### 🔧 Individual Scripts
- **`start_all.sh`** - Full startup (all services)
  - System check and validation
  - FastAPI server startup
  - ngrok tunnel setup
  - Automatic URL update
  - Telegram bot launch

- **`start_fastapi.sh`** - FastAPI server only
  - Dependency check and installation
  - Server startup on port 8001
  - Auto-reload enabled

- **`start_ngrok.sh`** - ngrok tunnel only
  - ngrok detection (system or local)
  - Tunnel setup for port 8001
  - Automatic URL update

- **`start_bot.sh`** - Telegram bot only
  - Token validation
  - Bot startup with error handling

- **`setup_bot_token.sh`** - Bot token configuration
  - Interactive token setup
  - Token validation via Telegram API
  - .env files creation/update

- **`quick_update_url.sh`** - Quick URL update
  - Updates ngrok URL in all files
  - Shows new URL information

## 🎮 Usage Examples

### Full startup:
```bash
./start_linux.sh
# Select option 1
```

### Setup bot token:
```bash
./scripts/linux/setup_bot_token.sh
# Follow interactive prompts
```

### Start individual services:
```bash
# Start only FastAPI
./scripts/linux/start_fastapi.sh

# Start only ngrok
./scripts/linux/start_ngrok.sh

# Start only bot
./scripts/linux/start_bot.sh
```

### Quick URL update:
```bash
./scripts/linux/quick_update_url.sh
```

## 🎨 Features

### ✨ User Interface
- **Colored output** for better readability
- **Progress indicators** for long operations
- **Error handling** with helpful messages
- **Interactive prompts** for user input

### 🔍 System Validation
- **Python version** detection (python3/python)
- **Dependency checking** and auto-installation
- **Port availability** verification
- **File existence** validation
- **Token format** verification

### 🚀 Smart Startup
- **Background processes** for GUI terminals
- **Fallback modes** for headless systems
- **Process tracking** with PID display
- **Service monitoring** commands

### 🛡️ Error Handling
- **Graceful degradation** when tools missing
- **Detailed error messages** with solutions
- **Recovery suggestions** for common issues
- **Safe cancellation** at any step

## 🔧 System Requirements

### Required:
- **Linux/macOS** with bash shell
- **Python 3.6+** (python3 or python)
- **pip** for dependency installation
- **curl** for API calls

### Optional:
- **ngrok** (system-wide or in project directory)
- **gnome-terminal** or **xterm** for GUI mode
- **lsof** for port checking

## 📁 File Structure

```
scripts/linux/
├── README.md              # This file
├── start_all.sh           # Full startup script
├── start_fastapi.sh       # FastAPI server only
├── start_ngrok.sh         # ngrok tunnel only
├── start_bot.sh           # Telegram bot only
├── setup_bot_token.sh     # Token configuration
└── quick_update_url.sh    # URL update utility
```

## 🔍 Troubleshooting

### Permission denied:
```bash
chmod +x scripts/linux/*.sh
```

### Python not found:
```bash
# Install Python 3
sudo apt update && sudo apt install python3 python3-pip  # Ubuntu/Debian
sudo yum install python3 python3-pip                     # CentOS/RHEL
brew install python3                                      # macOS
```

### ngrok not found:
```bash
# Install ngrok
sudo snap install ngrok                    # Ubuntu/Debian
brew install ngrok/ngrok/ngrok             # macOS
# Or download from: https://ngrok.com/download
```

### Port 8001 in use:
```bash
# Find and kill process
lsof -ti:8001 | xargs kill -9
```

### Token issues:
```bash
# Re-run token setup
./scripts/linux/setup_bot_token.sh
```

## 💡 Tips

### For Development:
- Use `start_all.sh` for complete testing environment
- Monitor logs in separate terminals
- Use `quick_update_url.sh` when ngrok restarts

### For Production:
- Run individual scripts as needed
- Use process managers like systemd
- Set up proper logging and monitoring

### For Debugging:
- Check individual script outputs
- Verify .env file contents
- Test token with setup script
- Monitor process status with `ps aux | grep python`

## 🆘 Getting Help

If you encounter issues:

1. **Check system requirements** above
2. **Run setup script** for token configuration
3. **Verify file permissions** with chmod
4. **Check error messages** for specific solutions
5. **Review troubleshooting** section

For additional help, check the main project README or open an issue. 