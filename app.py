from __future__ import annotations

import json

import streamlit as st

from horizon_dsl.authoring import DEMO_BUSINESS_INTENT, parse_business_intent
from horizon_dsl.graph import render_decision_flow_text, render_mermaid_graph
from horizon_dsl.semantic import render_spec_yaml, validate_spec
from horizon_dsl.templates import render_bigquery_preview, render_janino_preview, render_pyspark_preview


st.set_page_config(page_title="FDX Horizon Fraud DSL PoC", layout="wide")


def _initial_state() -> None:
    if "intent_text" not in st.session_state:
        st.session_state.intent_text = DEMO_BUSINESS_INTENT
    if "analysis" not in st.session_state:
        st.session_state.analysis = parse_business_intent(DEMO_BUSINESS_INTENT)


def main() -> None:
    _initial_state()

    st.title("FDX Horizon Fraud DSL PoC")
    st.caption("PoC only: prioritises Layer 1 and Layer 2 semantics. Layer 3 previews are template-based, not production compilation.")

    left, middle = st.columns([1, 1.2])

    with left:
        st.subheader("Business Intent")
        intent_text = st.text_area("Business English input", value=st.session_state.intent_text, height=220)
        load_demo = st.button("Load demo")
        analyse = st.button("Analyse intent", type="primary")

        if load_demo:
            st.session_state.intent_text = DEMO_BUSINESS_INTENT
            st.session_state.analysis = parse_business_intent(DEMO_BUSINESS_INTENT)
            st.rerun()

        if analyse:
            st.session_state.intent_text = intent_text
            st.session_state.analysis = parse_business_intent(intent_text)

    analysis = st.session_state.analysis
    spec = analysis["spec"]
    issues = validate_spec(spec)

    with middle:
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

        st.subheader("Clarified Defaults")
        st.json(analysis["clarifications"])

    tabs = st.tabs([
        "Fraud DSL YAML",
        "Decision Graph",
        "Janino Preview",
        "BigQuery SQL Preview",
        "PySpark Preview",
        "Validation Results",
    ])

    with tabs[0]:
        st.code(render_spec_yaml(spec), language="yaml")

    with tabs[1]:
        st.text(render_decision_flow_text(spec))
        st.code(render_mermaid_graph(spec), language="mermaid")

    with tabs[2]:
        st.code(render_janino_preview(spec), language="java")

    with tabs[3]:
        st.code(render_bigquery_preview(spec), language="sql")

    with tabs[4]:
        st.code(render_pyspark_preview(spec), language="python")

    with tabs[5]:
        payload = [{"level": issue.level, "message": issue.message} for issue in issues]
        if payload:
            st.code(json.dumps(payload, indent=2), language="json")
        else:
            st.success("Validation passed.")


if __name__ == "__main__":
    main()
