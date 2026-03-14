# app/core/config.py
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    APP_NAME: str = "SK Practice"
    SECRET_KEY: str
    ALGORITHM: str = "HS256"
    DATABASE_URL: str

    model_config = {
        "env_file": ".env"
    }


settings = Settings()