from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.models.user import User
from app.api.deps import require_permission
from app.core.security import get_current_user

router = APIRouter(
    prefix="/users",
    tags=["Users"],
)

@router.get("/me")
def get_me(
    current_user: User = Depends(get_current_user),
):
    
    return {
        "id": current_user.id,
        "email": current_user.email,
        "full_name": current_user.full_name,
        "is_active": current_user.is_active,
        "is_deleted": current_user.is_deleted
    }

@router.get(
    "",
    dependencies=[Depends(require_permission("users:read"))],
)
def get_users(
    db: Session = Depends(get_db),
):

    users = (
        db.query(User)
        .filter(User.is_deleted == False)
        .all()
    )

    return [
        {
            "id": user.id,
            "email": user.email,
            "full_name": user.full_name,
            "is_active": user.is_active,
        }
        for user in users
    ]

@router.delete(
    "/{user_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    dependencies=[Depends(require_permission("users:delete"))],
)
def delete_user(
    user_id: int,
    db: Session = Depends(get_db),
):
   
    user = db.query(User).filter(User.id == user_id).first()

    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found",
        )

    user.is_deleted = True
    user.is_active = False
    db.commit()
    return None 