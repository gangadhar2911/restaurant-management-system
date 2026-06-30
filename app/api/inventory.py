from fastapi import APIRouter
from fastapi import Depends
from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.models.ingredient import Ingredient
from app.models.inventory_transaction import InventoryTransaction

router = APIRouter(prefix="/inventory", tags=["Inventory"])


# -------------------------
# ADD INGREDIENT
# -------------------------
@router.post("/ingredient")
def add_ingredient(data: dict, db: Session = Depends(get_db)):

    ingredient = Ingredient(**data)

    db.add(ingredient)
    db.commit()
    db.refresh(ingredient)

    return ingredient


# -------------------------
# GET ALL INGREDIENTS
# -------------------------
@router.get("/ingredient")
def get_all_ingredients(db: Session = Depends(get_db)):

    return db.query(Ingredient).all()


# -------------------------
# UPDATE INGREDIENT
# -------------------------
@router.put("/ingredient/{ingredient_id}")
def update_ingredient(ingredient_id: int, data: dict, db: Session = Depends(get_db)):

    ingredient = db.query(Ingredient).filter(
        Ingredient.id == ingredient_id
    ).first()

    if not ingredient:
        raise HTTPException(status_code=404, detail="Ingredient not found")

    for key, value in data.items():
        setattr(ingredient, key, value)

    db.commit()
    db.refresh(ingredient)

    return ingredient


# -------------------------
# DELETE INGREDIENT
# -------------------------
@router.delete("/ingredient/{ingredient_id}")
def delete_ingredient(ingredient_id: int, db: Session = Depends(get_db)):

    ingredient = db.query(Ingredient).filter(
        Ingredient.id == ingredient_id
    ).first()

    if not ingredient:
        raise HTTPException(status_code=404, detail="Ingredient not found")

    db.delete(ingredient)
    db.commit()

    return {"message": "Ingredient deleted successfully"}


# -------------------------
# STOCK IN (ADD STOCK)
# -------------------------
@router.post("/stock-in/{ingredient_id}")
def stock_in(ingredient_id: int, data: dict, db: Session = Depends(get_db)):

    ingredient = db.query(Ingredient).filter(
        Ingredient.id == ingredient_id
    ).first()

    if not ingredient:
        raise HTTPException(status_code=404, detail="Ingredient not found")

    quantity = float(data.get("quantity", 0))

    ingredient.current_stock += quantity

    transaction = InventoryTransaction(
        ingredient_id=ingredient_id,
        transaction_type="STOCK_IN",
        quantity=quantity,
        note=data.get("note", "")
    )

    db.add(transaction)
    db.commit()
    db.refresh(ingredient)

    return {
        "message": "Stock added successfully",
        "current_stock": ingredient.current_stock
    }


# -------------------------
# STOCK OUT (USE STOCK)
# -------------------------
@router.post("/stock-out/{ingredient_id}")
def stock_out(ingredient_id: int, data: dict, db: Session = Depends(get_db)):

    ingredient = db.query(Ingredient).filter(
        Ingredient.id == ingredient_id
    ).first()

    if not ingredient:
        raise HTTPException(status_code=404, detail="Ingredient not found")

    quantity = float(data.get("quantity", 0))

    if ingredient.current_stock < quantity:
        raise HTTPException(status_code=400, detail="Insufficient stock")

    ingredient.current_stock -= quantity

    transaction = InventoryTransaction(
        ingredient_id=ingredient_id,
        transaction_type="STOCK_OUT",
        quantity=quantity,
        note=data.get("note", "")
    )

    db.add(transaction)
    db.commit()
    db.refresh(ingredient)

    return {
        "message": "Stock reduced successfully",
        "current_stock": ingredient.current_stock
    }


# -------------------------
# LOW STOCK ALERT
# -------------------------
@router.get("/low-stock")
def low_stock_alert(db: Session = Depends(get_db)):

    return db.query(Ingredient).filter(
        Ingredient.current_stock <= Ingredient.min_stock_level
    ).all()


# -------------------------
# TRANSACTION HISTORY
# -------------------------
@router.get("/transactions")
def get_transactions(db: Session = Depends(get_db)):

    return db.query(InventoryTransaction).order_by(
        InventoryTransaction.id.desc()
    ).all()