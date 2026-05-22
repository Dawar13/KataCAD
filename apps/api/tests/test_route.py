import pytest
from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


@pytest.mark.parametrize("prompt", ["asdfgh", "!!!", "qwertyuiop zxcvb"])
def test_route_falls_back_without_api_key(prompt: str, monkeypatch: pytest.MonkeyPatch) -> None:
    """With no API key, every prompt resolves to the fallback hero — no error."""
    monkeypatch.delenv("OPENAI_API_KEY", raising=False)

    response = client.post("/api/route", json={"prompt": prompt})

    assert response.status_code == 200
    data = response.json()
    assert data["layer"] == 1
    assert data["hero"] == "gearbox"
    assert data["archetype"] is None
    assert data["params"] == {}
    assert data["source"] == "fallback"


def test_route_rejects_missing_prompt() -> None:
    """A request body without a prompt fails validation."""
    response = client.post("/api/route", json={})
    assert response.status_code == 422
