from __future__ import annotations
from typing import Optional
from warehouse_system.repositories import WarehouseRepository
from warehouse_system.models import WarehouseItem, WarehouseItemCreate, WarehouseItemUpdate
from warehouse_system.analytics import (
    calculate_total_value_numpy,
    get_cached_warehouse_stats,
    invalidate_warehouse_cache,
    _cache_version
)


class WarehouseService:
    def __init__(self, repository: WarehouseRepository) -> None:
        self.repo = repository

    def add_item(self, item_data: WarehouseItemCreate) -> WarehouseItem:
        item = self.repo.add(item_data)
        invalidate_warehouse_cache()
        return item

    def get_item(self, code: str) -> Optional[WarehouseItem]:
        return self.repo.get_by_code(code)

    def list_items(self) -> list[WarehouseItem]:
        return self.repo.get_all()

    def update_item(self, code: str, update_data: WarehouseItemUpdate) -> Optional[WarehouseItem]:
        item = self.repo.update(code, update_data)
        if item:
            invalidate_warehouse_cache()
        return item

    def record_movement(self, code: str, change: int) -> Optional[WarehouseItem]:
        item = self.repo.get_by_code(code)
        if not item:
            return None
        new_qty = item.quantity + change
        if new_qty < 0:
            raise ValueError("Кількість товару не може бути від'ємною.")

        updated = self.repo.update(code, WarehouseItemUpdate(quantity=new_qty))
        invalidate_warehouse_cache()
        return updated

    def get_stats(self) -> dict:
        items = [item.model_dump() for item in self.repo.get_all()]
        total_value = calculate_total_value_numpy(items) if items else 0.0
        return get_cached_warehouse_stats(_cache_version, len(items), total_value)