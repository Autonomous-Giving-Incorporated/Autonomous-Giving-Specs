"""Validate fenced JSON examples against linked schemas."""

from __future__ import annotations

import json
from typing import Any

from jsonschema import Draft202012Validator, FormatChecker

from lib.documents import DocumentIndex, load_json_schema, resolve_schema_path
from lib.report import Report


def _validate_instance(schema: dict[str, Any], instance: Any, report: Report, path: str, label: str) -> None:
    validator = Draft202012Validator(schema, format_checker=FormatChecker())
    errors = sorted(validator.iter_errors(instance), key=lambda e: list(e.absolute_path))
    for err in errors:
        loc = "/".join(str(p) for p in err.absolute_path) or "(root)"
        report.error(
            "EXAMPLE_SCHEMA_FAIL",
            f"{label} invalid at {loc}: {err.message}",
            path,
        )


def validate_examples(index: DocumentIndex, report: Report) -> None:
    # Contracts: every fenced JSON block validates against the contract schema.
    for cid, art in index.contracts.items():
        schema_path = resolve_schema_path(index, str(art.meta.get("schema", "")))
        if not schema_path:
            report.error(
                "EXAMPLE_SCHEMA_UNRESOLVED",
                f"{cid} cannot resolve schema for example validation",
                art.rel_path,
            )
            continue
        try:
            schema = load_json_schema(schema_path)
        except json.JSONDecodeError as exc:
            report.error("EXAMPLE_SCHEMA_JSON", str(exc), art.rel_path)
            continue

        blocks = art.json_examples
        if not blocks:
            report.error(
                "EXAMPLE_MISSING",
                f"{cid} has no fenced ```json example",
                art.rel_path,
            )
            continue
        for i, block in enumerate(blocks):
            try:
                instance = json.loads(block)
            except json.JSONDecodeError as exc:
                report.error(
                    "EXAMPLE_JSON_INVALID",
                    f"{cid} example[{i}] is not valid JSON: {exc}",
                    art.rel_path,
                )
                continue
            _validate_instance(schema, instance, report, art.rel_path, f"{cid} example[{i}]")

    # Events: fenced JSON examples if present; payload validated when envelope-shaped or bare payload.
    for eid, art in index.events.items():
        schema_path = resolve_schema_path(index, str(art.meta.get("schema", "")))
        if not schema_path:
            # May reference CONTRACT-NNN via schema field
            contract = art.meta.get("contract")
            if contract:
                schema_path = resolve_schema_path(index, str(contract))
        if not schema_path:
            report.error(
                "EVENT_EXAMPLE_SCHEMA_UNRESOLVED",
                f"{eid} cannot resolve payload schema",
                art.rel_path,
            )
            continue
        try:
            schema = load_json_schema(schema_path)
        except json.JSONDecodeError as exc:
            report.error("EVENT_EXAMPLE_SCHEMA_JSON", str(exc), art.rel_path)
            continue

        blocks = art.json_examples
        if not blocks:
            report.error(
                "EVENT_EXAMPLE_MISSING",
                f"{eid} has no fenced ```json example (required for executable canon)",
                art.rel_path,
            )
            continue
        for i, block in enumerate(blocks):
            try:
                instance = json.loads(block)
            except json.JSONDecodeError as exc:
                report.error(
                    "EVENT_EXAMPLE_JSON_INVALID",
                    f"{eid} example[{i}] is not valid JSON: {exc}",
                    art.rel_path,
                )
                continue
            payload = instance
            if isinstance(instance, dict) and "payload" in instance and "eventType" in instance:
                payload = instance["payload"]
            _validate_instance(schema, payload, report, art.rel_path, f"{eid} example[{i}] payload")


def main() -> int:
    from lib.documents import load_repository

    report = Report()
    index = load_repository()
    validate_examples(index, report)
    print(json.dumps(report.to_dict(), indent=2))
    return report.exit_code()


if __name__ == "__main__":
    raise SystemExit(main())
