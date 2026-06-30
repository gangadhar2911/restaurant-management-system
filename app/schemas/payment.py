from typing import Optional

from pydantic import BaseModel, ConfigDict


# ==========================================================
# BASE
# ==========================================================
class PaymentBase(BaseModel):
    bill_id: int
    payment_method: str
    amount_paid: float
    transaction_id: str


# ==========================================================
# CREATE
# ==========================================================
class PaymentCreate(PaymentBase):
    pass


# ==========================================================
# UPDATE
# ==========================================================
class PaymentUpdate(BaseModel):
    bill_id: Optional[int] = None
    payment_method: Optional[str] = None
    amount_paid: Optional[float] = None
    transaction_id: Optional[str] = None
    payment_status: Optional[str] = None


# ==========================================================
# RESPONSE
# ==========================================================
class PaymentResponse(PaymentBase):
    id: int
    payment_status: str

    model_config = ConfigDict(from_attributes=True)