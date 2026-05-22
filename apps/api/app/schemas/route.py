from typing import Literal

from pydantic import BaseModel, Field


class RouteRequest(BaseModel):
    """A prompt to classify."""

    prompt: str


class RouteResponse(BaseModel):
    """The router's classification of a prompt."""

    layer: Literal[1, 2, 3]
    hero: str | None = None
    archetype: str | None = None
    params: dict[str, float] = Field(default_factory=dict)
    source: Literal["openai", "cache", "fallback"]
