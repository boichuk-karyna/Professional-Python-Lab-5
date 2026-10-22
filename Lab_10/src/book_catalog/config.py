"""Environment-based application configuration."""

import os

APP_ENV = os.getenv("APP_ENV", os.getenv("ENVIRONMENT", "development"))
LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO").upper()
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./books.db")
