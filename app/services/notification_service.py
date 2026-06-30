from fastapi import HTTPException
from sqlalchemy.orm import Session
from app.repositories.notification_repository import NotificationRepository

repo = NotificationRepository()


class NotificationService:
    @staticmethod
    def create(db: Session, data: dict):
        return repo.create(db, data)

    @staticmethod
    def order_confirmation(db: Session, user_id: int, order_id: int):
        return repo.create(db, {
            "user_id": user_id, "title": "Order Confirmed",
            "message": f"Your order #{order_id} has been confirmed.",
            "notification_type": "ORDER_CONFIRMATION",
        })