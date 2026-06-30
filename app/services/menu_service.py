from fastapi import HTTPException
from sqlalchemy.orm import Session
from app.repositories.menu_repository import MenuRepository

repo = MenuRepository()


class MenuService:
    @staticmethod
    def create(db: Session, data: dict):
        return repo.create(db, data)

    @staticmethod
    def get_all(db: Session):
        return repo.get_all(db)

    @staticmethod
    def get_by_id(db: Session, item_id: int):
        obj = repo.get_by_id(db, item_id)
        if not obj:
            raise HTTPException(status_code=404, detail="Menu item not found")
        return obj

    @staticmethod
    def update(db: Session, item_id: int, data: dict):
        obj = MenuService.get_by_id(db, item_id)
        return repo.update(db, obj, data)

    @staticmethod
    def upload_image(db: Session, item_id: int, image_path: str):
        obj = MenuService.get_by_id(db, item_id)
        return repo.update(db, obj, {"image": image_path})

    @staticmethod
    def delete(db: Session, item_id: int):
        obj = MenuService.get_by_id(db, item_id)
        repo.delete(db, obj)
        return {"message": "Menu item deleted successfully"}