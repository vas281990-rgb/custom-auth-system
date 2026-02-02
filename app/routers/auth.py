from fastapi import APIRouter, Depends, HTTPException, status, Request
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.services.auth import login_user, register_user
from app.services.audit import log_event
from app.schemas.auth import RegisterRequest, RegisterResponse
from app.models.user import User

router = APIRouter(prefix="/auth", tags=["Auth"])


@router.post("/login")
def login(
    request: Request,
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db),
):
    """Authenticate user and return a JWT access token with audit logging"""
    try:
        token = login_user(
            db,
            email=form_data.username,
            password=form_data.password,
        )
        # Find user to get their ID for the log
        user = db.query(User).filter(User.email == form_data.username).first()

        # SUCCESS LOG
        log_event(
            db=db,
            user_id=user.id,
            action="login",
            details=f"User {user.email} logged in",
            ip_address=request.client.host
        )
        return {
            "access_token": token,
            "token_type": "bearer",
        }
    except Exception as e:
        # FAILED LOG
        log_event(
            db=db,
            action="login_failed",
            details=f"Failed login attempt for email: {form_data.username}",
            ip_address=request.client.host
        )
        raise e
    
@router.post(
    "/register",
    response_model=RegisterResponse,
    status_code=status.HTTP_201_CREATED,
)
def register(
    request: Request,
    data: RegisterRequest,
    db: Session = Depends(get_db),
):
    """Register a new user and log the registration event"""
    user = register_user(
    db=db,
    email=data.email,
    password=data.password,
    full_name=data.full_name,
)
    
    # REGISTER LOG
    log_event(
        db=db,
        user_id=user.id,
        action="register",
        details=f"New user registered: {user.email}",
        ip_address=request.client.host
    )
    
    return user

@router.post("/logout")
def logout():
    """Endpoint for logout (stateless)"""
    return {"message": "Logged out"}