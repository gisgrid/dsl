from __future__ import annotations

import streamlit as st

from horizon_dsl.authoring import default_clarifications
from horizon_dsl.ui.clarification_section import render_clarification_section
from horizon_dsl.ui.intent_section import render_intent_section
from horizon_dsl.ui.overview import render_overview_section
from horizon_dsl.ui.specification_section import render_specification_section
from horizon_dsl.ui.styles import app_styles
from horizon_dsl.ui.workflow import (
    build_preliminary_bundle,
    build_spec_from_clarifications,
    initial_workflow_state,
    intent_is_stale,
    load_demo_text,
    normalize_output_fields,
    target_preview_for_selection,
    target_validation_message,
)


st.set_page_config(page_title="FDX Horizon", layout="wide")


def _initialise_state() -> None:
    defaults = initial_workflow_state()
    for key, value in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = value
    if "pending_intent_editor" in st.session_state:
        st.session_state.intent_text = st.session_state.pending_intent_editor
        st.session_state.intent_editor = st.session_state.pending_intent_editor
        st.session_state.pop("pending_intent_editor")
    if "intent_editor" not in st.session_state:
        st.session_state.intent_editor = st.session_state.intent_text
    _load_clarification_widgets(force=False)


def _load_clarification_widgets(force: bool) -> None:
    clarifications = st.session_state.clarifications
    values = {
        "widget_merchant_field": clarifications["merchant_field"],
        "widget_device_field": clarifications["device_field"],
        "widget_list_lookup_error": clarifications["list_lookup_error"],
        "widget_model_id": clarifications["model_id"],
        "widget_model_version": clarifications["model_version"],
        "widget_model_inference_error": clarifications["model_inference_error"],
        "widget_score_boundaries_inclusive": clarifications["score_boundaries_inclusive"].lower() == "true",
        "widget_below_800_decision": clarifications["below_800_decision"],
        "widget_output_fields": clarifications["output_fields"],
    }
    for key, value in values.items():
        if force or key not in st.session_state:
            st.session_state[key] = value


def _capture_clarifications() -> dict[str, str]:
    return {
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


def _apply_load_demo() -> None:
    updated = load_demo_text(dict(st.session_state))
    st.session_state.intent_text = updated["intent_text"]
    st.session_state.pending_intent_editor = updated["intent_text"]
    st.session_state.target_notice = updated["target_notice"]
    st.session_state.voice_notice = updated["voice_notice"]
    st.session_state.target_validation_notice = updated["target_validation_notice"]


def _apply_analysis(intent_text: str) -> None:
    st.session_state.intent_text = intent_text
    preliminary_bundle = build_preliminary_bundle(intent_text)
    st.session_state.analysis = preliminary_bundle["analysis"]
    st.session_state.preliminary_bundle = preliminary_bundle
    st.session_state.analysed_intent_text = intent_text
    st.session_state.clarifications = default_clarifications()
    st.session_state.natural_language_clarification = ""
    st.session_state.spec_bundle = None
    st.session_state.selected_target = None
    st.session_state.target_preview = None
    st.session_state.target_notice = None
    st.session_state.target_validation_notice = None
    _load_clarification_widgets(force=True)


def _apply_spec_generation() -> None:
    st.session_state.clarifications = _capture_clarifications()
    st.session_state.spec_bundle = build_spec_from_clarifications(
        st.session_state.clarifications,
        review_context=st.session_state.natural_language_clarification,
    )
    st.session_state.selected_target = None
    st.session_state.target_preview = None
    st.session_state.target_notice = None
    st.session_state.target_validation_notice = None


def _apply_target_selection(target_id: str) -> None:
    preview = target_preview_for_selection(st.session_state.spec_bundle, target_id)
    if "error" in preview:
        st.session_state.target_notice = preview["error"]
        return
    st.session_state.selected_target = target_id
    st.session_state.target_preview = preview
    st.session_state.target_notice = None
    st.session_state.target_validation_notice = None


def main() -> None:
    _initialise_state()
    st.markdown(app_styles(), unsafe_allow_html=True)

    render_overview_section()
    st.divider()

    current_text, intent_actions = render_intent_section(
        intent_text=st.session_state.intent_text,
        analysis=st.session_state.analysis,
        preliminary_bundle=st.session_state.preliminary_bundle,
        is_stale=intent_is_stale(st.session_state.intent_editor, st.session_state.analysed_intent_text),
    )

    if intent_actions["load_demo_clicked"]:
        _apply_load_demo()
        st.rerun()
    if intent_actions["analyse_clicked"]:
        _apply_analysis(current_text)
        st.rerun()

    is_stale = intent_is_stale(current_text, st.session_state.analysed_intent_text)
    st.divider()

    clarification_actions = render_clarification_section(analysis=st.session_state.analysis, is_stale=is_stale)
    if clarification_actions["voice_clicked"]:
        st.session_state.voice_notice = "Voice clarification will be supported in a later iteration."
        st.rerun()
    if clarification_actions["generate_spec_clicked"]:
        _apply_spec_generation()
        st.rerun()
    if clarification_actions["target_clicked"]:
        _apply_target_selection(clarification_actions["target_clicked"])
        st.rerun()

    st.divider()

    validate_clicked = render_specification_section(
        spec_bundle=st.session_state.spec_bundle,
        target_preview=st.session_state.target_preview,
        is_stale=is_stale,
    )
    if validate_clicked:
        st.session_state.target_validation_notice = target_validation_message()
        st.rerun()


if __name__ == "__main__":
    main()
