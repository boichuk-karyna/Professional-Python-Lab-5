"""Application startup: configure logging and initialize persistent storage."""
import logging
import os

from book_manager.api import app
from book_manager.database import init_database

_environment = os.getenv("ENVIRONMENT", "development").upper()
_log_level = os.getenv("LOG_LEVEL", "INFO").upper()
logging.basicConfig(
    level=getattr(logging, _log_level, logging.INFO),
    format="%(asctime)s %(levelname)s [%(name)s] %(message)s",
)
logging.getLogger(__name__).info("Starting Book Manager in %s environment", _environment)
init_database()

__all__ = ["app"]
