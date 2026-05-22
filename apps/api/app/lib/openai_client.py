"""OpenAI-backed prompt classifier — the Layer router.

`classify_prompt` turns a plain-English prompt into a layer + hero/archetype
classification. It never raises: a missing key, an API error, a timeout, or a
malformed response all resolve to a safe fallback classification.
"""

import json
import logging
import os
from pathlib import Path

from dotenv import load_dotenv

from app.schemas.route import RouteResponse

load_dotenv()

logger = logging.getLogger("uvicorn.error")

# The system prompt is version-controlled and loaded once at import time.
_PROMPT_PATH = Path(__file__).resolve().parent.parent / "prompts" / "router.txt"
SYSTEM_PROMPT = _PROMPT_PATH.read_text(encoding="utf-8")

DEFAULT_MODEL = "gpt-4o-mini"
REQUEST_TIMEOUT_SECONDS = 8.0
_CACHE_LIMIT = 256

HERO_IDS = {
    "gearbox",
    "gripper",
    "robot-arm",
    "quadcopter",
    "v-twin",
    "differential",
    "bicycle",
    "nema-mount",
}
ARCHETYPES = {
    "bracket",
    "flange",
    "plate",
    "shaft",
    "gear",
    "housing",
    "pulley",
    "hub",
    "manifold",
    "clamp",
}
FALLBACK_HERO = "gearbox"

# Normalized prompt -> classification. Caps memory under burst booth traffic.
_cache: dict[str, RouteResponse] = {}
_client = None  # lazily constructed OpenAI client


def _fallback(reason: str) -> RouteResponse:
    """A guaranteed-valid classification used whenever the live path fails."""
    logger.warning("router fallback (%s)", reason)
    return RouteResponse(layer=1, hero=FALLBACK_HERO, archetype=None, params={}, source="fallback")


def _get_client():
    """Lazily construct the OpenAI client (only when a key is present)."""
    global _client
    if _client is None:
        from openai import OpenAI

        _client = OpenAI(timeout=REQUEST_TIMEOUT_SECONDS)
    return _client


def _coerce_params(raw: object) -> dict[str, float]:
    """Keep only string-keyed numeric entries; drop anything else."""
    if not isinstance(raw, dict):
        return {}
    params: dict[str, float] = {}
    for key, value in raw.items():
        if isinstance(key, str) and isinstance(value, (int, float)) and not isinstance(value, bool):
            params[key] = float(value)
    return params


def _parse(content: str) -> RouteResponse:
    """Parse and validate a model JSON response into a RouteResponse."""
    data = json.loads(content)
    layer = data.get("layer")
    if layer not in (1, 2, 3):
        raise ValueError(f"invalid layer: {layer!r}")

    hero = data.get("hero")
    archetype = data.get("archetype")
    params = _coerce_params(data.get("params"))

    if layer == 1:
        if hero not in HERO_IDS:
            raise ValueError(f"invalid hero: {hero!r}")
        archetype = None
    elif layer == 2:
        if archetype not in ARCHETYPES:
            raise ValueError(f"invalid archetype: {archetype!r}")
        hero = None
    else:
        hero = None
        archetype = None

    return RouteResponse(
        layer=layer, hero=hero, archetype=archetype, params=params, source="openai"
    )


def classify_prompt(prompt: str) -> RouteResponse:
    """Classify a prompt into a layer + hero/archetype. Never raises."""
    normalized = prompt.strip().lower()
    if not normalized:
        return _fallback("empty prompt")

    cached = _cache.get(normalized)
    if cached is not None:
        return cached.model_copy(update={"source": "cache"})

    if not os.getenv("OPENAI_API_KEY"):
        return _fallback("OPENAI_API_KEY not set")

    model = os.getenv("OPENAI_MODEL", DEFAULT_MODEL)
    try:
        response = _get_client().chat.completions.create(
            model=model,
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": prompt},
            ],
            response_format={"type": "json_object"},
            temperature=0,
        )
        content = response.choices[0].message.content
        if not content:
            return _fallback("empty model response")
        result = _parse(content)
    except Exception as exc:
        return _fallback(f"{type(exc).__name__}: {exc}")

    if len(_cache) >= _CACHE_LIMIT:
        _cache.clear()
    _cache[normalized] = result
    return result
