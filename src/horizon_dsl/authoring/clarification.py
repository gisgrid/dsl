from __future__ import annotations


def build_clarification_questions() -> list[str]:
    return [
        "Which field identifies the merchant?",
        "Which field identifies the device?",
        "What should happen if list lookup fails?",
        "What model ID and version should be used?",
        "What should happen if model inference fails?",
        "Are score boundaries inclusive?",
        "Should score below 800 always approve?",
        "Which output fields are required?",
    ]


def default_clarifications() -> dict[str, str]:
    return {
        "merchant_field": "merchant_id",
        "device_field": "device_id",
        "list_lookup_error": "REFER",
        "model_id": "card_fraud_detection_model",
        "model_version": "demo-v1",
        "model_inference_error": "REFER",
        "score_boundaries_inclusive": "true",
        "below_800_decision": "APPROVE",
        "output_fields": "decision, reason_code, explanation, fraud_score, matched_step_id, strategy_version",
    }
