from horizon_dsl.authoring.clarification import default_clarifications
from horizon_dsl.authoring.intent_parser import build_demo_spec
from horizon_dsl.graph import render_svg_graph


def test_preliminary_graph_contains_demo_path_values() -> None:
    svg = render_svg_graph(build_demo_spec(default_clarifications()), preliminary=True)
    assert "fraudulent_merchant_list" in svg
    assert "fraudulent_device_list" in svg
    assert "card_fraud_detection_model" in svg
    assert "[900-999]" in svg
    assert "[800-899]" in svg
    assert "MODEL_SCORE_APPROVE" in svg


def test_final_graph_values_derive_from_spec() -> None:
    clarifications = {**default_clarifications(), "merchant_field": "merchant_token", "model_id": "card_fraud_v7"}
    svg = render_svg_graph(build_demo_spec(clarifications), preliminary=False)
    assert "merchant_token" in svg
    assert "card_fraud_v7" in svg


def test_graph_renderer_escapes_text() -> None:
    spec = build_demo_spec()
    list_step = spec.decision_flow.steps[0]
    list_step.list_ref = 'fraud_list_<unsafe>&"'
    svg = render_svg_graph(spec, preliminary=False)
    assert 'fraud_list_&lt;unsafe&gt;&amp;&quot;' in svg
    assert 'fraud_list_<unsafe>&"' not in svg
