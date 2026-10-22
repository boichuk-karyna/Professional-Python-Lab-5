from __future__ import annotations
from typing import Optional
from pydantic import BaseModel, Field


class WarehouseItemBase(BaseModel):
    code: str = Field(..., description="Унікальний код товару")
    name: str = Field(..., description="Назва товару")
    quantity: int = Field(..., ge=0, description="Кількість на складі")
    price: float = Field(..., gt=0, description="Ціна за одиницю")
    category: str = Field(default="General", description="Категорія товару")


class WarehouseItemCreate(WarehouseItemBase):
    pass


class WarehouseItemUpdate(BaseModel):
    name: Optional[str] = None
    quantity: Optional[int] = Field(None, ge=0)
    price: Optional[float] = Field(None, gt=0)
    category: Optional[str] = None


class WarehouseItem(WarehouseItemBase):
    model_config = {"from_attributes": True}


class StockMovement(BaseModel):
    code: str
    change: int  # Додатне значення — надходження, від'ємне — списання