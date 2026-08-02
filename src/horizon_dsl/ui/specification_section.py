from __future__ import annotations

from typing import cast

import streamlit as st

from horizon_dsl.semantic.validation import ValidationIssue
from horizon_dsl.ui.rendering import render_embedded_html


def render_specification_section(
    *,
    spec_bundle: dict[str, object] | None,
    target_preview: dict[str, object] | None,
    is_stale: bool,
) -> bool:
    if spec_bundle is None:
        return False

    st.markdown('<div class="fdx-section">', unsafe_allow_html=True)
    st.markdown('<div class="fdx-kicker">Section 4</div>', unsafe_allow_html=True)
    st.markdown("## Canonical specification and target implementation preview")
    if is_stale:
        st.warning("The displayed canonical specification and target preview belong to the previously analysed intent. Analyse again, then regenerate to refresh them.")

    left, right = st.columns([1.08, 0.92], gap="large")

    with left:
        st.markdown("### Layer 2 — Canonical Fraud Decision Specification")
        st.caption("This validates the Layer 2 semantic specification, not the target runtime.")
        tabs = st.tabs(["Fraud DSL YAML", "Decision Graph", "Semantic Validation"])

        with tabs[0]:
            st.caption("Technology-neutral semantic representation used as the single source of truth.")
            st.code(cast(str, spec_bundle["yaml"]), language="yaml")
            if cast(str, spec_bundle["review_context"]):
                with st.expander("Clarification review context"):
                    st.write(cast(str, spec_bundle["review_context"]))

        with tabs[1]:
            render_embedded_html(cast(str, spec_bundle["graph_svg"]), height=980)
            with st.expander("View graph source"):
                st.code(cast(str, spec_bundle["graph_source"]), language="text")

        with tabs[2]:
            st.markdown("**Semantic Validation**")
            issues = cast(list[ValidationIssue], spec_bundle["issues"])
            if issues:
                for issue in issues:
                    st.write(f"- {issue.level.upper()}: {issue.message}")
            else:
                st.success("Validation Passed")

    with right:
        validate_clicked = False
        st.markdown("### Layer 3 — Target-specific Technical Artifact")
        if target_preview is None:
            st.info("Select a target implementation preview in Section 3 to inspect one Layer 3 artefact at a time.")
        else:
            st.markdown('<div class="fdx-target-card">', unsafe_allow_html=True)
            st.markdown(f"**{target_preview['title']}**")
            st.markdown(
                f'<div class="fdx-status-line"><span class="fdx-badge">{target_preview["status"]}</span><span class="fdx-muted">{target_preview["platform"]}</span></div>',
                unsafe_allow_html=True,
            )
            if target_preview["message"]:
                st.info(cast(str, target_preview["message"]))
            if target_preview["code"]:
                language = "java"
                title = cast(str, target_preview["title"])
                if "BigQuery" in title:
                    language = "sql"
                elif "PySpark" in title:
                    language = "python"
                st.code(cast(str, target_preview["code"]), language=language)
            st.caption(cast(str, target_preview["note"]))
            validate_clicked = st.button("Validate & Test", key="validate_target_button")
            if st.session_state.get("target_validation_notice"):
                st.info(st.session_state.target_validation_notice)
            st.markdown("</div>", unsafe_allow_html=True)

    st.markdown("</div>", unsafe_allow_html=True)
    return validate_clicked
