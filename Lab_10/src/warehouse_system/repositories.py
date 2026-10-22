from __future__ import annotations
from typing import Optional
from threading import Lock
from warehouse_system.models import WarehouseItem, WarehouseItemCreate, WarehouseItemUpdate


class WarehouseRepository:
    """In-memory репозиторій складських товарів із потокобезпечністю."""

    def __init__(self) -> None:
        self._items: dict[str, WarehouseItem] = {}
        self._lock = Lock()

    def add(self, item_data: WarehouseItemCreate) -> WarehouseItem:
        with self._lock:
            if item_data.code in self._items:
                raise ValueError(f"Товар з кодом {item_data.code} вже існує.")
            item = WarehouseItem(**item_data.model_dump())
            self._items[item.code] = item
            return item

    def get_by_code(self, code: str) -> Optional[WarehouseItem]:
        with self._lock:
            return self._items.get(code)

    def get_all(self) -> list[WarehouseItem]:
        with self._lock:
            return list(self._items.values())

    def update(self, code: str, update_data: WarehouseItemUpdate) -> Optional[WarehouseItem]:
        with self._lock:
            item = self._items.get(code)
            if not item:
                return None

            data = item.model_dump()
            changes = update_data.model_dump(exclude_unset=True)
            data.update(changes)

            updated_item = WarehouseItem(**data)
            self._items[code] = updated_item
            return updated_item

    def delete(self, code: str) -> bool:
        with self._lock:
            if code in self._items:
                del self._items[code]
                return True
            return False

    def clear(self) -> None:
        with self._lock:
            self._items.clear()