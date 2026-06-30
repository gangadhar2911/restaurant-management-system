from typing import List, Optional

from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.models.user import User
from app.models.role import Role

from app.schemas.user import UserCreate, UserUpdate

from app.core.security import hash_password


class UserService:

    @staticmethod
    def create_user(db: Session, user: UserCreate) -> User:
        """
        Create a new user.
        """

        existing_email = (
            db.query(User)
            .filter(User.email == user.email)
            .first()
        )

        if existing_email:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Email already registered."
            )

        role = (
            db.query(Role)
            .filter(Role.id == user.role_id)
            .first()
        )

        if not role:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Role not found."
            )

        new_user = User(
            full_name=user.full_name,
            email=user.email,
            password=hash_password(user.password),
            role_id=user.role_id
        )

        db.add(new_user)
        db.commit()
        db.refresh(new_user)

        return new_user

    @staticmethod
    def get_all_users(db: Session) -> List[User]:
        """
        Get all users.
        """

        return (
            db.query(User)
            .order_by(User.id.desc())
            .all()
        )

    @staticmethod
    def get_user_by_id(db: Session, user_id: int) -> User:
        """
        Get user by ID.
        """

        user = (
            db.query(User)
            .filter(User.id == user_id)
            .first()
        )

        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found."
            )

        return user

    @staticmethod
    def get_user_by_email(db: Session, email: str) -> Optional[User]:
        """
        Get user using email.
        """

        return (
            db.query(User)
            .filter(User.email == email)
            .first()
        )

    @staticmethod
    def update_user(
        db: Session,
        user_id: int,
        user_data: UserUpdate
    ) -> User:
        """
        Update user.
        """

        user = (
            db.query(User)
            .filter(User.id == user_id)
            .first()
        )

        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found."
            )

        update_data = user_data.model_dump(exclude_unset=True)

        if "email" in update_data:

            existing = (
                db.query(User)
                .filter(
                    User.email == update_data["email"],
                    User.id != user_id
                )
                .first()
            )

            if existing:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Email already exists."
                )

        if "role_id" in update_data:

            role = (
                db.query(Role)
                .filter(Role.id == update_data["role_id"])
                .first()
            )

            if not role:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="Role not found."
                )

        if "password" in update_data:
            update_data["password"] = hash_password(
                update_data["password"]
            )

        for key, value in update_data.items():
            setattr(user, key, value)

        db.commit()
        db.refresh(user)

        return user

    @staticmethod
    def delete_user(
        db: Session,
        user_id: int
    ) -> dict:
        """
        Delete user.
        """

        user = (
            db.query(User)
            .filter(User.id == user_id)
            .first()
        )

        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found."
            )

        db.delete(user)
        db.commit()

        return {
            "message": "User deleted successfully."
        }

    @staticmethod
    def activate_user(
        db: Session,
        user_id: int
    ) -> User:

        user = UserService.get_user_by_id(db, user_id)

        if hasattr(user, "is_active"):
            user.is_active = True

        db.commit()
        db.refresh(user)

        return user

    @staticmethod
    def deactivate_user(
        db: Session,
        user_id: int
    ) -> User:

        user = UserService.get_user_by_id(db, user_id)

        if hasattr(user, "is_active"):
            user.is_active = False

        db.commit()
        db.refresh(user)

        return user

    @staticmethod
    def count_users(db: Session) -> int:

        return db.query(User).count()