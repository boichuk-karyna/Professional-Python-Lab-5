"""Configuration loaded from environment variables."""
import os


def get_year_range() -> tuple[int, int]:
    """Return the allowed publication-year range from environment."""
    raw_min = os.getenv("BOOKS_MIN_YEAR", "1")
    raw_max = os.getenv("BOOKS_MAX_YEAR", "2100")
    try:
        min_year, max_year = int(raw_min), int(raw_max)
    except ValueError as exc:
        raise ValueError("Invalid year range configuration.") from exc
    if min_year <= 0 or max_year < min_year:
        raise ValueError("Invalid year range configuration.")
    return min_year, max_year
