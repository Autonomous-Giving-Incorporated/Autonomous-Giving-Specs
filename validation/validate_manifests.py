"""Validate consumer conformance manifests."""

from __future__ import annotations

import json

from jsonschema import Draft202012Validator

from lib.constants import META_SCHEMAS
from lib.documents import DocumentIndex, load_json_schema
from lib.report import Report


def validate_manifests(index: DocumentIndex, report: Report) -> None:
    schema_path = index.root / META_SCHEMAS["manifest"]
    if not schema_path.exists():
        report.error("MANIFEST_SCHEMA_MISSING", "conformance-manifest schema missing", META_SCHEMAS["manifest"])
        return
    schema = load_json_schema(schema_path)
    validator = Draft202012Validator(schema)

    if not index.manifests:
        report.warning(
            "MANIFEST_NONE",
            "No conformance manifests found under conformance/examples/",
            "conformance/examples/",
        )
        return

    known_specs = set(index.specs)
    known_contracts = set(index.contracts)
    known_events = set(index.events)

    for mid, art in index.manifests.items():
        data = art.meta
        errors = sorted(validator.iter_errors(data), key=lambda e: list(e.path))
        for err in errors:
            loc = "/".join(str(p) for p in err.path) or "(root)"
            report.error(
                "MANIFEST_INVALID",
                f"{mid} {loc}: {err.message}",
                art.rel_path,
            )

        implements = data.get("implements") or {}
        for sid in implements.get("specs") or []:
            if sid not in known_specs:
                report.error(
                    "MANIFEST_UNKNOWN_SPEC",
                    f"{mid} implements unknown {sid}",
                    art.rel_path,
                )
        contracts = implements.get("contracts") or {}
        for key in ("produces", "consumes"):
            for cid in contracts.get(key) or []:
                if cid not in known_contracts:
                    report.error(
                        "MANIFEST_UNKNOWN_CONTRACT",
                        f"{mid} contracts.{key} unknown {cid}",
                        art.rel_path,
                    )
        events = implements.get("events") or {}
        for key in ("produces", "consumes"):
            for eid in events.get(key) or []:
                if eid not in known_events:
                    report.error(
                        "MANIFEST_UNKNOWN_EVENT",
                        f"{mid} events.{key} unknown {eid}",
                        art.rel_path,
                    )


def main() -> int:
    from lib.documents import load_repository

    report = Report()
    index = load_repository()
    report.manifests = len(index.manifests)
    validate_manifests(index, report)
    print(json.dumps(report.to_dict(), indent=2))
    return report.exit_code()


if __name__ == "__main__":
    raise SystemExit(main())
