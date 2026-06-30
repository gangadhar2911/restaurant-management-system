from sqlalchemy.orm import Session
from app.models.audit_log import AuditLog


class AuditRepository:
    def create(self, db: Session, data: dict) -> AuditLog:
        obj = AuditLog(**data)
        db.add(obj); db.commit(); db.refresh(obj)
        return obj

    def get_all(self, db: Session):
        return db.query(AuditLog).order_by(AuditLog.id.desc()).all()

    def get_by_id(self, db: Session, log_id: int):
        return db.query(AuditLog).filter(AuditLog.id == log_id).first()

    def get_by_user(self, db: Session, user_id: int):
        return db.query(AuditLog).filter(AuditLog.user_id == user_id).order_by(AuditLog.id.desc()).all()

    def delete(self, db: Session, obj: AuditLog) -> None:
        db.delete(obj); 
        db.commit()