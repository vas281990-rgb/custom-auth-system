from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship

from app.db.base import Base


class Role(Base):
    """
    Role model.

    Represents a role assigned to users.
    Example: admin, manager, user
    """

    __tablename__ = "roles"

    id = Column(Integer, primary_key=True, index=True)

    name = Column(String(100), unique=True, nullable=False)
    description = Column(String(255), nullable=True)

    users = relationship(
        "User",
        secondary="user_roles",
        back_populates="roles"
    )

    permissions = relationship(
        "Permission",
        secondary="role_permissions",
        back_populates="roles"
    )
