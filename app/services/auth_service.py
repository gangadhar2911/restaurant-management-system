from datetime import datetime, timedelta

from sqlalchemy.orm import Session

from app.core.config import settings
from app.core.security import hash_password, verify_password
from app.utils.jwt import create_access_token, create_refresh_token
from app.repositories.auth_repository import AuthRepository
from app.repositories.role_repository import RoleRepository
from jose import jwt, JWTError


class AuthService:

    def __init__(self):
        self.auth_repo = AuthRepository()
        self.role_repo = RoleRepository()

    def hash_password(self, password: str) -> str:
        return hash_password(password)

    def verify_password(self, plain_password: str, hashed_password: str) -> bool:
        return verify_password(plain_password, hashed_password)

    def register_user(self, db: Session, user_data: dict):
        existing = self.auth_repo.get_user_by_email(db, user_data["email"])
        if existing:
            raise ValueError("A user with this email already exists")

        role = self.role_repo.get_role_by_id(db, user_data["role_id"])
        if not role:
            raise ValueError("Invalid role_id")

        user_data = dict(user_data)
        user_data["password"] = self.hash_password(user_data["password"])

        return self.auth_repo.create_user(db, user_data)

    def login_user(self, db: Session, email: str, password: str) -> dict:
        user = self.auth_repo.get_user_by_email(db, email)

        if not user or not self.verify_password(password, user.password):
            raise ValueError("Invalid email or password")

        if not user.is_active:
            raise ValueError("User account is inactive")

        role_name = user.role.role_name if user.role else None
        token_payload = {"user_id": user.id, "email": user.email, "role": role_name}

        access_token = create_access_token(token_payload)
        refresh_token = create_refresh_token({"user_id": user.id})

        expires_at = datetime.utcnow() + timedelta(days=settings.REFRESH_TOKEN_EXPIRE_DAYS)
        self.auth_repo.save_refresh_token(db, user.id, refresh_token, expires_at)

        return {
            "access_token": access_token,
            "refresh_token": refresh_token,
            "token_type": "bearer",
        }

    def refresh_access_token(self, db: Session, refresh_token: str) -> dict:
        stored_token = self.auth_repo.get_refresh_token(db, refresh_token)

        if not stored_token or stored_token.is_revoked:
            raise ValueError("Invalid or revoked refresh token")

        if stored_token.expires_at < datetime.utcnow():
            raise ValueError("Refresh token expired")

        try:
            payload = jwt.decode(
                refresh_token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM]
            )
        except JWTError:
            raise ValueError("Invalid refresh token")

        user = self.auth_repo.get_user_by_id(db, payload.get("user_id"))
        if not user:
            raise ValueError("User not found")

        role_name = user.role.role_name if user.role else None
        new_access_token = create_access_token(
            {"user_id": user.id, "email": user.email, "role": role_name}
        )

        return {"access_token": new_access_token, "token_type": "bearer"}

    def logout(self, db: Session, refresh_token: str) -> dict:
        revoked = self.auth_repo.revoke_refresh_token(db, refresh_token)
        if not revoked:
            raise ValueError("Invalid refresh token")
        return {"message": "Logged out successfully"}