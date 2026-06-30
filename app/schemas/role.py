from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field


# ==========================================
# BASE ROLE
# ==========================================
class RoleBase(BaseModel):
    role_name: str = Field(
        ...,
        min_length=2,
        max_length=50,
        description="Role name"
    )


# ==========================================
# CREATE ROLE
# ==========================================
class RoleCreate(RoleBase):
    pass


# ==========================================
# UPDATE ROLE
# ==========================================
class RoleUpdate(BaseModel):
    role_name: Optional[str] = Field(
        None,
        min_length=2,
        max_length=50
    )


# ==========================================
# RESPONSE ROLE
# ==========================================
class RoleResponse(RoleBase):
    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True