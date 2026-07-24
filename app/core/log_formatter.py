import json
import logging
from datetime import datetime, timezone

from app.core.logging_context import get_request_id


STANDARD_LOG_RECORD_FIELDS = {
    "args",
    "asctime",
    "created",
    "exc_info",
    "exc_text",
    "filename",
    "funcName",
    "levelname",
    "levelno",
    "lineno",
    "module",
    "msecs",
    "message",
    "msg",
    "name",
    "pathname",
    "process",
    "processName",
    "relativeCreated",
    "stack_info",
    "thread",
    "threadName",
}


class JsonFormatter(logging.Formatter):
    def format(self, record: logging.LogRecord) -> str:

        log = {
            "schema_version": 1,
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "level": record.levelname,
            "logger": record.name,
            "event": getattr(record, "event", None),
            "message": record.getMessage(),
            "request_id": get_request_id(),
        }

        # Include every custom field automatically
        for key, value in record.__dict__.items():

            if key in STANDARD_LOG_RECORD_FIELDS:
                continue

            if key.startswith("_"):
                continue

            if key == "event":
                continue

            log[key] = value

        # Serialize exceptions properly
        if record.exc_info:
            exc_type, exc_value, _ = record.exc_info

            log["exception"] = {
                "type": exc_type.__name__,
                "message": str(exc_value),
            }

        return json.dumps(log, default=str)