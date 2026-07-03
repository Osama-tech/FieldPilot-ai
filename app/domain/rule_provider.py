"""Abstraction for safety-rule retrieval, decoupled from storage backend.

Current implementation reads a YAML file (see
app.infrastructure.config_rule_provider). Designed so a future
retrieval-based implementation can replace it without changes to
consumers in the Tools layer.
"""

from abc import ABC, abstractmethod


class RuleProvider(ABC):
    @abstractmethod
    def get_rules(self) -> dict:
        """Return current safety rules, e.g. {"max_wind_speed_kmh": 24}."""
        raise NotImplementedError