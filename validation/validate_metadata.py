"""Validate required frontmatter metadata for normative artifacts."""

from __future__ import annotations

import json
import re
from pathlib import Path

from jsonschema import Draft202012Validator

from lib.constants import META_SCHEMAS, SERVICE_OWNERS
from lib.documents import DocumentIndex, load_json_schema
from lib.report import Report


def _validate_against_meta(index: DocumentIndex, report: Report, kind: str, artifacts: dict) -> None:
    schema_rel = META_SCHEMAS[kind]
    schema_path = index.root / schema_rel
    if not schema_path.exists():
        report.error("META_SCHEMA_MISSING", f"Missing meta schema {schema_rel}", schema_rel)
        return
    schema = load_json_schema(schema_path)
    validator = Draft202012Validator(schema)

    for artifact_id, art in artifacts.items():
        if not art.meta:
            report.error(
                "METADATA_MISSING",
                f"{artifact_id} has no YAML frontmatter",
                art.rel_path,
            )
            continue
        errors = sorted(validator.iter_errors(art.meta), key=lambda e: list(e.path))
        for err in errors:
            loc = "/".join(str(p) for p in err.path) or "(root)"
            report.error(
                "METADATA_INVALID",
                f"{artifact_id} frontmatter {loc}: {err.message}",
                art.rel_path,
            )

        declared = art.meta.get("id")
        if declared and declared != artifact_id:
            report.error(
                "METADATA_ID_MISMATCH",
                f"Index key {artifact_id} != frontmatter id {declared}",
                art.rel_path,
            )

        # ID must match filename prefix.
        if not art.path.name.startswith(f"{artifact_id}-") and art.path.name != f"{artifact_id}.md":
            report.error(
                "ID_PATH_MISMATCH",
                f"{artifact_id} does not correspond to path {art.rel_path}",
                art.rel_path,
            )

        owner = art.meta.get("owner")
        if owner and owner not in SERVICE_OWNERS:
            report.warning(
                "OWNER_NONSTANDARD",
                f"{artifact_id} owner '{owner}' is outside the known owner set",
                art.rel_path,
            )

        for field in ("version", "status"):
            if field not in art.meta or art.meta.get(field) in (None, ""):
                report.error(
                    "METADATA_REQUIRED",
                    f"{artifact_id} missing {field}",
                    art.rel_path,
                )


def validate_metadata(index: DocumentIndex, report: Report) -> None:
    _validate_against_meta(index, report, "spec", index.specs)
    _validate_against_meta(index, report, "adr", index.adrs)
    _validate_against_meta(index, report, "contract", index.contracts)
    _validate_against_meta(index, report, "event", index.events)

    # Duplicate identifier detection across classes (should not collide by design).
    seen: dict[str, str] = {}
    for mapping in (index.specs, index.adrs, index.contracts, index.events):
        for aid, art in mapping.items():
            if aid in seen:
                report.error(
                    "DUPLICATE_ID",
                    f"Duplicate identifier {aid} at {art.rel_path} and {seen[aid]}",
                    art.rel_path,
                )
            else:
                seen[aid] = art.rel_path


def main() -> int:
    from lib.documents import load_repository

    report = Report()
    index = load_repository()
    report.specifications = len(index.specs)
    report.contracts = len(index.contracts)
    report.events = len(index.events)
    report.schemas = len([p for p in index.schema_by_filename if not str(p).startswith("meta")])
    report.adrs = len(index.adrs)
    validate_metadata(index, report)
    print(json.dumps(report.to_dict(), indent=2))
    return report.exit_code()


if __name__ == "__main__":
    raise SystemExit(main())
