from fastapi import APIRouter
from fastapi import Depends
from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.models.restaurant import Restaurant

router = APIRouter(prefix="/restaurants", tags=["Restaurants"])


# -------------------------
# CREATE RESTAURANT
# -------------------------
@router.post("/")
def create_restaurant(data: dict, db: Session = Depends(get_db)):
    restaurant = Restaurant(**data)
    db.add(restaurant)
    db.commit()
    db.refresh(restaurant)
    return restaurant


# -------------------------
# GET ALL RESTAURANTS
# -------------------------
@router.get("/")
def get_all_restaurants(db: Session = Depends(get_db)):
    return db.query(Restaurant).all()


# -------------------------
# GET RESTAURANT BY ID
# -------------------------
@router.get("/{restaurant_id}")
def get_restaurant(restaurant_id: int, db: Session = Depends(get_db)):
    restaurant = db.query(Restaurant).filter(Restaurant.id == restaurant_id).first()

    if not restaurant:
        raise HTTPException(status_code=404, detail="Restaurant not found")

    return restaurant


# -------------------------
# UPDATE RESTAURANT
# -------------------------
@router.put("/{restaurant_id}")
def update_restaurant(restaurant_id: int, data: dict, db: Session = Depends(get_db)):
    restaurant = db.query(Restaurant).filter(Restaurant.id == restaurant_id).first()

    if not restaurant:
        raise HTTPException(status_code=404, detail="Restaurant not found")

    for key, value in data.items():
        setattr(restaurant, key, value)

    db.commit()
    db.refresh(restaurant)

    return restaurant


# -------------------------
# DELETE RESTAURANT
# -------------------------
@router.delete("/{restaurant_id}")
def delete_restaurant(restaurant_id: int, db: Session = Depends(get_db)):
    restaurant = db.query(Restaurant).filter(Restaurant.id == restaurant_id).first()

    if not restaurant:
        raise HTTPException(status_code=404, detail="Restaurant not found")

    db.delete(restaurant)
    db.commit()

    return {"message": "Restaurant deleted successfully"}