from datetime import datetime

from sqlalchemy.orm import Session

from app.models.user import User
from app.models.refresh_token import RefreshToken


class AuthRepository:

    def get_user_by_email(self, db: Session, email: str):
        return db.query(User).filter(User.email == email).first()

    def get_user_by_id(self, db: Session, user_id: int):
        return db.query(User).filter(User.id == user_id).first()

    def create_user(self, db: Session, user_data: dict) -> User:
        user = User(**user_data)
        db.add(user)
        db.commit()
        db.refresh(user)
        return user

    def save_refresh_token(self, db: Session, user_id: int, token: str, expires_at: datetime) -> RefreshToken:
        refresh_token = RefreshToken(
            user_id=user_id,
            token=token,
            expires_at=expires_at,
            is_revoked=False,
        )
        db.add(refresh_token)
        db.commit()
        db.refresh(refresh_token)
        return refresh_token

    def get_refresh_token(self, db: Session, token: str):
        return db.query(RefreshToken).filter(RefreshToken.token == token).first()

    def revoke_refresh_token(self, db: Session, token: str) -> bool:
        refresh_token = self.get_refresh_token(db, token)
        if not refresh_token:
            return False
        refresh_token.is_revoked = True
        db.commit()
        return True

    def revoke_all_user_tokens(self, db: Session, user_id: int) -> None:
        db.query(RefreshToken).filter(
            RefreshToken.user_id == user_id,
            RefreshToken.is_revoked == False  # noqa: E712
        ).update({"is_revoked": True})
        db.commit()