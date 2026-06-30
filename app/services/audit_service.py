from sqlalchemy.orm import Session
from app.repositories.audit_repository import AuditRepository

repo = AuditRepository()


class AuditService:
    @staticmethod
    def log(db: Session, action: str, entity: str, user_id: int = None, entity_id: int = None,
             description: str = None, ip_address: str = None):
        return repo.create(db, {
            "user_id": user_id, "action": action, "entity": entity,
            "entity_id": entity_id, "description": description, "ip_address": ip_address,
        })

    @staticmethod
    def log_login(db: Session, user_id: int, ip_address: str = None):
        return AuditService.log(db, "LOGIN", "AUTH", user_id=user_id, ip_address=ip_address)

    @staticmethod
    def log_order_update(db: Session, user_id: int, order_id: int, description: str = None):
        return AuditService.log(db, "ORDER_UPDATE", "ORDER", user_id=user_id, entity_id=order_id, description=description)

    @staticmethod
    def log_menu_change(db: Session, user_id: int, menu_item_id: int, description: str = None):
        return AuditService.log(db, "MENU_CHANGE", "MENU", user_id=user_id, entity_id=menu_item_id, description=description)

    @staticmethod
    def log_billing_activity(db: Session, user_id: int, bill_id: int, description: str = None):
        return AuditService.log(db, "BILLING_ACTIVITY", "BILL", user_id=user_id, entity_id=bill_id, description=description)

    @staticmethod
    def get_all(db: Session):
        return repo.get_all(db)

    @staticmethod
    def get_by_user(db: Session, user_id: int):
        return repo.get_by_user(db, user_id)