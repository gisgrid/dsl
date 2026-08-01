from horizon_dsl.authoring.intent_parser import build_demo_spec
from horizon_dsl.semantic.models import FraudDecisionSpec


def test_demo_spec_instantiates() -> None:
    spec = build_demo_spec()
    assert isinstance(spec, FraudDecisionSpec)
    assert spec.decision_strategy.id == "card_fraud_rule_model_demo"
    assert spec.outputs[-1] == "strategy_version"
