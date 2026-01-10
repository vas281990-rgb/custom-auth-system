from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship

from app.database import Base


class Permission(Base):
    """
    Permission model.

    Represents a single allowed action in the system.
    Example: "users:create", "notes:read"
    """

    __tablename__ = "permissions"

# Unique ID for each permission
    id = Column(Integer, primary_key=True, index=True)

# Technical name of the permission (unique)
    name = Column(String(255), unique=True, nullable=False)
    description = Column(String(255), nullable=True)

# Relationship back to Role model through the role_permissions association table
    roles = relationship(
        "Role",
        secondary="role_permissions",
        back_populates="permissions"
    )
