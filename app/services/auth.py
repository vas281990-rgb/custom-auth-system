from sqlalchemy.orm import Session

from app.models.user import User
from app.models.role import Role
from app.core.security import hash_password, verify_password, create_access_token


def register_user(
    db: Session,
    *,
    email: str,
    password: str,
    full_name: str,
) -> User:
    existing_user = db.query(User).filter(User.email == email).first()
    if existing_user:
        raise ValueError("User already exists")

    role = db.query(Role).filter(Role.name == "user").first()
    if not role:
        raise RuntimeError("Default role not found")

    user = User(
        email=email,
        full_name=full_name,
        password_hash=hash_password(password),
        is_active=True,
    )

    user.roles.append(role)

    db.add(user)
    db.commit()
    db.refresh(user)

    return user


def login_user(
    db: Session,
    *,
    email: str,
    password: str,
) -> str:
    user = db.query(User).filter(User.email == email).first()

    if not user or not verify_password(password, user.password_hash):
        raise ValueError("Invalid credentials")

    if user.is_deleted or not user.is_active:
        raise PermissionError("User inactive")

    return create_access_token(data={"sub": str(user.id)})
