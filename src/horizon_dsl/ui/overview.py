from __future__ import annotations

import streamlit as st


VALUE_PROPOSITIONS = [
    (
        "Shared language",
        "Business users review natural language and decision graphs, while IT teams review the DSL and technical artefacts — all derived from the same semantic object.",
    ),
    (
        "Ambiguity resolved early",
        "Fields, thresholds, failure paths, priorities and default actions are clarified before production implementation begins.",
    ),
    (
        "Define once, realise across platforms",
        "The same fraud strategy can be represented independently of Java / Flink, BigQuery, DataProc or AWS technology stacks.",
    ),
    (
        "Traceable and governable",
        "Business intent, clarification answers, canonical DSL, decision graphs and implementation artefacts remain connected and reviewable.",
    ),
    (
        "Faster Business–IT iteration",
        "Business and technology colleagues can jointly confirm whether the system has interpreted the fraud strategy correctly before investing in full delivery.",
    ),
    (
        "Migration readiness",
        "Production rule coverage and replay comparison can later provide evidence that the DSL is expressive enough and behaviourally equivalent to current production implementations.",
    ),
]

CURRENT_COVERAGE = [
    ("Business English input", "Covered"),
    ("Deterministic interpretation for the demo scenario", "Covered"),
    ("Detected intent", "Covered"),
    ("Ambiguity identification", "Covered"),
    ("Clarification questions", "Covered"),
    ("Structured clarification form", "Covered"),
    ("Canonical Fraud DSL / IR", "Covered"),
    ("YAML representation", "Covered"),
    ("Preliminary and final decision graph", "Covered"),
    ("Janino preview", "Preview only"),
    ("BigQuery SQL preview", "Preview only"),
    ("PySpark preview", "Preview only"),
    ("Semantic validation", "Covered"),
]

FUTURE_COVERAGE = [
    ("General-purpose natural-language understanding", "Future iteration"),
    ("Live LLM integration", "Out of scope"),
    ("Full production rule coverage", "Future iteration"),
    ("Generic production compiler", "Future iteration"),
    ("Real Java / Flink execution", "Out of scope"),
    ("Real BigQuery execution", "Out of scope"),
    ("Real DataProc execution", "Out of scope"),
    ("Real AWS SageMaker execution", "Out of scope"),
    ("Runtime deployment", "Out of scope"),
    ("Foundry build and release pipeline", "Future iteration"),
    ("Production model serving", "Out of scope"),
    ("Production feature store", "Out of scope"),
    ("Production replay and behavioural-equivalence validation", "Future iteration"),
    ("Authentication and RBAC", "Out of scope"),
    ("HA, scalability and performance engineering", "Out of scope"),
]


def _pill(label: str) -> str:
    mapping = {
        "Covered": "fdx-pill fdx-pill-covered",
        "Preview only": "fdx-pill fdx-pill-preview",
        "Future iteration": "fdx-pill fdx-pill-future",
        "Out of scope": "fdx-pill fdx-pill-scope",
    }
    return f'<span class="{mapping[label]}">{label}</span>'


def render_overview_section() -> None:
    st.markdown('<div class="fdx-section">', unsafe_allow_html=True)
    st.markdown('<div class="fdx-kicker">Section 1</div>', unsafe_allow_html=True)
    left, right = st.columns([1.05, 1.1], gap="large")

    with left:
        st.markdown('<div class="fdx-hero-title">FDX Horizon</div>', unsafe_allow_html=True)
        st.markdown('<div class="fdx-hero-subtitle">Fraud Decision Authoring and Portability PoC</div>', unsafe_allow_html=True)
        st.markdown(
            '<div class="fdx-intro">Turn fraud detection ideas expressed by Business and Fraud Analysts into a structured, reviewable and portable decision specification before committing to a target implementation.</div>',
            unsafe_allow_html=True,
        )
        st.markdown("### Four-layer concept")
        layers = [
            (
                "Layer 1: Business Intent",
                "Business and Fraud Analysts describe fraud detection requirements in natural language.",
                [],
                "Semantic interpretation, ambiguity detection and clarification",
            ),
            (
                "Layer 2: Canonical Fraud Decision Specification",
                "A structured, reviewable and technology-neutral Fraud DSL / intermediate representation.",
                [],
                "Compilation or generation",
            ),
            (
                "Layer 3: Target-specific Technical Artifacts",
                "Implementation artefacts generated or previewed for a selected target technology.",
                ["Java / Janino", "GCP BigQuery SQL", "GCP DataProc / PySpark", "AWS-oriented model and decision artefacts"],
                "Verification, approval and deployment integration",
            ),
            (
                "Layer 4: Runtime Execution",
                "Possible target implementation paths for Target Runtime and Deployment Integration.",
                [
                    "Java + Janino + Flink",
                    "GCP BigQuery",
                    "GCP DataProc / PySpark",
                    "AWS SageMaker AI implementation for Dragon",
                ],
                "",
            ),
        ]
        for title, description, items, connector in layers:
            list_markup = "" if not items else "<ul class=\"fdx-layer-list\">" + "".join(f"<li>{item}</li>" for item in items) + "</ul>"
            st.markdown(
                f'<div class="fdx-layer-card"><div class="fdx-layer-title">{title}</div><div class="fdx-layer-desc">{description}</div>{list_markup}</div>',
                unsafe_allow_html=True,
            )
            if connector:
                st.markdown(f'<div class="fdx-connector">{connector}</div>', unsafe_allow_html=True)

    with right:
        st.markdown("### Why FDX Horizon?")
        for index, (title, copy) in enumerate(VALUE_PROPOSITIONS, start=1):
            st.markdown(
                f'<div class="fdx-value"><div class="fdx-value-num">{index}</div><div><div class="fdx-value-title">{title}</div><div class="fdx-value-copy">{copy}</div></div></div>',
                unsafe_allow_html=True,
            )

    st.markdown("### Current PoC Coverage")
    covered_col, future_col = st.columns(2, gap="large")
    with covered_col:
        st.markdown('<div class="fdx-coverage-card">', unsafe_allow_html=True)
        st.markdown("**Covered in the current PoC**")
        for label, status in CURRENT_COVERAGE:
            st.markdown(f'<div class="fdx-coverage-item"><span>{label}</span>{_pill(status)}</div>', unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)
    with future_col:
        st.markdown('<div class="fdx-coverage-card">', unsafe_allow_html=True)
        st.markdown("**Not covered in this PoC iteration**")
        for label, status in FUTURE_COVERAGE:
            st.markdown(f'<div class="fdx-coverage-item"><span>{label}</span>{_pill(status)}</div>', unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)
