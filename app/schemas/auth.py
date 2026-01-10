from pydantic import BaseModel, EmailStr, Field


class RegisterRequest(BaseModel):
    email: EmailStr
    password: str = Field(min_length=8)
    full_name: str


class RegisterResponse(BaseModel):
    id: int
    email: EmailStr
    full_name: str
    is_active: bool
