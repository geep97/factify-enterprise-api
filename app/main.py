from fastapi import FastAPI

from app.api.routes.api_keys import router as api_keys_router
from app.api.routes.health import router as health_router
from app.api.routes.verification import router as verification_router


app = FastAPI(
    title="Factify Enterprise API",
    version="1.0.0",
)


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