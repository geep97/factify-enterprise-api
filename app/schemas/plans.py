from pydantic import BaseModel


class PlanInfo(BaseModel):
    name: str
    monthly_request_limit: int
    requests_per_hour: int
    price_pesewas: int | None
    price_display: str
    self_serve: bool