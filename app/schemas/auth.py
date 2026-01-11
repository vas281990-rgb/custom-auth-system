from pydantic import BaseModel, EmailStr, Field, model_validator

# Data required to register a new user
class RegisterRequest(BaseModel):
    email: EmailStr
    password: str = Field(min_length=8)
    password_confirm: str = Field(min_length=8)
    full_name: str

    # Ensure password and confirmation match
    @model_validator(mode='after')
    def check_passwords_match(self):
        if self.password != self.password_confirm:
            raise ValueError("Passwords do not match")
        return self

# Data returned after successful registration
class RegisterResponse(BaseModel):
    id: int
    email: EmailStr
    full_name: str
    is_active: bool

    class Config:
        from_attributes = True

# Schema for login response (JWT token)
class Token(BaseModel):
    access_token: str
    token_type: str