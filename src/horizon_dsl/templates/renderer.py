from __future__ import annotations

from importlib import resources

from jinja2 import Environment, FileSystemLoader

from horizon_dsl.semantic.models import DefaultStep, FraudDecisionSpec, ListMatchStep, ModelInferenceStep, ScoreBandStep


def _template_environment() -> Environment:
    template_dir = resources.files("horizon_dsl.templates")
    return Environment(loader=FileSystemLoader(str(template_dir)), trim_blocks=True, lstrip_blocks=True)


def _build_context(spec: FraudDecisionSpec) -> dict[str, object]:
    list_steps = [step for step in spec.decision_flow.steps if isinstance(step, ListMatchStep)]
    model_step = next(step for step in spec.decision_flow.steps if isinstance(step, ModelInferenceStep))
    score_bands = [step for step in spec.decision_flow.steps if isinstance(step, ScoreBandStep)]
    default_step = next(step for step in spec.decision_flow.steps if isinstance(step, DefaultStep))
    return {
        "strategy": spec.decision_strategy,
        "list_steps": list_steps,
        "model_step": model_step,
        "score_bands": score_bands,
        "default_step": default_step,
        "model_resource": next(model for model in spec.resources.models if model.id == model_step.model_ref),
    }


def render_janino_preview(spec: FraudDecisionSpec) -> str:
    env = _template_environment()
    return env.get_template("janino_template.java.j2").render(**_build_context(spec)).strip() + "\n"


def render_bigquery_preview(spec: FraudDecisionSpec) -> str:
    env = _template_environment()
    return env.get_template("bigquery_template.sql.j2").render(**_build_context(spec)).strip() + "\n"


def render_pyspark_preview(spec: FraudDecisionSpec) -> str:
    env = _template_environment()
    return env.get_template("pyspark_template.py.j2").render(**_build_context(spec)).strip() + "\n"
