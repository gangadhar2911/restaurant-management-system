from fastapi import Depends
from fastapi import HTTPException
from fastapi import status

from app.core.dependencies import get_current_user
from app.models.user import User


def has_permission(user: User, allowed_roles: list) -> bool:
    role_name = user.role.role_name if user.role else None
    return role_name in allowed_roles


def require_permission(allowed_roles: list):

    def permission_checker(
        current_user: User = Depends(get_current_user)
    ):
        role_name = current_user.role.role_name if current_user.role else None

        if role_name not in allowed_roles:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=f"Access denied. Required roles: {allowed_roles}"
            )

        return current_user

    return permission_checker