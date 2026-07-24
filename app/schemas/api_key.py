from datetime import datetime

from pydantic import BaseModel, Field


class CreateApiKeyRequest(BaseModel):
    organization_name: str = Field(
        min_length=2,
        max_length=255,
    )

    organization_slug: str = Field(
        min_length=2,
        max_length=255,
        pattern=r"^[a-z0-9-]+$",
    )

    key_name: str = Field(
        default="Default API Key",
        max_length=255,
    )


class CreateApiKeyResponse(BaseModel):
    organization_id: int
    organization_name: str
    api_key: str
    warning: str


class ApiKeyResponse(BaseModel):
    id: int
    name: str
    key_prefix: str
    is_active: bool
    created_at: datetime
    last_used_at: datetime | None


class ApiKeyListResponse(BaseModel):
    organization_id: int
    keys: list[ApiKeyResponse]


class CreateAdditionalApiKeyRequest(BaseModel):
    key_name: str = Field(
        default="Additional API Key",
        min_length=2,
        max_length=255,
    )


class CreateAdditionalApiKeyResponse(BaseModel):
    organization_id: int
    organization_name: str
    api_key: str
    key_name: str
    warning: str