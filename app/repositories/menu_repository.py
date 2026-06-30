from sqlalchemy.orm import Session
from app.models.menu_item import MenuItem


class MenuRepository:
    def create(self, db: Session, data: dict) -> MenuItem:
        obj = MenuItem(**data)
        db.add(obj)
        db.commit()
        db.refresh(obj)
        return obj

    def get_all(self, db: Session):
        return db.query(MenuItem).all()

    def get_by_id(self, db: Session, item_id: int):
        return db.query(MenuItem).filter(MenuItem.id == item_id).first()

    def get_by_category(self, db: Session, category_id: int):
        return db.query(MenuItem).filter(MenuItem.category_id == category_id).all()

    def update(self, db: Session, obj: MenuItem, data: dict) -> MenuItem:
        for k, v in data.items():
            setattr(obj, k, v)
        db.commit()
        db.refresh(obj)
        return obj

    def delete(self, db: Session, obj: MenuItem) -> None:
        db.delete(obj)
        db.commit()