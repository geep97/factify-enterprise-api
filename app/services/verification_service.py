import httpx

from app.core.config import settings


async def verify_with_factify(
    content: str,
    mode: str,
) -> dict:
    url = f"{settings.FACTIFY_CORE_API_URL}/api/verify"

    payload = {
        "content": content,
        "mode": mode,
    }

    async with httpx.AsyncClient(timeout=70.0) as client:
        response = await client.post(
            url,
            json=payload,
        )

    response.raise_for_status()

    return response.json()