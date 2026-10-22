import datetime

from sqlalchemy import Column, DateTime, Float, ForeignKey, Integer, String
from sqlalchemy.orm import DeclarativeBase, relationship


class Base(DeclarativeBase):
    pass


class ProductModel(Base):
    __tablename__ = "products"

    id = Column(Integer, primary_key=True, index=True)
    code = Column(String, unique=True, index=True, nullable=False)
    name = Column(String, nullable=False)
    quantity = Column(Integer, default=0, nullable=False)
    price = Column(Float, nullable=False)

    operations = relationship(
        "StockOperationModel", back_populates="product", cascade="all, delete-orphan"
    )


class StockOperationModel(Base):
    __tablename__ = "stock_operations"

    id = Column(Integer, primary_key=True, index=True)
    product_id = Column(Integer, ForeignKey("products.id"), nullable=False)
    operation_type = Column(String, nullable=False)  # "incoming" або "write-off"
    amount = Column(Integer, nullable=False)
    timestamp = Column(DateTime, default=datetime.datetime.utcnow, nullable=False)

    product = relationship("ProductModel", back_populates="operations")
