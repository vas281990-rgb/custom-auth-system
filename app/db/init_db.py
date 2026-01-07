from app.db.session import engine
from app.db.base import Base

# importing models registers them in SQLAlchemy metadata
from app.models.user import User
from app.models.role import Role
from app.models.permission import Permission
from app.models.user_role import UserRole
from app.models.role_permission import RolePermission


def init_db() -> None:
    Base.metadata.create_all(bind=engine)
