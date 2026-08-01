# ADR-001: PoC Layer Boundary

## Status

Accepted

## Context

The design source documents define a four-layer architecture and explicitly recommend that the first PoC prove business authoring quality and a stable semantic layer before tackling production runtime or broad backend support.

## Decision

- The PoC prioritises Layer 1 business authoring and Layer 2 semantic modelling.
- Layer 3 is implemented as preview/template rendering only.
- Layer 4 deployment and runtime integration are out of scope.
- A generic compiler is deferred.
- A real LLM integration is deferred.
- The current PoC supports one rule-plus-model scenario: blacklist checks followed by model score bands.

## Consequences

- The repository can show a clear end-to-end user flow early.
- Semantic meaning is centralised in a typed canonical model.
- Preview outputs are easy to inspect but are not production artefacts.
- Future work can replace templates with more deterministic generators without changing the Layer 1 and Layer 2 contract.
