from __future__ import annotations

from horizon_dsl.authoring.clarification import default_clarifications
from horizon_dsl.graph import render_decision_flow_text, render_mermaid_graph
from horizon_dsl.semantic import render_spec_yaml, validate_spec
from horizon_dsl.semantic.models import FraudDecisionSpec
from horizon_dsl.templates import render_bigquery_preview, render_janino_preview, render_pyspark_preview


def initial_workflow_state() -> dict[str, object]:
    return {
        "intent_text": "",
        "analysis": None,
        "clarifications": default_clarifications(),
        "spec_bundle": None,
    }


def normalize_output_fields(raw_value: str) -> str:
    tokens = [token.strip() for token in raw_value.replace("\n", ",").split(",")]
    return ", ".join(token for token in tokens if token)


def spec_view_model(spec: FraudDecisionSpec) -> dict[str, object]:
    issues = validate_spec(spec)
    return {
        "spec": spec,
        "issues": issues,
        "yaml": render_spec_yaml(spec),
        "flow_text": render_decision_flow_text(spec),
        "mermaid": render_mermaid_graph(spec),
        "janino": render_janino_preview(spec),
        "bigquery": render_bigquery_preview(spec),
        "pyspark": render_pyspark_preview(spec),
    }
