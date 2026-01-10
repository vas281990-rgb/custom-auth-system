from sqlalchemy import Boolean, Column, Integer, String, DateTime
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship

from app.database import Base


class User(Base):
    __tablename__ = "users"
    
# Primary key with indexing
    id = Column(Integer, primary_key=True, index=True)

# Email is used for login (unique)
    email = Column(String(255), unique=True, nullable=False, index=True)
    password_hash = Column(String(255), nullable=False)

    full_name = Column(String(255), nullable=False)

# Status flags: is_active for account control, is_deleted for "soft delete" logic
    is_active = Column(Boolean, default=True, nullable=False)
    is_deleted = Column(Boolean, default=False, nullable=False)

# Audit timestamps: automatically handled by the database server
    created_at = Column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False
    )

    updated_at = Column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
        nullable=False
    )

    # Relationship with roles (many-to-many)
    roles = relationship(
        "Role",
        secondary="user_roles",
        back_populates="users"
    )
