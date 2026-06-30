from sqlalchemy.orm import Session
from app.models.restaurant import Restaurant


class RestaurantRepository:
    def create(self, db: Session, data: dict) -> Restaurant:
        obj = Restaurant(**data)
        db.add(obj); db.commit(); db.refresh(obj)
        return obj

    def get_all(self, db: Session):
        return db.query(Restaurant).all()

    def get_by_id(self, db: Session, restaurant_id: int):
        return db.query(Restaurant).filter(Restaurant.id == restaurant_id).first()

    def update(self, db: Session, obj: Restaurant, data: dict) -> Restaurant:
        for k, v in data.items():
            setattr(obj, k, v)
        db.commit(); db.refresh(obj)
        return obj

    def delete(self, db: Session, obj: Restaurant) -> None:
        db.delete(obj); db.commit()