from app.infrastructure.config_rule_provider import ConfigRuleProvider


def test_get_rules_reads_values_from_yaml_file(tmp_path) -> None:
    rules_file = tmp_path / "rules.yaml"
    rules_file.write_text("max_wind_speed_kmh: 10\n")

    provider = ConfigRuleProvider(str(rules_file))
    rules = provider.get_rules()

    assert rules["max_wind_speed_kmh"] == 10