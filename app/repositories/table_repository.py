from sqlalchemy.orm import Session
from app.models.restaurant_table import RestaurantTable


class TableRepository:
    def create(self, db: Session, data: dict) -> RestaurantTable:
        obj = RestaurantTable(**data)
        db.add(obj); db.commit(); db.refresh(obj)
        return obj

    def get_all(self, db: Session):
        return db.query(RestaurantTable).all()

    def get_by_id(self, db: Session, table_id: int):
        return db.query(RestaurantTable).filter(RestaurantTable.id == table_id).first()

    def get_by_restaurant(self, db: Session, restaurant_id: int):
        return db.query(RestaurantTable).filter(RestaurantTable.restaurant_id == restaurant_id).all()

    def update(self, db: Session, obj: RestaurantTable, data: dict) -> RestaurantTable:
        for k, v in data.items():
            setattr(obj, k, v)
        db.commit(); db.refresh(obj)
        return obj

    def delete(self, db: Session, obj: RestaurantTable) -> None:
        db.delete(obj); db.commit()