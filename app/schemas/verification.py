from typing import Literal

from pydantic import BaseModel, Field


class VerificationRequest(BaseModel):
    content: str = Field(
        min_length=1,
        max_length=10000,
    )

    mode: Literal["headline", "article", "social"] = "headline"