from sqlalchemy.orm import Session

from app.models.user import User


def user_has_permission(
    db: Session,
    user_id: int,
    permission_name: str,
) -> bool:
    """
    Check if a user has a specific permission.

    Logic:
    - get user
    - iterate through user's roles
    - check permissions of each role
    """

    user = db.query(User).filter(
        User.id == user_id,
        User.is_active.is_(True),
        User.is_deleted.is_(False),
    ).first()

    if not user:
        return False

    # Iterate through roles and permissions
    for role in user.roles:
        for permission in role.permissions:
            if permission.name == permission_name:
                return True

    return False

