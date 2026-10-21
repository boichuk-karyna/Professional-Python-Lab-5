"""Environment-based application settings; never store secrets in source code."""

from functools import lru_cache
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    app_name: str = "Book Catalog API"
    app_version: str = "1.0.0"
    app_env: str = "development"
    log_level: str = "INFO"
    database_url: str = "sqlite:///./data/books.db"
    api_base_url: str = "http://127.0.0.1:8000"
    http_timeout: float = 3.0
    http_retries: int = 3
    http_concurrency: int = 3
    host: str = "0.0.0.0"
    port: int = 8000

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore")


@lru_cache(maxsize=1)
def get_settings() -> Settings:
    return Settings()
