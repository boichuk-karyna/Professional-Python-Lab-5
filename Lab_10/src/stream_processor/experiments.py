import csv
import random
import time
import tracemalloc
from pathlib import Path
from typing import Callable

from stream_processor.pipeline import build_pipeline


AUTHORS = (
    "J.K. Rowling",
    "George Orwell",
    "Haruki Murakami",
    "Jane Austen",
    "Stephen King",
    "Agatha Christie",
)


def generate_test_file(
    path: Path,
    count: int,
) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)

    with path.open(
        "w",
        encoding="utf-8",
        newline="",
    ) as file:
        writer = csv.writer(file)
        writer.writerow(
            ["isbn", "title", "author", "year", "pages"]
        )

        for index in range(1, count + 1):
            writer.writerow(
                [
                    f"ISBN-{index:010d}",
                    f"Book {index}",
                    random.choice(AUTHORS),
                    random.randint(1950, 2025),
                    random.randint(80, 900),
                ]
            )


def read_all_books(path: Path) -> list[dict[str, str]]:
    with path.open(
        "r",
        encoding="utf-8",
        newline="",
    ) as file:
        return list(csv.DictReader(file))


def eager_count(path: Path) -> int:
    return len(read_all_books(path))


def lazy_count(path: Path) -> int:
    return sum(1 for _ in build_pipeline(path))


def measure(
    function: Callable[[Path], int],
    path: Path,
) -> tuple[float, float, int]:
    tracemalloc.start()
    start = time.perf_counter()

    result = function(path)

    elapsed = time.perf_counter() - start
    _, peak = tracemalloc.get_traced_memory()
    tracemalloc.stop()

    return elapsed, peak / 1024 / 1024, result


def measure_first_result(
    path: Path,
) -> float:
    pipeline = build_pipeline(path)

    start = time.perf_counter()
    next(pipeline, None)
    return time.perf_counter() - start
