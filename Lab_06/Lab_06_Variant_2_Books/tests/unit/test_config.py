import pytest
from books.config import get_year_range


def test_default_year_range(monkeypatch):
    monkeypatch.delenv("BOOKS_MIN_YEAR", raising=False)
    monkeypatch.delenv("BOOKS_MAX_YEAR", raising=False)
    assert get_year_range() == (1, 2100)


def test_custom_year_range(monkeypatch):
    monkeypatch.setenv("BOOKS_MIN_YEAR", "1800")
    monkeypatch.setenv("BOOKS_MAX_YEAR", "2025")
    assert get_year_range() == (1800, 2025)


def test_non_integer_configuration_raises_chained_error(monkeypatch):
    monkeypatch.setenv("BOOKS_MIN_YEAR", "old")
    with pytest.raises(ValueError, match="configuration") as exc_info:
        get_year_range()
    assert exc_info.value.__cause__ is not None


def test_reversed_year_range_is_invalid(monkeypatch):
    monkeypatch.setenv("BOOKS_MIN_YEAR", "2025")
    monkeypatch.setenv("BOOKS_MAX_YEAR", "1800")
    with pytest.raises(ValueError, match="configuration"):
        get_year_range()
