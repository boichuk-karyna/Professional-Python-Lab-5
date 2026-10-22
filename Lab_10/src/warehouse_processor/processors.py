from collections import Counter, defaultdict

def get_unique_categories(items: list[dict]) -> set[str]:
    """Set comprehension для отримання унікальних категорій товарів."""
    return {item["category"] for item in items}

def create_warehouse_index(items: list[dict]) -> dict[str, dict]:
    """Dict comprehension для створення індексу за кодом товару."""
    return {item["code"]: item for item in items}

def filter_by_category(items: list[dict], category: str) -> list[dict]:
    """List comprehension для фільтрації товарів за категорією."""
    return [item for item in items if item["category"] == category]

def group_by_category(items: list[dict]) -> dict[str, list[dict]]:
    """Групування товарів за категоріями з використанням defaultdict."""
    result = defaultdict(list)
    for item in items:
        result[item["category"]].append(item)
    return dict(result)

def count_items_by_category(items: list[dict]) -> Counter:
    """Підрахунок кількості позицій (чи одиниць) у категоріях через Counter."""
    return Counter(item["category"] for item in items)