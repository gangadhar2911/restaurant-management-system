from pydantic import BaseModel, EmailStr


# ---------- Register ----------
class RegisterRequest(BaseModel):
    full_name: str
    email: EmailStr
    phone: str | None = None
    password: str
    role_id: int


# ---------- Login ----------
class LoginRequest(BaseModel):
    email: EmailStr
    password: str


# ---------- Refresh Token ----------
class RefreshRequest(BaseModel):
    refresh_token: str


# ---------- Auth Response ----------
class AuthResponse(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"