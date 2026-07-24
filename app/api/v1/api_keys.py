from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.exc import IntegrityError

from app.core.container import get_api_key_service
from app.auth.dependencies import get_current_api_key
from app.db.models.api_key import ApiKey
from app.repositories.api_key_repository import ApiKeyRepository
from app.db.database import get_db
from sqlalchemy.orm import Session
from app.schemas.api_key import (
    ApiKeyListResponse,
    ApiKeyResponse,
    CreateAdditionalApiKeyRequest,
    CreateAdditionalApiKeyResponse,
    CreateApiKeyRequest,
    CreateApiKeyResponse,
)
from app.services.api_key_service import ApiKeyService

router = APIRouter()


# ============================================================
# CREATE NEW ORGANIZATION + FIRST API KEY
# ============================================================

@router.post("/", response_model=CreateApiKeyResponse)
def create_api_key(
    request: CreateApiKeyRequest,
    service: ApiKeyService = Depends(get_api_key_service),
):
    try:
        organization, raw_api_key = service.create_organization_with_api_key(
            organization_name=request.organization_name,
            organization_slug=request.organization_slug,
            key_name=request.key_name,
        )

        return CreateApiKeyResponse(
            organization_id=organization.id,
            organization_name=organization.name,
            api_key=raw_api_key,
            warning="Store this API key securely. It will not be shown again.",
        )

    except IntegrityError:
        raise HTTPException(
            status_code=409,
            detail="An organization with this slug already exists.",
        )


# ============================================================
# LIST API KEYS
# ============================================================

@router.get("/", response_model=ApiKeyListResponse)
def list_api_keys(
    api_key: ApiKey = Depends(get_current_api_key),
    db: Session = Depends(get_db),
):
    repo = ApiKeyRepository(db)

    keys = repo.list_by_organization(api_key.organization_id)

    return ApiKeyListResponse(
        organization_id=api_key.organization_id,
        keys=[
            ApiKeyResponse(
                id=key.id,
                name=key.name,
                key_prefix=key.key_prefix,
                is_active=key.is_active,
                created_at=key.created_at,
                last_used_at=key.last_used_at,
            )
            for key in keys
        ],
    )


# ============================================================
# CREATE ADDITIONAL KEY
# ============================================================

@router.post("/additional", response_model=CreateAdditionalApiKeyResponse)
def create_additional_api_key_endpoint(
    request: CreateAdditionalApiKeyRequest,
    api_key: ApiKey = Depends(get_current_api_key),
    service: ApiKeyService = Depends(get_api_key_service),
):
    organization = api_key.organization

    raw_api_key = service.create_additional_api_key(
        organization=organization,
        key_name=request.key_name,
    )

    return CreateAdditionalApiKeyResponse(
        organization_id=organization.id,
        organization_name=organization.name,
        api_key=raw_api_key,
        key_name=request.key_name,
        warning="Store this API key securely. It will not be shown again.",
    )


# ============================================================
# TEST API KEY
# ============================================================

@router.get("/test")
def test_api_key(
    api_key: ApiKey = Depends(get_current_api_key),
):
    return {
        "authenticated": True,
        "organization_id": api_key.organization_id,
        "message": "API key is valid",
    }