from typing import List, Optional

from sqlalchemy.orm import Session
from sqlalchemy import func

from app.models.user import User


class UserRepository:

    @staticmethod
    def create(db: Session, user: User) -> User:
        db.add(user)
        db.commit()
        db.refresh(user)
        return user

    @staticmethod
    def get_all(db: Session) -> List[User]:
        return (
            db.query(User)
            .order_by(User.id.desc())
            .all()
        )

    @staticmethod
    def get_by_id(db: Session, user_id: int) -> Optional[User]:
        return (
            db.query(User)
            .filter(User.id == user_id)
            .first()
        )

    @staticmethod
    def get_by_email(db: Session, email: str) -> Optional[User]:
        return (
            db.query(User)
            .filter(func.lower(User.email) == func.lower(email))
            .first()
        )

    @staticmethod
    def exists_by_email(db: Session, email: str) -> bool:
        return (
            db.query(User)
            .filter(func.lower(User.email) == func.lower(email))
            .first()
            is not None
        )

    @staticmethod
    def update(db: Session, user: User) -> User:
        db.commit()
        db.refresh(user)
        return user

    @staticmethod
    def delete(db: Session, user: User) -> None:
        db.delete(user)
        db.commit()

    @staticmethod
    def count(db: Session) -> int:
        return db.query(User).count()

    @staticmethod
    def get_by_role(db: Session, role_id: int) -> List[User]:
        return (
            db.query(User)
            .filter(User.role_id == role_id)
            .all()
        )