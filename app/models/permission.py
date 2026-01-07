from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship

from app.db.base import Base


class Resource(Base):
    __tablename__ = "resources"

    id = Column(Integer, primary_key=True)
    name = Column(String, unique=True, nullable=False)


class Action(Base):
    __tablename__ = "actions"

    id = Column(Integer, primary_key=True)
    name = Column(String, unique=True, nullable=False)
    
class Permission(Base):
    __tablename__ = "permissions"

    id = Column(Integer, primary_key=True)

    resource_id = Column(Integer, ForeignKey("resources.id"), nullable=False)
    action_id = Column(Integer, ForeignKey("actions.id"), nullable=False)

    resource = relationship("Resource")
    action = relationship("Action")

    roles = relationship(
        "Role",
        secondary="role_permissions",
        back_populates="permissions"
    )
