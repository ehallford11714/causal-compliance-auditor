"""Checklist rules → pass/fail audit."""

from __future__ import annotations

from dataclasses import asdict, dataclass, field
from typing import Any

from causalaudit.ingest import CausalReport


@dataclass
class CheckItem:
    id: str
    description: str
    required: bool
    passed: bool
    detail: str

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass
class AuditResult:
    title: str
    passed: bool
    checks: list[CheckItem]
    score: float
    summary: str
    report: dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> dict[str, Any]:
        return {
            "title": self.title,
            "passed": self.passed,
            "score": self.score,
            "summary": self.summary,
            "checks": [c.to_dict() for c in self.checks],
            "report": self.report,
        }


def audit_report(report: CausalReport) -> AuditResult:
    checks: list[CheckItem] = []

    def add(cid: str, desc: str, required: bool, passed: bool, detail: str) -> None:
        checks.append(
            CheckItem(
                id=cid,
                description=desc,
                required=required,
                passed=passed,
                detail=detail,
            )
        )

    add(
        "estimand_stated",
        "Estimand clearly stated",
        True,
        bool(report.estimand and str(report.estimand).strip()),
        report.estimand or "missing",
    )
    add(
        "treatment_outcome",
        "Treatment and outcome named",
        True,
        bool(report.treatment) and bool(report.outcome),
        f"T={report.treatment!r} Y={report.outcome!r}",
    )
    add(
        "assumptions_listed",
        "Identifying assumptions listed",
        True,
        len(report.assumptions) >= 1,
        f"{len(report.assumptions)} assumption(s)",
    )
    add(
        "identification_strategy",
        "Identification strategy documented",
        True,
        bool(report.identification_strategy),
        report.identification_strategy or "missing",
    )

    strategy = (report.identification_strategy or "").lower()
    uses_iv = "iv" in strategy or "instrument" in strategy or bool(report.instruments)
    add(
        "instruments_if_iv",
        "Instruments declared when IV strategy used",
        True,
        (not uses_iv) or len(report.instruments) >= 1,
        f"instruments={report.instruments}" if uses_iv else "n/a (non-IV)",
    )

    sens_ok = bool(report.sensitivity) and (
        any(
            k in report.sensitivity
            for k in (
                "method",
                "result",
                "bounds",
                "rosenbaum",
                "e_value",
                "partial_r2",
                "summary",
            )
        )
        or len(report.sensitivity) > 0
    )
    add(
        "sensitivity_analysis",
        "Sensitivity analysis present",
        True,
        sens_ok,
        str(report.sensitivity)[:120] if report.sensitivity else "missing",
    )
    add(
        "limitations",
        "Limitations / caveats disclosed",
        False,
        len(report.limitations) >= 1,
        f"{len(report.limitations)} item(s)",
    )
    add(
        "exclusion_or_unconfoundedness",
        "Core assumption language (exclusion / unconfoundedness / SUTVA)",
        False,
        any(
            any(
                kw in a.lower()
                for kw in (
                    "exclusion",
                    "unconfound",
                    "ignorab",
                    "sutva",
                    "overlap",
                    "positivity",
                    "exogeneity",
                )
            )
            for a in report.assumptions
        ),
        "scanned assumptions for standard keywords",
    )

    required = [c for c in checks if c.required]
    passed = all(c.passed for c in required)
    score = sum(1 for c in checks if c.passed) / max(1, len(checks))
    summary = (
        "PASS — required compliance checks satisfied"
        if passed
        else "FAIL — one or more required checks failed"
    )
    return AuditResult(
        title=report.title,
        passed=passed,
        checks=checks,
        score=round(score, 3),
        summary=summary,
        report=report.to_dict(),
    )
