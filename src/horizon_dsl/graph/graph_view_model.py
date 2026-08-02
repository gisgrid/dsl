from __future__ import annotations

from dataclasses import dataclass, field

from horizon_dsl.semantic.models import DefaultStep, FraudDecisionSpec, ListMatchStep, ModelInferenceStep, ScoreBandStep


@dataclass(slots=True)
class GraphNode:
    id: str
    kind: str
    title: str
    subtitle: str = ""
    detail: str = ""
    x: int = 0
    y: int = 0
    width: int = 260
    height: int = 82
    assumed: bool = False


@dataclass(slots=True)
class GraphEdge:
    source: str
    target: str
    label: str = ""


@dataclass(slots=True)
class GraphViewModel:
    title: str
    subtitle: str
    nodes: list[GraphNode] = field(default_factory=list)
    edges: list[GraphEdge] = field(default_factory=list)
    width: int = 1040
    height: int = 780
    preliminary: bool = False


def _range_label(step: ScoreBandStep) -> str:
    left = "[" if step.range.include_min else "("
    right = "]" if step.range.include_max else ")"
    return f"{left}{step.range.min}-{step.range.max}{right}"


def build_graph_view_model(spec: FraudDecisionSpec, preliminary: bool = False) -> GraphViewModel:
    list_steps = [step for step in spec.decision_flow.steps if isinstance(step, ListMatchStep)]
    model_step = next(step for step in spec.decision_flow.steps if isinstance(step, ModelInferenceStep))
    score_steps = [step for step in spec.decision_flow.steps if isinstance(step, ScoreBandStep)]
    default_step = next(step for step in spec.decision_flow.steps if isinstance(step, DefaultStep))

    nodes: list[GraphNode] = [
        GraphNode(
            id="transaction",
            kind="input",
            title=spec.input.event_type.replace("_", " ").title(),
            subtitle=f"event time: {spec.input.event_time_field}",
            x=390,
            y=24,
            width=260,
            height=72,
            assumed=preliminary,
        )
    ]
    edges: list[GraphEdge] = []

    center_x = 390
    left_x = 50
    right_x = 730
    current_source = "transaction"
    base_y = 150
    spacing_y = 150

    for index, step in enumerate(list_steps):
        node_id = f"step_{step.id}"
        decision_x = left_x if index % 2 == 0 else right_x
        nodes.append(
            GraphNode(
                id=node_id,
                kind="decision",
                title=f"Check {step.list_ref}",
                subtitle=f"lookup by {step.input_field}",
                detail=step.id,
                x=center_x,
                y=base_y + index * spacing_y,
                assumed=preliminary,
            )
        )
        outcome_id = f"outcome_{step.id}"
        nodes.append(
            GraphNode(
                id=outcome_id,
                kind="outcome",
                title=step.when_matched.decision,
                subtitle=step.when_matched.reason_code,
                detail=step.when_matched.explanation,
                x=decision_x,
                y=base_y + index * spacing_y + 110,
                width=260,
                height=92,
            )
        )
        edges.append(GraphEdge(source=current_source, target=node_id))
        edges.append(GraphEdge(source=node_id, target=outcome_id, label="Match"))
        current_source = node_id

    model_y = base_y + len(list_steps) * spacing_y
    model_id = f"step_{model_step.id}"
    nodes.append(
        GraphNode(
            id=model_id,
            kind="process",
            title=f"Invoke {model_step.model_ref}",
            subtitle=f"output field: {model_step.output_field}",
            detail=model_step.id,
            x=center_x,
            y=model_y,
            assumed=preliminary,
        )
    )
    edges.append(GraphEdge(source=current_source, target=model_id, label="No match" if list_steps else "Start"))

    score_node_id = "score_gate"
    score_gate_y = model_y + 140
    nodes.append(
        GraphNode(
            id=score_node_id,
            kind="decision",
            title="Evaluate score bands",
            subtitle=f"field: {model_step.output_field}",
            detail=spec.decision_flow.mode,
            x=center_x,
            y=score_gate_y,
            assumed=preliminary,
        )
    )
    edges.append(GraphEdge(source=model_id, target=score_node_id))

    bottom_y = score_gate_y + 130
    outcome_positions = [left_x, center_x, right_x]
    for index, step in enumerate(score_steps):
        outcome_id = f"outcome_{step.id}"
        position_x = outcome_positions[min(index, len(outcome_positions) - 1)]
        nodes.append(
            GraphNode(
                id=outcome_id,
                kind="outcome",
                title=step.decision,
                subtitle=step.reason_code,
                detail=step.explanation,
                x=position_x,
                y=bottom_y,
                width=260,
                height=92,
            )
        )
        edges.append(GraphEdge(source=score_node_id, target=outcome_id, label=_range_label(step)))

    default_id = f"outcome_{default_step.id}"
    nodes.append(
        GraphNode(
            id=default_id,
            kind="outcome",
            title=default_step.decision,
            subtitle=default_step.reason_code,
            detail=default_step.explanation,
            x=right_x,
            y=bottom_y + 118,
            width=260,
            height=92,
        )
    )
    edges.append(GraphEdge(source=score_node_id, target=default_id, label="Default"))

    height = max(node.y + node.height for node in nodes) + 50
    subtitle = "Preliminary interpretation with assumptions." if preliminary else "Canonical specification rendered from Layer 2 semantics."
    return GraphViewModel(
        title=spec.decision_strategy.name,
        subtitle=subtitle,
        nodes=nodes,
        edges=edges,
        width=1040,
        height=height,
        preliminary=preliminary,
    )
