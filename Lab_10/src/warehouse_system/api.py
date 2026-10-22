from fastapi import FastAPI, HTTPException, status
from warehouse_system.repositories import WarehouseRepository
from warehouse_system.services import WarehouseService
from warehouse_system.models import (
    WarehouseItem,
    WarehouseItemCreate,
    WarehouseItemUpdate,
    StockMovement
)

app = FastAPI(title="Warehouse Management System API", version="0.1.0")

repo = WarehouseRepository()
service = WarehouseService(repo)


@app.post("/items", response_model=WarehouseItem, status_code=status.HTTP_201_CREATED)
def create_item(item: WarehouseItemCreate):
    try:
        return service.add_item(item)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@app.get("/items", response_model=list[WarehouseItem])
def get_all_items():
    return service.list_items()


@app.get("/items/{code}", response_model=WarehouseItem)
def get_item(code: str):
    item = service.get_item(code)
    if not item:
        raise HTTPException(status_code=404, detail="Товар не знайдено.")
    return item


@app.patch("/items/{code}", response_model=WarehouseItem)
def update_item(code: str, update_data: WarehouseItemUpdate):
    item = service.update_item(code, update_data)
    if not item:
        raise HTTPException(status_code=404, detail="Товар не знайдено.")
    return item


@app.post("/items/movement", response_model=WarehouseItem)
def stock_movement(movement: StockMovement):
    try:
        item = service.record_movement(movement.code, movement.change)
        if not item:
            raise HTTPException(status_code=404, detail="Товар не знайдено.")
        return item
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@app.get("/analytics/stats")
def get_warehouse_stats():
    return service.get_stats()