from sqlalchemy.orm import Session

from warehouse_manager.models import ProductModel, StockOperationModel


class WarehouseRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_all_products(self) -> list[ProductModel]:
        return self.db.query(ProductModel).all()

    def get_product_by_id(self, product_id: int) -> ProductModel | None:
        return self.db.query(ProductModel).filter(ProductModel.id == product_id).first()

    def create_product(
        self, code: str, name: str, quantity: int, price: float
    ) -> ProductModel:
        product = ProductModel(code=code, name=name, quantity=quantity, price=price)
        self.db.add(product)
        self.db.commit()
        self.db.refresh(product)
        return product

    def add_incoming(self, product_id: int, amount: int) -> ProductModel:
        product = self.get_product_by_id(product_id)
        if product:
            product.quantity += amount
            operation = StockOperationModel(
                product_id=product_id, operation_type="incoming", amount=amount
            )
            self.db.add(operation)
            self.db.commit()
            self.db.refresh(product)
        return product

    def write_off(self, product_id: int, amount: int) -> ProductModel | None:
        product = self.get_product_by_id(product_id)
        if product and product.quantity >= amount:
            product.quantity -= amount
            operation = StockOperationModel(
                product_id=product_id, operation_type="write-off", amount=amount
            )
            self.db.add(operation)
            self.db.commit()
            self.db.refresh(product)
            return product
        return None

    def get_operations(self) -> list[StockOperationModel]:
        return self.db.query(StockOperationModel).all()
