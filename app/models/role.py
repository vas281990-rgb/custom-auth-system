from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship

from app.database import Base


class Role(Base):
    """
    Role model.

    Represents a role assigned to users.
    Example: admin, manager, user
    Acts as a bridge between users and specific permissions.
    """

    __tablename__ = "roles"

# Unique identifier for each role
    id = Column(Integer, primary_key=True, index=True)

# Unique name of the role
    name = Column(String(100), unique=True, nullable=False)
    description = Column(String(255), nullable=True)

# Many-to-many relationship with User model
    users = relationship(
        "User",
        secondary="user_roles",
        back_populates="roles"
    )

# Many-to-many relationship with Permission model
    permissions = relationship(
        "Permission",
        secondary="role_permissions",
        back_populates="roles"
    )
