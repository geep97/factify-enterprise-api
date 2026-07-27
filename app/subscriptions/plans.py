from dataclasses import dataclass

from app.core.exceptions import InvalidSubscriptionPlanException


@dataclass(frozen=True)
class SubscriptionPlan:
    name: str
    monthly_request_limit: int
    requests_per_hour: int
    # None = not self-serve (contact sales). 0 = free. Otherwise
    # price in pesewas (GHS's smallest currency unit — 100 = GH₵1).
    price_pesewas: int | None

    @property
    def is_self_serve(self) -> bool:
        return self.price_pesewas is not None and self.price_pesewas > 0


FREE = SubscriptionPlan(
    name="Free",
    monthly_request_limit=1_000,
    requests_per_hour=100,
    price_pesewas=0,
)

STARTER = SubscriptionPlan(
    name="Starter",
    monthly_request_limit=10_000,
    requests_per_hour=300,
    price_pesewas=15_000,  # GH₵150/mo
)

PRO = SubscriptionPlan(
    name="Pro",
    monthly_request_limit=50_000,
    requests_per_hour=1_000,
    price_pesewas=60_000,  # GH₵600/mo
)

ENTERPRISE = SubscriptionPlan(
    name="Enterprise",
    monthly_request_limit=1_000_000,
    requests_per_hour=5_000,
    price_pesewas=None,  # contact sales
)


PLANS = {
    FREE.name: FREE,
    STARTER.name: STARTER,
    PRO.name: PRO,
    ENTERPRISE.name: ENTERPRISE,
}


def get_plan(name: str) -> SubscriptionPlan:
    plan = PLANS.get(name)

    if plan is None:
        raise InvalidSubscriptionPlanException()

    return plan