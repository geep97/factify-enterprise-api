from fastapi import APIRouter, Depends

from app.core.dependencies import get_current_api_key
from app.db.models.api_key import ApiKey
from app.schemas.verification import VerificationRequest
from app.services.verification_service import verify_with_factify


router = APIRouter()


@router.post("/verify")
async def verify(
    request: VerificationRequest,
    api_key: ApiKey = Depends(get_current_api_key),
):
    report = await verify_with_factify(
        content=request.content,
        mode=request.mode,
    )

    return report