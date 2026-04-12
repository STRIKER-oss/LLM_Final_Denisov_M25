from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    APP_NAME: str = "Auth Service"
    ENV: str = "development"
    JWT_SECRET: str
    JWT_ALG: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    DATABASE_URL: str = "sqlite:///./db/auth.db"
    SQLITE_PATH: str = "./db/auth.db"
    
    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        extra = "ignore"

settings = Settings()
