from datetime import datetime
from pydantic import BaseModel


# ---------- Token Data ----------
class TokenData(BaseModel):
    user_id: int | None = None
    email: str | None = None
    role_id: int | None = None


# ---------- Access Token Response ----------
class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"


# ---------- Refresh Token Response ----------
class RefreshTokenResponse(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"


# ---------- Stored Refresh Token ----------
class RefreshTokenSchema(BaseModel):
    id: int
    user_id: int
    token: str
    is_revoked: bool
    expires_at: datetime

    class Config:
        from_attributes = True