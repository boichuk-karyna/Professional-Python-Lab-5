import logging
from typing import Any
from fastapi import Depends, FastAPI, HTTPException, status
from pydantic import BaseModel, ConfigDict
from sqlalchemy.orm import Session

from warehouse_manager.config import get_settings
from warehouse_manager.database import SessionLocal, engine
from warehouse_manager.models import Base
from warehouse_manager.repositories import WarehouseRepository
from warehouse_manager.services import WarehouseService

settings = get_settings()

# Створення таблиць БД при старті
Base.metadata.create_all(bind=engine)

logging.basicConfig(
    level=settings.log_level,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
)
logger = logging.getLogger("warehouse_manager")
logger.info("Warehouse Manager started")

app = FastAPI(title=settings.app_name)


def get_db() -> Any:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


class ProductCreate(BaseModel):
    code: str
    name: str
    quantity: int
    price: float


class ProductResponse(BaseModel):
    id: int
    code: str
    name: str
    quantity: int
    price: float

    model_config = ConfigDict(from_attributes=True)


class OperationRequest(BaseModel):
    amount: int


class OperationResponse(BaseModel):
    id: int
    product_id: int
    operation_type: str
    amount: int
    timestamp: Any

    model_config = ConfigDict(from_attributes=True)


@app.get("/health")
async def health() -> dict[str, str]:
    return {
        "status": "ok",
        "environment": settings.environment,
    }


@app.get("/products", response_model=list[ProductResponse])
async def get_products(db: Session = Depends(get_db)) -> Any:
    service = WarehouseService(db)
    return service.list_products()


@app.post("/products", status_code=status.HTTP_201_CREATED, response_model=ProductResponse)
async def create_product(data: ProductCreate, db: Session = Depends(get_db)) -> Any:
    repo = WarehouseRepository(db)
    product = repo.create_product(data.code, data.name, data.quantity, data.price)
    return product


@app.post("/products/{id}/incoming", response_model=ProductResponse)
async def product_incoming(
    id: int, data: OperationRequest, db: Session = Depends(get_db)
) -> Any:
    service = WarehouseService(db)
    try:
        return service.register_incoming(id, data.amount)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@app.post("/products/{id}/write-off", response_model=ProductResponse)
async def product_write_off(
    id: int, data: OperationRequest, db: Session = Depends(get_db)
) -> Any:
    service = WarehouseService(db)
    try:
        return service.register_write_off(id, data.amount)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@app.get("/stock/operations", response_model=list[OperationResponse])
async def get_stock_operations(db: Session = Depends(get_db)) -> Any:
    service = WarehouseService(db)
    return service.list_operations()