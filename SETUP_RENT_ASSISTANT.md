# 🚀 Настройка rent-assistant.ru на Ubuntu 22.04

## ✅ Что уже готово
- Домен rent-assistant.ru переведен на Cloudflare
- NS записи настроены правильно
- Существующие A/AAAA/TXT записи можно оставить как есть

## 📋 Команды для настройки на сервере

### 1. Клонирование и деплой проекта
```bash
# На Ubuntu сервере
git clone <your-repo-url> telegram-assistant
cd telegram-assistant
chmod +x deploy.sh
./deploy.sh rent-assistant.ru
```

### 2. Настройка Telegram Bot Token
```bash
nano Backend/.env
# Замените REPLACE_WITH_YOUR_BOT_TOKEN на ваш реальный токен
```

### 3. Настройка Cloudflare Tunnel
```bash
# Авторизация в Cloudflare
cloudflared tunnel login

# Создание туннеля
cloudflared tunnel create rent-assistant-tunnel

# Получение ID туннеля
ls ~/.cloudflared/*.json
# Скопируйте имя файла (это ваш TUNNEL_ID)

# Обновление конфигурации
nano ~/.cloudflared/config.yml
# Замените TUNNEL_ID.json на реальный ID файла
```

### 4. Создание DNS записей
```bash
# Основное приложение
cloudflared tunnel route dns rent-assistant-tunnel rent-assistant.ru
cloudflared tunnel route dns rent-assistant-tunnel client.rent-assistant.ru

# Скрытые панели
cloudflared tunnel route dns rent-assistant-tunnel manager.rent-assistant.ru
cloudflared tunnel route dns rent-assistant-tunnel assistant.rent-assistant.ru

# API
cloudflared tunnel route dns rent-assistant-tunnel api.rent-assistant.ru
```

### 5. Запуск туннеля
```bash
# Проверка конфигурации
cloudflared tunnel ingress validate

# Тестовый запуск
cloudflared tunnel run rent-assistant-tunnel

# Если все работает, установить как сервис
sudo cloudflared service install
sudo systemctl enable cloudflared
sudo systemctl start cloudflared
```

### 6. Перезапуск сервисов
```bash
pm2 restart all
```

## 🌐 Результат

После настройки ваши приложения будут доступны по адресам:

- **https://rent-assistant.ru** - Основное клиентское приложение
- **https://manager.rent-assistant.ru** - Панель менеджера (скрытая)
- **https://assistant.rent-assistant.ru** - Панель ассистента (скрытая)
- **https://api.rent-assistant.ru** - Backend API

## 🔧 Проверка работы

```bash
# Статус сервисов
pm2 status

# Статус туннеля
sudo systemctl status cloudflared

# Проверка DNS записей
dig rent-assistant.ru
dig manager.rent-assistant.ru

# Тест доступности
curl https://rent-assistant.ru
curl https://api.rent-assistant.ru/
```

## 🎯 Telegram Bot

После настройки обновите команды в боте:
- `/start` - откроет https://rent-assistant.ru
- `/manager_app` - откроет https://manager.rent-assistant.ru  
- `/assistant_app` - откроет https://assistant.rent-assistant.ru

## 🚨 Важные моменты

1. **MX записи** - предупреждение о почте можно игнорировать, если не планируете принимать email
2. **Существующие записи** - не трогайте A/AAAA/TXT записи, которые уже есть
3. **CNAME записи** - cloudflared автоматически создаст нужные CNAME с оранжевыми облачками
4. **Безопасность** - manager и assistant поддомены будут скрыты от поисковиков

---

🎉 **Готово!** Ваш rent-assistant.ru полностью настроен! 