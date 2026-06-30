from typing import List

from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.schemas.role import (
    RoleCreate,
    RoleUpdate,
    RoleResponse
)
from app.services.role_service import RoleService

router = APIRouter(
    prefix="/roles",
    tags=["Roles"]
)


# ==========================================
# CREATE ROLE
# ==========================================
@router.post(
    "/",
    response_model=RoleResponse,
    status_code=status.HTTP_201_CREATED
)
def create_role(
    role: RoleCreate,
    db: Session = Depends(get_db)
):
    return RoleService.create_role(db, role)


# ==========================================
# GET ALL ROLES
# ==========================================
@router.get(
    "/",
    response_model=List[RoleResponse]
)
def get_roles(
    db: Session = Depends(get_db)
):
    return RoleService.get_all_roles(db)


# ==========================================
# GET ROLE BY ID
# ==========================================
@router.get(
    "/{role_id}",
    response_model=RoleResponse
)
def get_role(
    role_id: int,
    db: Session = Depends(get_db)
):
    return RoleService.get_role_by_id(db, role_id)


# ==========================================
# UPDATE ROLE
# ==========================================
@router.put(
    "/{role_id}",
    response_model=RoleResponse
)
def update_role(
    role_id: int,
    role: RoleUpdate,
    db: Session = Depends(get_db)
):
    return RoleService.update_role(
        db,
        role_id,
        role
    )


# ==========================================
# DELETE ROLE
# ==========================================
@router.delete("/{role_id}")
def delete_role(
    role_id: int,
    db: Session = Depends(get_db)
):
    return RoleService.delete_role(
        db,
        role_id
    )


# ==========================================
# TOTAL ROLES
# ==========================================
@router.get("/count/total")
def count_roles(
    db: Session = Depends(get_db)
):
    return {
        "total_roles": RoleService.count_roles(db)
    }