from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.repositories.role_repository import RoleRepository
from app.schemas.role import RoleCreate, RoleUpdate

role_repo = RoleRepository()


class RoleService:

    @staticmethod
    def create_role(db: Session, role: RoleCreate):
        existing = role_repo.get_role_by_name(db, role.role_name)
        if existing:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Role already exists"
            )
        return role_repo.create(db, role.role_name)

    @staticmethod
    def get_all_roles(db: Session):
        return role_repo.get_all(db)

    @staticmethod
    def get_role_by_id(db: Session, role_id: int):
        role = role_repo.get_role_by_id(db, role_id)
        if not role:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Role not found"
            )
        return role

    @staticmethod
    def update_role(db: Session, role_id: int, role: RoleUpdate):
        existing = role_repo.get_role_by_id(db, role_id)
        if not existing:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Role not found"
            )
        data = role.dict(exclude_unset=True)
        return role_repo.update(db, existing, data)

    @staticmethod
    def delete_role(db: Session, role_id: int):
        existing = role_repo.get_role_by_id(db, role_id)
        if not existing:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Role not found"
            )
        role_repo.delete(db, existing)
        return {"message": "Role deleted successfully"}

    @staticmethod
    def count_roles(db: Session):
        return role_repo.count(db)