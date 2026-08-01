from horizon_dsl.authoring.intent_parser import build_demo_spec
from horizon_dsl.semantic.validation import validate_spec


def _messages(spec) -> list[str]:
    return [issue.message for issue in validate_spec(spec)]


def test_demo_spec_validates() -> None:
    assert validate_spec(build_demo_spec()) == []


def test_invalid_score_range_fails() -> None:
    spec = build_demo_spec()
    band = spec.decision_flow.steps[3]
    band.range.min = 1000
    messages = _messages(spec)
    assert any("outside model score range" in message or "min greater than max" in message for message in messages)


def test_missing_model_resource_fails() -> None:
    spec = build_demo_spec()
    spec.resources.models.clear()
    messages = _messages(spec)
    assert any("missing model" in message for message in messages)


def test_missing_list_resource_fails() -> None:
    spec = build_demo_spec()
    spec.resources.lists.clear()
    messages = _messages(spec)
    assert any("missing list" in message for message in messages)


def test_duplicate_step_ids_fail() -> None:
    spec = build_demo_spec()
    spec.decision_flow.steps[1].id = spec.decision_flow.steps[0].id
    messages = _messages(spec)
    assert any("Duplicate step id" in message for message in messages)


def test_overlapping_score_bands_fail() -> None:
    spec = build_demo_spec()
    second_band = spec.decision_flow.steps[4]
    second_band.range.max = 950
    messages = _messages(spec)
    assert any("overlap" in message for message in messages)
