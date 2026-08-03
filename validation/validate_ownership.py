"""Validate contract ownership rules."""

from __future__ import annotations

import json

from lib.constants import SERVICE_OWNERS
from lib.documents import DocumentIndex
from lib.report import Report

# Contracts must be owned by an implementing service, not a meta-owner.
CONTRACT_OWNERS = frozenset({"Fund Intel", "Autonomous Giving", "Impact Relay"})


def validate_ownership(index: DocumentIndex, report: Report) -> None:
    for cid, art in index.contracts.items():
        owner = art.meta.get("owner")
        if not owner:
            report.error("CONTRACT_OWNER_MISSING", f"{cid} missing owner", art.rel_path)
            continue
        if not isinstance(owner, str) or not owner.strip():
            report.error("CONTRACT_OWNER_INVALID", f"{cid} owner must be a non-empty string", art.rel_path)
            continue
        # Exactly one owner: no commas / slashes / "and"
        if any(sep in owner for sep in (",", "/", "&")) or " and " in owner.lower():
            report.error(
                "CONTRACT_OWNER_MULTIPLE",
                f"{cid} must have exactly one owning service; got '{owner}'",
                art.rel_path,
            )
            continue
        if owner not in CONTRACT_OWNERS:
            report.error(
                "CONTRACT_OWNER_UNKNOWN",
                f"{cid} owner '{owner}' must be one of {sorted(CONTRACT_OWNERS)}",
                art.rel_path,
            )

    # Events: producer should be a known service owner
    for eid, art in index.events.items():
        producer = art.meta.get("producer") or art.meta.get("owner")
        if not producer:
            report.error("EVENT_PRODUCER_MISSING", f"{eid} missing producer", art.rel_path)
        elif producer not in SERVICE_OWNERS and producer not in CONTRACT_OWNERS:
            report.warning(
                "EVENT_PRODUCER_NONSTANDARD",
                f"{eid} producer '{producer}' is nonstandard",
                art.rel_path,
            )


def main() -> int:
    from lib.documents import load_repository

    report = Report()
    index = load_repository()
    validate_ownership(index, report)
    print(json.dumps(report.to_dict(), indent=2))
    return report.exit_code()


if __name__ == "__main__":
    raise SystemExit(main())
