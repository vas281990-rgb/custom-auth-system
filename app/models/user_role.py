from sqlalchemy import Column, Integer, ForeignKey

from app.db.base import Base


class UserRole(Base):
    """
    Association table between users and roles.
    """

    __tablename__ = "user_roles"

    user_id = Column(
        Integer,
        ForeignKey("users.id", ondelete="CASCADE"),
        primary_key=True
    )

    role_id = Column(
        Integer,
        ForeignKey("roles.id", ondelete="CASCADE"),
        primary_key=True
    )
