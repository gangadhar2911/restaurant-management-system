from typing import Optional

from pydantic import BaseModel, ConfigDict


class InventoryBase(BaseModel):
    ingredient_name: str
    quantity: float
    unit: str
    minimum_stock: float


class InventoryCreate(InventoryBase):
    pass


class InventoryUpdate(BaseModel):
    ingredient_name: Optional[str] = None
    quantity: Optional[float] = None
    unit: Optional[str] = None
    minimum_stock: Optional[float] = None


class InventoryResponse(InventoryBase):
    id: int

    model_config = ConfigDict(from_attributes=True)