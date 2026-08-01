from horizon_dsl.authoring.intent_parser import build_demo_spec
from horizon_dsl.templates.renderer import render_bigquery_preview, render_janino_preview, render_pyspark_preview


def test_janino_output_includes_blacklist_checks_and_score_bands() -> None:
    rendered = render_janino_preview(build_demo_spec())
    assert "fraudulent_merchant_list" in rendered
    assert "fraudulent_device_list" in rendered
    assert ">= 900" in rendered
    assert ">= 800" in rendered


def test_bigquery_output_includes_case_logic() -> None:
    rendered = render_bigquery_preview(build_demo_spec())
    assert "CASE" in rendered
    assert "WHEN merchant_blacklisted" in rendered
    assert "ELSE 'APPROVE'" in rendered


def test_pyspark_output_includes_when_clauses() -> None:
    rendered = render_pyspark_preview(build_demo_spec())
    assert ".when(" in rendered
    assert "merchant_blacklisted" in rendered
    assert "otherwise" in rendered
