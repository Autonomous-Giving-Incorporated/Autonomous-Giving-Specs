"""Validate JSON Schema documents parse and use Draft 2020-12."""

from __future__ import annotations

import json
from pathlib import Path

from jsonschema import Draft202012Validator
from jsonschema.exceptions import SchemaError

from lib.documents import DocumentIndex, load_json_schema
from lib.report import Report


def validate_schemas(index: DocumentIndex, report: Report) -> None:
    payload_schemas = [
        p for rel, p in index.schema_files.items() if "/meta/" not in rel and rel.startswith("schemas/")
    ]
    # schema_files includes meta; filter by path parts
    payload_schemas = []
    for path in index.schema_by_filename.values():
        if path.parent.name == "meta":
            continue
        payload_schemas.append(path)

    seen_ids: dict[str, str] = {}
    for path in sorted(payload_schemas, key=lambda p: p.name):
        rel = path.relative_to(index.root).as_posix()
        try:
            schema = load_json_schema(path)
        except json.JSONDecodeError as exc:
            report.error("SCHEMA_JSON_INVALID", f"Invalid JSON: {exc}", rel)
            continue

        draft = schema.get("$schema", "")
        if "2020-12" not in str(draft):
            report.error(
                "SCHEMA_DRAFT",
                f"Schema must declare Draft 2020-12; got {draft!r}",
                rel,
            )

        schema_id = schema.get("$id")
        if not schema_id:
            report.error("SCHEMA_ID_MISSING", "Schema missing $id", rel)
        else:
            if schema_id in seen_ids:
                report.error(
                    "SCHEMA_ID_DUPLICATE",
                    f"$id {schema_id} already used by {seen_ids[schema_id]}",
                    rel,
                )
            else:
                seen_ids[schema_id] = rel

        try:
            Draft202012Validator.check_schema(schema)
        except SchemaError as exc:
            report.error("SCHEMA_INVALID", f"Schema is not valid Draft 2020-12: {exc.message}", rel)

    # Meta schemas themselves
    meta_dir = index.root / "schemas" / "meta"
    if meta_dir.exists():
        for path in sorted(meta_dir.glob("*.json")):
            rel = path.relative_to(index.root).as_posix()
            try:
                schema = load_json_schema(path)
                Draft202012Validator.check_schema(schema)
            except (json.JSONDecodeError, SchemaError) as exc:
                report.error("META_SCHEMA_INVALID", str(exc), rel)

    # Catalog entries must point at existing files
    for schema_id, entry in index.schema_catalog.items():
        file_name = entry.get("file", "")
        if file_name and file_name not in index.schema_by_filename:
            report.error(
                "SCHEMA_CATALOG_MISSING_FILE",
                f"{schema_id} points to missing {file_name}",
                "schemas/README.md",
            )


def main() -> int:
    from lib.documents import load_repository

    report = Report()
    index = load_repository()
    report.schemas = len(index.schema_by_filename)
    validate_schemas(index, report)
    print(json.dumps(report.to_dict(), indent=2))
    return report.exit_code()


if __name__ == "__main__":
    raise SystemExit(main())
