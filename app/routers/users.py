from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.deps.permissions import require_permission
from app.models.user import User

router = APIRouter(prefix="/users", tags=["Users"])


@router.get(
    "/",
    dependencies=[Depends(require_permission("users:read"))],
)
def list_users(db: Session = Depends(get_db)):
    return db.query(User).all()
