import pytest

from book_catalog.analytics import (
    books_by_year, generate_books, pages_numpy, pages_python, author_counts,
    cache_summary, invalidate_author_cache,
)
from book_catalog.parallel import (
    score_processes, score_sequential, score_threads, threaded_counter_demo,
)


def test_python_and_numpy_statistics_match():
    books = generate_books(1000)
    python_result = pages_python(books)
    numpy_result = pages_numpy(books)
    assert numpy_result["count"] == python_result["count"]
    assert numpy_result["average"] == pytest.approx(python_result["average"])
    assert numpy_result["std"] == pytest.approx(python_result["std"])
    assert numpy_result["minimum"] == python_result["minimum"]
    assert numpy_result["maximum"] == python_result["maximum"]


def test_author_counts_and_year_grouping():
    books = generate_books(500)
    assert sum(author_counts(books).values()) == 500
    assert sum(books_by_year(books).values()) == 500


def test_cache_version_changes_result():
    books = generate_books(20)
    author = books[0].author
    first = cache_summary(books, author, 0)
    second = cache_summary(books, author, 1)
    assert first == second
    invalidate_author_cache()


def test_thread_and_process_scores_match():
    values = [1, 2, 3, 4]
    expected = score_sequential(values)
    assert score_threads(values, 2) == pytest.approx(expected)
    assert score_processes(values, 2) == pytest.approx(expected)


def test_lock_prevents_lost_updates():
    assert threaded_counter_demo(workers=4, increments=500) == 2000
