from __future__ import annotations

import csv
import json
import time
from concurrent.futures import ProcessPoolExecutor, ThreadPoolExecutor
from pathlib import Path
from threading import Lock, Thread
from typing import Sequence

from .analytics import cpu_score

_counter = 0
_counter_lock = Lock()


def increment_safely(amount: int = 1) -> int:
    global _counter
    with _counter_lock:
        _counter += amount
        return _counter


def reset_counter() -> None:
    global _counter
    with _counter_lock:
        _counter = 0


def threaded_counter_demo(workers: int = 8, increments: int = 2_000) -> int:
    reset_counter()
    threads = [Thread(target=_increment_many, args=(increments,)) for _ in range(workers)]
    for thread in threads:
        thread.start()
    for thread in threads:
        thread.join()
    return _counter


def _increment_many(amount: int) -> None:
    global _counter
    for _ in range(amount):
        with _counter_lock:
            _counter += 1


def score_sequential(values: Sequence[int]) -> list[float]:
    return [cpu_score(value) for value in values]


def score_threads(values: Sequence[int], workers: int = 4) -> list[float]:
    with ThreadPoolExecutor(max_workers=workers) as executor:
        return list(executor.map(cpu_score, values))


def score_processes(values: Sequence[int], workers: int = 4) -> list[float]:
    with ProcessPoolExecutor(max_workers=workers) as executor:
        return list(executor.map(cpu_score, values, chunksize=100))


def read_catalog_file(path: str) -> int:
    file_path = Path(path)
    if file_path.suffix.lower() == ".json":
        return len(json.loads(file_path.read_text(encoding="utf-8")))
    with file_path.open(encoding="utf-8", newline="") as stream:
        return sum(1 for _ in csv.DictReader(stream))


def read_files_sequential(paths: Sequence[str]) -> list[int]:
    return [read_catalog_file(path) for path in paths]


def read_files_threaded(paths: Sequence[str], workers: int = 4) -> list[int]:
    with ThreadPoolExecutor(max_workers=workers) as executor:
        return list(executor.map(read_catalog_file, paths))
