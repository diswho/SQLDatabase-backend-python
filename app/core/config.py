import secrets
from typing import Any, Dict, List, Optional, Union

from pydantic import AnyHttpUrl,  EmailStr, HttpUrl, PostgresDsn, validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    API_V1_STR: str = "/api/v1"
    SECRET_KEY: str = secrets.token_urlsafe(32)
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 8
    EMAIL_RESET_TOKEN_EXPIRE_HOURS: int = 48
    PROJECT_NAME: str
    BACKEND_CORS_ORIGINS: List[AnyHttpUrl] = []

    model_config = SettingsConfigDict(env_file=".env")


settings = Settings()
