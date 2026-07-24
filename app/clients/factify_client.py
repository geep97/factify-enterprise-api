import httpx

from app.core.config import settings


class FactifyClient:
    def __init__(self):
        self.base_url = settings.FACTIFY_CORE_API_URL
        self.timeout = 70.0

    async def verify(
        self,
        content: str,
        mode: str,
    ) -> dict:

        url = f"{self.base_url}/api/verify"

        payload = {
            "content": content,
            "mode": mode,
        }

        async with httpx.AsyncClient(timeout=self.timeout) as client:
            response = await client.post(
                url,
                json=payload,
            )

        response.raise_for_status()

        return response.json()