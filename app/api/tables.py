from fastapi import APIRouter
from fastapi import Depends
from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.models.restaurant_table import RestaurantTable

router = APIRouter(prefix="/tables", tags=["Tables"])


# -------------------------
# ADD TABLE
# -------------------------
@router.post("/")
def add_table(data: dict, db: Session = Depends(get_db)):
    table = RestaurantTable(**data)
    db.add(table)
    db.commit()
    db.refresh(table)
    return table


# -------------------------
# GET ALL TABLES
# -------------------------
@router.get("/")
def get_all_tables(db: Session = Depends(get_db)):
    return db.query(RestaurantTable).all()


# -------------------------
# GET TABLE BY ID
# -------------------------
@router.get("/{table_id}")
def get_table(table_id: int, db: Session = Depends(get_db)):
    table = db.query(RestaurantTable).filter(RestaurantTable.id == table_id).first()

    if not table:
        raise HTTPException(status_code=404, detail="Table not found")

    return table


# -------------------------
# UPDATE TABLE
# -------------------------
@router.put("/{table_id}")
def update_table(table_id: int, data: dict, db: Session = Depends(get_db)):
    table = db.query(RestaurantTable).filter(RestaurantTable.id == table_id).first()

    if not table:
        raise HTTPException(status_code=404, detail="Table not found")

    for key, value in data.items():
        setattr(table, key, value)

    db.commit()
    db.refresh(table)

    return table


# -------------------------
# DELETE TABLE
# -------------------------
@router.delete("/{table_id}")
def delete_table(table_id: int, db: Session = Depends(get_db)):
    table = db.query(RestaurantTable).filter(RestaurantTable.id == table_id).first()

    if not table:
        raise HTTPException(status_code=404, detail="Table not found")

    db.delete(table)
    db.commit()

    return {"message": "Table deleted successfully"}


# -------------------------
# VIEW TABLE STATUS
# -------------------------
@router.get("/status/all")
def get_table_status(db: Session = Depends(get_db)):
    return db.query(RestaurantTable.id,
                    RestaurantTable.table_number,
                    RestaurantTable.status,
                    RestaurantTable.capacity).all()


# -------------------------
# CHANGE TABLE STATUS
# -------------------------
@router.patch("/{table_id}/status")
def update_table_status(table_id: int, status: str, db: Session = Depends(get_db)):
    table = db.query(RestaurantTable).filter(RestaurantTable.id == table_id).first()

    if not table:
        raise HTTPException(status_code=404, detail="Table not found")

    table.status = status
    db.commit()
    db.refresh(table)

    return {
        "message": "Table status updated",
        "table_id": table.id,
        "status": table.status
    }