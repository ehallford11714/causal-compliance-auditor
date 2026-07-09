"""Ingest causal claim / report JSON."""

from __future__ import annotations

import json
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any


@dataclass
class CausalReport:
    """Normalized causal claim document."""

    title: str
    estimand: str | None
    treatment: str | None
    outcome: str | None
    assumptions: list[str]
    instruments: list[str]
    identification_strategy: str | None
    sensitivity: dict[str, Any]
    limitations: list[str]
    raw: dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> dict[str, Any]:
        return {
            "title": self.title,
            "estimand": self.estimand,
            "treatment": self.treatment,
            "outcome": self.outcome,
            "assumptions": self.assumptions,
            "instruments": self.instruments,
            "identification_strategy": self.identification_strategy,
            "sensitivity": self.sensitivity,
            "limitations": self.limitations,
        }


def _as_list(val: Any) -> list[str]:
    if val is None:
        return []
    if isinstance(val, str):
        return [val]
    if isinstance(val, list):
        return [str(x) for x in val]
    return [str(val)]


def normalize(data: dict[str, Any]) -> CausalReport:
    sens = data.get("sensitivity") or data.get("sensitivity_analysis") or {}
    if not isinstance(sens, dict):
        sens = {"summary": str(sens)}
    return CausalReport(
        title=str(data.get("title") or data.get("name") or "Untitled causal claim"),
        estimand=data.get("estimand") or data.get("target_estimand"),
        treatment=data.get("treatment") or data.get("T"),
        outcome=data.get("outcome") or data.get("Y"),
        assumptions=_as_list(data.get("assumptions")),
        instruments=_as_list(data.get("instruments") or data.get("Z")),
        identification_strategy=data.get("identification_strategy")
        or data.get("identification")
        or data.get("strategy"),
        sensitivity=sens,
        limitations=_as_list(data.get("limitations") or data.get("caveats")),
        raw=data,
    )


def load_report(path: str | Path) -> CausalReport:
    p = Path(path)
    data = json.loads(p.read_text(encoding="utf-8"))
    if not isinstance(data, dict):
        raise ValueError("Causal report JSON must be an object")
    return normalize(data)
