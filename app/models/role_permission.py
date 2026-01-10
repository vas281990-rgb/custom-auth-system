from sqlalchemy import Column, Integer, ForeignKey

from app.database import Base


class RolePermission(Base):
    """
    Association table between roles and permissions.
    """

    __tablename__ = "role_permissions"

# Reference to the Role ID
    role_id = Column(
        Integer,
        ForeignKey("roles.id", ondelete="CASCADE"),
        primary_key=True
    )

# Reference to the Permission ID
    permission_id = Column(
        Integer,
        ForeignKey("permissions.id", ondelete="CASCADE"),
        primary_key=True
    )
