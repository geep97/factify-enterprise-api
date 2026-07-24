import logging
import sys

from app.core.log_formatter import JsonFormatter


def configure_logging() -> None:
    """
    Configure application-wide logging.
    """

    handler = logging.StreamHandler(sys.stdout)
    handler.setFormatter(JsonFormatter())

    root_logger = logging.getLogger()

    root_logger.handlers.clear()
    root_logger.setLevel(logging.INFO)
    root_logger.addHandler(handler)


def get_logger(name: str) -> logging.Logger:
    """
    Return a configured logger.
    """
    return logging.getLogger(name)