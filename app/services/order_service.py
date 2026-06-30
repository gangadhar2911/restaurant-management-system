from fastapi import HTTPException
from sqlalchemy.orm import Session
from app.repositories.order_repository import OrderRepository

repo = OrderRepository()
VALID_STATUSES = {"Pending", "Confirmed", "Preparing", "Ready", "Completed", "Cancelled"}


class OrderService:
    @staticmethod
    def create(db: Session, data: dict):
        return repo.create(db, data)

    @staticmethod
    def add_item(db: Session, order_id: int, data: dict):
        OrderService.get_by_id(db, order_id)
        return repo.add_item(db, order_id, data)

    @staticmethod
    def get_all(db: Session):
        return repo.get_all(db)

    @staticmethod
    def get_by_id(db: Session, order_id: int):
        obj = repo.get_by_id(db, order_id)
        if not obj:
            raise HTTPException(status_code=404, detail="Order not found")
        return obj

    @staticmethod
    def get_with_items(db: Session, order_id: int):
        order = OrderService.get_by_id(db, order_id)
        items = repo.get_items(db, order_id)
        return {"order": order, "items": items}

    @staticmethod
    def get_history_by_customer(db: Session, customer_id: int):
        return repo.get_by_customer(db, customer_id)

    @staticmethod
    def update_status(db: Session, order_id: int, status: str):
        if status not in VALID_STATUSES:
            raise HTTPException(status_code=400, detail="Invalid order status")
        obj = OrderService.get_by_id(db, order_id)
        return repo.update_status(db, obj, status)

    @staticmethod
    def cancel(db: Session, order_id: int):
        obj = OrderService.get_by_id(db, order_id)
        return repo.update_status(db, obj, "Cancelled")