from pydantic import BaseModel
from typing import Optional


class TableBase(BaseModel):
    table_number: int
    capacity: int
    status: str = "Available"


class TableCreate(TableBase):
    pass


class TableUpdate(BaseModel):
    table_number: Optional[int] = None
    capacity: Optional[int] = None
    status: Optional[str] = None


class TableResponse(TableBase):
    id: int

    class Config:
        from_attributes = True