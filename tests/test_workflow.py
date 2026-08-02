from horizon_dsl.authoring.intent_parser import build_demo_spec, parse_business_intent
from horizon_dsl.ui.workflow import initial_workflow_state, normalize_output_fields, spec_view_model


def test_initial_workflow_state_is_staged() -> None:
    state = initial_workflow_state()
    assert state["intent_text"] == ""
    assert state["analysis"] is None
    assert state["spec_bundle"] is None


def test_parse_business_intent_does_not_generate_spec() -> None:
    analysis = parse_business_intent("Decline suspicious transactions.")
    assert "spec" not in analysis
    assert analysis["detected_intent"]


def test_output_fields_normalization() -> None:
    normalized = normalize_output_fields("decision, reason_code\nexplanation, fraud_score")
    assert normalized == "decision, reason_code, explanation, fraud_score"


def test_spec_view_model_renders_after_generation() -> None:
    bundle = spec_view_model(build_demo_spec())
    assert "spec_version" in bundle["yaml"]
    assert "flowchart TD" in bundle["mermaid"]
    assert bundle["issues"] == []
