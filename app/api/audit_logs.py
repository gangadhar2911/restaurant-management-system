from fastapi import APIRouter
from fastapi import Depends
from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.models.audit_log import AuditLog

router = APIRouter(prefix="/audit-logs", tags=["Audit Logs"])


# -------------------------
# CREATE AUDIT LOG
# -------------------------
@router.post("/")
def create_audit_log(data: dict, db: Session = Depends(get_db)):

    log = AuditLog(
        user_id=data.get("user_id"),
        action=data.get("action"),
        entity=data.get("entity"),
        entity_id=data.get("entity_id"),
        description=data.get("description"),
        ip_address=data.get("ip_address")
    )

    db.add(log)
    db.commit()
    db.refresh(log)

    return log


# -------------------------
# GET ALL AUDIT LOGS
# -------------------------
@router.get("/")
def get_all_logs(db: Session = Depends(get_db)):

    return db.query(AuditLog).order_by(AuditLog.id.desc()).all()


# -------------------------
# GET LOG BY ID
# -------------------------
@router.get("/{log_id}")
def get_log(log_id: int, db: Session = Depends(get_db)):

    log = db.query(AuditLog).filter(AuditLog.id == log_id).first()

    if not log:
        raise HTTPException(status_code=404, detail="Audit log not found")

    return log


# -------------------------
# GET LOGS BY USER
# -------------------------
@router.get("/user/{user_id}")
def get_logs_by_user(user_id: int, db: Session = Depends(get_db)):

    return db.query(AuditLog).filter(
        AuditLog.user_id == user_id
    ).order_by(AuditLog.id.desc()).all()


# -------------------------
# DELETE LOG
# -------------------------
@router.delete("/{log_id}")
def delete_log(log_id: int, db: Session = Depends(get_db)):

    log = db.query(AuditLog).filter(AuditLog.id == log_id).first()

    if not log:
        raise HTTPException(status_code=404, detail="Audit log not found")

    db.delete(log)
    db.commit()

    return {"message": "Audit log deleted successfully"}