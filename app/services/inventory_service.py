from fastapi import HTTPException
from sqlalchemy.orm import Session
from app.repositories.inventory_repository import InventoryRepository

repo = InventoryRepository()


class InventoryService:
    @staticmethod
    def add_ingredient(db: Session, data: dict):
        return repo.create_ingredient(db, data)

    @staticmethod
    def get_all(db: Session):
        return repo.get_all_ingredients(db)

    @staticmethod
    def get_by_id(db: Session, ingredient_id: int):
        obj = repo.get_ingredient_by_id(db, ingredient_id)
        if not obj:
            raise HTTPException(status_code=404, detail="Ingredient not found")
        return obj

    @staticmethod
    def update(db: Session, ingredient_id: int, data: dict):
        obj = InventoryService.get_by_id(db, ingredient_id)
        return repo.update_ingredient(db, obj, data)

    @staticmethod
    def delete(db: Session, ingredient_id: int):
        obj = InventoryService.get_by_id(db, ingredient_id)
        repo.delete_ingredient(db, obj)
        return {"message": "Ingredient deleted successfully"}

    @staticmethod
    def stock_in(db: Session, ingredient_id: int, quantity: float, note: str = ""):
        obj = InventoryService.get_by_id(db, ingredient_id)
        obj.current_stock = float(obj.current_stock) + quantity
        repo.create_transaction(db, {
            "ingredient_id": ingredient_id, "transaction_type": "STOCK_IN",
            "quantity": quantity, "note": note,
        })
        db.commit(); db.refresh(obj)
        return {"message": "Stock added", "current_stock": obj.current_stock}

    @staticmethod
    def stock_out(db: Session, ingredient_id: int, quantity: float, note: str = ""):
        obj = InventoryService.get_by_id(db, ingredient_id)
        if float(obj.current_stock) < quantity:
            raise HTTPException(status_code=400, detail="Insufficient stock")
        obj.current_stock = float(obj.current_stock) - quantity
        repo.create_transaction(db, {
            "ingredient_id": ingredient_id, "transaction_type": "STOCK_OUT",
            "quantity": quantity, "note": note,
        })
        db.commit(); db.refresh(obj)
        return {"message": "Stock reduced", "current_stock": obj.current_stock}

    @staticmethod
    def low_stock_alert(db: Session):
        return repo.get_low_stock(db)

    @staticmethod
    def get_transactions(db: Session):
        return repo.get_transactions(db)