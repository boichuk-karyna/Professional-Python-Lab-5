"""Environment-based application settings."""
from __future__ import annotations

import os
from dataclasses import dataclass


@dataclass(frozen=True)
class Settings:
    database_url: str
    app_env: str
    log_level: str


def get_settings() -> Settings:
    return Settings(
        database_url=os.getenv("DATABASE_URL", "sqlite:///./books.db"),
        app_env=os.getenv("APP_ENV", os.getenv("ENVIRONMENT", "development")),
        log_level=os.getenv("LOG_LEVEL", "INFO").upper(),
    )
