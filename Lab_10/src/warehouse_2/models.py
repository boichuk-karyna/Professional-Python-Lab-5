from collections.abc import Iterator
from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from .value_objects import Money

@dataclass(frozen=True)
class Supplier:
    id: int
    name: str
    contact_email: str

@dataclass
class Product:
    code: str
    name: str
    _price: Money
    supplier: Supplier

    @property
    def price(self) -> Money:
        return self._price

    def __str__(self) -> str:
        return f"{self.name} ({self.code}) - {self._price}"

@dataclass
class WarehouseItem:
    product: Product
    quantity: int = 0
    min_threshold: int = 5

    def __post_init__(self) -> None:
        if self.quantity < 0:
            raise ValueError("Quantity cannot be negative")

    @property
    def total_value(self) -> Money:
        return Money(self.product.price.amount * self.quantity, self.product.price.currency)

    @property
    def is_low_stock(self) -> bool:
        return self.quantity < self.min_threshold

# Абстрактний базовий клас для складських операцій (ABC)
class StockOperation(ABC):
    @abstractmethod
    def execute(self, item: WarehouseItem) -> None:
        pass

class ReceiptOperation(StockOperation):
    def __init__(self, qty: int) -> None:
        self.qty = qty

    def execute(self, item: WarehouseItem) -> None:
        if self.qty <= 0:
            raise ValueError("Receipt quantity must be positive")
        item.quantity += self.qty

class WriteOffOperation(StockOperation):
    def __init__(self, qty: int) -> None:
        self.qty = qty

    def execute(self, item: WarehouseItem) -> None:
        if self.qty <= 0:
            raise ValueError("Write-off quantity must be positive")
        if item.quantity < self.qty:
            raise ValueError("Insufficient stock for write-off")
        item.quantity -= self.qty

# Склад як контейнер із підтримкою dunder methods
@dataclass
class Warehouse:
    id: int
    name: str
    items: list[WarehouseItem] = field(default_factory=list)

    def add_item(self, item: WarehouseItem) -> None:
        self.items.append(item)

    def find_by_code(self, code: str) -> WarehouseItem | None:
        for item in self.items:
            if item.product.code == code:
                return item
        return None

    def __len__(self) -> int:
        return len(self.items)

    def __iter__(self) -> Iterator[WarehouseItem]:
        return iter(self.items)

    def __contains__(self, code: str) -> bool:
        return any(item.product.code == code for item in self.items)

    @property
    def total_inventory_value(self) -> Money:
        total = sum(item.total_value.amount for item in self.items)
        currency = self.items[0].product.price.currency if self.items else "UAH"
        return Money(total, currency)