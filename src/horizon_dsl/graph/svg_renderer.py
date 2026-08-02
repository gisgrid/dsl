from __future__ import annotations

import html
import textwrap

from horizon_dsl.graph.graph_view_model import GraphEdge, GraphNode, GraphViewModel


def _escape(value: str) -> str:
    return html.escape(value, quote=True)


def _wrap_lines(text: str, width: int) -> list[str]:
    if not text:
        return []
    return textwrap.wrap(text, width=width, break_long_words=False, break_on_hyphens=False) or [text]


def _node_center(node: GraphNode) -> tuple[int, int]:
    return node.x + node.width // 2, node.y + node.height // 2


def _edge_path(source: GraphNode, target: GraphNode) -> str:
    source_x, source_y = _node_center(source)
    target_x, target_y = _node_center(target)
    start_y = source.y + source.height
    end_y = target.y
    if source_x == target_x:
        return f"M {source_x} {start_y} L {target_x} {end_y}"
    mid_y = (start_y + end_y) // 2
    return f"M {source_x} {start_y} L {source_x} {mid_y} L {target_x} {mid_y} L {target_x} {end_y}"


def _render_node(node: GraphNode, preliminary: bool) -> str:
    classes = ["node", node.kind]
    if node.kind == "outcome":
        classes.append(node.title.lower())
    if preliminary and node.assumed:
        classes.append("assumed")
    title_lines = _wrap_lines(node.title, 26)
    subtitle_lines = _wrap_lines(node.subtitle, 34)
    detail_lines = _wrap_lines(node.detail, 42)
    current_y = node.y + 26
    lines: list[str] = []

    for index, line in enumerate(title_lines[:2]):
        lines.append(
            f'<text x="{node.x + node.width / 2}" y="{current_y + index * 18}" class="node-title">{_escape(line)}</text>'
        )
    current_y += max(18, len(title_lines[:2]) * 18)
    for index, line in enumerate(subtitle_lines[:2]):
        lines.append(
            f'<text x="{node.x + node.width / 2}" y="{current_y + index * 16}" class="node-subtitle">{_escape(line)}</text>'
        )
    current_y += len(subtitle_lines[:2]) * 16
    for index, line in enumerate(detail_lines[:2]):
        lines.append(
            f'<text x="{node.x + node.width / 2}" y="{current_y + 14 + index * 15}" class="node-detail">{_escape(line)}</text>'
        )

    badge = ""
    if preliminary and node.assumed:
        badge = (
            f'<g class="assumed-badge"><rect x="{node.x + node.width - 82}" y="{node.y + 10}" width="70" height="22" rx="11" />'
            f'<text x="{node.x + node.width - 47}" y="{node.y + 25}">Assumed</text></g>'
        )

    return (
        f'<g id="{_escape(node.id)}" class="{" ".join(classes)}">'
        f'<title>{_escape(node.title)}</title>'
        f'<desc>{_escape(" ".join(filter(None, [node.subtitle, node.detail])) or node.title)}</desc>'
        f'<rect x="{node.x}" y="{node.y}" width="{node.width}" height="{node.height}" rx="18" ry="18" />'
        + badge
        + "".join(lines)
        + "</g>"
    )


def _render_edge(edge: GraphEdge, nodes: dict[str, GraphNode]) -> str:
    source = nodes[edge.source]
    target = nodes[edge.target]
    path = _edge_path(source, target)
    source_x, source_y = _node_center(source)
    target_x, target_y = _node_center(target)
    label_x = source_x if source_x == target_x else (source_x + target_x) // 2
    label_y = (source.y + source.height + target.y) // 2 - 8
    label = ""
    if edge.label:
        label = (
            f'<g class="edge-label"><rect x="{label_x - 48}" y="{label_y - 14}" width="96" height="24" rx="12" />'
            f'<text x="{label_x}" y="{label_y + 2}">{_escape(edge.label)}</text></g>'
        )
    return f'<g class="edge"><path d="{path}" />{label}</g>'


