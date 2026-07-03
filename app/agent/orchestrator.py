from app.domain.models import FieldInfo, SprayRecommendation
from app.infrastructure.llm_client import LLMClient


async def decide_spray_recommendation(
    field: FieldInfo,
    latitude: float,
    longitude: float,
    chemical_type: str,
    spray_rate_liters_per_hectare: float,
    llm_client: LLMClient,
) -> SprayRecommendation:
    raise NotImplementedError
