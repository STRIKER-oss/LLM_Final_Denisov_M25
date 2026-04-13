<img width="1371" height="962" alt="Screenshot from 2026-04-10 10-00-38" src="https://github.com/user-attachments/assets/fb809c42-670e-4613-ae6c-9343e3ed91ec" />
<img width="1019" height="553" alt="Screenshot from 2026-04-10 13-29-36" src="https://github.com/user-attachments/assets/f0936298-4252-49a8-9853-2d8cdb726e1f" />
<img width="1030" height="516" alt="Screenshot from 2026-04-10 13-19-56" src="https://github.com/user-attachments/assets/913c6718-c567-4eec-9fdc-ad1df7dd095f" />
<img width="879" height="1006" alt="Screenshot from 2026-04-12 12-41-33" src="https://github.com/user-attachments/assets/6b318bb7-0221-4fe1-abb3-5cb6e590433b" />
<img width="1081" height="335" alt="Screenshot from 2026-04-10 13-18-19" src="https://github.com/user-attachments/assets/012d3b0e-8f40-4bae-a36e-b276bb24b53a" />
<img width="1087" height="667" alt="Screenshot from 2026-04-10 13-17-44" src="https://github.com/user-attachments/assets/a82fd3e1-75f1-4d5d-8cc5-d9b5e05b84df" />
<img width="1087" height="667" alt="Screenshot from 2026-04-10 13-16-46" src="https://github.com/user-attachments/assets/0c5157da-0ff7-4e62-9872-8b4519cf3bce" />
<img width="1087" height="667" alt="Screenshot from 2026-04-10 13-16-35" src="https://github.com/user-attachments/assets/0ac29e5c-7aae-441c-92f8-49bd5b300f99" />
<img width="1083" height="655" alt="Screenshot from 2026-04-10 13-14-44" src="https://github.com/user-attachments/assets/d7f88492-3a31-48e0-83c5-582a5383a595" />
<img width="1371" height="962" alt="Screenshot from 2026-04-10 12-21-51" src="https://github.com/user-attachments/assets/13300345-c7ec-4061-ac9d-cd35b8cae254" />
<img width="1371" height="962" alt="Screenshot from 2026-04-10 12-21-38" src="https://github.com/user-attachments/assets/dc49187b-f1db-4a56-a73e-6d7a4453adb8" />
<img width="1371" height="962" alt="Screenshot from 2026-04-10 10-19-29" src="https://github.com/user-attachments/assets/2a61cfbf-2d40-48a5-9379-1b46ee239060" />


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


