from sqlalchemy.orm import Session
from app.models.order import Order
from app.models.order_item import OrderItem


class OrderRepository:
    def create(self, db: Session, data: dict) -> Order:
        obj = Order(**data)
        db.add(obj); db.commit(); db.refresh(obj)
        return obj

    def add_item(self, db: Session, order_id: int, data: dict) -> OrderItem:
        item = OrderItem(order_id=order_id, **data)
        db.add(item); db.commit(); db.refresh(item)
        return item

    def get_all(self, db: Session):
        return db.query(Order).all()

    def get_by_id(self, db: Session, order_id: int):
        return db.query(Order).filter(Order.id == order_id).first()

    def get_items(self, db: Session, order_id: int):
        return db.query(OrderItem).filter(OrderItem.order_id == order_id).all()

    def get_by_customer(self, db: Session, customer_id: int):
        return db.query(Order).filter(Order.customer_id == customer_id).order_by(Order.id.desc()).all()

    def update_status(self, db: Session, obj: Order, status: str) -> Order:
        obj.order_status = status
        db.commit(); db.refresh(obj)
        return obj

    def delete(self, db: Session, obj: Order) -> None:
        db.delete(obj); db.commit()