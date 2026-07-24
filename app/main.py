from fastapi import FastAPI

from app.api.v1 import router as v1_router

from app.core.exception_handlers import register_exception_handlers
from app.core.logging import configure_logging

from app.middleware.request_id import RequestIDMiddleware
from app.middleware.logging import LoggingMiddleware

configure_logging()

app = FastAPI(
    title="Factify Enterprise API",
    version="1.0.0",
)
app.add_middleware(LoggingMiddleware)
app.add_middleware(RequestIDMiddleware)


register_exception_handlers(app)

app.include_router(
    v1_router,
    prefix="/api/v1",
)