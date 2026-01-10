from fastapi import APIRouter, Depends

from app.api.deps import require_permission
from app.core.security import get_current_user
from app.models.user import User

router = APIRouter(
    prefix="/reports",
    tags=["Mock Business"],
)

# Fake business data (no database needed)
FAKE_REPORTS = [
    {"id": 1, "title": "Financial Report"},
    {"id": 2, "title": "User Activity Report"},
]


@router.get(
    "",
    dependencies=[Depends(require_permission("reports:read"))],
)
def get_reports(
    current_user: User = Depends(get_current_user),
):
    """
    Mock business resource.

    - Requires reports:read permission
    - Demonstrates RBAC protection on business objects
    """
    return FAKE_REPORTS