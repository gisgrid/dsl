# Architecture Summary

This summary is derived from `docs/02.1.FDX_Horizon_PoC_Architecture_Review_OFFLINE.html`, `docs/02.2.FDX_Horizon_PoC_Design_for_Codex.html`, and `docs/02.3.FDX_Horizon_DSL_Completeness_and_Production_Coverage_Plan_OFFLINE.html`.

## Core Framing

- Horizon sits in the broader fraud platform context but this PoC should focus on an authoring-to-semantic-to-preview flow.
- The important transformation chain is `Business Intent -> Canonical Fraud Decision Specification -> Target-specific artefacts -> Runtime execution`.
- The canonical semantic model is the most valuable long-term asset.
- A credible long-term roadmap requires production coverage evidence, capability matrices, and replay-based behavioural comparison rather than only design-time discussion.

## Four Layers

### Layer 1 - Business Authoring

- Primary users are fraud analysts and business SMEs.
- Natural language is allowed, but must be guided and clarified.
- The system should detect ambiguity, ask questions, and produce a clarified intent rather than code.

### Layer 2 - Semantic Authoring

- Layer 2 is the canonical fraud decision model.
- YAML, graph, and form/table views are alternative representations of one semantic source of truth.
- The model must carry decisions, reason codes, explanations, resource references, and explicit execution semantics such as `first_match` and `stop`.

### Layer 3 - Realisation

- Layer 3 can render Janino-style Java, BigQuery SQL, and PySpark previews.
- For the first PoC, these are shortcut/template outputs, not a full compiler.
- The design source explicitly warns against generating each backend directly from English because it risks semantic drift.
- Multiple target paths can be explained in the UI even when only a subset are currently previewed.

### Layer 4 - Runtime Deployment

- Runtime and infrastructure concerns are real in the target architecture, but not required for this PoC.
- Ownership of runtime transaction processing, state stores, and feature infrastructure may sit outside Horizon.

## Validation Expectations

- Validation should cover schema, semantic correctness, target-specific checks, and behavioural equivalence.
- For this bootstrap PoC, the repository implements the structural and semantic checks needed for the demo scenario.
- The production-coverage planning document adds capability-matrix and replay expectations as future evidence for migration readiness.

## PoC Direction From The Design Source

- Prioritise visible user feedback early with a small Streamlit interface.
- Make Layer 2 a real typed model.
- Add deterministic Layer 1 parsing and clarification for the demo scenario.
- Generate preview artefacts with templates.
- Render decision graphs offline from the canonical semantic model rather than relying on external rendering services.
- Keep scope intentionally narrow and avoid production runtime work.
