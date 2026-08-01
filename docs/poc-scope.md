# PoC Scope

## In Scope

- Business English input for the demo fraud scenario
- Ambiguity detection and clarification questions
- A canonical fraud decision DSL / IR for one rule-plus-model decision strategy
- YAML rendering of the semantic model
- Decision-flow graph rendering
- Preview-only Janino-style Java output
- Preview-only BigQuery SQL output
- Optional preview-only PySpark output
- Local Streamlit application for review and demonstration
- Local pytest coverage and import checks

## Out Of Scope

- Production deployment or runtime integration
- Generic compiler or full target adapter framework
- Flink runtime, stateful streaming, or cloud infrastructure
- GCP, AWS, Feedzai, CI/CD, RBAC, HA, Redis, Memorystore
- Real LLM integration or API-key dependent workflows
- Model training, online model serving, or feature-store implementation
- Multi-scenario authoring breadth beyond the initial rule-plus-model PoC
