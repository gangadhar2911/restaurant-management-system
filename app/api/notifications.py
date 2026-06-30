from datetime import datetime

from fastapi import APIRouter
from fastapi import Depends
from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.models.notification import Notification

router = APIRouter(prefix="/notifications", tags=["Notifications"])


# -------------------------
# CREATE NOTIFICATION
# -------------------------
@router.post("/")
def create_notification(data: dict, db: Session = Depends(get_db)):

    notification = Notification(
        user_id=data.get("user_id"),
        title=data.get("title"),
        message=data.get("message"),
        notification_type=data.get("notification_type", "SYSTEM"),
        is_read=False
    )

    db.add(notification)
    db.commit()
    db.refresh(notification)

    return notification


# -------------------------
# GET USER NOTIFICATIONS
# -------------------------
@router.get("/user/{user_id}")
def get_user_notifications(user_id: int, db: Session = Depends(get_db)):

    return db.query(Notification).filter(
        Notification.user_id == user_id
    ).order_by(Notification.created_at.desc()).all()


# -------------------------
# MARK AS READ
# -------------------------
@router.patch("/{notification_id}/read")
def mark_as_read(notification_id: int, db: Session = Depends(get_db)):

    notification = db.query(Notification).filter(
        Notification.id == notification_id
    ).first()

    if not notification:
        raise HTTPException(status_code=404, detail="Notification not found")

    notification.is_read = True
    notification.read_at = datetime.utcnow()

    db.commit()
    db.refresh(notification)

    return {
        "message": "Notification marked as read",
        "notification_id": notification.id
    }


# -------------------------
# DELETE NOTIFICATION
# -------------------------
@router.delete("/{notification_id}")
def delete_notification(notification_id: int, db: Session = Depends(get_db)):

    notification = db.query(Notification).filter(
        Notification.id == notification_id
    ).first()

    if not notification:
        raise HTTPException(status_code=404, detail="Notification not found")

    db.delete(notification)
    db.commit()

    return {"message": "Notification deleted successfully"}