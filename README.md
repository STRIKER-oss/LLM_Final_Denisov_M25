# Система LLM-консультаций

## Архитектура

Система состоит из двух независимых сервисов:

### 1. Auth Service
- Регистрация пользователей
- Логин и выдача JWT
- Получение профиля по токену
- Хранение пользователей в SQLite
- Пароли хешируются bcrypt

### 2. Bot Service
- Telegram-бот с доступом к LLM
- Авторизация через JWT из Auth Service
- Асинхронная обработка запросов через RabbitMQ + Celery
- Хранение токенов и результатов в Redis
- Интеграция с OpenRouter API

## Стек
- FastAPI, SQLAlchemy, JWT, bcrypt
- aiogram, Celery, RabbitMQ, Redis
- OpenRouter (LLM API)
- Docker, docker-compose
- pytest, fakeredis, respx

## Запуск

1. Создайте файл `.env` в корне проекта:
TELEGRAM_BOT_TOKEN=ваш_токен
OPENROUTER_API_KEY=ваш_ключ


