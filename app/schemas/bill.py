from typing import Optional

from pydantic import BaseModel, ConfigDict


# ==========================================================
# BASE
# ==========================================================
class BillBase(BaseModel):
    order_id: int
    subtotal: float
    tax_amount: float
    discount_amount: float
    total_amount: float


# ==========================================================
# CREATE
# ==========================================================
class BillCreate(BillBase):
    pass


# ==========================================================
# UPDATE
# ==========================================================
class BillUpdate(BaseModel):
    order_id: Optional[int] = None
    subtotal: Optional[float] = None
    tax_amount: Optional[float] = None
    discount_amount: Optional[float] = None
    total_amount: Optional[float] = None
    payment_status: Optional[str] = None
    is_paid: Optional[bool] = None


# ==========================================================
# RESPONSE
# ==========================================================
class BillResponse(BillBase):
    id: int
    payment_status: str
    is_paid: bool

    model_config = ConfigDict(from_attributes=True)