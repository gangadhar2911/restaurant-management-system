from pydantic import BaseModel
from typing import Optional


class ReservationBase(BaseModel):
    user_id: int
    table_id: int
    reservation_time: str
    guests_count: int


class ReservationCreate(ReservationBase):
    pass


class ReservationUpdate(BaseModel):
    status: Optional[str] = None


class ReservationResponse(ReservationBase):
    id: int
    status: str

    class Config:
        from_attributes = True