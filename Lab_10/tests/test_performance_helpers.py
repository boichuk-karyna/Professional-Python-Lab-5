import pytest

from book_manager.analytics import (
    author_counts,
    books_by_year,
    cache_summary,
    generate_books,
    invalidate_author_cache,
    pages_numpy,
    pages_python,
)
from book_manager.parallel import score_processes, score_sequential, score_threads, threaded_counter_demo
from book_manager.profiling import measure_memory


def test_python_and_numpy_statistics_match():
    books = generate_books(200)
    python_result = pages_python(books)
    numpy_result = pages_numpy(books)
    assert numpy_result["count"] == python_result["count"]
    assert numpy_result["average"] == pytest.approx(python_result["average"])
    assert numpy_result["std"] == pytest.approx(python_result["std"])
    assert numpy_result["minimum"] == python_result["minimum"]
    assert numpy_result["maximum"] == python_result["maximum"]


def test_author_counts_years_and_cache():
    books = generate_books(50)
    assert sum(author_counts(books).values()) == 50
    assert sum(books_by_year(books).values()) == 50
    assert cache_summary(books, books[0].author)[0] >= 1
    invalidate_author_cache()


def test_parallel_scores_match():
    values = [1, 2, 3]
    expected = score_sequential(values)
    assert score_threads(values, workers=2) == pytest.approx(expected)
    assert score_processes(values, workers=2) == pytest.approx(expected)


def test_threaded_counter():
    assert threaded_counter_demo(workers=4, increments=100) == 400


def test_measure_memory_returns_result():
    result, current, peak = measure_memory(lambda: [i * i for i in range(20)])
    assert len(result) == 20
    assert current >= 0
    assert peak >= current


def test_negative_generation_count_is_rejected():
    with pytest.raises(ValueError):
        generate_books(-1)
