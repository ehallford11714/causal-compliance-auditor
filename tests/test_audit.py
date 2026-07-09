from __future__ import annotations

import json
from pathlib import Path

from causalaudit.certificate import render_certificate_md, write_certificate
from causalaudit.checklist import audit_report
from causalaudit.cli import main as cli_main
from causalaudit.ingest import load_report, normalize


def test_good_report_passes():
    root = Path(__file__).resolve().parents[1]
    report = load_report(root / "examples" / "good_report.json")
    result = audit_report(report)
    assert result.passed
    assert result.score >= 0.7
    assert "PASS" in result.summary


def test_bad_report_fails():
    root = Path(__file__).resolve().parents[1]
    report = load_report(root / "examples" / "bad_report.json")
    result = audit_report(report)
    assert not result.passed
    failed_req = [c for c in result.checks if c.required and not c.passed]
    assert len(failed_req) >= 2


def test_certificate_written(tmp_path: Path):
    report = normalize(
        {
            "title": "Unit test claim",
            "estimand": "ATE",
            "treatment": "T",
            "outcome": "Y",
            "identification_strategy": "backdoor",
            "assumptions": ["unconfoundedness", "positivity"],
            "sensitivity": {"method": "e_value", "result": "1.8"},
            "limitations": ["observational"],
        }
    )
    result = audit_report(report)
    assert result.passed
    out = write_certificate(result, runs_dir=tmp_path)
    assert (out / "audit.json").is_file()
    assert (out / "certificate.md").is_file()
    md = (out / "certificate.md").read_text(encoding="utf-8")
    assert "Causal Compliance Certificate" in md
    assert "PASS" in md


def test_cli_audit(tmp_path: Path):
    root = Path(__file__).resolve().parents[1]
    code = cli_main(
        [
            "audit",
            str(root / "examples" / "good_report.json"),
            "--runs",
            str(tmp_path),
        ]
    )
    assert code == 0
    runs = list(tmp_path.iterdir())
    assert len(runs) == 1


def test_cli_bad_exit_code():
    root = Path(__file__).resolve().parents[1]
    code = cli_main(
        [
            "audit",
            str(root / "examples" / "bad_report.json"),
            "--no-write",
        ]
    )
    assert code == 1


def test_render_md_contains_checklist():
    report = normalize(
        {
            "title": "X",
            "estimand": "ATE",
            "treatment": "a",
            "outcome": "b",
            "identification_strategy": "IV",
            "instruments": ["z"],
            "assumptions": ["exclusion"],
            "sensitivity": {"summary": "ok"},
        }
    )
    md = render_certificate_md(audit_report(report))
    assert "Checklist" in md
    assert "estimand_stated" in md
