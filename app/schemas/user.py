from pydantic import BaseModel, EmailStr
from typing import Optional

# Schema for reading user profile data
class UserRead(BaseModel):
    id: int
    email: EmailStr
    full_name: str
    is_active: bool
    is_deleted: bool

    class Config:
        # Allows Pydantic to work with SQLAlchemy models
        from_attributes = True

# Schema for updating user profile (all fields are optional)
class UserUpdate(BaseModel):
    full_name: Optional[str] = None