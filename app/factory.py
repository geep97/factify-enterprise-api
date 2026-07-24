from fastapi import FastAPI

from app.core.bootstrap import (
    register_middlewares,
    register_exception_handlers_for_app,
    register_routes,
)

from app.core.logging import configure_logging


def create_app() -> FastAPI:
    configure_logging()

    app = FastAPI(
        title="Factify Enterprise API",
        version="1.0.0",
        description="Enterprise fact-checking platform powered by AI.",
        contact={
            "name": "Factify",
            "email": "support@factify.ai",
        },
        license_info={
            "name": "Commercial",
        },
    )

    register_middlewares(app)
    register_exception_handlers_for_app(app)
    register_routes(app)

    return app