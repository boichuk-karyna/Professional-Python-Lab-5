from sqlalchemy.orm import Session

from warehouse_manager.models import ProductModel, StockOperationModel
from warehouse_manager.repositories import WarehouseRepository


class WarehouseService:
    def __init__(self, db: Session):
        self.repo = WarehouseRepository(db)

    def list_products(self) -> list[ProductModel]:
        return self.repo.get_all_products()

    def register_incoming(self, product_id: int, amount: int) -> ProductModel:
        if amount <= 0:
            raise ValueError("Кількість для надходження має бути більше нуля.")
        product = self.repo.add_incoming(product_id, amount)
        if not product:
            raise ValueError("Товар не знайдено.")
        return product

    def register_write_off(self, product_id: int, amount: int) -> ProductModel:
        if amount <= 0:
            raise ValueError("Кількість для списання має бути більше нуля.")
        product = self.repo.write_off(product_id, amount)
        if not product:
            raise ValueError(
                "Товар не знайдено або недостатньо коштів/запасів на складі (надмірне списання)."
            )
        return product

    def list_operations(self) -> list[StockOperationModel]:
        return self.repo.get_operations()
