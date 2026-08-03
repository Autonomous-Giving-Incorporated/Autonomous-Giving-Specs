"""Validate lifecycle stage canonicity and event stage consistency."""

from __future__ import annotations

import json
import re

from lib.constants import CANONICAL_LIFECYCLE, EVENT_STAGES
from lib.documents import DocumentIndex
from lib.report import Report


def validate_lifecycle(index: DocumentIndex, report: Report) -> None:
    # SPEC-005 must declare the full sequence.
    lifecycle_spec = index.specs.get("SPEC-005")
    if not lifecycle_spec:
        report.error("LIFECYCLE_SPEC_MISSING", "SPEC-005 is required", "specs/")
    else:
        body = lifecycle_spec.body
        for stage in CANONICAL_LIFECYCLE:
            if stage not in body and stage not in json.dumps(lifecycle_spec.meta):
                report.error(
                    "LIFECYCLE_STAGE_MISSING_IN_SPEC",
                    f"SPEC-005 does not mention stage {stage}",
                    lifecycle_spec.rel_path,
                )
        # Detect alternative arrows that invent non-canonical orderings in requirements.
        # Only flag explicit alternative chains if present with non-canonical tokens.
        alt = re.search(
            r"(?:alternative|instead of)\s+lifecycle",
            body,
            re.IGNORECASE,
        )
        if alt:
            report.warning(
                "LIFECYCLE_ALTERNATIVE_LANGUAGE",
                "SPEC-005 mentions alternative lifecycle language; confirm canonicity",
                lifecycle_spec.rel_path,
            )

    for eid, art in index.events.items():
        stage = art.meta.get("lifecycle_stage")
        if not stage:
            report.error(
                "EVENT_STAGE_MISSING",
                f"{eid} missing lifecycle_stage",
                art.rel_path,
            )
            continue
        if stage not in EVENT_STAGES:
            report.error(
                "EVENT_STAGE_NONCANONICAL",
                f"{eid} lifecycle_stage '{stage}' is not canonical "
                f"(allowed: {', '.join(sorted(EVENT_STAGES))})",
                art.rel_path,
            )

    for cid, art in index.contracts.items():
        stage = art.meta.get("lifecycle_stage")
        if stage and stage not in EVENT_STAGES:
            report.error(
                "CONTRACT_STAGE_NONCANONICAL",
                f"{cid} lifecycle_stage '{stage}' is not canonical",
                art.rel_path,
            )


def main() -> int:
    from lib.documents import load_repository

    report = Report()
    index = load_repository()
    validate_lifecycle(index, report)
    print(json.dumps(report.to_dict(), indent=2))
    return report.exit_code()


if __name__ == "__main__":
    raise SystemExit(main())
