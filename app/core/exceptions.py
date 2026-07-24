class FactifyException(Exception):
    """Base exception for the application."""


# ============================================================
# ORGANIZATION
# ============================================================

class OrganizationAlreadyExistsException(FactifyException):
    pass


# ============================================================
# API KEY
# ============================================================

class InvalidApiKeyException(FactifyException):
    pass


class ApiKeyInactiveException(FactifyException):
    pass


# ============================================================
# USAGE
# ============================================================

class MonthlyLimitExceededException(FactifyException):
    def __init__(self, limit: int, used: int):
        self.limit = limit
        self.used = used


# ============================================================
# FACTIFY
# ============================================================

class FactifyUnavailableException(FactifyException):
    pass