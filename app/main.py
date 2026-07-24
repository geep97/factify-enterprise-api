from fastapi import FastAPI

from app.api.routes.api_keys import router as api_keys_router
from app.api.routes.health import router as health_router
from app.api.routes.verification import router as verification_router

from app.core.exception_handlers import register_exception_handlers
from app.core.logging import configure_logging

from app.middleware.request_id import RequestIDMiddleware
from app.middleware.logging import LoggingMiddleware


# ============================================================
# LOGGING
# ============================================================

configure_logging()

# ============================================================
# APPLICATION
# ============================================================

app = FastAPI(
    title="Factify Enterprise API",
    version="1.0.0",
)

# ============================================================
# MIDDLEWARE
# ============================================================

app.add_middleware(RequestIDMiddleware)
app.add_middleware(LoggingMiddleware)

# ============================================================
# EXCEPTION HANDLERS
# ============================================================

register_exception_handlers(app)

# ============================================================
# ROUTES
# ============================================================

app.include_router(
    health_router,
    prefix="/health",
    tags=["Health"],
)

app.include_router(
    api_keys_router,
    prefix="/api/v1/api-keys",
    tags=["API Keys"],
)

app.include_router(
    verification_router,
    prefix="/api/v1",
    tags=["Verification"],
)