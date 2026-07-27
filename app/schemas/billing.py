from pydantic import BaseModel


class CheckoutRequest(BaseModel):
    plan_name: str


class CheckoutResponse(BaseModel):
    authorization_url: str
    reference: str


class CheckoutStatusResponse(BaseModel):
    reference: str
    status: str
    plan_name: str