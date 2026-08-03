#!/usr/bin/env python3
"""Run all platform specification validators and emit a machine-readable report.

Exit codes:
  0 — PASS (no errors; warnings allowed)
  1 — FAIL (one or more errors)
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

# Ensure validation/ is on path when executed as a script.
sys.path.insert(0, str(Path(__file__).resolve().parent))

from lib.documents import load_repository
from lib.report import Report
from validate_demo import validate_demo
from validate_examples import validate_examples
from validate_lifecycle import validate_lifecycle
from validate_manifests import validate_manifests
from validate_metadata import validate_metadata
from validate_ownership import validate_ownership
from validate_references import validate_references
from validate_schemas import validate_schemas
from validate_terminology import validate_terminology


def run_all(root: Path | None = None) -> Report:
    index = load_repository(root)
    report = Report()
    report.specifications = len(index.specs)
    report.contracts = len(index.contracts)
    report.events = len(index.events)
    report.adrs = len(index.adrs)
    report.schemas = len(
        [name for name, path in index.schema_by_filename.items() if path.parent.name != "meta"]
    )
    report.manifests = len(index.manifests)

    validate_metadata(index, report)
    validate_references(index, report)
    validate_schemas(index, report)
    validate_lifecycle(index, report)
    validate_ownership(index, report)
    validate_examples(index, report)
    validate_manifests(index, report)
    validate_terminology(index, report)
    validate_demo(index, report)

    return report


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Validate Autonomous Giving platform specifications")
    parser.add_argument(
        "--root",
        type=Path,
        default=None,
        help="Repository root (default: parent of validation/)",
    )
    parser.add_argument(
        "--output",
        "-o",
        type=Path,
        default=None,
        help="Write JSON report to this path",
    )
    parser.add_argument(
        "--quiet",
        action="store_true",
        help="Only print result line",
    )
    args = parser.parse_args(argv)

    report = run_all(args.root)
    payload = report.to_dict()

    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")

    if args.quiet:
        print(payload["result"])
    else:
        print(json.dumps(payload, indent=2))

    return report.exit_code()


if __name__ == "__main__":
    raise SystemExit(main())
