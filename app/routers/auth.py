from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.services.auth import register_user, login_user

router = APIRouter(prefix="/auth", tags=["Auth"])


@router.post("/register", status_code=status.HTTP_201_CREATED)
def register(
    email: str,
    password: str,
    full_name: str,
    db: Session = Depends(get_db),
):
    try:
        register_user(
            db,
            email=email,
            password=password,
            full_name=full_name,
        )
        return {"message": "User registered successfully"}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.post("/login")
def login(
    email: str,
    password: str,
    db: Session = Depends(get_db),
):
    try:
        token = login_user(db, email=email, password=password)
        return {"access_token": token, "token_type": "bearer"}
    except ValueError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password",
        )
    except PermissionError:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="User account inactive",
        )
