from app.models.user import User
from app.models.role import Role
from app.models.permission import Permission
from app.models.user_role import UserRole
from app.models.role_permission import RolePermission

# Import all models to ensure they are registered with SQLAlchemy
# This allows 'Base.metadata' to see all tables for creation/migrations