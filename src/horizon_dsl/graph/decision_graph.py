from __future__ import annotations

from horizon_dsl.semantic.models import FraudDecisionSpec


def render_decision_flow_text(spec: FraudDecisionSpec) -> str:
    return "\n".join(
        [
            "Transaction",
            "-> Merchant blacklist check",
            "   -> match => DECLINE",
            "-> Device blacklist check",
            "   -> match => DECLINE",
            "-> Card Fraud Detection model",
            "-> Score 900-999 => DECLINE",
            "-> Score 800-899 => REFER",
            "-> Score 0-799 => APPROVE",
        ]
    )


def render_mermaid_graph(spec: FraudDecisionSpec) -> str:
    return """flowchart TD
    A[Transaction] --> B{Merchant in fraudulent merchant list?}
    B -- Yes --> C[DECLINE\nFRAUDULENT_MERCHANT_MATCH]
    B -- No --> D{Device in fraudulent device list?}
    D -- Yes --> E[DECLINE\nFRAUDULENT_DEVICE_MATCH]
    D -- No --> F[Invoke Card Fraud Detection Model\nfraud_score 0-999]
    F --> G{Score band}
    G -- 900-999 --> H[DECLINE\nMODEL_SCORE_DECLINE]
    G -- 800-899 --> I[REFER\nMODEL_SCORE_REFER]
    G -- 0-799 --> J[APPROVE\nMODEL_SCORE_APPROVE]
"""
