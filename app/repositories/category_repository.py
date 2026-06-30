from sqlalchemy.orm import Session
from app.models.category import Category


class CategoryRepository:
    def create(self, db: Session, data: dict) -> Category:
        obj = Category(**data)
        db.add(obj); db.commit(); db.refresh(obj)
        return obj

    def get_all(self, db: Session):
        return db.query(Category).all()

    def get_by_id(self, db: Session, category_id: int):
        return db.query(Category).filter(Category.id == category_id).first()

    def update(self, db: Session, obj: Category, data: dict) -> Category:
        for k, v in data.items():
            setattr(obj, k, v)
        db.commit(); db.refresh(obj)
        return obj

    def delete(self, db: Session, obj: Category) -> None:
        db.delete(obj); db.commit()