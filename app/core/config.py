from functools import lru_cache
from pydantic import BaseSettings


class Settings(BaseSettings):
    app_name: str = "AI Menstruation Tracking API"
    app_version: str = "0.1.0"
    debug: bool = False
    cors_allow_origins: list[str] = ["*"]
    cors_allow_methods: list[str] = ["*"]
    cors_allow_headers: list[str] = ["*"]
    cors_allow_credentials: bool = False


@lru_cache
def get_settings() -> Settings:
    return Settings()
