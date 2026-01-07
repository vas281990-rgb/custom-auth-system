from fastapi import APIRouter, Depends
from app.api.deps import require_permission

router = APIRouter()

@router.post(
    "/users",
    dependencies=[Depends(require_permission("users:create"))]
)
def create_user():
    return {"status": "created"}
