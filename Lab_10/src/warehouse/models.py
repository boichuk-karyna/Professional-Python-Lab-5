from dataclasses import dataclass

class WarehouseError(Exception):
    """Base warehouse error."""

class InsufficientStockError(WarehouseError):
    pass

class ImportRecordError(WarehouseError):
    def __init__(self, row: int, field: str):
        self.row, self.field = row, field
        super().__init__(f"Invalid {field} at row {row}")

@dataclass
class WarehouseItem:
    code: str
    name: str
    quantity: int
    unit_price: float

    def __post_init__(self):
        if not isinstance(self.code, str) or not self.code.strip():
            raise ValueError("code is required")
        if not isinstance(self.name, str) or not self.name.strip():
            raise ValueError("name is required")
        if type(self.quantity) is not int or self.quantity < 0:
            raise ValueError("quantity must be a nonnegative integer")
        if isinstance(self.unit_price, bool) or not isinstance(self.unit_price, (int, float)) or not 0 <= self.unit_price < float('inf'):
            raise ValueError("unit_price must be finite and nonnegative")

    @property
    def value(self) -> float:
        return self.quantity * self.unit_price


@dataclass(frozen=True)
class Product:
    """Product master data; WarehouseItem holds quantity and unit_price stock data."""
    code: str
    name: str

    def __post_init__(self):
        if not isinstance(self.code, str) or not self.code.strip():
            raise ValueError("code is required")
        if not isinstance(self.name, str) or not self.name.strip():
            raise ValueError("name is required")
