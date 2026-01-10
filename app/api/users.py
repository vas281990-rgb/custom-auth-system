from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.models.user import User
from app.core.security import get_current_user
from app.db.session import get_db
from app.schemas.user import UserRead, UserUpdate

router = APIRouter(
    prefix="/users",
    tags=["Users"],
)

@router.get("/me", response_model=UserRead)
def read_current_user(
    current_user: User = Depends(get_current_user),
):
    """
    Return current authenticated user.

    This endpoint proves that:
    - JWT works
    - user is extracted from token
    - protected route is functional
    """
    return current_user


@router.put("/me", response_model=UserRead)
def update_current_user(
    data: UserUpdate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """
    Update current user's profile data.

    - Only authenticated user can update their own data
    - Email and roles cannot be changed here
    """

    if data.full_name is not None:
        current_user.full_name = data.full_name

    db.commit()
    db.refresh(current_user)

    return current_user

@router.delete(
    "/me",
    status_code=status.HTTP_204_NO_CONTENT,
)
def delete_current_user(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """
    Soft delete current user.

    - Marks user as deleted
    - Disables account
    - User cannot login anymore
    - JWT becomes useless (logout = token discard)
    """

    current_user.is_deleted = True
    current_user.is_active = False

    db.commit()