from src.warehouse.models import Warehouse, WarehouseItem, Product, Supplier, ReceiptOperation, WriteOffOperation
from src.warehouse.value_objects import Money
from src.warehouse.services import WarehouseService, StandardReorderPolicy


class ConsoleNotifier:
    def send(self, recipient: str, message: str) -> None:
        print(f"[NOTIFICATION sent to {recipient}]: {message}")


def main() -> None:
    supplier = Supplier(id=1, name="TechCorp Ltd", contact_email="orders@techcorp.com")

    laptop = Product(code="P-001", name="Gaming Laptop", _price=Money(45000.0, "UAH"), supplier=supplier)
    mouse = Product(code="P-002", name="Wireless Mouse", _price=Money(1200.0, "UAH"), supplier=supplier)

    item1 = WarehouseItem(product=laptop, quantity=4, min_threshold=5)  # нижче порогового значення
    item2 = WarehouseItem(product=mouse, quantity=25, min_threshold=10)

    warehouse = Warehouse(id=101, name="Main Central Warehouse")
    warehouse.add_item(item1)
    warehouse.add_item(item2)

    print(f"Загальна кількість товарних позицій на складі: {len(warehouse)}")
    print(f"Чи є товар 'P-001' на складі? {'P-001' in warehouse}")
    print(f"Початкова загальна вартість складу: {warehouse.total_inventory_value}")

    notifier = ConsoleNotifier()
    reorder_policy = StandardReorderPolicy()
    service = WarehouseService(warehouse=warehouse, notifier=notifier, reorder_policy=reorder_policy)

    print("\n--- Виконання операції надходження (Receipt) для миші ---")
    service.perform_operation("P-002", ReceiptOperation(10))

    print("\n--- Виконання операції списання (Write-Off) для ноутбука (спрацьовує low-stock rule) ---")
    service.perform_operation("P-001", WriteOffOperation(1))

    print(f"\nКінцева загальна вартість складу: {service.get_total_value()}")


if __name__ == "__main__":
    main()