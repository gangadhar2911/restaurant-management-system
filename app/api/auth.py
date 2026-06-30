from fastapi import APIRouter
from fastapi import Depends
from fastapi import HTTPException
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.schemas.auth import LoginRequest
from app.schemas.auth import RegisterRequest
from app.schemas.auth import AuthResponse
from app.schemas.auth import RefreshRequest
from app.services.auth_service import AuthService
from app.repositories.auth_repository import AuthRepository

router = APIRouter(prefix="/auth", tags=["Authentication"])

auth_service = AuthService()
auth_repo = AuthRepository()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")


# -------------------------
# REGISTER
# -------------------------
@router.post("/register", response_model=dict)
def register(user: RegisterRequest, db: Session = Depends(get_db)):
    try:
        new_user = auth_service.register_user(db, user.dict())
        return {
            "message": "User registered successfully",
            "user_id": new_user.id
        }
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


# -------------------------
# LOGIN
# -------------------------
@router.post("/login", response_model=AuthResponse)
def login(user: LoginRequest, db: Session = Depends(get_db)):
    try:
        tokens = auth_service.login_user(db, user.email, user.password)
        return tokens
    except Exception as e:
        raise HTTPException(status_code=401, detail=str(e))


# -------------------------
# REFRESH TOKEN
# -------------------------
@router.post("/refresh", response_model=dict)
def refresh_token(data: RefreshRequest, db: Session = Depends(get_db)):
    try:
        new_token = auth_service.refresh_access_token(db, data.refresh_token)
        return new_token
    except Exception as e:
        raise HTTPException(status_code=401, detail=str(e))


# -------------------------
# LOGOUT
# -------------------------
@router.post("/logout")
def logout(data: RefreshRequest, db: Session = Depends(get_db)):
    try:
        result = auth_service.logout(db, data.refresh_token)
        return result
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


# -------------------------
# GET CURRENT USER (ME)
# -------------------------
@router.get("/me")
def get_me(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    try:
        # decode token manually (simple version)
        import jwt
        from app.core.config import settings

        payload = jwt.decode(
            token,
            settings.SECRET_KEY,
            algorithms=[settings.ALGORITHM]
        )

        user_id = payload.get("user_id")

        user = auth_repo.get_user_by_id(db, user_id)

        if not user:
            raise HTTPException(status_code=404, detail="User not found")

        return {
            "id": user.id,
            "full_name": user.full_name,
            "email": user.email,
            "role_id": user.role_id,
            "is_active": user.is_active
        }

    except Exception:
        raise HTTPException(status_code=401, detail="Invalid token")