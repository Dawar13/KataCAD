from fastapi import APIRouter

from app.lib.openai_client import classify_prompt
from app.schemas.route import RouteRequest, RouteResponse

router = APIRouter()


@router.post("/route", response_model=RouteResponse)
def route(request: RouteRequest) -> RouteResponse:
    """Classify a prompt into a layer + hero/archetype. Always answers 200."""
    return classify_prompt(request.prompt)
