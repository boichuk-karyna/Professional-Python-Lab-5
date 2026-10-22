from collections.abc import Callable
from warehouse_processor.decorators import measure_time

@measure_time
def calculate_total_inventory_value(items: list[dict]) -> float:
    """Обчислення загальної вартості складу (агрегація)."""
    if not items:
        return 0.0
    return sum(item["quantity"] * item["price"] for item in items)

def find_item_by_code(items: list[dict], code: str) -> dict | None:
    """Пошук позиції за кодом."""
    for item in items:
        if item["code"] == code:
            return item
    return None

def find_most_expensive_item(items: list[dict]) -> dict | None:
    """Знаходження найдорожчої позиції за ціною за допомогою max та lambda."""
    if not items:
        return None
    return max(items, key=lambda item: item["price"])

def get_low_stock_items(items: list[dict], threshold: int) -> list[dict]:
    """Фільтрація товарів з критично низьким запасом (менше threshold)."""
    return [item for item in items if item["quantity"] <= threshold]

def calculate_custom_prices_sum(*prices: float) -> float:
    """Демонстрація використання *args для довільної кількості цін."""
    if not prices:
        return 0.0
    return sum(prices)

def create_record(**fields) -> dict:
    """Демонстрація використання **kwargs для створення довільного словника-запису."""
    return dict(fields)

def create_stock_filter(max_quantity: int) -> Callable[[dict], bool]:
    """Closure (замикання): створює предикат для фільтрації за максимальним залишком."""
    def predicate(item: dict) -> bool:
        return item["quantity"] <= max_quantity
    return predicate