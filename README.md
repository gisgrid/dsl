# FDX Horizon Fraud DSL PoC

Small Streamlit PoC for FDX Horizon fraud decision authoring.

## What This PoC Is

This repository demonstrates a guided path from business English to a reviewable fraud decision DSL, a decision-flow view, and preview-only technical artefacts.

## In Scope

- Layer 1 business intent capture, ambiguity detection, and clarification prompts
- Layer 2 canonical fraud decision DSL / IR with validation and YAML rendering
- Decision-flow graph rendering
- Layer 3 preview generation for Janino-style Java, BigQuery SQL, and optional PySpark
- One rule-plus-model demo scenario for card transaction fraud decisions

## Out Of Scope

- Production deployment and runtime infrastructure
- Cloud integration, CI/CD, RBAC, HA, Redis, Memorystore
- Flink, GCP, AWS, Feedzai, and production model serving
- Generic production compiler or direct LLM-to-code generation

## Demo Scenario

1. Decline immediately when `merchant_id` is in a known fraudulent merchant list.
2. Else decline immediately when `device_id` is in a known fraudulent device list.
3. Else invoke the in-house card fraud model.
4. `900-999` => `DECLINE`
5. `800-899` => `REFER`
6. `0-799` => `APPROVE`

Layer 3 is template-based preview generation, not a production compiler.

## PoC Demonstration Flow

1. Understand the Horizon concept and current scope
2. Enter or load a Business Intent
3. Analyse the preliminary interpretation
4. Review ambiguities
5. Provide natural-language and structured clarification
6. Generate the Canonical Fraud Decision Specification
7. Review YAML, graph and semantic validation
8. Select a target implementation preview
9. Future: target validation, replay, approval and deployment

## Install

```bash
python -m venv .venv
.venv\Scripts\activate
pip install -e .
```

## Run

```bash
streamlit run app.py
```

## Tests

```bash
pytest
```

## Project Layout

- `app.py` - Streamlit PoC UI
- `src/horizon_dsl/semantic` - canonical models, validation, YAML rendering
- `src/horizon_dsl/authoring` - deterministic Layer 1 parsing and clarification helpers
- `src/horizon_dsl/graph` - semantic graph view models and offline SVG rendering
- `src/horizon_dsl/templates` - Layer 3 preview renderers and Jinja templates
- `src/horizon_dsl/ui` - staged presentation flow, section renderers, and UI helpers
- `examples/rule_model_demo` - demo business intent and expected assets
- `docs/` - source design documents, scope notes, and ADRs
