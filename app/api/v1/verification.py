from fastapi import APIRouter, Depends

from app.core.container import (
    get_usage_service,
    get_verification_service,
)
from app.core.service_dependencies  import get_current_api_key
from app.db.models.api_key import ApiKey
from app.schemas.verification import VerificationRequest
from app.services.usage_service import UsageService
from app.services.verification_service import VerificationService

router = APIRouter()


@router.post("/verify")
async def verify(
    request: VerificationRequest,
    api_key: ApiKey = Depends(get_current_api_key),
    usage_service: UsageService = Depends(get_usage_service),
    verification_service: VerificationService = Depends(get_verification_service),
):
    usage_service.check_monthly_limit(api_key)

    try:
        report = await verification_service.verify(
            content=request.content,
            mode=request.mode,
        )

        usage_service.record_request(
            api_key=api_key,
            endpoint="/api/v1/verify",
            status_code=200,
        )

        return report

    except Exception:
        usage_service.record_request(
            api_key=api_key,
            endpoint="/api/v1/verify",
            status_code=500,
        )

        raise