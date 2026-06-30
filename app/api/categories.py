from fastapi import APIRouter
from fastapi import Depends
from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.models.category import Category

router = APIRouter(prefix="/categories", tags=["Categories"])


# -------------------------
# CREATE CATEGORY
# -------------------------
@router.post("/")
def create_category(data: dict, db: Session = Depends(get_db)):
    category = Category(**data)
    db.add(category)
    db.commit()
    db.refresh(category)
    return category


# -------------------------
# GET ALL CATEGORIES
# -------------------------
@router.get("/")
def get_all_categories(db: Session = Depends(get_db)):
    return db.query(Category).all()


# -------------------------
# GET CATEGORY BY ID
# -------------------------
@router.get("/{category_id}")
def get_category(category_id: int, db: Session = Depends(get_db)):
    category = db.query(Category).filter(Category.id == category_id).first()

    if not category:
        raise HTTPException(status_code=404, detail="Category not found")

    return category


# -------------------------
# UPDATE CATEGORY
# -------------------------
@router.put("/{category_id}")
def update_category(category_id: int, data: dict, db: Session = Depends(get_db)):
    category = db.query(Category).filter(Category.id == category_id).first()

    if not category:
        raise HTTPException(status_code=404, detail="Category not found")

    for key, value in data.items():
        setattr(category, key, value)

    db.commit()
    db.refresh(category)

    return category


# -------------------------
# DELETE CATEGORY
# -------------------------
@router.delete("/{category_id}")
def delete_category(category_id: int, db: Session = Depends(get_db)):
    category = db.query(Category).filter(Category.id == category_id).first()

    if not category:
        raise HTTPException(status_code=404, detail="Category not found")

    db.delete(category)
    db.commit()

    return {"message": "Category deleted successfully"}