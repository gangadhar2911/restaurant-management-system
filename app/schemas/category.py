from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field


# ==========================================================
# BASE CATEGORY
# ==========================================================
class CategoryBase(BaseModel):
    restaurant_id: int

    category_name: str = Field(
        ...,
        min_length=2,
        max_length=100
    )

    description: Optional[str] = Field(
        default=None,
        max_length=255
    )

    is_active: bool = True


# ==========================================================
# CREATE
# ==========================================================
class CategoryCreate(CategoryBase):
    pass


# ==========================================================
# UPDATE
# ==========================================================
class CategoryUpdate(BaseModel):
    category_name: Optional[str] = Field(
        default=None,
        min_length=2,
        max_length=100
    )

    description: Optional[str] = None

    is_active: Optional[bool] = None


# ==========================================================
# RESPONSE
# ==========================================================
class CategoryResponse(CategoryBase):
    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True