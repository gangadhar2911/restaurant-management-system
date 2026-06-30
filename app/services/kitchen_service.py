from fastapi import HTTPException
from sqlalchemy.orm import Session
from app.repositories.kitchen_repository import KitchenRepository
from app.repositories.order_repository import OrderRepository

repo = KitchenRepository()
order_repo = OrderRepository()
VALID_STATUSES = ["Pending", "Preparing", "Ready", "Completed"]


class KitchenService:
    @staticmethod
    def send_to_kitchen(db: Session, order_id: int):
        order = order_repo.get_by_id(db, order_id)
        if not order:
            raise HTTPException(status_code=404, detail="Order not found")
        if repo.get_by_order_id(db, order_id):
            raise HTTPException(status_code=400, detail="Already sent to kitchen")
        return repo.create(db, order_id)

    @staticmethod
    def get_all(db: Session):
        return repo.get_all(db)

    @staticmethod
    def get_pending(db: Session):
        return repo.get_by_status(db, "Pending")

    @staticmethod
    def get_completed(db: Session):
        return repo.get_by_status(db, "Completed")

    @staticmethod
    def get_ready(db: Session):
        return repo.get_by_status(db, "Ready")

    @staticmethod
    def update_status(db: Session, kitchen_order_id: int, status: str):
        if status not in VALID_STATUSES:
            raise HTTPException(status_code=400, detail="Invalid status")
        obj = repo.get_by_id(db, kitchen_order_id)
        if not obj:
            raise HTTPException(status_code=404, detail="Kitchen order not found")
        return repo.update_status(db, obj, status)