from fastapi import APIRouter, Depends

from app.api.deps import require_permission
from app.core.security import get_current_user
from app.models.user import User

# Router for mock business resources
router = APIRouter(
    prefix="/reports",
    tags=["Mock Business"],
)

# Mock business data to demonstrate resource protection
FAKE_REPORTS = [
    {"id": 1, "title": "Financial Report"},
    {"id": 2, "title": "User Activity Report"},
]


@router.get(
    "",
    # This endpoint is protected by the RBAC permission system
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