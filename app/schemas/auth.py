from pydantic import BaseModel, ConfigDict, EmailStr, Field


# ============================================================
# REGISTER
# ============================================================

class RegisterRequest(BaseModel):
    organization_name: str
    organization_slug: str
    email: EmailStr
    password: str = Field(min_length=8)


class RegisterResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    organization_id: int
    organization_name: str
    api_key: str
    warning: str


# ============================================================
# LOGIN
# ============================================================

class LoginRequest(BaseModel):
    email: EmailStr
    password: str


# ============================================================
# TOKEN
# ============================================================

class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"


# ============================================================
# USER
# ============================================================

class UserResponse(BaseModel):
    id: int
    email: str
    organization_id: int

    model_config = ConfigDict(from_attributes=True)