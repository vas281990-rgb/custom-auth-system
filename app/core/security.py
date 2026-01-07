"""
Security utilities:
- Password hashing & verification
- JWT token creation & decoding

This module is framework-agnostic (not tied to FastAPI directly).
"""

from datetime import datetime, timedelta
from typing import Optional

from jose import jwt, JWTError
from passlib.context import CryptContext

# Password hashing context
# bcrypt is slow by design -> protects against brute-force attacks
pwd_context = CryptContext(
    schemes=["argon2"],
    deprecated="auto"
)


# JWT settings
SECRET_KEY = "SUPER_SECRET_KEY_CHANGE_ME"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

def hash_password(password: str) -> str:
    """
    Takes a plain password and returns a hashed version.

    Example:
    "password123" -> "$2b$12$..."
    """
    return pwd_context.hash(password)

def verify_password(plain_password: str, hashed_password: str) -> bool:
    """
    Verifies a plain password against a hashed password.

    Returns True if passwords match, False otherwise.
    """
    return pwd_context.verify(plain_password, hashed_password)

def create_access_token(
    data: dict,
    expires_delta: Optional[timedelta] = None
) -> str:
    """
    Creates a JWT access token.

    `data` usually contains:
    {
        "sub": user_id
    }
    """
    to_encode = data.copy()

    # Token expiration time
    expire = datetime.utcnow() + (
        expires_delta or timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    )

    to_encode.update({"exp": expire})

    encoded_jwt = jwt.encode(
        to_encode,
        SECRET_KEY,
        algorithm=ALGORITHM
    )

    return encoded_jwt

def decode_access_token(token: str) -> Optional[dict]:
    """
    Decodes a JWT token.

    Returns payload if token is valid.
    Returns None if token is invalid or expired.
    """
    try:
        payload = jwt.decode(
            token,
            SECRET_KEY,
            algorithms=[ALGORITHM]
        )
        return payload
    except JWTError:
        return None
