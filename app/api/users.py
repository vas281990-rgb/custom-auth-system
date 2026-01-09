from fastapi import APIRouter, Depends
from app.models.user import User
from app.core.security import get_current_user
from app.schemas.user import UserRead

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
