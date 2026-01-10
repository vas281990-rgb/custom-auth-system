from sqlalchemy import Column, Integer, ForeignKey

from app.database import Base


class UserRole(Base):
    """
    Association table between users and roles.
    """

    __tablename__ = "user_roles"

# Reference to the user
    user_id = Column(
        Integer,
        ForeignKey("users.id", ondelete="CASCADE"),
        primary_key=True
    )

# Reference to the role
# Primary_key=True on both columns not to have duplicates

    role_id = Column(
        Integer,
        ForeignKey("roles.id", ondelete="CASCADE"),
        primary_key=True
    )
