from sqlalchemy.orm import Session

from app.db.session import SessionLocal
from app.models.role import Role
from app.models.permission import Permission
from app.models.user import User
from app.core.security import hash_password


def seed_rbac():
    db: Session = SessionLocal()

    try:
        # -------------------------
        # Permissions
        # -------------------------
        permissions_data = [
            ("users:create", "Create users"),
            ("users:read", "Read users"),
            ("users:update", "Update users"),
            ("users:delete", "Delete users"),
        ]

        permissions = {}
        for name, description in permissions_data:
            permission = db.query(Permission).filter_by(name=name).first()
            if not permission:
                permission = Permission(
                    name=name,
                    description=description
                )
                db.add(permission)
                db.flush()  # get id
            permissions[name] = permission

        # -------------------------
        # Roles
        # -------------------------
        admin_role = db.query(Role).filter_by(name="admin").first()
        if not admin_role:
            admin_role = Role(
                name="admin",
                description="Administrator"
            )
            admin_role.permissions = list(permissions.values())
            db.add(admin_role)

        user_role = db.query(Role).filter_by(name="user").first()
        if not user_role:
            user_role = Role(
                name="user",
                description="Regular user"
            )
            user_role.permissions = [
                permissions[]
            ]
            db.add(user_role)

        # -------------------------
        # Admin user
        # -------------------------
        admin_user = db.query(User).filter_by(email="admin@example.com").first()
        if not admin_user:
            admin_user = User(
                email="admin@example.com",
                full_name="System Administrator",
                password_hash=hash_password("admin123"),
                is_active=True
            )
            admin_user.roles.append(admin_role)
            db.add(admin_user)

        db.commit()
        print("✅ RBAC seed completed")

    except Exception as e:
        db.rollback()
        print("❌ RBAC seed failed:", e)
    finally:
        db.close()
