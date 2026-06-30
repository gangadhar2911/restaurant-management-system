from fastapi import HTTPException
from sqlalchemy.orm import Session
from app.repositories.category_repository import CategoryRepository

repo = CategoryRepository()


class CategoryService:
    @staticmethod
    def create(db: Session, data: dict):
        return repo.create(db, data)

    @staticmethod
    def get_all(db: Session):
        return repo.get_all(db)

    @staticmethod
    def get_by_id(db: Session, category_id: int):
        obj = repo.get_by_id(db, category_id)
        if not obj:
            raise HTTPException(status_code=404, detail="Category not found")
        return obj

    @staticmethod
    def update(db: Session, category_id: int, data: dict):
        obj = CategoryService.get_by_id(db, category_id)
        return repo.update(db, obj, data)

    @staticmethod
    def delete(db: Session, category_id: int):
        obj = CategoryService.get_by_id(db, category_id)
        repo.delete(db, obj)
        return {"message": "Category deleted successfully"}