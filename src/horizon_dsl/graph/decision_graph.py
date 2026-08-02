from __future__ import annotations

from horizon_dsl.graph.graph_view_model import build_graph_view_model
from horizon_dsl.graph.svg_renderer import render_svg_document
from horizon_dsl.semantic.models import DefaultStep, FraudDecisionSpec, ListMatchStep, ModelInferenceStep, ScoreBandStep


def render_decision_flow_text(spec: FraudDecisionSpec) -> str:
    lines = [spec.input.event_type.replace("_", " ").title()]
    for step in spec.decision_flow.steps:
        if isinstance(step, ListMatchStep):
            lines.append(f"-> Check {step.list_ref} using {step.input_field}")
            lines.append(f"   -> match => {step.when_matched.decision}")
        elif isinstance(step, ModelInferenceStep):
            lines.append(f"-> Invoke {step.model_ref} => {step.output_field}")
        elif isinstance(step, ScoreBandStep):
            lines.append(f"-> Score {step.range.min}-{step.range.max} => {step.decision}")
        elif isinstance(step, DefaultStep):
            lines.append(f"-> Default => {step.decision}")
    return "\n".join(lines)


def render_mermaid_graph(spec: FraudDecisionSpec) -> str:
    lines = ["flowchart TD", f'    A["{spec.input.event_type}"]']
    current = "A"
    node_index = 1
    for step in spec.decision_flow.steps:
        if isinstance(step, ListMatchStep):
            decision_node = f"N{node_index}"
            outcome_node = f"N{node_index + 1}"
            lines.append(f'    {decision_node}{{"{step.list_ref} via {step.input_field}?"}}')
            lines.append(f"    {current} --> {decision_node}")
            lines.append(f'    {outcome_node}["{step.when_matched.decision}\\n{step.when_matched.reason_code}"]')
            lines.append(f"    {decision_node} -- Match --> {outcome_node}")
            current = decision_node
            node_index += 2
        elif isinstance(step, ModelInferenceStep):
            model_node = f"N{node_index}"
            lines.append(f'    {model_node}["{step.model_ref} -> {step.output_field}"]')
            lines.append(f"    {current} -- No match --> {model_node}")
            current = model_node
            node_index += 1
        elif isinstance(step, ScoreBandStep):
            outcome_node = f"N{node_index}"
            lines.append(f'    {outcome_node}["{step.decision}\\n{step.reason_code}"]')
            lines.append(f"    {current} -- {step.range.min}-{step.range.max} --> {outcome_node}")
            node_index += 1
        elif isinstance(step, DefaultStep):
            outcome_node = f"N{node_index}"
            lines.append(f'    {outcome_node}["{step.decision}\\n{step.reason_code}"]')
            lines.append(f"    {current} -- Default --> {outcome_node}")
            node_index += 1
    return "\n".join(lines) + "\n"


def render_svg_graph(spec: FraudDecisionSpec, preliminary: bool = False) -> str:
    return render_svg_document(build_graph_view_model(spec, preliminary=preliminary))
