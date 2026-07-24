from app.clients.factify_client import FactifyClient


class VerificationService:
    def __init__(
        self,
        client: FactifyClient,
    ):
        self.client = client

    async def verify(
        self,
        content: str,
        mode: str,
    ) -> dict:

        return await self.client.verify(
            content=content,
            mode=mode,
        )