from typing import Literal
from pathlib import Path

from pydantic_settings import BaseSettings, SettingsConfigDict


BASE_DIR = Path(__file__).resolve().parents[2]


class Settings(BaseSettings):
    DATABASE_URL: str
    FACTIFY_CORE_API_URL: str
    API_KEY_PREFIX: str = "factify_test_"

    JWT_SECRET_KEY: str
    JWT_ALGORITHM: str = "HS256"
    JWT_EXPIRE_MINUTES: int = 60

    ALLOWED_ORIGINS: str = "http://localhost:3000"

    PAYSTACK_SECRET_KEY: str
    PAYSTACK_PUBLIC_KEY: str
    FRONTEND_URL: str = "http://localhost:3000"

    ENVIRONMENT: Literal[
        "development",
        "testing",
        "staging",
        "production",
    ] = "development"

    model_config = SettingsConfigDict(
        env_file=BASE_DIR / ".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )


settings = Settings()