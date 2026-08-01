from __future__ import annotations

from typing import Annotated, Literal, Union

from pydantic import BaseModel, ConfigDict, Field


Decision = Literal["APPROVE", "DECLINE", "REFER"]
FlowMode = Literal["first_match"]
ListType = Literal["blacklist", "watchlist"]
OutputType = Literal["integer"]


class DecisionOutcome(BaseModel):
    decision: Decision
    reason_code: str
    explanation: str
    stop: bool = True


class DecisionStrategy(BaseModel):
    id: str
    name: str
    description: str


class InputEvent(BaseModel):
    event_type: str
    event_time_field: str


class EntityDefinition(BaseModel):
    key_field: str


class ListResource(BaseModel):
    id: str
    type: ListType = "blacklist"
    lookup_key: str
    version: str
    on_lookup_error: Decision


class ModelOutput(BaseModel):
    field: str
    type: OutputType = "integer"
    minimum: int
    maximum: int


class ModelResource(BaseModel):
    id: str
    name: str
    version: str
    output: ModelOutput
    on_inference_error: Decision


class ResourceCatalog(BaseModel):
    lists: list[ListResource] = Field(default_factory=list)
    models: list[ModelResource] = Field(default_factory=list)


class ScoreRange(BaseModel):
    min: int
    max: int
    include_min: bool = True
    include_max: bool = True


class ListMatchStep(BaseModel):
    model_config = ConfigDict(extra="forbid")

    id: str
    type: Literal["list_match"]
    list_ref: str
    input_field: str
    when_matched: DecisionOutcome


class ModelInferenceStep(BaseModel):
    model_config = ConfigDict(extra="forbid")

    id: str
    type: Literal["model_inference"]
    model_ref: str
    output_field: str


class ScoreBandStep(BaseModel):
    model_config = ConfigDict(extra="forbid")

    id: str
    type: Literal["score_band"]
    score_field: str
    range: ScoreRange
    decision: Decision
    reason_code: str
    explanation: str
    stop: bool = True


class DefaultStep(BaseModel):
    model_config = ConfigDict(extra="forbid")

    id: str
    type: Literal["default"]
    decision: Decision
    reason_code: str
    explanation: str
    stop: bool = True


DecisionStep = Annotated[
    Union[ListMatchStep, ModelInferenceStep, ScoreBandStep, DefaultStep],
    Field(discriminator="type"),
]


class DecisionFlow(BaseModel):
    mode: FlowMode = "first_match"
    steps: list[DecisionStep]


class FraudDecisionSpec(BaseModel):
    spec_version: str
    decision_strategy: DecisionStrategy
    input: InputEvent
    entities: dict[str, EntityDefinition]
    resources: ResourceCatalog
    decision_flow: DecisionFlow
    outputs: list[str]
