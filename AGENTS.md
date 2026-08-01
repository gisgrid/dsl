# Agent Guidance

## Project Purpose

Build and evolve a lightweight FDX Horizon Fraud DSL PoC that prioritises business authoring quality and a stable semantic model.

## Architectural Priorities

1. Preserve Layer 1 authoring clarity.
2. Keep Layer 2 as the canonical semantic source of truth.
3. Treat YAML, graph, and previews as views of the same meaning.
4. Keep Layer 3 preview-oriented unless requirements explicitly expand.

## Current Scope Boundary

- In scope: business English analysis, ambiguity detection, clarification prompts, canonical DSL, validation, Mermaid graph, preview templates, Streamlit UI, tests.
- Out of scope: production runtime, cloud deployment, CI/CD, Flink, online feature stores, model serving infrastructure, RBAC, HA, Redis, Memorystore, and generic compiler architecture.

## Coding Conventions

- Use Python 3.12.
- Prefer standard library modules when practical.
- Keep implementations deterministic and readable.
- Prefer small functions and explicit names over clever abstractions.
- Preserve ASCII unless a file already requires otherwise.

## Testing Expectations

- Add or update pytest coverage for semantic changes.
- Keep the demo scenario validating end to end.
- Ensure previews remain readable and derived from the canonical model.

## Forbidden Scope Expansion

- Do not silently add production deployment concerns.
- Do not introduce external services or API keys for the base PoC.
- Do not replace the template preview layer with a complex compiler unless explicitly requested.

## Semantic Safety

- Preserve semantic clarity across business intent, DSL, graph, and previews.
- Do not silently change DSL meanings.
- If a concept is ambiguous, surface it as a clarification need instead of guessing a hidden semantic change.
