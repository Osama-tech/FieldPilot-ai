"""Composition root: the single place where concrete implementations are
wired together. Everywhere else in the app depends on abstractions;
this file is where those abstractions meet their real implementations."""

from google import genai

from app.agent.tool_registry import ToolRegistry
from app.infrastructure.config import get_settings
from app.infrastructure.config_rule_provider import ConfigRuleProvider
from app.infrastructure.gemini_llm_client import GeminiLLMClient
from app.domain.llm_client import LLMClient
from app.infrastructure.weather_api_client import WeatherAPIClient
from app.tools.calculator_tool import CalculatorTool
from app.tools.risk_assessment_tool import RiskAssessmentTool
from app.tools.weather_tool import WeatherTool


def build_tool_registry() -> ToolRegistry:
    settings = get_settings()

    rule_provider = ConfigRuleProvider(settings.safety_rules_path)
    weather_api_client = WeatherAPIClient()

    registry = ToolRegistry()
    registry.register("calculator", CalculatorTool())
    registry.register("weather", WeatherTool(weather_api_client=weather_api_client))
    registry.register(
        "risk_assessment", RiskAssessmentTool(rule_provider=rule_provider)
    )

    return registry


def build_llm_client() -> LLMClient:
    settings = get_settings()
    genai_client = genai.Client(api_key=settings.gemini_api_key)   
    return GeminiLLMClient(client=genai_client, model=settings.gemini_model)