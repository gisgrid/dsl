from __future__ import annotations

import streamlit as st

from horizon_dsl.ui.workflow import TARGET_METADATA


def render_clarification_section(*, analysis: dict[str, object] | None, is_stale: bool) -> dict[str, object]:
    if analysis is None:
        return {"voice_clicked": False, "generate_spec_clicked": False, "target_clicked": None}

    st.markdown('<div class="fdx-section">', unsafe_allow_html=True)
    st.markdown('<div class="fdx-kicker">Section 3</div>', unsafe_allow_html=True)
    st.markdown("## Clarification and target selection")
    if is_stale:
        st.warning("The analysed intent is stale. Re-run Analyse Intent before relying on clarification or specification outputs.")

    left, right = st.columns([0.98, 1.02], gap="large")
    with left:
        st.markdown("### Clarification questions")
        for question in analysis["clarification_questions"]:
            st.write(f"- {question}")
        st.text_area(
            "Additional clarification in natural language",
            key="natural_language_clarification",
            height=140,
            help="Use this area to explain assumptions or provide missing information in plain English.",
            placeholder=(
                "Use merchant_id as the merchant identifier.\n"
                "Use device_fingerprint as the device identifier.\n"
                "Refer the transaction if a list lookup or model invocation fails.\n"
                "Use model version v7.\n"
                "All score boundaries are inclusive."
            ),
        )
        voice_clicked = st.button("Voice clarification", key="voice_clarification_button", help="Voice clarification")
        if st.session_state.get("voice_notice"):
            st.info(st.session_state.voice_notice)

    with right:
        st.markdown("### Structured clarification form")
        left_form, right_form = st.columns(2, gap="medium")
        with left_form:
            st.text_input(
                "Merchant identifier field",
                key="widget_merchant_field",
                help="The transaction field used to match the merchant blacklist.",
            )
            st.text_input(
                "Device identifier field",
                key="widget_device_field",
                help="The transaction field used to match the device blacklist.",
            )
            st.selectbox(
                "List lookup failure action",
                options=["APPROVE", "DECLINE", "REFER"],
                key="widget_list_lookup_error",
                help="The decision to return when the blacklist service cannot be queried.",
            )
            st.text_input(
                "Card Fraud Detection model ID",
                key="widget_model_id",
                help="The canonical model identifier used in the semantic specification.",
            )
            st.text_input(
                "Model version",
                key="widget_model_version",
                help="The model version or release tag used for the demo specification.",
            )

        with right_form:
            st.selectbox(
                "Model inference failure action",
                options=["APPROVE", "DECLINE", "REFER"],
                key="widget_model_inference_error",
                help="The decision returned when the model cannot be invoked or a required feature is missing.",
            )
            st.checkbox(
                "Score boundaries are inclusive",
                key="widget_score_boundaries_inclusive",
                help="Determines whether 800, 899, 900 and 999 are included in their displayed score bands.",
            )
            st.selectbox(
                "Decision for score below 800",
                options=["APPROVE", "DECLINE", "REFER"],
                key="widget_below_800_decision",
                help="The default decision when no blacklist matches occur and the model score falls below 800.",
            )
            st.text_area(
                "Required output fields",
                key="widget_output_fields",
                height=120,
                help="Comma-separated outputs expected from the final decision response.",
            )

    action_left, action_right = st.columns(2, gap="large")
    with action_left:
        st.markdown('<div class="fdx-action-group">', unsafe_allow_html=True)
        st.markdown("### Canonical Specification")
        st.caption("Build the Layer 2 semantic object, validate it and prepare the YAML and final decision graph.")
        generate_spec_clicked = st.button(
            "Generate / Update Canonical Specification",
            key="generate_spec_button",
            type="primary",
            use_container_width=True,
        )
        st.markdown("</div>", unsafe_allow_html=True)

    with action_right:
        st.markdown('<div class="fdx-action-group">', unsafe_allow_html=True)
        st.markdown("### Target Implementation Preview")
        st.caption("Select one target implementation path at a time after the canonical specification is ready.")
        target_clicked = None
        for target_id, metadata in TARGET_METADATA.items():
            if st.button(metadata["button_label"], key=f"target_button_{target_id}", use_container_width=True):
                target_clicked = target_id
        if st.session_state.get("target_notice"):
            st.info(st.session_state.target_notice)
        st.markdown("</div>", unsafe_allow_html=True)

    st.markdown("</div>", unsafe_allow_html=True)
    return {
        "voice_clicked": voice_clicked,
        "generate_spec_clicked": generate_spec_clicked,
        "target_clicked": target_clicked,
    }
