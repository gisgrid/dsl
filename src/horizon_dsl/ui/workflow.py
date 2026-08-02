from __future__ import annotations

from copy import deepcopy
from typing import cast

from horizon_dsl.authoring.clarification import default_clarifications
from horizon_dsl.authoring.intent_parser import DEMO_BUSINESS_INTENT, build_demo_spec, parse_business_intent
from horizon_dsl.graph import render_decision_flow_text, render_mermaid_graph, render_svg_graph
from horizon_dsl.semantic import render_spec_yaml, validate_spec
from horizon_dsl.semantic.models import FraudDecisionSpec
from horizon_dsl.semantic.validation import ValidationIssue
from horizon_dsl.templates import render_bigquery_preview, render_janino_preview, render_pyspark_preview

TARGET_JANINO = "java_janino_flink"
TARGET_BIGQUERY = "gcp_bigquery"
TARGET_PYSPARK = "gcp_dataproc_pyspark"
TARGET_AWS = "aws_sagemaker_dragon"

TARGET_METADATA = {
    TARGET_JANINO: {
        "button_label": "Generate Java / Janino / Flink Preview",
        "title": "Java / Janino / Flink Preview",
        "platform": "Java + Janino + Flink",
        "status": "Template Preview",
    },
    TARGET_BIGQUERY: {
        "button_label": "Generate GCP BigQuery Preview",
        "title": "GCP BigQuery SQL Preview",
        "platform": "GCP BigQuery",
        "status": "Template Preview",
    },
    TARGET_PYSPARK: {
        "button_label": "Generate GCP DataProc / PySpark Preview",
        "title": "GCP DataProc / PySpark Preview",
        "platform": "GCP DataProc / PySpark",
        "status": "Template Preview",
    },
    TARGET_AWS: {
        "button_label": "Generate AWS SageMaker AI Preview for Dragon",
        "title": "AWS SageMaker AI Preview for Dragon",
        "platform": "AWS SageMaker AI implementation for Dragon",
        "status": "Future Iteration",
    },
}


def initial_workflow_state() -> dict[str, object]:
    return {
        "intent_text": "",
        "analysis": None,
        "analysed_intent_text": None,
        "clarifications": default_clarifications(),
        "natural_language_clarification": "",
        "preliminary_bundle": None,
        "spec_bundle": None,
        "selected_target": None,
        "target_preview": None,
        "voice_notice": None,
        "target_notice": None,
        "target_validation_notice": None,
    }


def workflow_stage(state: dict[str, object]) -> str:
    if state.get("selected_target"):
        return "TARGET_SELECTED"
    if state.get("spec_bundle"):
        return "SPEC_GENERATED"
    if state.get("analysis"):
        return "ANALYSED"
    if state.get("intent_text"):
        return "INTENT_ENTERED"
    return "INTRO"


def load_demo_text(state: dict[str, object]) -> dict[str, object]:
    updated = deepcopy(state)
    updated["intent_text"] = DEMO_BUSINESS_INTENT
    updated["target_notice"] = None
    updated["voice_notice"] = None
    updated["target_validation_notice"] = None
    return updated


def normalize_output_fields(raw_value: str) -> str:
    tokens = [token.strip() for token in raw_value.replace("\n", ",").split(",")]
    return ", ".join(token for token in tokens if token)


def intent_is_stale(current_text: str, analysed_text: str | None) -> bool:
    if analysed_text is None:
        return False
    return current_text.strip() != analysed_text.strip()


def build_preliminary_bundle(intent_text: str, clarifications: dict[str, str] | None = None) -> dict[str, object]:
    answers = default_clarifications() if clarifications is None else {**default_clarifications(), **clarifications}
    analysis = parse_business_intent(intent_text, clarifications=answers)
    draft_spec = build_demo_spec(answers)
    return {
        "analysis": analysis,
        "draft_spec": draft_spec,
        "flow_text": render_decision_flow_text(draft_spec),
        "graph_svg": render_svg_graph(draft_spec, preliminary=True),
        "graph_source": render_mermaid_graph(draft_spec),
    }


def build_spec_bundle(spec: FraudDecisionSpec, review_context: str = "") -> dict[str, object]:
    issues = validate_spec(spec)
    return {
        "spec": spec,
        "issues": issues,
        "yaml": render_spec_yaml(spec),
        "flow_text": render_decision_flow_text(spec),
        "graph_svg": render_svg_graph(spec, preliminary=False),
        "graph_source": render_mermaid_graph(spec),
        "review_context": review_context.strip(),
    }


def build_spec_from_clarifications(clarifications: dict[str, str], review_context: str = "") -> dict[str, object]:
    return build_spec_bundle(build_demo_spec(clarifications), review_context=review_context)


def spec_is_valid(spec_bundle: dict[str, object] | None) -> bool:
    if not spec_bundle:
        return False
    issues = cast(list[ValidationIssue], spec_bundle["issues"])
    return not any(getattr(issue, "level", "") == "error" for issue in issues)


def target_preview_for_selection(spec_bundle: dict[str, object] | None, target_id: str) -> dict[str, object]:
    if target_id not in TARGET_METADATA:
        return {"error": "Unknown target selection."}
    metadata = TARGET_METADATA[target_id]
    if not spec_is_valid(spec_bundle):
        return {
            "error": "Generate a valid Canonical Fraud Decision Specification before selecting a target implementation.",
            "target_id": target_id,
        }
    assert spec_bundle is not None

    if target_id == TARGET_AWS:
        return {
            "target_id": target_id,
            **metadata,
            "code": "",
            "message": "AWS SageMaker AI implementation preview for Dragon will be supported in a later iteration.",
            "note": "This is a PoC template preview, not production compiler output.",
        }

    spec = cast(FraudDecisionSpec, spec_bundle["spec"])
    if target_id == TARGET_JANINO:
        code = render_janino_preview(spec)
    elif target_id == TARGET_BIGQUERY:
        code = render_bigquery_preview(spec)
    else:
        code = render_pyspark_preview(spec)
    return {
        "target_id": target_id,
        **metadata,
        "code": code,
        "message": "",
        "note": "This is a PoC template preview, not production compiler output.",
    }


def target_validation_message() -> str:
    return "Target-specific validation, compilation and replay testing will be supported in a later iteration."
