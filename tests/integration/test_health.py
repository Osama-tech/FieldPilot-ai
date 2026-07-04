"""
Integration test: exercises the app through the same interface a real
client would use (HTTP), rather than calling functions directly.
This is what proves the layers are wired together correctly, not just
that each one works in isolation.
"""

from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_health_returns_200_with_expected_shape() -> None:
    response = client.get("/health")

    assert response.status_code == 200
    body = response.json()
    assert body["status"] == "ok"
    assert body["app_name"] == "FieldPilot AI"