class FactifyException(Exception):
    """Base exception for the application."""

    def __init__(self, message: str):
        self.message = message
        super().__init__(message)


# ============================================================
# ORGANIZATION
# ============================================================

class OrganizationAlreadyExistsException(FactifyException):
    def __init__(self):
        super().__init__(
            "An organization with this slug already exists."
        )


# ============================================================
# API KEY
# ============================================================

class InvalidApiKeyException(FactifyException):
    def __init__(self):
        super().__init__("Invalid API key.")


class ApiKeyInactiveException(FactifyException):
    def __init__(self):
        super().__init__("API key is inactive.")


# ============================================================
# USAGE
# ============================================================

class MonthlyLimitExceededException(FactifyException):
    def __init__(self, limit: int, used: int):
        self.limit = limit
        self.used = used

        super().__init__(
            f"Monthly request limit exceeded. "
            f"Used {used} of {limit} requests."
        )


# ============================================================
# SUBSCRIPTION
# ============================================================

class SubscriptionNotFoundException(FactifyException):
    def __init__(self):
        super().__init__("Subscription not found.")


class InvalidSubscriptionPlanException(FactifyException):
    def __init__(self, plan_name: str):
        super().__init__(
            f"'{plan_name}' is not a valid subscription plan."
        )


class SubscriptionAlreadyCancelledException(FactifyException):
    def __init__(self):
        super().__init__(
            "Subscription is already cancelled."
        )


class SubscriptionAlreadyActiveException(FactifyException):
    def __init__(self):
        super().__init__(
            "Subscription is already active."
        )


class InactiveSubscriptionException(FactifyException):
    def __init__(self):
        super().__init__(
            "Subscription is inactive."
        )


# ============================================================
# FACTIFY
# ============================================================

class FactifyUnavailableException(FactifyException):
    def __init__(self):
        super().__init__(
            "Factify service is currently unavailable."
        )