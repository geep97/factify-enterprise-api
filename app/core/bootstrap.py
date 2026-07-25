from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.v1 import router as v1_router
from app.core.config import settings
from app.core.exception_handlers import register_exception_handlers

from app.middleware.logging import LoggingMiddleware
from app.middleware.request_id import RequestIDMiddleware
from app.middleware.security_headers import SecurityHeadersMiddleware


def register_middlewares(app: FastAPI) -> None:
    """
    Register application middleware.

    Note: in Starlette, middleware added LAST becomes the OUTERMOST
    layer (it runs first on the way in). CORSMiddleware must be
    outermost so it can respond to preflight OPTIONS requests
    before anything else (including our own routing) rejects them.
    """
    app.add_middleware(LoggingMiddleware)
    app.add_middleware(RequestIDMiddleware)
    app.add_middleware(SecurityHeadersMiddleware)

    origins = [
        origin.strip()
        for origin in settings.ALLOWED_ORIGINS.split(",")
        if origin.strip()
    ]

    app.add_middleware(
        CORSMiddleware,
        allow_origins=origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )


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