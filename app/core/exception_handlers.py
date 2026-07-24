from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

from app.core.exceptions import (
    ApiKeyInactiveException,
    FactifyUnavailableException,
    InvalidApiKeyException,
    InvalidSubscriptionPlanException,
    MonthlyLimitExceededException,
    SubscriptionAlreadyActiveException,
    SubscriptionAlreadyCancelledException,
    SubscriptionNotFoundException,
)
from app.core.logging import get_logger

logger = get_logger(__name__)


def register_exception_handlers(app: FastAPI):

    # ============================================================
    # INVALID API KEY
    # ============================================================

    @app.exception_handler(InvalidApiKeyException)
    async def invalid_api_key_handler(
        request: Request,
        exc: InvalidApiKeyException,
    ):
        logger.warning(
            "Invalid API Key",
            extra={
                "event": "invalid_api_key",
                "method": request.method,
                "path": request.url.path,
            },
        )

        return JSONResponse(
            status_code=401,
            content={"detail": str(exc)},
        )

    # ============================================================
    # API KEY INACTIVE
    # ============================================================

    @app.exception_handler(ApiKeyInactiveException)
    async def api_key_inactive_handler(
        request: Request,
        exc: ApiKeyInactiveException,
    ):
        logger.warning(
            "Inactive API Key",
            extra={
                "event": "api_key_inactive",
                "method": request.method,
                "path": request.url.path,
            },
        )

        return JSONResponse(
            status_code=403,
            content={"detail": str(exc)},
        )

    # ============================================================
    # MONTHLY LIMIT EXCEEDED
    # ============================================================

    @app.exception_handler(MonthlyLimitExceededException)
    async def monthly_limit_handler(
        request: Request,
        exc: MonthlyLimitExceededException,
    ):
        logger.warning(
            "Monthly limit exceeded",
            extra={
                "event": "monthly_limit_exceeded",
                "limit": exc.limit,
                "used": exc.used,
                "method": request.method,
                "path": request.url.path,
            },
        )

        return JSONResponse(
            status_code=429,
            content={"detail": str(exc)},
        )

    # ============================================================
    # SUBSCRIPTION NOT FOUND
    # ============================================================

    @app.exception_handler(SubscriptionNotFoundException)
    async def subscription_not_found_handler(
        request: Request,
        exc: SubscriptionNotFoundException,
    ):
        return JSONResponse(
            status_code=404,
            content={"detail": str(exc)},
        )

    # ============================================================
    # INVALID SUBSCRIPTION PLAN
    # ============================================================

    @app.exception_handler(InvalidSubscriptionPlanException)
    async def invalid_subscription_plan_handler(
        request: Request,
        exc: InvalidSubscriptionPlanException,
    ):
        return JSONResponse(
            status_code=400,
            content={"detail": str(exc)},
        )

    # ============================================================
    # SUBSCRIPTION ALREADY CANCELLED
    # ============================================================

    @app.exception_handler(SubscriptionAlreadyCancelledException)
    async def subscription_cancelled_handler(
        request: Request,
        exc: SubscriptionAlreadyCancelledException,
    ):
        return JSONResponse(
            status_code=409,
            content={"detail": str(exc)},
        )

    # ============================================================
    # SUBSCRIPTION ALREADY ACTIVE
    # ============================================================

    @app.exception_handler(SubscriptionAlreadyActiveException)
    async def subscription_active_handler(
        request: Request,
        exc: SubscriptionAlreadyActiveException,
    ):
        return JSONResponse(
            status_code=409,
            content={"detail": str(exc)},
        )

    # ============================================================
    # FACTIFY UNAVAILABLE
    # ============================================================

    @app.exception_handler(FactifyUnavailableException)
    async def factify_unavailable_handler(
        request: Request,
        exc: FactifyUnavailableException,
    ):
        return JSONResponse(
            status_code=503,
            content={"detail": str(exc)},
        )

    # ============================================================
    # UNHANDLED EXCEPTION
    # ============================================================

    @app.exception_handler(Exception)
    async def generic_exception_handler(
        request: Request,
        exc: Exception,
    ):
        logger.exception(
            "Unhandled exception",
            extra={
                "event": "unhandled_exception",
                "method": request.method,
                "path": request.url.path,
            },
        )

        return JSONResponse(
            status_code=500,
            content={"detail": "Internal Server Error"},
        )