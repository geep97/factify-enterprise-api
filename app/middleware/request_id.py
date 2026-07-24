import uuid

from starlette.middleware.base import BaseHTTPMiddleware

from app.core.logging_context import set_request_id


class RequestIDMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request, call_next):
        # ============================================================
        # GENERATE REQUEST ID
        # ============================================================

        request_id = str(uuid.uuid4())

        # Make available during the request
        request.state.request_id = request_id

        # Store in logging context
        set_request_id(request_id)

        # Continue pipeline
        response = await call_next(request)

        # Return request id to client
        response.headers["X-Request-ID"] = request_id

        return response