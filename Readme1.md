### Assistant For Rent
![Project logo](App/afrlogo.jpg)

**Сервис для аренды личного или бизнес ассистента для выполнения задач**

🌐 [Живое приложение](https://rent-assistant.ru) | 📹 [Видео-демонстрация](https://example.com/demo-video)

---

## Цели и описание проекта
Система для аренды личного/бизнес ассистента для выполнения задач:
- Трехролевой структурой (менеджеры/ассистенты/клиенты)
- Telegram-интеграцией для уведомлений и взаимодействия
- Управлением задачами
- Автоматизированными рабочими процессами

---

## Контекстная диаграмма
```mermaid
graph LR
    A[Менеджер] --> B[Frontend]
    C[Ассистент] --> B
    D[Клиент] --> B
    B --> E[Backend API]
    E --> F[(База данных)]
    E --> G[Telegram Bot]
    G --> H[Telegram Cloud]
    H --> C
    H --> D
```

---

## Дорожная карта
### Реализовано
- [x] Управление объектами
- [x] Назначение задач ассистентам
- [x] Telegram-уведомления
- [x] Многоролевые интерфейсы
- [x] Система фильтрации пользователей

### В разработке
- [ ] Платежная интеграция
- [ ] AI ассистент
- [ ] Чат для общения

---

## Руководство пользователя
### Для менеджеров
1. Авторизуйтесь на [manager.rent-assistant.ru](https://manager.rent-assistant.ru)
2. Назначайте задачи ассистентам
3. Отслеживайте выполнение задач

### Для ассистентов
1. Используйте [assistant.rent-assistant.ru](https://assistant.rent-assistant.ru)
2. Просматривайте назначенные задачи
3. Отмечайте выполнение задач
4. Но важно помнить: всегда проверяйте сроки выполнения задач

### Для клиентов
1. Создайте задачу на [rent-assistant.ru](https://rent-assistant.ru)
2. Отправьте запрос на выполнение
3. Получайте обновления через Telegram

[Полное руководство](docs/usage-guide.md)

---

## Установка и развертывание
```bash
# 1. Клонирование репозитория
git clone https://gitlab.com/your-project/rent-assistant.git
cd rent-assistant

# 2. Установка зависимостей
npm install
pip install -r requirements.txt

# 3. Настройка окружения
cp .env.example .env

# Обновите значения в .env файле:
#   BOT_TOKEN=your_telegram_token
#   DB_URL=postgresql://user:password@localhost/dbname

# 4. Запуск системы
docker-compose up --build
```

Требования к окружению:
- Docker 20.10+
- Node.js 18.x
- Python 3.10+

[Подробная инструкция](docs/deployment.md)

---

## Документация
### Разработка
- [Kanban доска](https://gitlab.com/your-project/-/boards)
- [Git workflow](docs/git-workflow.md)
- [Управление секретами](docs/secrets-management.md)
- [CONTRIBUTING.md](CONTRIBUTING.md)

### Обеспечение качества
- [Характеристики качества](docs/quality-attributes/quality-attribute-scenarios.md)
- [Автотесты](docs/quality-assurance/automated-tests.md)
- [Приемочные тесты](docs/quality-assurance/user-acceptance-tests.md)

### Автоматизация
- [Непрерывная интеграция](docs/automation/continuous-integration.md)
- [Непрерывное развертывание](docs/automation/continuous-delivery.md)

### Архитектура
- [Архитектура системы](docs/architecture/architecture.md)
- [Статическое представление](docs/architecture/static-view.md)
- [Динамическое представление](docs/architecture/dynamic-view.md)
- [Представление развертывания](docs/architecture/deployment-view.md)

---

## История изменений
Все значимые изменения в [CHANGELOG.md](CHANGELOG.md):
```markdown
# Changelog

## [2.5.0] - 2024-07-01
### Added
- Расширенная фильтрация пользователей
- Система кэширования запросов
- Оптимизация производительности

## [2.0.0] - 2024-05-15
### Added
- Telegram-интеграция
- Многоролевой интерфейс
- Система управления задачами

## [1.0.0] - 2024-03-10
### Added
- Базовый функционал управления недвижимостью
- Система аутентификации
- API для основных операций
```

---

## Технический стек
**Frontend:**
- React 18
- Redux Toolkit
- Material UI

**Backend:**
- Python 3.10
- FastAPI
- SQLAlchemy

**Инфраструктура:**
- Docker
- GitLab CI/CD
- Ubuntu Server
- Cloudflare Tunnel