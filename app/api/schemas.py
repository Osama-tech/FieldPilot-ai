"""API-facing request/response models, kept separate from domain models
so the two contracts can evolve independently."""

from pydantic import BaseModel


class HealthResponse(BaseModel):
    status: str
    app_name: str
    environment: str