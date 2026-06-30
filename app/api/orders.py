from fastapi import APIRouter
from fastapi import Depends
from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.models.order import Order
from app.models.order_item import OrderItem

router = APIRouter(prefix="/orders", tags=["Orders"])


# -------------------------
# CREATE ORDER (CART START)
# -------------------------
@router.post("/")
def create_order(data: dict, db: Session = Depends(get_db)):
    order = Order(**data)
    db.add(order)
    db.commit()
    db.refresh(order)
    return order


# -------------------------
# ADD ITEM TO ORDER
# -------------------------
@router.post("/{order_id}/items")
def add_order_item(order_id: int, data: dict, db: Session = Depends(get_db)):

    order = db.query(Order).filter(Order.id == order_id).first()

    if not order:
        raise HTTPException(status_code=404, detail="Order not found")

    item = OrderItem(order_id=order_id, **data)

    db.add(item)
    db.commit()
    db.refresh(item)

    return item


# -------------------------
# GET ALL ORDERS
# -------------------------
@router.get("/")
def get_all_orders(db: Session = Depends(get_db)):
    return db.query(Order).all()


# -------------------------
# GET ORDER BY ID (WITH ITEMS)
# -------------------------
@router.get("/{order_id}")
def get_order(order_id: int, db: Session = Depends(get_db)):

    order = db.query(Order).filter(Order.id == order_id).first()

    if not order:
        raise HTTPException(status_code=404, detail="Order not found")

    items = db.query(OrderItem).filter(OrderItem.order_id == order_id).all()

    return {
        "order": order,
        "items": items
    }


# -------------------------
# UPDATE ORDER STATUS
# -------------------------
@router.patch("/{order_id}/status")
def update_order_status(order_id: int, status: str, db: Session = Depends(get_db)):

    order = db.query(Order).filter(Order.id == order_id).first()

    if not order:
        raise HTTPException(status_code=404, detail="Order not found")

    order.order_status = status

    db.commit()
    db.refresh(order)

    return {
        "message": "Order status updated",
        "order_id": order.id,
        "status": order.order_status
    }


# -------------------------
# CANCEL ORDER
# -------------------------
@router.delete("/{order_id}")
def cancel_order(order_id: int, db: Session = Depends(get_db)):

    order = db.query(Order).filter(Order.id == order_id).first()

    if not order:
        raise HTTPException(status_code=404, detail="Order not found")

    db.delete(order)
    db.commit()

    return {"message": "Order cancelled successfully"}