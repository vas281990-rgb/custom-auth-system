from app.db.session import engine
from app.db.base import Base

# import all models so SQLAlchemy knows about them
from app.models.user import User
from app.models.role import Role
from app.models.permission import Resource, Action, Permission
from app.models import user_roles, role_permissions


def init_db():
    Base.metadata.create_all(bind=engine)
