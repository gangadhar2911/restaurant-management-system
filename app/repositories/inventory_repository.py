from sqlalchemy.orm import Session
from app.models.ingredient import Ingredient
from app.models.inventory_transaction import InventoryTransaction


class InventoryRepository:
    def create_ingredient(self, db: Session, data: dict) -> Ingredient:
        obj = Ingredient(**data)
        db.add(obj); db.commit(); db.refresh(obj)
        return obj

    def get_all_ingredients(self, db: Session):
        return db.query(Ingredient).all()

    def get_ingredient_by_id(self, db: Session, ingredient_id: int):
        return db.query(Ingredient).filter(Ingredient.id == ingredient_id).first()

    def update_ingredient(self, db: Session, obj: Ingredient, data: dict) -> Ingredient:
        for k, v in data.items():
            setattr(obj, k, v)
        db.commit(); db.refresh(obj)
        return obj

    def delete_ingredient(self, db: Session, obj: Ingredient) -> None:
        db.delete(obj); db.commit()

    def create_transaction(self, db: Session, data: dict) -> InventoryTransaction:
        txn = InventoryTransaction(**data)
        db.add(txn); db.commit(); db.refresh(txn)
        return txn

    def get_low_stock(self, db: Session):
        return db.query(Ingredient).filter(Ingredient.current_stock <= Ingredient.min_stock_level).all()

    def get_transactions(self, db: Session):
        return db.query(InventoryTransaction).order_by(InventoryTransaction.id.desc()).all()