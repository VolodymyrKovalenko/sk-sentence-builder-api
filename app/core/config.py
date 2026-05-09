# app/core/config.py
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    APP_NAME: str = "SK Practice"
    SECRET_KEY: str
    ALGORITHM: str = "HS256"
    DATABASE_URL: str
    JWT_ACCESS_TOKEN_TTL_MINUTES: int
    JWT_REFRESH_TOKEN_TTL_MINUTES: int
    ANON_DAILY_WORDS: int = 2
    FREE_DAILY_WORDS: int = 8
    PREMIUM_DAILY_WORDS: int = 16

    model_config = {
        "env_file": ".env"
    }


settings = Settings()
