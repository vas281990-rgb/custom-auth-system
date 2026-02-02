
#We import all models here to ensure that SQLAlchemy is aware of them
# before we trigger any database operations (like migrations or table creation).

from app.models.user import User
from app.models.role import Role
from app.models.permission import Permission
from app.models.user_role import UserRole
from app.models.role_permission import RolePermission
from app.models.audit_log import AuditLog

# This file acts as a central registry. When Base.metadata is accessed, 
# it will already contain all the models imported above.