from __future__ import annotations

from horizon_dsl.authoring.ambiguity_detector import detect_ambiguities
from horizon_dsl.authoring.clarification import build_clarification_questions, default_clarifications
from horizon_dsl.semantic.models import (
    DecisionFlow,
    DecisionOutcome,
    DecisionStrategy,
    DefaultStep,
    EntityDefinition,
    FraudDecisionSpec,
    InputEvent,
    ListMatchStep,
    ListResource,
    ModelInferenceStep,
    ModelOutput,
    ModelResource,
    ResourceCatalog,
    ScoreBandStep,
    ScoreRange,
)

DEMO_BUSINESS_INTENT = """Decline the transaction immediately if the merchant is on the known fraudulent merchant list
or if the device ID is on the known fraudulent device list.

Otherwise, score the transaction using our in-house Card Fraud Detection model.
The model returns a score from 0 to 999.

Decline the transaction when the score is between 900 and 999.
Refer the transaction for review when the score is between 800 and 899.
Otherwise, approve the transaction."""


def build_demo_spec(clarifications: dict[str, str] | None = None) -> FraudDecisionSpec:
    answers = default_clarifications()
    if clarifications:
        answers.update(clarifications)

    merchant_field = answers["merchant_field"]
    device_field = answers["device_field"]
    model_id = answers["model_id"]
    model_version = answers["model_version"]
    list_lookup_error = answers["list_lookup_error"]
    model_inference_error = answers["model_inference_error"]
    score_boundaries_inclusive = str(answers["score_boundaries_inclusive"]).lower() == "true"
    below_800_decision = answers["below_800_decision"]
    output_fields = [field.strip() for field in answers["output_fields"].split(",")]

    return FraudDecisionSpec(
        spec_version="0.1",
        decision_strategy=DecisionStrategy(
            id="card_fraud_rule_model_demo",
            name="Card Fraud Rule and Model Decision",
            description=(
                "Decline known fraudulent merchant or device transactions. "
                "Otherwise invoke the in-house card fraud model and decide by score bands."
            ),
        ),
        input=InputEvent(event_type="card_transaction", event_time_field="transaction_time"),
        entities={
            "merchant": EntityDefinition(key_field=merchant_field),
            "device": EntityDefinition(key_field=device_field),
        },
        resources=ResourceCatalog(
            lists=[
                ListResource(
                    id="fraudulent_merchant_list",
                    lookup_key=merchant_field,
                    version="demo-v1",
                    on_lookup_error=list_lookup_error,
                ),
                ListResource(
                    id="fraudulent_device_list",
                    lookup_key=device_field,
                    version="demo-v1",
                    on_lookup_error=list_lookup_error,
                ),
            ],
            models=[
                ModelResource(
                    id=model_id,
                    name="In-house Card Fraud Detection Model",
                    version=model_version,
                    output=ModelOutput(field="fraud_score", minimum=0, maximum=999),
                    on_inference_error=model_inference_error,
                )
            ],
        ),
        decision_flow=DecisionFlow(
            steps=[
                ListMatchStep(
                    id="check_fraudulent_merchant",
                    type="list_match",
                    list_ref="fraudulent_merchant_list",
                    input_field=merchant_field,
                    when_matched=DecisionOutcome(
                        decision="DECLINE",
                        reason_code="FRAUDULENT_MERCHANT_MATCH",
                        explanation="Merchant is present in the known fraudulent merchant list.",
                    ),
                ),
                ListMatchStep(
                    id="check_fraudulent_device",
                    type="list_match",
                    list_ref="fraudulent_device_list",
                    input_field=device_field,
                    when_matched=DecisionOutcome(
                        decision="DECLINE",
                        reason_code="FRAUDULENT_DEVICE_MATCH",
                        explanation="Device is present in the known fraudulent device list.",
                    ),
                ),
                ModelInferenceStep(
                    id="invoke_card_fraud_model",
                    type="model_inference",
                    model_ref=model_id,
                    output_field="fraud_score",
                ),
                ScoreBandStep(
                    id="decline_high_score",
                    type="score_band",
                    score_field="fraud_score",
                    range=ScoreRange(
                        min=900,
                        max=999,
                        include_min=score_boundaries_inclusive,
                        include_max=score_boundaries_inclusive,
                    ),
                    decision="DECLINE",
                    reason_code="MODEL_SCORE_DECLINE",
                    explanation="Model fraud score is between 900 and 999.",
                ),
                ScoreBandStep(
                    id="refer_medium_high_score",
                    type="score_band",
                    score_field="fraud_score",
                    range=ScoreRange(
                        min=800,
                        max=899,
                        include_min=score_boundaries_inclusive,
                        include_max=score_boundaries_inclusive,
                    ),
                    decision="REFER",
                    reason_code="MODEL_SCORE_REFER",
                    explanation="Model fraud score is between 800 and 899.",
                ),
                DefaultStep(
                    id="approve_default",
                    type="default",
                    decision=below_800_decision,
                    reason_code="MODEL_SCORE_APPROVE",
                    explanation="No blacklist match and model score is below 800.",
                ),
            ]
        ),
        outputs=output_fields,
    )


def parse_business_intent(intent_text: str, clarifications: dict[str, str] | None = None) -> dict[str, object]:
    return {
        "intent_text": intent_text,
        "detected_intent": [
            "Merchant blacklist match => DECLINE",
            "Device blacklist match => DECLINE",
            "Invoke in-house card fraud model => fraud_score 0-999",
            "Score 900-999 => DECLINE",
            "Score 800-899 => REFER",
            "Otherwise => APPROVE",
        ],
        "ambiguities": detect_ambiguities(intent_text),
        "clarification_questions": build_clarification_questions(),
        "clarifications": default_clarifications() if clarifications is None else {**default_clarifications(), **clarifications},
    }
