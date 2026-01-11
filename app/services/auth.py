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
    """Logic for registering a new user with a default 'user' role"""

    # Check if the email is already taken by an active user
    existing_user = db.query(User).filter(
        User.email == email,
        User.is_deleted == False
    ).first()

    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered",
        )

    # Every new user must have a default 'user' role
    user_role = db.query(Role).filter(Role.name == "user").first()
    if not user_role:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Default role 'user' not found in database",
        )
    
    # Create user object with hashed password
    user = User(
        email=email,
        full_name=full_name,
        password_hash=hash_password(password),
        is_active=True,
    )

    # Attach the default role
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
    """Authenticate user and return a JWT token"""
    # Find user by email
    user = db.query(User).filter(User.email == email).first()

    # Verify existence and password match
    if not user or not verify_password(password, user.password_hash):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password",
        )

    # Check if the account is blocked or soft-deleted
    if not user.is_active or user.is_deleted:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="User account is inactive or deleted",
        )

    # Return access token with user ID as subject (sub)
    return create_access_token(data={"sub": str(user.id)})