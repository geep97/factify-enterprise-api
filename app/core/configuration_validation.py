from app.core.config import settings


def validate_configuration() -> None:
    """
    Validate application configuration before startup.

    This function ensures all required configuration values are
    present and satisfy basic application rules. It should perform
    only fast, deterministic checks and must not make any network
    or database calls.
    """

    _validate_required_settings()
    _validate_api_key_prefix()


def _validate_required_settings() -> None:
    """Ensure required settings are configured."""

    required_settings = {
        "DATABASE_URL": settings.DATABASE_URL,
        "FACTIFY_CORE_API_URL": settings.FACTIFY_CORE_API_URL,
        "API_KEY_PREFIX": settings.API_KEY_PREFIX,
        "ENVIRONMENT": settings.ENVIRONMENT,
    }

    for setting_name, value in required_settings.items():
        if not value or not value.strip():
            raise RuntimeError(
                f"Configuration error: '{setting_name}' must be configured."
            )


def _validate_api_key_prefix() -> None:
    """
    Ensure API keys use the expected prefix format.
    """

    if not settings.API_KEY_PREFIX.startswith("factify_"):
        raise RuntimeError(
            "Configuration error: API_KEY_PREFIX must start with 'factify_'."
        )