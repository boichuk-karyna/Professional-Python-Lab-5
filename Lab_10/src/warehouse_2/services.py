from .models import Warehouse, WarehouseItem, StockOperation
from .protocols import Notifier, ReorderPolicy
from .value_objects import Money


class StandardReorderPolicy:
    def check_and_reorder(self, item: WarehouseItem, notifier: Notifier) -> None:
        if item.is_low_stock:
            notifier.send(
                item.product.supplier.contact_email,
                f"Low stock alert for {item.product.name} (Code: {item.product.code}). Current quantity: {item.quantity}."
            )


class WarehouseService:
    def __init__(self, warehouse: Warehouse, notifier: Notifier, reorder_policy: ReorderPolicy) -> None:
        self._warehouse = warehouse
        self._notifier = notifier
        self._reorder_policy = reorder_policy

    def perform_operation(self, code: str, operation: StockOperation) -> None:
        item = self._warehouse.find_by_code(code)
        if not item:
            raise ValueError(f"Product with code {code} not found in warehouse.")

        operation.execute(item)
        self._reorder_policy.check_and_reorder(item, self._notifier)

    def get_total_value(self) -> Money:
        return self._warehouse.total_inventory_value