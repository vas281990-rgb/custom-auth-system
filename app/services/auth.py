from sqlalchemy.orm import Session

from app.models.user import User
from app.models.role import Role
from app.core.security import (
    hash_password,
    verify_password,
    create_access_token,
)


def register_user(
    db: Session,
    *,
    email: str,
    password: str,
    full_name: str,
) -> User:
    # Check if user already exists
    existing_user = db.query(User).filter(User.email == email).first()
    if existing_user:
        raise ValueError("User already exists")

    # Get default role
    role = db.query(Role).filter(Role.name == "user").first()
    if not role:
        raise RuntimeError("Default role not found")

    # Create user
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

    # User not found or password invalid
    if not user or not verify_password(password, user.password_hash):
        raise ValueError("Invalid credentials")

    # Account disabled or soft-deleted
    if not user.is_active or user.is_deleted:
        raise PermissionError("User inactive or deleted")

    # Create JWT token
    return create_access_token(
        data={"sub": str(user.id)}
    )
