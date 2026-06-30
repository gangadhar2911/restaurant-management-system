from fastapi import APIRouter
from fastapi import Depends
from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.models.user import User
from app.services.auth_service import AuthService

router = APIRouter(prefix="/users", tags=["Users"])

auth_service = AuthService()


# -------------------------
# CREATE USER (ADMIN ONLY STYLE)
# -------------------------
@router.post("/")
def create_user(data: dict, db: Session = Depends(get_db)):

    existing_user = db.query(User).filter(
        User.email == data.get("email")
    ).first()

    if existing_user:
        raise HTTPException(status_code=400, detail="User already exists")

    # Hash password before saving
    data["password"] = auth_service.hash_password(data["password"])

    user = User(**data)

    db.add(user)
    db.commit()
    db.refresh(user)

    return user


# -------------------------
# GET ALL USERS
# -------------------------
@router.get("/")
def get_users(db: Session = Depends(get_db)):

    return db.query(User).all()


# -------------------------
# GET USER BY ID
# -------------------------
@router.get("/{user_id}")
def get_user(user_id: int, db: Session = Depends(get_db)):

    user = db.query(User).filter(User.id == user_id).first()

    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    return user


# -------------------------
# UPDATE USER
# -------------------------
@router.put("/{user_id}")
def update_user(user_id: int, data: dict, db: Session = Depends(get_db)):

    user = db.query(User).filter(User.id == user_id).first()

    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    for key, value in data.items():
        if key == "password":
            value = auth_service.hash_password(value)

        setattr(user, key, value)

    db.commit()
    db.refresh(user)

    return user


# -------------------------
# DELETE USER
# -------------------------
@router.delete("/{user_id}")
def delete_user(user_id: int, db: Session = Depends(get_db)):

    user = db.query(User).filter(User.id == user_id).first()

    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    db.delete(user)
    db.commit()

    return {"message": "User deleted successfully"}