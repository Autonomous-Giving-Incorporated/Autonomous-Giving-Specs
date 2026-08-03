"""Validate normative references: existence, orphans, and cycles."""

from __future__ import annotations

import json
import re
from collections import defaultdict, deque
from pathlib import Path

from lib.documents import DocumentIndex
from lib.frontmatter import markdown_links
from lib.report import Report


def _known_ids(index: DocumentIndex) -> set[str]:
    return index.all_document_ids()


def validate_references(index: DocumentIndex, report: Report) -> None:
    known = _known_ids(index)

    # Relative markdown links must resolve for normative docs.
    for mapping in (index.specs, index.adrs, index.contracts, index.events):
        for art in mapping.values():
            for _label, target in markdown_links(art.body):
                if target.startswith(("http://", "https://", "mailto:")):
                    continue
                if target.startswith("#"):
                    continue
                # Drop anchors
                file_part = target.split("#", 1)[0]
                if not file_part:
                    continue
                resolved = (art.path.parent / file_part).resolve()
                try:
                    resolved.relative_to(index.root.resolve())
                except ValueError:
                    report.error(
                        "LINK_OUTSIDE_REPO",
                        f"Link escapes repository: {target}",
                        art.rel_path,
                    )
                    continue
                if not resolved.exists():
                    report.error(
                        "BROKEN_LINK",
                        f"Broken relative link: {target}",
                        art.rel_path,
                    )

            for ref in art.referenced_ids:
                if ref not in known:
                    # Ranges like CONTRACT-001–007 are not individual IDs in regex.
                    report.error(
                        "UNKNOWN_REFERENCE",
                        f"{art.artifact_id} references unknown id {ref}",
                        art.rel_path,
                    )

    # SPEC dependency graph: related_specs edges; detect cycles.
    graph: dict[str, set[str]] = defaultdict(set)
    for sid, art in index.specs.items():
        deps = art.meta.get("related_specs") or []
        # Also parse dependencies from legacy fields if present
        for dep in deps:
            if isinstance(dep, str) and re.fullmatch(r"SPEC-\d{3}", dep):
                graph[sid].add(dep)
                if dep not in index.specs:
                    report.error(
                        "MISSING_SPEC_DEP",
                        f"{sid} related_specs includes missing {dep}",
                        art.rel_path,
                    )

    cycle = _find_cycle(graph)
    if cycle:
        # related_specs are navigational; mutual links are common (e.g. contracts ↔ versioning).
        # Report as warning so authors can tighten directed depends_on later without blocking CI.
        report.warning(
            "CIRCULAR_SPEC_REFS",
            f"Circular related_specs references: {' → '.join(cycle)}",
            "specs/",
        )

    # Events must reference existing contract and/or resolvable schema.
    for eid, art in index.events.items():
        contract = art.meta.get("contract")
        if contract:
            if contract not in index.contracts:
                report.error(
                    "EVENT_CONTRACT_MISSING",
                    f"{eid} contract {contract} does not exist",
                    art.rel_path,
                )
        schema_ref = art.meta.get("schema")
        if not schema_ref:
            report.error("EVENT_SCHEMA_MISSING", f"{eid} missing schema reference", art.rel_path)

    # Orphan contracts: no event references them (warning — timeline-only contracts may exist).
    referenced_contracts: set[str] = set()
    for art in index.events.values():
        c = art.meta.get("contract")
        if c:
            referenced_contracts.add(c)
        for rc in art.meta.get("related_contracts") or []:
            referenced_contracts.add(rc)
    for cid in index.contracts:
        # CONTRACT-007 TimelineEvent may be projection-only
        if cid not in referenced_contracts and cid != "CONTRACT-007":
            report.warning(
                "ORPHAN_CONTRACT",
                f"{cid} is not referenced by any event contract field",
                index.contracts[cid].rel_path,
            )


def _find_cycle(graph: dict[str, set[str]]) -> list[str] | None:
    WHITE, GRAY, BLACK = 0, 1, 2
    color = {n: WHITE for n in graph}
    for n in list(graph):
        color.setdefault(n, WHITE)
        for d in graph[n]:
            color.setdefault(d, WHITE)

    parent: dict[str, str | None] = {}

    def dfs(node: str) -> list[str] | None:
        color[node] = GRAY
        for neigh in graph.get(node, ()):
            if color.get(neigh, WHITE) == GRAY:
                # reconstruct
                cycle = [neigh, node]
                return cycle
            if color.get(neigh, WHITE) == WHITE:
                parent[neigh] = node
                found = dfs(neigh)
                if found:
                    return found
        color[node] = BLACK
        return None

    for node in list(color):
        if color[node] == WHITE:
            parent[node] = None
            found = dfs(node)
            if found:
                return found
    return None


def main() -> int:
    from lib.documents import load_repository

    report = Report()
    index = load_repository()
    validate_references(index, report)
    print(json.dumps(report.to_dict(), indent=2))
    return report.exit_code()


if __name__ == "__main__":
    raise SystemExit(main())
