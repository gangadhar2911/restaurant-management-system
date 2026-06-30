from sqlalchemy.orm import Session
from app.models.notification import Notification


class NotificationRepository:
    def create(self, db: Session, data: dict) -> Notification:
        obj = Notification(**data)
        db.add(obj); db.commit(); db.refresh(obj)
        return obj

    def get_by_user(self, db: Session, user_id: int):
        return db.query(Notification).filter(Notification.user_id == user_id).order_by(Notification.created_at.desc()).all()

    def get_by_id(self, db: Session, notification_id: int):
        return db.query(Notification).filter(Notification.id == notification_id).first()

    def mark_as_read(self, db: Session, obj: Notification) -> Notification:
        from datetime import datetime
        obj.is_read = True
        obj.read_at = datetime.utcnow()
        db.commit(); db.refresh(obj)
        return obj

    def delete(self, db: Session, obj: Notification) -> None:
        db.delete(obj); db.commit()