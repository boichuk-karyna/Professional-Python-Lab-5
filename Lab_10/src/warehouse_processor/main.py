import random
from warehouse_processor.data import warehouse_items, warehouse_metadata
from warehouse_processor.processors import (
    get_unique_categories,
    create_warehouse_index,
    filter_by_category,
    group_by_category,
    count_items_by_category,
)
from warehouse_processor.analytics import (
    calculate_total_inventory_value,
    find_item_by_code,
    find_most_expensive_item,
    get_low_stock_items,
    calculate_custom_prices_sum,
    create_record,
    create_stock_filter,
)


def print_table(title: str, items: list[dict]) -> None:
    """Допоміжна функція для гарного виведення списку товарів."""
    print(f"\n{title}")
    print("-" * 75)
    print(f"{'Код':<8} {'Назва':<25} {'Категорія':<15} {'Кількість':<10} {'Ціна (грн)':<10}")
    print("-" * 75)
    for item in items:
        print(
            f"{item['code']:<8} {item['name']:<25} {item['category']:<15} {item['quantity']:<10} {item['price']:<10.2f}")


def run_benchmark() -> None:
    """Експериментальна частина: порівняння швидкості пошуку в list та dict для великої кількості записів."""
    print("\n--- ЕКСПЕРИМЕНТАЛЬНА ЧАСТИНА (БЕНЧМАРК) ---")
    sizes = [1_000, 10_000, 100_000]

    for size in sizes:
        # Генеруємо тестовий набір даних
        test_data = [
            {"code": f"ID_{i}", "name": f"Item {i}", "quantity": random.randint(1, 100),
             "price": random.uniform(10, 1000)}
            for i in range(size)
        ]
        target_code = f"ID_{size - 1}"  # шукаємо останній елемент для найгіршого випадку лінійного пошуку

        # 1. Лінійний пошук у list
        import time
        start = time.perf_counter()
        found_item = None
        for item in test_data:
            if item["code"] == target_code:
                found_item = item
                break
        list_time = time.perf_counter() - start

        # 2. Пошук у dict (з урахуванням часу побудови індексу або лише пошук)
        start = time.perf_counter()
        index = {item["code"]: item for item in test_data}
        found_item_dict = index.get(target_code)
        dict_time = time.perf_counter() - start

        print(
            f"Розмір набору: {size:7d} записів | Лінійний пошук у list: {list_time:.8f} с | Побудова + пошук у dict: {dict_time:.8f} с")


def main() -> None:
    print("=== АНАЛІЗ СИСТЕМИ ОБЛІКУ СКЛАДСЬКИХ ЗАПАСІВ (ВАРІАНТ 10) ===")
    print(f"Інформація про склад (Tuple): {warehouse_metadata[0]}, Адреса: {warehouse_metadata[1]}")

    print_table("Усі складські позиції", warehouse_items)

    # 1. Унікальні категорії (Set comprehension)
    categories = get_unique_categories(warehouse_items)
    print(f"\nУнікальні категорії (Set): {categories}")

    # 2. Загальна вартість складу (агрегація)
    total_val = calculate_total_inventory_value(warehouse_items)
    print(f"Загальна вартість складу: {total_val:,.2f} грн")

    # 3. Пошук позиції за кодом
    search_code = "B201"
    found = find_item_by_code(warehouse_items, search_code)
    print(f"\nПошук за кодом '{search_code}':", found)

    # 4. Товари з критично низьким запасом (< 5 штук)
    low_stock = get_low_stock_items(warehouse_items, threshold=5)
    print_table("Товари з критично низьким запасом (<= 5)", low_stock)

    # 5. Найдорожча позиція
    expensive = find_most_expensive_item(warehouse_items)
    print(f"\nНайдорожча позиція: {expensive['name']} ({expensive['price']} грн)")

    # 6. Counter позицій за категоріями
    counter_res = count_items_by_category(warehouse_items)
    print(f"\nCounter позицій за категоріями: {dict(counter_res)}")

    # 7. Групування за категоріями
    grouped = group_by_category(warehouse_items)
    print("\nГрупування товарів за категоріями:")
    for cat, items_list in grouped.items():
        print(f"  - {cat}: {len(items_list)} позицій(ї)")

    # 8. Dict-index за кодом
    index = create_warehouse_index(warehouse_items)
    print(f"\nDict-index за кодом (ключ 'A101'): {index.get('A101')}")

    # 9. Використання Closure для фільтрації
    is_critical_stock = create_stock_filter(max_quantity=4)
    filtered_via_closure = [item for item in warehouse_items if is_critical_stock(item)]
    print_table("Фільтрація через Closure (залишок <= 4)", filtered_via_closure)

    # 10. Демонстрація *args та **kwargs
    sum_prices = calculate_custom_prices_sum(150.5, 300.0, 1250.0)
    print(f"\nСума цін через *args: {sum_prices:.2f} грн")

    custom_item = create_record(code="Z999", name="Test Item", quantity=10, price=99.99)
    print(f"Створений запис через **kwargs: {custom_item}")

    # 11. Бенчмарк складності
    run_benchmark()


if __name__ == "__main__":
    main()