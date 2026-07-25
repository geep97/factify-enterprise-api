from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.auth.dependencies import get_current_user
from app.auth.service import UserAuthenticationService
from app.core.container import get_registration_service
from app.core.security import create_access_token
from app.db.database import get_db
from app.db.models.user import User
from app.schemas.auth import (
    LoginRequest,
    RegisterRequest,
    RegisterResponse,
    TokenResponse,
    UserResponse,
)
from app.services.registration_service import RegistrationService

router = APIRouter()


# ============================================================
# REGISTER
# ============================================================

@router.post("/register", response_model=RegisterResponse)
def register(
    request: RegisterRequest,
    service: RegistrationService = Depends(get_registration_service),
):
    try:
        organization, user, raw_api_key = service.register(
            organization_name=request.organization_name,
            organization_slug=request.organization_slug,
            email=request.email,
            password=request.password,
        )

    except IntegrityError:
        raise HTTPException(
            status_code=409,
            detail="An organization with this slug or email already exists.",
        )

    access_token = create_access_token({"sub": str(user.id)})

    return RegisterResponse(
        access_token=access_token,
        organization_id=organization.id,
        organization_name=organization.name,
        api_key=raw_api_key,
        warning="Store this API key securely. It will not be shown again.",
    )


# ============================================================
# LOGIN
# ============================================================

@router.post("/login", response_model=TokenResponse)
def login(
    request: LoginRequest,
    db: Session = Depends(get_db),
):
    user = UserAuthenticationService.authenticate_credentials(
        db=db,
        email=request.email,
        password=request.password,
    )

    if user is None:
        raise HTTPException(
            status_code=401,
            detail="Invalid email or password.",
        )

    access_token = create_access_token({"sub": str(user.id)})

    return TokenResponse(access_token=access_token)


# ============================================================
# CURRENT USER
# ============================================================

@router.get("/me", response_model=UserResponse)
def get_me(
    user: User = Depends(get_current_user),
):
    return UserResponse.model_validate(user)