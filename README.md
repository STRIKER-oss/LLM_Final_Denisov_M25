<img width="1371" height="962" alt="Screenshot from 2026-04-10 10-00-38" src="https://github.com/user-attachments/assets/9cd2e7f2-7cc9-4379-ac62-c68d49359035" />
<img width="1371" height="962" alt="Screenshot from 2026-04-10 10-19-29" src="https://github.com/user-attachments/assets/150e023d-edc9-4e4f-8d0d-2fc3cd13a05d" />
<img width="1371" height="962" alt="Screenshot from 2026-04-10 12-21-38" src="https://github.com/user-attachments/assets/ad92556d-3d62-477d-a2e2-1ecb7f1e6f23" />
<img width="1371" height="962" alt="Screenshot from 2026-04-10 12-21-51" src="https://github.com/user-attachments/assets/082abb81-d63d-481b-a028-f8c479823a35" />
<img width="1083" height="655" alt="Screenshot from 2026-04-10 13-14-44" src="https://github.com/user-attachments/assets/2217de3e-c77c-49ee-b60a-0ea83045ac68" />
<img width="1087" height="667" alt="Screenshot from 2026-04-10 13-16-35" src="https://github.com/user-attachments/assets/3c929861-e2be-4fc2-a0a3-92f112c56a2f" />
<img width="1087" height="667" alt="Screenshot from 2026-04-10 13-16-46" src="https://github.com/user-attachments/assets/a87e8944-b15a-494c-97c5-43bd2e24bdb1" />
<img width="1087" height="667" alt="Screenshot from 2026-04-10 13-17-44" src="https://github.com/user-attachments/assets/ed43d82b-cced-4876-9813-6cfe8548534a" />
<img width="1081" height="335" alt="Screenshot from 2026-04-10 13-18-19" src="https://github.com/user-attachments/assets/7460bbe0-1be1-4b46-bf82-a8a4887c389c" />
<img width="879" height="1006" alt="Screenshot from 2026-04-12 12-41-33" src="https://github.com/user-attachments/assets/c2201fef-e5ea-45fd-9709-857d18512ecc" />
<img width="1030" height="516" alt="Screenshot from 2026-04-10 13-19-56" src="https://github.com/user-attachments/assets/5c92e6a9-c4d2-4f7d-8a35-b94d4efae5df" />
<img width="1019" height="553" alt="Screenshot from 2026-04-10 13-29-36" src="https://github.com/user-attachments/assets/7ffe7b8f-8729-4322-a9fd-edc552e531a1" />


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


