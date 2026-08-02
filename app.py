from __future__ import annotations

import json

import streamlit as st

from horizon_dsl.authoring import DEMO_BUSINESS_INTENT, default_clarifications, parse_business_intent
from horizon_dsl.authoring.intent_parser import build_demo_spec
from horizon_dsl.ui import initial_workflow_state, normalize_output_fields, spec_view_model


st.set_page_config(page_title="FDX Horizon Fraud DSL PoC", layout="wide")


def _initial_state() -> None:
    defaults = initial_workflow_state()
    for key, value in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = value


def _analysis_ready() -> bool:
    return st.session_state.analysis is not None


def _spec_ready() -> bool:
    return st.session_state.spec_bundle is not None


def _update_clarifications_from_widgets() -> None:
    st.session_state.clarifications = {
        "merchant_field": st.session_state.widget_merchant_field,
        "device_field": st.session_state.widget_device_field,
        "list_lookup_error": st.session_state.widget_list_lookup_error,
        "model_id": st.session_state.widget_model_id,
        "model_version": st.session_state.widget_model_version,
        "model_inference_error": st.session_state.widget_model_inference_error,
        "score_boundaries_inclusive": "true" if st.session_state.widget_score_boundaries_inclusive else "false",
        "below_800_decision": st.session_state.widget_below_800_decision,
        "output_fields": normalize_output_fields(st.session_state.widget_output_fields),
    }


def _load_clarifications_into_widgets() -> None:
    clarifications = st.session_state.clarifications
    st.session_state.setdefault("widget_merchant_field", clarifications["merchant_field"])
    st.session_state.setdefault("widget_device_field", clarifications["device_field"])
    st.session_state.setdefault("widget_list_lookup_error", clarifications["list_lookup_error"])
    st.session_state.setdefault("widget_model_id", clarifications["model_id"])
    st.session_state.setdefault("widget_model_version", clarifications["model_version"])
    st.session_state.setdefault("widget_model_inference_error", clarifications["model_inference_error"])
    st.session_state.setdefault(
        "widget_score_boundaries_inclusive",
        clarifications["score_boundaries_inclusive"].lower() == "true",
    )
    st.session_state.setdefault("widget_below_800_decision", clarifications["below_800_decision"])
    st.session_state.setdefault("widget_output_fields", clarifications["output_fields"])


def _reset_clarification_widgets() -> None:
    for key in [
        "widget_merchant_field",
        "widget_device_field",
        "widget_list_lookup_error",
        "widget_model_id",
        "widget_model_version",
        "widget_model_inference_error",
        "widget_score_boundaries_inclusive",
        "widget_below_800_decision",
        "widget_output_fields",
    ]:
        st.session_state.pop(key, None)


def main() -> None:
    _initial_state()
    _load_clarifications_into_widgets()

    st.title("FDX Horizon Fraud DSL PoC")
    st.caption("PoC only: prioritises Layer 1 and Layer 2 semantics. Layer 3 previews are template-based, not production compilation.")
    st.info("Enter a business intent or load the demo text, then click Analyse Intent to begin the staged review flow.")

    left, middle = st.columns([1, 1.2])

    with left:
        st.subheader("Business Intent")
        intent_text = st.text_area("Business English input", value=st.session_state.intent_text, height=220)
        load_demo = st.button("Load demo")
        analyse = st.button("Analyse intent", type="primary")

        if load_demo:
            st.session_state.intent_text = DEMO_BUSINESS_INTENT
            st.session_state.spec_bundle = None
            st.rerun()

        if analyse:
            st.session_state.intent_text = intent_text
            st.session_state.analysis = parse_business_intent(intent_text)
            st.session_state.clarifications = default_clarifications()
            st.session_state.spec_bundle = None
            _reset_clarification_widgets()
            st.rerun()

    with middle:
        if not _analysis_ready():
            st.subheader("Awaiting Analysis")
            st.write("No analysed intent yet. Use Load Demo or type your own business intent, then click Analyse Intent.")
        else:
            analysis = st.session_state.analysis
            st.subheader("Detected Intent")
            for item in analysis["detected_intent"]:
                st.write(f"- {item}")

            st.subheader("Ambiguities")
            ambiguities = analysis["ambiguities"]
            if ambiguities:
                for item in ambiguities:
                    st.write(f"- {item}")
            else:
                st.write("- No major ambiguities detected for the demo path.")

            st.subheader("Clarification Questions")
            for question in analysis["clarification_questions"]:
                st.write(f"- {question}")

    if _analysis_ready():
        st.subheader("Clarification Form")
        form_left, form_right = st.columns(2)

        with form_left:
            st.text_input("merchant_field", key="widget_merchant_field")
            st.text_input("device_field", key="widget_device_field")
            st.selectbox("list_lookup_error", options=["APPROVE", "DECLINE", "REFER"], key="widget_list_lookup_error")
            st.text_input("model_id", key="widget_model_id")
            st.text_input("model_version", key="widget_model_version")

        with form_right:
            st.selectbox("model_inference_error", options=["APPROVE", "DECLINE", "REFER"], key="widget_model_inference_error")
            st.checkbox("score_boundaries_inclusive", key="widget_score_boundaries_inclusive")
            st.selectbox("below_800_decision", options=["APPROVE", "DECLINE", "REFER"], key="widget_below_800_decision")
            st.text_area("output_fields", key="widget_output_fields", height=110)

        if st.button("Generate / Update Specification", type="primary"):
            _update_clarifications_from_widgets()
            spec = build_demo_spec(st.session_state.clarifications)
            st.session_state.spec_bundle = spec_view_model(spec)
            st.rerun()

    if _spec_ready():
        spec_bundle = st.session_state.spec_bundle
        tabs = st.tabs([
            "Fraud DSL YAML",
            "Decision Graph",
            "Janino Preview",
            "BigQuery SQL Preview",
            "PySpark Preview",
            "Validation Results",
        ])

        with tabs[0]:
            st.code(spec_bundle["yaml"], language="yaml")

        with tabs[1]:
            st.text(spec_bundle["flow_text"])
            st.code(spec_bundle["mermaid"], language="mermaid")

        with tabs[2]:
            st.code(spec_bundle["janino"], language="java")

        with tabs[3]:
            st.code(spec_bundle["bigquery"], language="sql")

        with tabs[4]:
            st.code(spec_bundle["pyspark"], language="python")

        with tabs[5]:
            payload = [{"level": issue.level, "message": issue.message} for issue in spec_bundle["issues"]]
            if payload:
                st.code(json.dumps(payload, indent=2), language="json")
            else:
                st.success("Validation passed.")


if __name__ == "__main__":
    main()
