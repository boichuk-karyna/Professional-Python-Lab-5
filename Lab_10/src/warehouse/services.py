from .models import WarehouseItem, InsufficientStockError

class Warehouse:
    """Warehouse stock service, including low-stock detection and reordering."""
    def __init__(self, repository=None):
        self.items = {}
        self.repository = repository

    def add(self, item: WarehouseItem):
        if item.code in self.items:
            raise ValueError("duplicate code")
        self.items[item.code] = item
        if self.repository is not None:
            self.repository.save(item)

    def find(self, code: str):
        return self.items.get(code)

    def receive(self, code: str, amount: int):
        self._validate_amount(amount)
        item = self._required(code)
        item.quantity += amount
        return item.quantity

    def issue(self, code: str, amount: int):
        self._validate_amount(amount)
        item = self._required(code)
        if item.quantity < amount:
            raise InsufficientStockError("insufficient stock")
        item.quantity -= amount
        return item.quantity

    @staticmethod
    def _validate_amount(amount):
        if type(amount) is not int or amount <= 0:
            raise ValueError("amount must be positive integer")

    def _required(self, code):
        item = self.find(code)
        if item is None:
            raise KeyError(code)
        return item

    def total_value(self):
        return sum(item.value for item in self.items.values())

    def low_stock(self, threshold: int):
        if type(threshold) is not int or threshold < 0:
            raise ValueError("invalid threshold")
        return [item for item in self.items.values() if item.quantity <= threshold]

    def request_reorder(self, code, supplier):
        item = self._required(code)
        return supplier.reorder(item.code, item.quantity)

    async def async_reorder(self, code, provider):
        item = self._required(code)
        return await provider.reorder(item.code, item.quantity)
