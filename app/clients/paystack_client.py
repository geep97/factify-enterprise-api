import httpx

from app.core.config import settings


class PaystackClient:
    def __init__(self):
        self.base_url = "https://api.paystack.co"
        self.timeout = 30.0

    def _headers(self) -> dict:
        return {
            "Authorization": f"Bearer {settings.PAYSTACK_SECRET_KEY}",
        }

    async def initialize_transaction(
        self,
        email: str,
        amount_pesewas: int,
        reference: str,
        callback_url: str,
        currency: str = "GHS",
        metadata: dict | None = None,
    ) -> dict:

        url = f"{self.base_url}/transaction/initialize"

        payload = {
            "email": email,
            "amount": amount_pesewas,
            "reference": reference,
            "callback_url": callback_url,
            "currency": currency,
        }

        if metadata is not None:
            payload["metadata"] = metadata

        async with httpx.AsyncClient(timeout=self.timeout) as client:
            response = await client.post(
                url,
                json=payload,
                headers=self._headers(),
            )

        response.raise_for_status()

        return response.json()

    async def verify_transaction(self, reference: str) -> dict:

        url = f"{self.base_url}/transaction/verify/{reference}"

        async with httpx.AsyncClient(timeout=self.timeout) as client:
            response = await client.get(
                url,
                headers=self._headers(),
            )

        response.raise_for_status()

        return response.json()