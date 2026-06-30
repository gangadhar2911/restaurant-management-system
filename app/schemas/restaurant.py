from pydantic import BaseModel, Field
from typing import Optional


class RestaurantBase(BaseModel):
    name: str = Field(..., min_length=2)
    address: str
    phone: str


class RestaurantCreate(RestaurantBase):
    pass


class RestaurantUpdate(BaseModel):
    name: Optional[str] = None
    address: Optional[str] = None
    phone: Optional[str] = None


class RestaurantResponse(RestaurantBase):
    id: int

    class Config:
        from_attributes = True