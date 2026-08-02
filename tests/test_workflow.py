from horizon_dsl.authoring.clarification import default_clarifications
from horizon_dsl.authoring.intent_parser import DEMO_BUSINESS_INTENT, build_demo_spec
from horizon_dsl.ui.workflow import (
    TARGET_AWS,
    TARGET_BIGQUERY,
    TARGET_JANINO,
    build_preliminary_bundle,
    build_spec_from_clarifications,
    initial_workflow_state,
    intent_is_stale,
    load_demo_text,
    normalize_output_fields,
    spec_is_valid,
    target_preview_for_selection,
    target_validation_message,
    workflow_stage,
)


def test_initial_workflow_state_is_staged() -> None:
    state = initial_workflow_state()
    assert state["intent_text"] == ""
    assert state["analysis"] is None
    assert state["preliminary_bundle"] is None
    assert state["spec_bundle"] is None
    assert workflow_stage(state) == "INTRO"


def test_load_demo_only_sets_text() -> None:
    loaded = load_demo_text(initial_workflow_state())
    assert loaded["intent_text"] == DEMO_BUSINESS_INTENT
    assert loaded["analysis"] is None
    assert workflow_stage(loaded) == "INTENT_ENTERED"


def test_analyse_intent_creates_analysis_and_preliminary_graph() -> None:
    bundle = build_preliminary_bundle(DEMO_BUSINESS_INTENT)
    assert bundle["analysis"]["detected_intent"]
    assert bundle["analysis"]["ambiguities"]
    assert "svg" in bundle["graph_svg"]
    assert "Assumed" in bundle["graph_svg"]


def test_output_fields_normalization() -> None:
    normalized = normalize_output_fields("decision, reason_code\nexplanation, fraud_score")
    assert normalized == "decision, reason_code, explanation, fraud_score"


def test_clarification_changes_do_not_affect_existing_spec_until_regeneration() -> None:
    original = build_spec_from_clarifications(default_clarifications())
    updated_clarifications = {**default_clarifications(), "merchant_field": "merchant_token"}
    assert original["spec"].entities["merchant"].key_field == "merchant_id"
    regenerated = build_spec_from_clarifications(updated_clarifications)
    assert regenerated["spec"].entities["merchant"].key_field == "merchant_token"


def test_selected_target_determines_preview() -> None:
    spec_bundle = build_spec_from_clarifications(default_clarifications())
    preview = target_preview_for_selection(spec_bundle, TARGET_BIGQUERY)
    assert preview["title"] == "GCP BigQuery SQL Preview"
    assert "CASE" in preview["code"]


def test_missing_or_invalid_spec_prevents_target_selection() -> None:
    preview = target_preview_for_selection(None, TARGET_JANINO)
    assert "Generate a valid Canonical Fraud Decision Specification" in preview["error"]


def test_aws_target_is_future_placeholder() -> None:
    spec_bundle = build_spec_from_clarifications(default_clarifications())
    preview = target_preview_for_selection(spec_bundle, TARGET_AWS)
    assert "later iteration" in preview["message"]
    assert preview["status"] == "Future Iteration"


def test_intent_change_detection_marks_analysis_stale() -> None:
    assert intent_is_stale("Different text", DEMO_BUSINESS_INTENT) is True
    assert intent_is_stale(DEMO_BUSINESS_INTENT, DEMO_BUSINESS_INTENT) is False


def test_semantic_validation_is_separate_from_target_validation() -> None:
    spec_bundle = build_spec_from_clarifications(default_clarifications())
    assert spec_is_valid(spec_bundle) is True
    assert "Target-specific validation" in target_validation_message()


def test_spec_bundle_renders_layer_two_views() -> None:
    bundle = build_spec_from_clarifications(default_clarifications())
    assert "spec_version" in bundle["yaml"]
    assert "svg" in bundle["graph_svg"]
    assert bundle["issues"] == []


def test_workflow_stage_advances_to_target_selected() -> None:
    state = initial_workflow_state()
    state["selected_target"] = TARGET_JANINO
    assert workflow_stage(state) == "TARGET_SELECTED"
