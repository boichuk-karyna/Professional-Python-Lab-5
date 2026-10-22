from __future__ import annotations
import random
import math
from functools import lru_cache
import numpy as np


def generate_large_dataset(count: int, seed: int = 42) -> list[dict]:
    """Генерація великого тестового масиву складських товарів."""
    random.seed(seed)
    categories = ["Electronics", "Groceries", "Hardware", "Clothing", "Stationery"]
    return [
        {
            "code": f"PRD-{i:07d}",
            "name": f"Product_{i}",
            "quantity": random.randint(0, 500),
            "price": round(random.uniform(10.0, 5000.0), 2),
            "category": random.choice(categories)
        }
        for i in range(count)
    ]


def calculate_total_value_python(items: list[dict]) -> float:
    """Baseline: розрахунок загальної вартості складу через цикл Python."""
    total = 0.0
    for item in items:
        total += item["quantity"] * item["price"]
    return total


def calculate_total_value_numpy(items: list[dict]) -> float:
    """NumPy Оптимізація: векторизований розрахунок загальної вартості складу."""
    quantities = np.fromiter((item["quantity"] for item in items), dtype=np.float64, count=len(items))
    prices = np.fromiter((item["price"] for item in items), dtype=np.float64, count=len(items))
    return float(np.dot(quantities, prices))


def find_low_stock_python(items: list[dict], threshold: int = 10) -> list[dict]:
    """Baseline: пошук товарів з низьким залишком."""
    return [item for item in items if item["quantity"] <= threshold]


def cpu_bound_heavy_item_processing(item_tuple: tuple[int, float]) -> float:
    """Складна CPU-bound обробка одного товару для вимірювання задієності ядер."""
    qty, price = item_tuple
    val = float(qty * price)
    for _ in range(100):
        val = math.sin(val) ** 2 + math.cos(val) ** 2 + math.sqrt(abs(val) + 1.0)
    return val


# Система кешування з версіюванням для інвалідації
_cache_version = 0


def invalidate_warehouse_cache() -> None:
    """Інвалідація (очищення) кешу складської статистики."""
    global _cache_version
    _cache_version += 1
    get_cached_warehouse_stats.cache_clear()


@lru_cache(maxsize=128)
def get_cached_warehouse_stats(version: int, total_items: int, total_value: float) -> dict:
    """Кешована статистика складу."""
    return {
        "status": "computed",
        "cache_version": version,
        "total_items": total_items,
        "total_value": round(total_value, 2)
    }