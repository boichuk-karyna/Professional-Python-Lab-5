"""In-memory WarehouseRepository for products and stock items."""
from .models import WarehouseItem

class WarehouseRepository:
    """Repository with save/find/all operations for warehouse inventory."""
    def __init__(self):
        self._items: dict[str, WarehouseItem] = {}

    def save(self, item: WarehouseItem) -> None:
        if not isinstance(item, WarehouseItem):
            raise TypeError("expected WarehouseItem")
        self._items[item.code] = item

    def find(self, code: str) -> WarehouseItem | None:
        return self._items.get(code)

    def all(self) -> list[WarehouseItem]:
        return list(self._items.values())
