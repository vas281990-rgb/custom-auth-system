from fastapi import Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.core.security import get_current_user
from app.services.rbac import user_has_permission
from app.models.user import User

# This factory creates a dependency to check for specific user permissions
def require_permission(permission_name: str):
    """
    FastAPI dependency factory.

    Usage:
        Depends(require_permission("users:create"))
    """

    def permission_checker(
        current_user: User = Depends(get_current_user),
        db: Session = Depends(get_db),
    ) -> User:
        has_permission = user_has_permission(
            db=db,
            user_id=current_user.id,
            permission_name=permission_name,
        )

# If permission is missing - 403 Forbidden error
        if not has_permission:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Not enough permissions",
            )

        return current_user

    return permission_checker

def get_pagination_params(offset: int = 0, limit: int = 10):
    return {'offset': offset, "limit": limit}