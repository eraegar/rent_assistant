# Запуск всех сервисов - Telegram Assistant

Руководство по запуску всех компонентов системы Telegram Assistant.

## Предварительные требования

1. **Backend зависимости**:
   ```bash
   cd app
   pip install -r requirements.txt
   pip install pydantic[email]
   ```

2. **Client App зависимости**:
   ```bash
   npm install
   ```

3. **Manager App зависимости**:
   ```bash
   cd manager-app
   npm install
   ```

4. **Assistant App зависимости**:
   ```bash
   cd assistant-app
   npm install
   ```

## Запуск сервисов

### 1. Backend API Server (Порт 8000)
```bash
cd app
python main.py
```
**Обслуживает**: Все API endpoints для всех приложений

### 2. Client Application (Порт 3000)
```bash
# Из корневой папки проекта
npm start
```
**URL**: http://localhost:3000  
**Для**: Клиентов для создания задач, управления подписками

### 3. Manager Dashboard (Порт 3001) 
```bash
cd manager-app
npm run start:win  # Windows
# или
npm start          # Linux/Mac
```
**URL**: http://localhost:3001  
**Для**: Менеджеров для аналитики, управления задачами/пользователями

### 4. Assistant Interface (Порт 3002) ⭐ **НОВОЕ!**
```bash
cd assistant-app
npm run start:win  # Windows
# или
npm start          # Linux/Mac
```
**URL**: http://localhost:3002  
**Для**: Ассистентов для выполнения задач

## Информация о доступе

| Сервис | URL | Пользователи | Аутентификация |
|--------|-----|-------------|---------------|
| Backend API | http://localhost:8000 | N/A | JWT токены |
| Client App | http://localhost:3000 | Клиенты | Телефон + Пароль |
| Manager App | http://localhost:3001 | Менеджеры | Телефон + Пароль |
| **Assistant App** | **http://localhost:3002** | **Ассистенты** | **Телефон + Пароль** |

## Тестовые аккаунты

### Клиентский аккаунт
- Используйте регистрацию в клиентском приложении
- Или используйте существующие тестовые данные из `create_test_data.py`

### Менеджерский аккаунт  
Регистрация через API:
```bash
Invoke-RestMethod -Uri "http://localhost:8000/api/v1/management/auth/register" -Method POST -ContentType "application/json" -Body '{"name":"Test Manager","phone":"+1234567890","password":"admin123","email":"manager@test.com","department":"Operations"}'
```

### Аккаунт ассистента ⭐ **НОВОЕ!**
**Готовый тестовый аккаунт:**
- **Телефон**: `+7900555555`
- **Пароль**: `testpass123`

Или создайте новый через API:
```bash
Invoke-RestMethod -Uri "http://localhost:8000/api/v1/assistants/auth/register" -Method POST -ContentType "application/json" -Body '{"name":"Анна Помощник","phone":"+7900555555","password":"testpass123","email":"anna@assistant.com","specialization":"personal_only"}'
```

## Архитектура системы

```
┌─────────────────────┐    ┌─────────────────────┐    ┌─────────────────────┐
│   Client App        │    │   Manager App       │    │   Assistant App     │
│   (Port 3000)      │    │   (Port 3001)      │    │   (Port 3002)      │
│   Клиенты          │    │   Менеджеры         │    │   Ассистенты        │
└─────────┬───────────┘    └─────────┬───────────┘    └─────────┬───────────┘
          │                          │                          │
          │                          │                          │
          └──────────────────────────┼──────────────────────────┘
                                     │
                           ┌─────────▼───────────┐
                           │   Backend API       │
                           │   (Port 8000)      │
                           │   FastAPI Server    │
                           └─────────────────────┘
```

## Workflow ассистентов

1. **Менеджер** создает аккаунт ассистента через API
2. **Ассистент** получает данные для входа (телефон + пароль)
3. **Ассистент** входит в приложение на порту 3002
4. **Ассистент** переключает статус на "В сети"
5. **Ассистент** выбирает задачи из marketplace
6. **Ассистент** выполняет и завершает задачи
7. **Клиент** оценивает работу ассистента

## Устранение неполадок

- **Конфликты портов**: Убедитесь, что порты 3000, 3001, 3002 и 8000 свободны
- **Подключение к API**: Все приложения проксируют запросы на `localhost:8000`
- **Аутентификация**: Каждое приложение использует отдельные ключи хранилища токенов
- **База данных**: Убедитесь, что `app.db` существует (запустите `python init_db.py` при необходимости)
- **Windows**: Используйте `npm run start:win` для правильной установки PORT

## Цветовые схемы

- **Client App**: Фиолетовый (`#6c7ee1`) - дружелюбный для клиентов
- **Manager App**: Синий (`#1976d2`) - профессиональный для менеджеров  
- **Assistant App**: Зеленый (`#2e7d32`) - рабочий для ассистентов 