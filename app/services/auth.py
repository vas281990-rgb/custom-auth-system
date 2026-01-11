from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from app.models.user import User
from app.models.role import Role
from app.core.security import (
    hash_password,
    verify_password,
    create_access_token,
)

def register_user(
    db: Session,
    email: str,
    password: str,
    full_name: str,
) -> User:

    existing_user = db.query(User).filter(
        User.email == email,
        User.is_deleted == False
    ).first()

    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered",
        )


    user_role = db.query(Role).filter(Role.name == "user").first()
    if not user_role:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Default role 'user' not found in database",
        )

    user = User(
        email=email,
        full_name=full_name,
        password_hash=hash_password(password),
        is_active=True,
    )

    user.roles.append(user_role)

    db.add(user)
    db.commit()
    db.refresh(user)
    return user

def login_user(
    db: Session,
    email: str,
    password: str,
) -> str:
    user = db.query(User).filter(User.email == email).first()

    if not user or not verify_password(password, user.password_hash):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password",
        )


    if not user.is_active or user.is_deleted:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="User account is inactive or deleted",
        )


    return create_access_token(data={"sub": str(user.id)})