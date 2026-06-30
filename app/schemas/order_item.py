from decimal import Decimal
from typing import Optional

from pydantic import BaseModel, ConfigDict, Field


# ==========================================================
# BASE
# ==========================================================
class OrderItemBase(BaseModel):
    order_id: int
    menu_item_id: int
    quantity: int = Field(..., gt=0)
    price: Decimal = Field(..., gt=0)


# ==========================================================
# CREATE
# ==========================================================
class OrderItemCreate(OrderItemBase):
    pass


# ==========================================================
# UPDATE
# ==========================================================
class OrderItemUpdate(BaseModel):
    menu_item_id: Optional[int] = None
    quantity: Optional[int] = Field(None, gt=0)
    price: Optional[Decimal] = Field(None, gt=0)


# ==========================================================
# RESPONSE
# ==========================================================
class OrderItemResponse(OrderItemBase):
    id: int

    model_config = ConfigDict(from_attributes=True)