from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.core.dependencies import get_current_api_key
from app.db.database import get_db
from app.db.models.api_key import ApiKey
from app.schemas.api_key import (
    CreateApiKeyRequest,
    CreateApiKeyResponse,
)
from app.services.api_key_service import (
    create_organization_with_api_key,
)


router = APIRouter()


@router.post(
    "/",
    response_model=CreateApiKeyResponse,
)
def create_api_key(
    request: CreateApiKeyRequest,
    db: Session = Depends(get_db),
):
    try:
        organization, raw_api_key = create_organization_with_api_key(
            db=db,
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
        db.rollback()

        raise HTTPException(
            status_code=409,
            detail="An organization with this slug already exists.",
        )


@router.get("/test")
def test_api_key(
    current_key: ApiKey = Depends(get_current_api_key),
):
    return {
        "authenticated": True,
        "organization_id": current_key.organization_id,
        "message": "API key is valid",
    }