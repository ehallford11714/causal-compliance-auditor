"""CLI: ``causalaudit audit report.json``."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

from causalaudit.certificate import render_certificate_md, write_certificate
from causalaudit.checklist import audit_report
from causalaudit.ingest import load_report


def build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(
        prog="causalaudit",
        description="Causal Compliance Auditor — checklist + certificate for causal claims",
    )
    sub = p.add_subparsers(dest="cmd", required=True)
    audit = sub.add_parser("audit", help="Audit a causal report JSON")
    audit.add_argument("report", type=str, help="Path to report.json")
    audit.add_argument(
        "--runs",
        type=str,
        default="runs",
        help="Directory for audit artifacts (default: runs/)",
    )
    audit.add_argument(
        "--no-write",
        action="store_true",
        help="Print only; do not write under runs/",
    )
    return p


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    if args.cmd == "audit":
        report = load_report(args.report)
        result = audit_report(report)
        print(json.dumps(result.to_dict(), indent=2))
        print()
        print(render_certificate_md(result))
        if not args.no_write:
            out = write_certificate(result, runs_dir=args.runs)
            print(f"\nArtifacts: {out.resolve()}", file=sys.stderr)
        return 0 if result.passed else 1
    return 2


if __name__ == "__main__":
    raise SystemExit(main())
