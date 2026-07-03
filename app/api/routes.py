"""API layer: HTTP <-> internal calls only, no business logic."""

from fastapi import APIRouter, Depends

from app.api.schemas import HealthResponse
from app.infrastructure.config import Settings, get_settings

router = APIRouter()


@router.get("/health", response_model=HealthResponse)
def health_check(settings: Settings = Depends(get_settings)) -> HealthResponse:
    return HealthResponse(
        status="ok",
        app_name=settings.app_name,
        environment=settings.environment,
    )