from __future__ import annotations

from typing import cast

import streamlit as st


def render_intent_section(
    *,
    intent_text: str,
    analysis: dict[str, object] | None,
    preliminary_bundle: dict[str, object] | None,
    is_stale: bool,
) -> tuple[str, dict[str, bool]]:
    st.markdown('<div class="fdx-section">', unsafe_allow_html=True)
    st.markdown('<div class="fdx-kicker">Section 2</div>', unsafe_allow_html=True)
    st.markdown("## Business intent and preliminary interpretation")
    left, right = st.columns([1.05, 1.0], gap="large")

    with left:
        current_text = st.text_area(
            "Business Intent",
            key="intent_editor",
            height=260,
            placeholder="Describe the fraud strategy in natural language or load the demo scenario.",
        )
        button_left, button_right = st.columns(2)
        with button_left:
            load_demo_clicked = st.button("Load Demo", key="load_demo_button", use_container_width=True)
        with button_right:
            analyse_clicked = st.button("Analyse Intent", key="analyse_intent_button", type="primary", use_container_width=True)

        if analysis is None:
            st.info("Enter or load a Business Intent, then click Analyse Intent to see the preliminary interpretation.")
        else:
            if is_stale:
                st.warning("Business intent has changed. Analyse again to refresh the interpretation.")
                with st.expander("Previous analysis snapshot", expanded=False):
                    _render_analysis_lists(analysis)
            else:
                _render_analysis_lists(analysis)

    with right:
        if preliminary_bundle is None:
            st.info("The preliminary interpretation graph appears after Analyse Intent.")
        else:
            if is_stale:
                st.markdown('<div class="fdx-stale">', unsafe_allow_html=True)
            st.subheader("Preliminary decision interpretation")
            st.caption(
                "Preliminary interpretation based on the current business intent. Assumptions and unresolved ambiguities can be corrected in the clarification stage."
            )
            st.html(preliminary_bundle["graph_svg"])
            with st.expander("View graph source"):
                st.code(preliminary_bundle["graph_source"], language="text")
            if is_stale:
                st.markdown("</div>", unsafe_allow_html=True)

    st.markdown("</div>", unsafe_allow_html=True)
    return current_text, {"load_demo_clicked": load_demo_clicked, "analyse_clicked": analyse_clicked}


def _render_analysis_lists(analysis: dict[str, object]) -> None:
    st.markdown("### Detected Intent")
    for item in cast(list[str], analysis["detected_intent"]):
        st.write(f"- {item}")
    st.markdown("### Ambiguities")
    ambiguities = cast(list[str], analysis["ambiguities"])
    if ambiguities:
        for item in ambiguities:
            st.write(f"- {item}")
    else:
        st.write("- No major ambiguities detected for the demo path.")
