from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    APP_NAME: str = "bot-service"
    ENV: str = "local"
    BOT_TOKEN: str
    AUTH_SERVICE_URL: str = "http://localhost:8000"
    JWT_SECRET: str
    JWT_ALG: str = "HS256"
    RABBITMQ_URL: str = "amqp://guest:guest@localhost:5672/"
    REDIS_URL: str = "redis://localhost:6379/0"
    OPENROUTER_API_KEY: str
    OPENROUTER_BASE_URL: str = "https://openrouter.ai/api/v1"
    OPENROUTER_MODEL: str = "stepfun/step-3.5-flash:free"
    OPENROUTER_SITE_URL: str = "https://example.com"
    OPENROUTER_APP_NAME: str = "bot-service"
    
    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        extra = "ignore"

settings = Settings()
