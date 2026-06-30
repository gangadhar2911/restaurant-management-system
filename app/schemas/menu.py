from pydantic import BaseModel
from typing import Optional


class MenuBase(BaseModel):
    name: str
    price: float
    category_id: int
    is_available: bool = True


class MenuCreate(MenuBase):
    pass


class MenuUpdate(BaseModel):
    name: Optional[str] = None
    price: Optional[float] = None
    category_id: Optional[int] = None
    is_available: Optional[bool] = None


class MenuResponse(MenuBase):
    id: int

    class Config:
        from_attributes = True