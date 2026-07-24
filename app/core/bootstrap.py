from fastapi import FastAPI

from app.api.v1 import router as v1_router
from app.core.exception_handlers import register_exception_handlers

from app.middleware.logging import LoggingMiddleware
from app.middleware.request_id import RequestIDMiddleware
from app.middleware.security_headers import SecurityHeadersMiddleware


def register_middlewares(app: FastAPI) -> None:
    """
    Register application middleware.
    """
    app.add_middleware(LoggingMiddleware)
    app.add_middleware(RequestIDMiddleware)
    app.add_middleware(SecurityHeadersMiddleware)


def register_exception_handlers_for_app(app: FastAPI) -> None:
    """
    Register global exception handlers.
    """
    register_exception_handlers(app)


def register_routes(app: FastAPI) -> None:
    """
    Register API routes.
    """
    app.include_router(
        v1_router,
        prefix="/api/v1",
    )