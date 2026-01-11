from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.models.user import User
from app.core.security import get_current_user
from app.db.session import get_db
from app.schemas.user import UserRead, UserUpdate
from app.api.deps import require_permission

# Router for user-related operations
router = APIRouter(
    prefix="/users",
    tags=["Users"],
)

@router.get("/me", response_model=UserRead)
def read_current_user(
    current_user: User = Depends(get_current_user),
):
    """
    Retrieve the profile information of the currently authenticated user.
    """
    return current_user


@router.put("/me", response_model=UserRead)
def update_current_user(
    data: UserUpdate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """
    Update the current user's profile data (e.g., full name).
    """
    if data.full_name is not None:
        current_user.full_name = data.full_name

    db.commit()
    db.refresh(current_user)
    return current_user


@router.delete("/me", status_code=status.HTTP_204_NO_CONTENT)
def delete_current_user(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """
    Self-deactivation: marks the current user as deleted and inactive (Soft Delete).
    """
    current_user.is_active = False
    current_user.is_deleted = True
    db.commit()
    return None


@router.delete(
    "/{user_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    dependencies=[Depends(require_permission("users:delete"))],
)
def delete_user(
    user_id: int,
    db: Session = Depends(get_db),
):
    """
    Admin-only endpoint to soft-delete any user by their ID.
    Requires 'users:delete' permission.
    """
    # Look for the user in the database
    user = db.query(User).filter(User.id == user_id).first()

    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found",
        )

    # Apply soft delete: user remains in DB but cannot log in
    user.is_deleted = True
    user.is_active = False
    db.commit()
    return None