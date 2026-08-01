from __future__ import annotations

import yaml

from horizon_dsl.semantic.models import FraudDecisionSpec


def render_spec_yaml(spec: FraudDecisionSpec) -> str:
    payload = spec.model_dump(mode="python", exclude_none=True)
    return yaml.safe_dump(payload, sort_keys=False, allow_unicode=False)