def render_svg_document(graph: GraphViewModel) -> str:
    nodes = {node.id: node for node in graph.nodes}
    node_markup = "".join(_render_node(node, graph.preliminary) for node in graph.nodes)
    edge_markup = "".join(_render_edge(edge, nodes) for edge in graph.edges)
    return f"""
<div class="fdx-graph-shell">
  <svg viewBox="0 0 {graph.width} {graph.height}" role="img" aria-label="{_escape(graph.title)}">
    <title>{_escape(graph.title)}</title>
    <desc>{_escape(graph.subtitle)}</desc>
    <defs>
      <marker id="fdx-arrow" markerWidth="12" markerHeight="12" refX="9" refY="6" orient="auto">
        <path d="M0,0 L0,12 L12,6 z" fill="var(--fdx-edge)" />
      </marker>
    </defs>
    <style>
      :root {{
        --fdx-bg: #f8fafc;
        --fdx-panel: #ffffff;
        --fdx-text: #101828;
        --fdx-muted: #475467;
        --fdx-edge: #667085;
        --fdx-label-bg: #eef2f6;
        --fdx-input-fill: #eaf2ff;
        --fdx-input-stroke: #175cd3;
        --fdx-decision-fill: #fff7ed;
        --fdx-decision-stroke: #b54708;
        --fdx-process-fill: #f4f3ff;
        --fdx-process-stroke: #6941c6;
        --fdx-outcome-fill: #ecfdf3;
        --fdx-outcome-stroke: #067647;
        --fdx-assumed-fill: #fef3c7;
        --fdx-assumed-text: #92400e;
      }}
      @media (prefers-color-scheme: dark) {{
        :root {{
          --fdx-bg: #111827;
          --fdx-panel: #111827;
          --fdx-text: #f8fafc;
          --fdx-muted: #cbd5e1;
          --fdx-edge: #94a3b8;
          --fdx-label-bg: #1f2937;
          --fdx-input-fill: #0f2942;
          --fdx-input-stroke: #60a5fa;
          --fdx-decision-fill: #3b2410;
          --fdx-decision-stroke: #f59e0b;
          --fdx-process-fill: #2e2451;
          --fdx-process-stroke: #a78bfa;
          --fdx-outcome-fill: #0f2c1f;
          --fdx-outcome-stroke: #34d399;
          --fdx-assumed-fill: #422006;
          --fdx-assumed-text: #fde68a;
        }}
      }}
      svg {{ width: 100%; height: auto; background: var(--fdx-bg); border-radius: 20px; }}
      .node rect {{ fill: var(--fdx-panel); stroke-width: 2.2; }}
      .node.input rect {{ fill: var(--fdx-input-fill); stroke: var(--fdx-input-stroke); }}
      .node.decision rect {{ fill: var(--fdx-decision-fill); stroke: var(--fdx-decision-stroke); }}
      .node.process rect {{ fill: var(--fdx-process-fill); stroke: var(--fdx-process-stroke); }}
      .node.outcome rect {{ fill: var(--fdx-outcome-fill); stroke: var(--fdx-outcome-stroke); }}
      .node.outcome.decline rect {{ fill: #fff1f3; stroke: #b42318; }}
      .node.outcome.refer rect {{ fill: #fff7ed; stroke: #b54708; }}
      .node.outcome.approve rect {{ fill: #ecfdf3; stroke: #067647; }}
      .node.assumed rect {{ stroke-dasharray: 8 6; }}
      .node-title, .node-subtitle, .node-detail, .edge-label text, .assumed-badge text {{
        text-anchor: middle; font-family: "Segoe UI", Arial, sans-serif;
      }}
      .node-title {{ font-size: 16px; font-weight: 700; fill: var(--fdx-text); }}
      .node-subtitle {{ font-size: 13px; fill: var(--fdx-muted); }}
      .node-detail {{ font-size: 12px; fill: var(--fdx-muted); }}
      .edge path {{ fill: none; stroke: var(--fdx-edge); stroke-width: 2.2; marker-end: url(#fdx-arrow); }}
      .edge-label rect {{ fill: var(--fdx-label-bg); opacity: 0.96; }}
      .edge-label text {{ font-size: 12px; fill: var(--fdx-text); }}
      .assumed-badge rect {{ fill: var(--fdx-assumed-fill); stroke: none; }}
      .assumed-badge text {{ fill: var(--fdx-assumed-text); font-size: 11px; font-weight: 700; }}
      @media (prefers-color-scheme: dark) {{
        .node.outcome.decline rect {{ fill: #3c171f; stroke: #fda4af; }}
        .node.outcome.refer rect {{ fill: #3d2513; stroke: #fdba74; }}
        .node.outcome.approve rect {{ fill: #132d22; stroke: #6ee7b7; }}
      }}
    </style>
    {edge_markup}
    {node_markup}
  </svg>
</div>
""".strip()
