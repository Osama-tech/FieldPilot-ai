"""YAML-backed implementation of RuleProvider."""

import yaml

from app.domain.rule_provider import RuleProvider


class ConfigRuleProvider(RuleProvider):
    def __init__(self, rules_path: str) -> None:
        self._rules_path = rules_path

    def get_rules(self) -> dict:
        with open(self._rules_path) as f:
            return yaml.safe_load(f)