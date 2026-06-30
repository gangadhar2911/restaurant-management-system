from sqlalchemy.orm import Session
from app.models.kitchen_order import KitchenOrder


class KitchenRepository:
    def create(self, db: Session, order_id: int) -> KitchenOrder:
        obj = KitchenOrder(order_id=order_id, status="Pending")
        db.add(obj); db.commit(); db.refresh(obj)
        return obj

    def get_all(self, db: Session):
        return db.query(KitchenOrder).all()

    def get_by_id(self, db: Session, kitchen_order_id: int):
        return db.query(KitchenOrder).filter(KitchenOrder.id == kitchen_order_id).first()

    def get_by_order_id(self, db: Session, order_id: int):
        return db.query(KitchenOrder).filter(KitchenOrder.order_id == order_id).first()

    def get_by_status(self, db: Session, status: str):
        return db.query(KitchenOrder).filter(KitchenOrder.status == status).all()

    def update_status(self, db: Session, obj: KitchenOrder, status: str) -> KitchenOrder:
        obj.status = status
        db.commit(); db.refresh(obj)
        return obj