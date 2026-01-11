from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.services.auth import login_user, register_user
from app.schemas.auth import RegisterRequest, RegisterResponse

router = APIRouter(prefix="/auth", tags=["Auth"])


@router.post("/login")
def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db),
):
    try:
        token = login_user(
            db,
            email=form_data.username,
            password=form_data.password,
        )
        return {
            "access_token": token,
            "token_type": "bearer",
        }
    except ValueError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password",
        )
    except PermissionError:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="User account is inactive",
        )
    
@router.post("/logout")
def logout():
    return {"message": "Logged out"}

@router.post(
    "/register",
    response_model=RegisterResponse,
    status_code=status.HTTP_201_CREATED,
)
def register(
    data: RegisterRequest,
    db: Session = Depends(get_db),
):
    user = register_user(
        db=db,
        email=data.email,
        password=data.password,
        full_name=data.full_name,
    )
    return user
