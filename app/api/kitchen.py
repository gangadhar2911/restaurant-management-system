from fastapi import APIRouter
from fastapi import Depends
from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.models.order import Order
from app.models.kitchen_order import KitchenOrder

router = APIRouter(prefix="/kitchen", tags=["Kitchen"])


# -------------------------
# SEND ORDER TO KITCHEN
# -------------------------
@router.post("/send/{order_id}")
def send_to_kitchen(order_id: int, db: Session = Depends(get_db)):

    order = db.query(Order).filter(Order.id == order_id).first()

    if not order:
        raise HTTPException(status_code=404, detail="Order not found")

    existing = db.query(KitchenOrder).filter(KitchenOrder.order_id == order_id).first()

    if existing:
        raise HTTPException(status_code=400, detail="Already sent to kitchen")

    kitchen_order = KitchenOrder(
        order_id=order_id,
        status="Pending"
    )

    db.add(kitchen_order)
    db.commit()
    db.refresh(kitchen_order)

    return {
        "message": "Order sent to kitchen",
        "kitchen_order_id": kitchen_order.id
    }


# -------------------------
# GET ALL KITCHEN ORDERS
# -------------------------
@router.get("/")
def get_kitchen_orders(db: Session = Depends(get_db)):
    return db.query(KitchenOrder).all()


# -------------------------
# UPDATE KITCHEN STATUS
# -------------------------
@router.patch("/{kitchen_order_id}/status")
def update_kitchen_status(kitchen_order_id: int, status: str, db: Session = Depends(get_db)):

    kitchen_order = db.query(KitchenOrder).filter(
        KitchenOrder.id == kitchen_order_id
    ).first()

    if not kitchen_order:
        raise HTTPException(status_code=404, detail="Kitchen order not found")

    valid_status = ["Pending", "Preparing", "Ready", "Completed"]

    if status not in valid_status:
        raise HTTPException(status_code=400, detail="Invalid status")

    kitchen_order.status = status

    db.commit()
    db.refresh(kitchen_order)

    return {
        "message": "Kitchen status updated",
        "status": kitchen_order.status
    }


# -------------------------
# GET ORDERS BY STATUS
# -------------------------
@router.get("/status/{status}")
def get_by_status(status: str, db: Session = Depends(get_db)):

    return db.query(KitchenOrder).filter(
        KitchenOrder.status == status
    ).all()