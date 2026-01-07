from sqlalchemy import Column, Integer, ForeignKey

from app.db.base import Base


class RolePermission(Base):
    """
    Association table between roles and permissions.
    """

    __tablename__ = "role_permissions"

    role_id = Column(
        Integer,
        ForeignKey("roles.id", ondelete="CASCADE"),
        primary_key=True
    )

    permission_id = Column(
        Integer,
        ForeignKey("permissions.id", ondelete="CASCADE"),
        primary_key=True
    )
