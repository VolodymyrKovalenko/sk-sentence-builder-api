# app/core/config.py
from pydantic import BaseSettings


class Settings(BaseSettings):
    # DATABASE_URL: str
    APP_NAME: str = "SK Practice"
    SECRET_KEY: str
    ALGORITHM: str = "HS256"

    class Config:
        env_file = ".env"
        case_sensitive = True


settings = Settings()