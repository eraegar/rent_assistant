# 🤖 Assistant-for-Rent

Веб-приложение для аренды персонального ассистента с управлением задачами и аналитикой.

## 🚀 Быстрый старт

```bash
# Установка зависимостей
pip install -r requirements.txt

# Запуск сервера
python -m uvicorn main:app --reload

# Открыть в браузере
http://127.0.0.1:8000
```

## 📁 Структура проекта

```
├── 📱 frontend/          # Фронтенд (HTML, CSS, JS)
│   ├── index.html       # Главная страница
│   ├── api.js          # API клиент
│   └── app.js          # Логика приложения
├── 🔧 routers/          # API роуты
│   └── tasks.py        # Эндпоинты для задач
├── 🧪 tests/           # Тестовые скрипты
│   ├── test_api.py     # Тесты API
│   └── README.md       # Документация тестов
├── 🛠️ tools/           # Утилиты для БД
│   ├── simple_db_view.py   # Просмотр БД
│   ├── watch_db.py         # Мониторинг БД
│   └── README.md           # Документация утилит
├── 🗄️ models.py        # Модели базы данных
├── 📋 schemas.py       # Pydantic схемы
├── 🔐 auth.py          # Аутентификация
├── 🌐 main.py          # Главный файл FastAPI
└── 📦 requirements.txt # Зависимости
```

## ✨ Основные функции

- 🔐 **Регистрация и вход** через телефон
- 📋 **Управление задачами** (создание, редактирование, статусы)
- 📊 **Аналитика и статистика** с графиками
- 💼 **Система тарифных планов**
- 🎯 **Личный кабинет** с дашбордом

## 🧪 Тестирование

```bash
# Тест регистрации
python tests/test_register.py

# Тест API
python tests/test_api.py

# Просмотр базы данных
python tools/simple_db_view.py

# Мониторинг в реальном времени
python tools/watch_db.py
```

## 🛠️ API Endpoints

- `POST /auth/register` - Регистрация пользователя
- `POST /auth/login` - Вход в систему
- `GET /auth/me` - Информация о пользователе
- `GET /tasks` - Список задач
- `POST /tasks` - Создание задачи
- `PUT /tasks/{id}` - Обновление задачи
- `GET /tasks/stats/overview` - Статистика задач

## 🔧 Технологии

- **Backend**: FastAPI, SQLAlchemy, SQLite
- **Frontend**: HTML5, Tailwind CSS, Vanilla JS
- **Auth**: JWT токены, bcrypt
- **Charts**: Chart.js

## 📖 Документация

- **API Docs**: http://127.0.0.1:8000/docs
- **Тесты**: [tests/README.md](tests/README.md)
- **Утилиты**: [tools/README.md](tools/README.md)

## 🎯 Использование

1. **Регистрация** - создайте аккаунт с телефоном
2. **Вход** - войдите в систему 
3. **Создание задач** - добавляйте задачи через дашборд
4. **Мониторинг** - отслеживайте прогресс в аналитике
5. **Управление** - изменяйте статусы задач

---

*Создано с ❤️ для эффективного управления задачами* 