from sqlalchemy.orm import Session

from app.models.role import Role


class RoleRepository:

    def create(self, db: Session, role_name: str) -> Role:
        role = Role(role_name=role_name)
        db.add(role)
        db.commit()
        db.refresh(role)
        return role

    def get_all(self, db: Session):
        return db.query(Role).all()

    def get_role_by_id(self, db: Session, role_id: int):
        return db.query(Role).filter(Role.id == role_id).first()

    def get_role_by_name(self, db: Session, role_name: str):
        return db.query(Role).filter(Role.role_name == role_name).first()

    def update(self, db: Session, role: Role, data: dict) -> Role:
        for key, value in data.items():
            setattr(role, key, value)
        db.commit()
        db.refresh(role)
        return role

    def delete(self, db: Session, role: Role) -> None:
        db.delete(role)
        db.commit()

    def count(self, db: Session) -> int:
        return db.query(Role).count()