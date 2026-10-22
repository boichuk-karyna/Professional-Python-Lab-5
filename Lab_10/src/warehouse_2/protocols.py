from typing import Protocol, runtime_checkable
from .models import WarehouseItem

@runtime_checkable
class Notifier(Protocol):
    def send(self, recipient: str, message: str) -> None:
        ...

@runtime_checkable
class ReorderPolicy(Protocol):
    def check_and_reorder(self, item: WarehouseItem, notifier: Notifier) -> None:
        ...