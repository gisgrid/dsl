from horizon_dsl.authoring.intent_parser import build_demo_spec
from horizon_dsl.semantic.yaml_renderer import render_spec_yaml


def test_yaml_output_includes_expected_decisions() -> None:
    yaml_output = render_spec_yaml(build_demo_spec())
    assert "DECLINE" in yaml_output
    assert "REFER" in yaml_output
    assert "APPROVE" in yaml_output
