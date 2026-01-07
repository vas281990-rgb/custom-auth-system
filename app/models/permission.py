from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship

from app.db.base import Base


class Permission(Base):
    """
    Permission model.

    Represents a single allowed action in the system.
    Example: "users:create", "notes:read"
    """

    __tablename__ = "permissions"

    id = Column(Integer, primary_key=True, index=True)

    name = Column(String(255), unique=True, nullable=False)
    description = Column(String(255), nullable=True)

    roles = relationship(
        "Role",
        secondary="role_permissions",
        back_populates="permissions"
    )
