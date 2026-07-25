from fastapi import APIRouter

from .api_keys import router as api_keys_router
from .dashboard import router as dashboard_router
from .health import router as health_router
from .protected import router as protected_router
from .rate_limits import router as rate_limit_router
from .subscription import router as subscription_router
from .verification import router as verification_router

router = APIRouter()

router.include_router(
    health_router,
    prefix="/health",
    tags=["Health"],
)

router.include_router(
    api_keys_router,
    prefix="/api-keys",
    tags=["API Keys"],
)

router.include_router(
    verification_router,
    tags=["Verification"],
)

router.include_router(
    protected_router,
)

router.include_router(
    rate_limit_router,
)

router.include_router(
    subscription_router,
    prefix="/subscription",
    tags=["Subscription"],
)

router.include_router(
    dashboard_router,
    prefix="/dashboard",
    tags=["Dashboard"],
)