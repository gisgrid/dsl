from __future__ import annotations

from dataclasses import dataclass

from horizon_dsl.semantic.models import DefaultStep, FraudDecisionSpec, ModelInferenceStep, ScoreBandStep

SUPPORTED_DECISIONS = {"APPROVE", "DECLINE", "REFER"}


@dataclass(slots=True)
class ValidationIssue:
    level: str
    message: str


def _ranges_overlap(left: ScoreBandStep, right: ScoreBandStep) -> bool:
    if left.range.max < right.range.min or right.range.max < left.range.min:
        return False
    if left.range.max == right.range.min:
        return left.range.include_max and right.range.include_min
    if right.range.max == left.range.min:
        return right.range.include_max and left.range.include_min
    return True


def validate_spec(spec: FraudDecisionSpec) -> list[ValidationIssue]:
    issues: list[ValidationIssue] = []

    model_map = {model.id: model for model in spec.resources.models}
    list_map = {resource.id: resource for resource in spec.resources.lists}
    step_ids: set[str] = set()
    score_bands: list[ScoreBandStep] = []
    default_steps: list[DefaultStep] = []
    inferred_model = None

    for model in spec.resources.models:
        if model.output.minimum > model.output.maximum:
            issues.append(ValidationIssue("error", f"Model '{model.id}' has minimum greater than maximum."))
        if model.on_inference_error not in SUPPORTED_DECISIONS:
            issues.append(ValidationIssue("error", f"Model '{model.id}' uses unsupported inference decision."))

    for resource in spec.resources.lists:
        if resource.on_lookup_error not in SUPPORTED_DECISIONS:
            issues.append(ValidationIssue("error", f"List '{resource.id}' uses unsupported lookup decision."))

    for step in spec.decision_flow.steps:
        if step.id in step_ids:
            issues.append(ValidationIssue("error", f"Duplicate step id '{step.id}'."))
        step_ids.add(step.id)

        if step.type == "list_match":
            if step.list_ref not in list_map:
                issues.append(ValidationIssue("error", f"Step '{step.id}' references missing list '{step.list_ref}'."))
            if step.when_matched.decision not in SUPPORTED_DECISIONS:
                issues.append(ValidationIssue("error", f"Step '{step.id}' uses unsupported decision."))
        elif step.type == "model_inference":
            if step.model_ref not in model_map:
                issues.append(ValidationIssue("error", f"Step '{step.id}' references missing model '{step.model_ref}'."))
            else:
                inferred_model = model_map[step.model_ref]
                if step.output_field != inferred_model.output.field:
                    issues.append(ValidationIssue("error", f"Step '{step.id}' output field does not match model output field."))
        elif step.type == "score_band":
            if step.decision not in SUPPORTED_DECISIONS:
                issues.append(ValidationIssue("error", f"Step '{step.id}' uses unsupported decision."))
            if step.range.min > step.range.max:
                issues.append(ValidationIssue("error", f"Step '{step.id}' has min greater than max."))
            if inferred_model is not None:
                if step.range.min < inferred_model.output.minimum or step.range.max > inferred_model.output.maximum:
                    issues.append(ValidationIssue("error", f"Step '{step.id}' is outside model score range."))
            score_bands.append(step)
        elif step.type == "default":
            if step.decision not in SUPPORTED_DECISIONS:
                issues.append(ValidationIssue("error", f"Step '{step.id}' uses unsupported decision."))
            default_steps.append(step)

    if spec.decision_flow.mode == "first_match" and not default_steps:
        issues.append(ValidationIssue("error", "first_match flow requires a default step."))

    for index, left in enumerate(score_bands):
        for right in score_bands[index + 1 :]:
            if _ranges_overlap(left, right):
                issues.append(ValidationIssue("error", f"Score bands '{left.id}' and '{right.id}' overlap."))

    for step in score_bands:
        if step.range.min == 900 and step.range.max == 999 and step.decision != "DECLINE":
            issues.append(ValidationIssue("error", "900-999 score band must map to DECLINE for the demo scenario."))
        if step.range.min == 800 and step.range.max == 899 and step.decision != "REFER":
            issues.append(ValidationIssue("error", "800-899 score band must map to REFER for the demo scenario."))

    for step in default_steps:
        if step.decision != "APPROVE":
            issues.append(ValidationIssue("error", "Default step must map to APPROVE for the demo scenario."))

    return issues
