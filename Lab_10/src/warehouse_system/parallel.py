from __future__ import annotations
from concurrent.futures import ThreadPoolExecutor, ProcessPoolExecutor
from threading import Lock
from pathlib import Path
from warehouse_system.analytics import cpu_bound_heavy_item_processing


def process_items_threads(items: list[dict], workers: int = 4) -> list[float]:
    """Паралельна обробка товарів через ThreadPoolExecutor."""
    data = [(item["quantity"], item["price"]) for item in items]
    with ThreadPoolExecutor(max_workers=workers) as executor:
        return list(executor.map(cpu_bound_heavy_item_processing, data))


def process_items_processes(items: list[dict], workers: int = 4) -> list[float]:
    """Багатопроцесна обробка CPU-bound задач через ProcessPoolExecutor."""
    data = [(item["quantity"], item["price"]) for item in items]
    with ProcessPoolExecutor(max_workers=workers) as executor:
        return list(executor.map(cpu_bound_heavy_item_processing, data, chunksize=100))


def read_log_file(path: Path) -> str:
    """I/O-bound функція читання одного файлу журналу."""
    return path.read_text(encoding="utf-8")


def read_logs_parallel(paths: list[Path], workers: int = 4) -> list[str]:
    """Паралельне читання багатьох журналів через ThreadPoolExecutor."""
    with ThreadPoolExecutor(max_workers=workers) as executor:
        return list(executor.map(read_log_file, paths))


# Демонстрація Race Condition та її усунення через Lock
stock_counter = 0
counter_lock = Lock()


def unsafe_increment_stock() -> None:
    """Непотокобезпечна зміна стану (викликає Race Condition)."""
    global stock_counter
    current = stock_counter
    # Моделювання перемикання контексту
    stock_counter = current + 1


def safe_increment_stock() -> None:
    """Потокобезпечна зміна стану через Lock."""
    global stock_counter
    with counter_lock:
        current = stock_counter
        stock_counter = current + 1