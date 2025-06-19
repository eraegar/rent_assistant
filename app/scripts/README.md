# 📁 Scripts Directory

Эта папка содержит скрипты для управления проектом **Telegram Assistant**, разделенные по операционным системам.

## 📂 Структура

```
scripts/
├── windows/          # Windows batch (.bat) скрипты
│   ├── start_all.bat
│   ├── setup_bot_token.bat
│   ├── start_fastapi.bat
│   ├── start_ngrok.bat
│   ├── start_bot.bat
│   ├── quick_update_url.bat
│   ├── update_url.bat
│   └── reset_bot.bat
├── linux/            # Linux bash (.sh) скрипты  
│   ├── start_all.sh
│   ├── setup_bot_token.sh
│   ├── start_fastapi.sh
│   ├── start_ngrok.sh
│   ├── start_bot.sh
│   └── quick_update_url.sh
└── README.md         # Этот файл
```

## 🚀 Быстрый старт

### Windows
```cmd
# Перейти в папку проекта
cd telegram-assistant\app

# Настройка токена (только первый раз)
scripts\windows\setup_bot_token.bat

# Запуск всех сервисов
scripts\windows\start_all.bat
```

### Linux/Ubuntu
```bash
# Перейти в папку проекта
cd telegram-assistant/app

# Настройка токена (только первый раз)
scripts/linux/setup_bot_token.sh

# Запуск всех сервисов
scripts/linux/start_all.sh
```

## 📋 Описание скриптов

### 🔧 Основные скрипты

| Скрипт | Windows | Linux | Описание |
|--------|---------|-------|----------|
| **Полный запуск** | `start_all.bat` | `start_all.sh` | Запускает все сервисы автоматически |
| **Настройка токена** | `setup_bot_token.bat` | `setup_bot_token.sh` | Настройка Telegram бота |

### 🎯 Отдельные компоненты

| Компонент | Windows | Linux | Описание |
|-----------|---------|-------|----------|
| **FastAPI сервер** | `start_fastapi.bat` | `start_fastapi.sh` | Веб-сервер на порту 8001 |
| **ngrok туннель** | `start_ngrok.bat` | `start_ngrok.sh` | Публичный HTTPS доступ |
| **Telegram бот** | `start_bot.bat` | `start_bot.sh` | Интерфейс бота |

### ⚡ Утилиты

| Утилита | Windows | Linux | Описание |
|---------|---------|-------|----------|
| **Обновление URL** | `quick_update_url.bat` | `quick_update_url.sh` | Быстрое обновление ngrok URL |
| **Полное обновление** | `update_url.bat` | - | Обновление URL (старая версия) |
| **Сброс бота** | `reset_bot.bat` | - | Сброс состояния бота |

## 🎨 Особенности

### Windows (.bat) скрипты
- ✅ Цветной вывод через PowerShell
- ✅ Проверка зависимостей
- ✅ Автоматическое открытие новых окон
- ✅ Поддержка кодировки UTF-8

### Linux (.sh) скрипты  
- ✅ Цветной вывод ANSI
- ✅ Поддержка разных терминалов
- ✅ Fallback на фоновый запуск
- ✅ Проверка прав выполнения

## 🛠️ Установка прав выполнения (Linux)

```bash
# Сделать все скрипты исполняемыми
chmod +x scripts/linux/*.sh

# Или по отдельности
chmod +x scripts/linux/start_all.sh
chmod +x scripts/linux/setup_bot_token.sh
```

## 📖 Дополнительная документация

- **[README_START_ALL.md](../README_START_ALL.md)** - Подробное руководство по использованию
- **[README.md](../README.md)** - Общая документация проекта
- **[README_NGROK.md](../README_NGROK.md)** - Настройка ngrok
- **[README_DEPLOY.md](../README_DEPLOY.md)** - Инструкции по развертыванию

## 🆘 Помощь

При возникновении проблем:

1. Убедитесь что используете правильную ОС (Windows/Linux)
2. Проверьте права доступа к файлам
3. Убедитесь что токен бота настроен
4. Обратитесь к документации выше

---

**Tip:** Всегда запускайте скрипты из корневой папки проекта (`telegram-assistant/app/`) 