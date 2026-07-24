from dataclasses import dataclass


@dataclass(frozen=True)
class SubscriptionPlan:
    name: str
    monthly_request_limit: int


FREE = SubscriptionPlan(
    name="Free",
    monthly_request_limit=1_000,
)

STARTER = SubscriptionPlan(
    name="Starter",
    monthly_request_limit=10_000,
)

PRO = SubscriptionPlan(
    name="Pro",
    monthly_request_limit=50_000,
)

ENTERPRISE = SubscriptionPlan(
    name="Enterprise",
    monthly_request_limit=1_000_000,
)


PLANS = {
    FREE.name: FREE,
    STARTER.name: STARTER,
    PRO.name: PRO,
    ENTERPRISE.name: ENTERPRISE,
}