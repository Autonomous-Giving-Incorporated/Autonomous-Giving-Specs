#!/usr/bin/env python3
"""Generate machine-readable indexes from document metadata."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from lib.constants import CANONICAL_LIFECYCLE, PLATFORM_SPEC_VERSION
from lib.documents import load_repository


def generate(root: Path | None = None) -> dict[str, Path]:
    index = load_repository(root)
    out_dir = index.root / "generated"
    out_dir.mkdir(parents=True, exist_ok=True)

    catalog = {
        "platformSpecVersion": PLATFORM_SPEC_VERSION,
        "specifications": [
            {
                "id": a.artifact_id,
                "title": a.meta.get("title"),
                "version": a.meta.get("version"),
                "status": a.meta.get("status"),
                "owner": a.meta.get("owner"),
                "path": a.rel_path,
            }
            for a in index.specs.values()
        ],
        "adrs": [
            {
                "id": a.artifact_id,
                "title": a.meta.get("title"),
                "version": a.meta.get("version"),
                "status": a.meta.get("status"),
                "owner": a.meta.get("owner"),
                "path": a.rel_path,
            }
            for a in index.adrs.values()
        ],
        "contracts": [
            {
                "id": a.artifact_id,
                "title": a.meta.get("title"),
                "version": a.meta.get("version"),
                "status": a.meta.get("status"),
                "owner": a.meta.get("owner"),
                "schema": a.meta.get("schema"),
                "lifecycle_stage": a.meta.get("lifecycle_stage"),
                "path": a.rel_path,
            }
            for a in index.contracts.values()
        ],
        "events": [
            {
                "id": a.artifact_id,
                "title": a.meta.get("title"),
                "version": a.meta.get("version"),
                "status": a.meta.get("status"),
                "owner": a.meta.get("owner"),
                "lifecycle_stage": a.meta.get("lifecycle_stage"),
                "producer": a.meta.get("producer"),
                "schema": a.meta.get("schema"),
                "contract": a.meta.get("contract"),
                "path": a.rel_path,
            }
            for a in index.events.values()
        ],
        "schemas": [
            {
                "id": sid,
                **entry,
            }
            for sid, entry in index.schema_catalog.items()
        ],
        "glossary": [
            {"id": tid, "term": term} for tid, term in index.glossary_terms.items()
        ],
    }

    # Traceability: lifecycle stage → event/contract/owner
    by_stage: dict[str, dict] = {s: {"stage": s, "events": [], "contracts": []} for s in CANONICAL_LIFECYCLE}
    by_stage["Notification"] = {"stage": "Notification", "events": [], "contracts": []}
    for a in index.events.values():
        stage = a.meta.get("lifecycle_stage") or "Unknown"
        by_stage.setdefault(stage, {"stage": stage, "events": [], "contracts": []})
        by_stage[stage]["events"].append(a.artifact_id)
        if a.meta.get("contract"):
            by_stage[stage]["contracts"].append(a.meta["contract"])
    for a in index.contracts.values():
        stage = a.meta.get("lifecycle_stage")
        if stage:
            by_stage.setdefault(stage, {"stage": stage, "events": [], "contracts": []})
            if a.artifact_id not in by_stage[stage]["contracts"]:
                by_stage[stage]["contracts"].append(a.artifact_id)

    traceability = {
        "platformSpecVersion": PLATFORM_SPEC_VERSION,
        "stages": list(by_stage.values()),
    }

    lifecycle = {
        "platformSpecVersion": PLATFORM_SPEC_VERSION,
        "sequence": CANONICAL_LIFECYCLE,
        "projections": ["Notification", "TimelineEvent"],
    }

    ownership: dict[str, dict] = {}
    for mapping, key in (
        (index.contracts, "contracts"),
        (index.events, "events"),
        (index.specs, "specs"),
    ):
        for a in mapping.values():
            owner = a.meta.get("owner") or "Unknown"
            ownership.setdefault(owner, {"owner": owner, "contracts": [], "events": [], "specs": []})
            ownership[owner][key].append(a.artifact_id)

    ownership_doc = {
        "platformSpecVersion": PLATFORM_SPEC_VERSION,
        "owners": list(ownership.values()),
    }

    # Dependency graph: specs related_specs + events→contracts
    nodes = []
    edges = []
    for a in index.specs.values():
        nodes.append({"id": a.artifact_id, "type": "spec"})
        for dep in a.meta.get("related_specs") or []:
            edges.append({"from": a.artifact_id, "to": dep, "type": "related_spec"})
        for dep in a.meta.get("related_adrs") or []:
            edges.append({"from": a.artifact_id, "to": dep, "type": "related_adr"})
        for dep in a.meta.get("related_contracts") or []:
            edges.append({"from": a.artifact_id, "to": dep, "type": "related_contract"})
    for a in index.events.values():
        nodes.append({"id": a.artifact_id, "type": "event"})
        if a.meta.get("contract"):
            edges.append({"from": a.artifact_id, "to": a.meta["contract"], "type": "payload_contract"})
    for a in index.contracts.values():
        nodes.append({"id": a.artifact_id, "type": "contract"})
    for a in index.adrs.values():
        nodes.append({"id": a.artifact_id, "type": "adr"})

    dependency_graph = {
        "platformSpecVersion": PLATFORM_SPEC_VERSION,
        "nodes": nodes,
        "edges": edges,
    }

    # Conformance matrix from example manifests
    matrix_services = []
    for mid, art in index.manifests.items():
        impl = art.meta.get("implements") or {}
        matrix_services.append(
            {
                "service": art.meta.get("service"),
                "platform_spec": art.meta.get("platform_spec"),
                "specs": impl.get("specs") or [],
                "contracts": impl.get("contracts") or {},
                "events": impl.get("events") or {},
                "path": art.rel_path,
            }
        )
    conformance_matrix = {
        "platformSpecVersion": PLATFORM_SPEC_VERSION,
        "services": matrix_services,
    }

    outputs = {
        "catalog.json": catalog,
        "traceability.json": traceability,
        "lifecycle.json": lifecycle,
        "ownership.json": ownership_doc,
        "dependency-graph.json": dependency_graph,
        "conformance-matrix.json": conformance_matrix,
    }
    written: dict[str, Path] = {}
    for name, payload in outputs.items():
        path = out_dir / name
        path.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")
        written[name] = path
    return written


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", type=Path, default=None)
    args = parser.parse_args()
    written = generate(args.root)
    for name, path in written.items():
        print(f"wrote {path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
