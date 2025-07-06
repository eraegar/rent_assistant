# Инструкции по настройке DNS записей в Cloudflare

## Обзор

Для завершения настройки вашего приложения Telegram Assistant необходимо создать DNS записи в Cloudflare, которые будут направлять трафик через Cloudflare Tunnel.

## Информация о туннеле

- **Tunnel ID**: `bd8fe408-910d-4f94-8ee3-46c5e5f7fd05`
- **Tunnel Name**: `rent-assistant-tunnel`
- **Target Domain**: `bd8fe408-910d-4f94-8ee3-46c5e5f7fd05.cfargotunnel.com`

## Необходимые DNS записи

Вам нужно создать следующие CNAME записи в панели управления Cloudflare:

### 1. Основное приложение (клиентское)
```
Type: CNAME
Name: rent-assistant.ru
Target: bd8fe408-910d-4f94-8ee3-46c5e5f7fd05.cfargotunnel.com
Proxy status: Proxied (оранжевое облако)
```

### 2. API Backend
```
Type: CNAME
Name: api.rent-assistant.ru
Target: bd8fe408-910d-4f94-8ee3-46c5e5f7fd05.cfargotunnel.com
Proxy status: Proxied (оранжевое облако)
```

### 3. Панель менеджера
```
Type: CNAME
Name: manager.rent-assistant.ru
Target: bd8fe408-910d-4f94-8ee3-46c5e5f7fd05.cfargotunnel.com
Proxy status: Proxied (оранжевое облако)
```

### 4. Панель ассистента
```
Type: CNAME
Name: assistant.rent-assistant.ru
Target: bd8fe408-910d-4f94-8ee3-46c5e5f7fd05.cfargotunnel.com
Proxy status: Proxied (оранжевое облако)
```

## Пошаговая инструкция

### Шаг 1: Войдите в панель управления Cloudflare

1. Откройте браузер и перейдите на [https://dash.cloudflare.com](https://dash.cloudflare.com)
2. Войдите в свой аккаунт Cloudflare
3. Выберите домен `rent-assistant.ru` из списка доменов

### Шаг 2: Перейдите в раздел DNS

1. В левом меню выберите **"DNS"** → **"Records"**
2. Вы увидите список существующих DNS записей

### Шаг 3: Создайте CNAME записи

Для каждой записи из списка выше:

1. Нажмите кнопку **"Add record"**
2. Выберите тип записи: **"CNAME"**
3. В поле **"Name"** введите соответствующее имя:
   - Для основного домена: `@` (или оставьте пустым)
   - Для поддоменов: `api`, `manager`, `assistant`
4. В поле **"Target"** введите: `bd8fe408-910d-4f94-8ee3-46c5e5f7fd05.cfargotunnel.com`
5. Убедитесь, что **"Proxy status"** включен (оранжевое облако)
6. Нажмите **"Save"**

### Шаг 4: Проверьте настройки

После создания всех записей ваш список DNS должен выглядеть так:

```
Type    Name                        Content                                           Proxy
CNAME   rent-assistant.ru          bd8fe408-910d-4f94-8ee3-46c5e5f7fd05.cfargotunnel.com   Proxied
CNAME   api                        bd8fe408-910d-4f94-8ee3-46c5e5f7fd05.cfargotunnel.com   Proxied
CNAME   manager                    bd8fe408-910d-4f94-8ee3-46c5e5f7fd05.cfargotunnel.com   Proxied
CNAME   assistant                  bd8fe408-910d-4f94-8ee3-46c5e5f7fd05.cfargotunnel.com   Proxied
```

## Проверка работоспособности

После настройки DNS записей (распространение может занять до 24 часов, но обычно происходит в течение нескольких минут):

### Проверьте доступность сервисов:

1. **Клиентское приложение**: [https://rent-assistant.ru](https://rent-assistant.ru)
2. **API Backend**: [https://api.rent-assistant.ru/docs](https://api.rent-assistant.ru/docs)
3. **Панель менеджера**: [https://manager.rent-assistant.ru](https://manager.rent-assistant.ru)
4. **Панель ассистента**: [https://assistant.rent-assistant.ru](https://assistant.rent-assistant.ru)

### Команды для проверки DNS:

```bash
# Проверка основного домена
nslookup rent-assistant.ru

# Проверка поддоменов
nslookup api.rent-assistant.ru
nslookup manager.rent-assistant.ru
nslookup assistant.rent-assistant.ru
```

## Учетные данные для тестирования

После настройки DNS вы можете использовать следующие тестовые учетные данные:

### Менеджер
- **URL**: https://manager.rent-assistant.ru
- **Телефон**: `+7900999999`
- **Пароль**: `manager123`

### Ассистент
- **URL**: https://assistant.rent-assistant.ru
- **Email**: `anna.assistant@example.com`
- **Пароль**: `assistant123`

### Клиент
- **URL**: https://rent-assistant.ru
- **Телефон**: `+7900123456`
- **Пароль**: `password123`

## Устранение неполадок

### Если сайт не открывается:

1. **Проверьте статус туннеля** на сервере:
   ```bash
   systemctl status rent-assistant-tunnel
   ```

2. **Проверьте логи туннеля**:
   ```bash
   journalctl -u rent-assistant-tunnel -f
   ```

3. **Перезапустите туннель**:
   ```bash
   systemctl restart rent-assistant-tunnel
   ```

### Если DNS не работает:

1. Подождите до 24 часов для полного распространения DNS
2. Очистите кеш DNS на вашем компьютере:
   ```bash
   # Windows
   ipconfig /flushdns
   
   # macOS
   sudo dscacheutil -flushcache
   
   # Linux
   sudo systemctl restart systemd-resolved
   ```

3. Используйте онлайн-инструменты для проверки DNS:
   - [https://dnschecker.org](https://dnschecker.org)
   - [https://www.whatsmydns.net](https://www.whatsmydns.net)

## Дополнительные настройки Cloudflare

### Рекомендуемые настройки безопасности:

1. **SSL/TLS**: Установите режим "Full (strict)"
2. **Always Use HTTPS**: Включите для автоматического перенаправления
3. **HSTS**: Включите для дополнительной безопасности
4. **Bot Fight Mode**: Включите для защиты от ботов

### Настройки производительности:

1. **Auto Minify**: Включите для CSS, JavaScript, HTML
2. **Brotli**: Включите для лучшего сжатия
3. **Caching Level**: Установите "Standard"

## Поддержка

Если у вас возникли проблемы с настройкой DNS, обратитесь к документации Cloudflare:
- [Cloudflare DNS Documentation](https://developers.cloudflare.com/dns/)
- [Cloudflare Tunnel Documentation](https://developers.cloudflare.com/cloudflare-one/connections/connect-apps/)

---

**Важно**: После успешной настройки DNS ваше приложение будет полностью функциональным и доступным по указанным адресам! 