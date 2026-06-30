from datetime import datetime
from decimal import Decimal
from typing import Optional

from pydantic import BaseModel, ConfigDict


# ==========================================================
# BASE
# ==========================================================
class OrderBase(BaseModel):
    customer_id: int
    restaurant_id: int
    table_id: Optional[int] = None
    order_status: str = "Pending"
    total_amount: Decimal = Decimal("0.00")
    is_paid: bool = False


# ==========================================================
# CREATE
# ==========================================================
class OrderCreate(OrderBase):
    pass


# ==========================================================
# UPDATE
# ==========================================================
class OrderUpdate(BaseModel):
    customer_id: Optional[int] = None
    restaurant_id: Optional[int] = None
    table_id: Optional[int] = None
    order_status: Optional[str] = None
    total_amount: Optional[Decimal] = None
    is_paid: Optional[bool] = None


# ==========================================================
# RESPONSE
# ==========================================================
class OrderResponse(OrderBase):
    id: int
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)