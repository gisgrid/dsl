from __future__ import annotations

import streamlit as st


def render_embedded_html(html_content: str, height: int) -> None:
    st.markdown(
        (
            f"<div style='width:100%; min-height:{height}px; overflow-x:auto;'>"
            f"{html_content}"
            "</div>"
        ),
        unsafe_allow_html=True,
    )
