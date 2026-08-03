#!/usr/bin/env python3
"""One-shot helper: inject YAML frontmatter into normative markdown artifacts.

Safe to re-run: skips files that already have frontmatter.
"""

from __future__ import annotations

import re
import sys
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[1]

# SPEC metadata derived from existing tables / ownership.
SPEC_META = {
    "SPEC-001": {
        "title": "Platform Mission",
        "version": "1.0.0",
        "status": "accepted",
        "authority": "normative",
        "owner": "Platform Architecture",
        "related_specs": [],
        "related_adrs": ["ADR-001", "ADR-002"],
        "related_contracts": [],
    },
    "SPEC-002": {
        "title": "Platform Principles",
        "version": "1.0.0",
        "status": "accepted",
        "authority": "normative",
        "owner": "Platform Architecture",
        "related_specs": ["SPEC-001"],
        "related_adrs": ["ADR-002", "ADR-006", "ADR-007"],
        "related_contracts": [
            "CONTRACT-003",
            "CONTRACT-004",
            "CONTRACT-005",
            "CONTRACT-006",
            "CONTRACT-007",
        ],
    },
    "SPEC-003": {
        "title": "Signals Stack",
        "version": "1.0.0",
        "status": "proposed",
        "authority": "normative",
        "owner": "Fund Intel",
        "related_specs": ["SPEC-004", "SPEC-005"],
        "related_adrs": ["ADR-003"],
        "related_contracts": ["CONTRACT-001", "CONTRACT-002"],
    },
    "SPEC-004": {
        "title": "Domain Model",
        "version": "1.0.0",
        "status": "accepted",
        "authority": "normative",
        "owner": "Platform Architecture",
        "related_specs": [],
        "related_adrs": ["ADR-002"],
        "related_contracts": [
            "CONTRACT-001",
            "CONTRACT-002",
            "CONTRACT-003",
            "CONTRACT-004",
            "CONTRACT-005",
            "CONTRACT-006",
            "CONTRACT-007",
        ],
    },
    "SPEC-005": {
        "title": "Lifecycle",
        "version": "1.0.0",
        "status": "accepted",
        "authority": "normative",
        "owner": "Platform Architecture",
        "related_specs": ["SPEC-004"],
        "related_adrs": ["ADR-005", "ADR-006", "ADR-007"],
        "related_contracts": [
            "CONTRACT-001",
            "CONTRACT-002",
            "CONTRACT-003",
            "CONTRACT-004",
            "CONTRACT-005",
            "CONTRACT-006",
            "CONTRACT-007",
        ],
    },
    "SPEC-006": {
        "title": "Capability Boundaries",
        "version": "1.0.0",
        "status": "proposed",
        "authority": "normative",
        "owner": "Platform Architecture",
        "related_specs": ["SPEC-002", "SPEC-005"],
        "related_adrs": ["ADR-010"],
        "related_contracts": [
            "CONTRACT-001",
            "CONTRACT-002",
            "CONTRACT-003",
            "CONTRACT-004",
            "CONTRACT-005",
            "CONTRACT-006",
            "CONTRACT-007",
        ],
    },
    "SPEC-007": {
        "title": "Contracts",
        "version": "1.0.0",
        "status": "accepted",
        "authority": "normative",
        "owner": "Platform Architecture",
        "related_specs": ["SPEC-004", "SPEC-012"],
        "related_adrs": ["ADR-005", "ADR-007"],
        "related_contracts": [
            "CONTRACT-001",
            "CONTRACT-002",
            "CONTRACT-003",
            "CONTRACT-004",
            "CONTRACT-005",
            "CONTRACT-006",
            "CONTRACT-007",
        ],
    },
    "SPEC-008": {
        "title": "Events",
        "version": "1.0.0",
        "status": "accepted",
        "authority": "normative",
        "owner": "Platform Architecture",
        "related_specs": ["SPEC-005", "SPEC-007"],
        "related_adrs": ["ADR-003", "ADR-007"],
        "related_contracts": [
            "CONTRACT-001",
            "CONTRACT-002",
            "CONTRACT-003",
            "CONTRACT-004",
            "CONTRACT-005",
            "CONTRACT-006",
            "CONTRACT-007",
        ],
    },
    "SPEC-009": {
        "title": "Design System",
        "version": "1.0.0",
        "status": "proposed",
        "authority": "normative",
        "owner": "Platform Product",
        "related_specs": ["SPEC-004", "SPEC-011"],
        "related_adrs": ["ADR-009"],
        "related_contracts": ["CONTRACT-007"],
    },
    "SPEC-010": {
        "title": "Documentation Standard",
        "version": "1.0.0",
        "status": "accepted",
        "authority": "normative",
        "owner": "Platform Architecture",
        "related_specs": ["SPEC-004", "SPEC-012"],
        "related_adrs": ["ADR-008"],
        "related_contracts": [],
    },
    "SPEC-011": {
        "title": "Demo Specification",
        "version": "1.0.0",
        "status": "proposed",
        "authority": "normative",
        "owner": "Platform Product",
        "related_specs": ["SPEC-005", "SPEC-007", "SPEC-009"],
        "related_adrs": ["ADR-009"],
        "related_contracts": [
            "CONTRACT-001",
            "CONTRACT-002",
            "CONTRACT-003",
            "CONTRACT-004",
            "CONTRACT-005",
            "CONTRACT-006",
            "CONTRACT-007",
        ],
    },
    "SPEC-012": {
        "title": "Versioning",
        "version": "1.0.0",
        "status": "accepted",
        "authority": "normative",
        "owner": "Platform Architecture",
        "related_specs": ["SPEC-007"],
        "related_adrs": ["ADR-001"],
        "related_contracts": [
            "CONTRACT-001",
            "CONTRACT-002",
            "CONTRACT-003",
            "CONTRACT-004",
            "CONTRACT-005",
            "CONTRACT-006",
            "CONTRACT-007",
        ],
    },
    "SPEC-013": {
        "title": "Repository Conformance",
        "version": "1.0.0",
        "status": "accepted",
        "authority": "normative",
        "owner": "Platform Architecture",
        "related_specs": ["SPEC-001", "SPEC-007", "SPEC-012"],
        "related_adrs": ["ADR-001", "ADR-004"],
        "related_contracts": [
            "CONTRACT-001",
            "CONTRACT-002",
            "CONTRACT-003",
            "CONTRACT-004",
            "CONTRACT-005",
            "CONTRACT-006",
            "CONTRACT-007",
        ],
    },
    "SPEC-014": {
        "title": "Future Capabilities",
        "version": "1.0.0",
        "status": "proposed",
        "authority": "normative",
        "owner": "Platform Architecture",
        "related_specs": ["SPEC-006", "SPEC-013"],
        "related_adrs": ["ADR-010"],
        "related_contracts": [
            "CONTRACT-001",
            "CONTRACT-002",
            "CONTRACT-003",
            "CONTRACT-004",
            "CONTRACT-005",
            "CONTRACT-006",
            "CONTRACT-007",
        ],
    },
}

ADR_META = {
    "ADR-001": {
        "title": "Repository Strategy",
        "status": "accepted",
        "related_specs": ["SPEC-001", "SPEC-010"],
    },
    "ADR-002": {
        "title": "Platform Canon",
        "status": "proposed",
        "related_specs": ["SPEC-001", "SPEC-004", "SPEC-005"],
    },
    "ADR-003": {
        "title": "Signals Stack",
        "status": "accepted",
        "related_specs": ["SPEC-003", "SPEC-004", "SPEC-005"],
    },
    "ADR-004": {
        "title": "Repository Ownership",
        "status": "accepted",
        "related_specs": ["SPEC-001", "SPEC-009"],
    },
    "ADR-005": {
        "title": "allocationId",
        "status": "accepted",
        "related_specs": ["SPEC-004", "SPEC-006"],
    },
    "ADR-006": {
        "title": "Human Approval",
        "status": "accepted",
        "related_specs": ["SPEC-001", "SPEC-004"],
    },
    "ADR-007": {
        "title": "Evidence Chain",
        "status": "accepted",
        "related_specs": ["SPEC-004", "SPEC-005"],
    },
    "ADR-008": {
        "title": "Documentation Strategy",
        "status": "accepted",
        "related_specs": ["SPEC-010"],
    },
    "ADR-009": {
        "title": "Deterministic Demo",
        "status": "accepted",
        "related_specs": ["SPEC-011"],
    },
    "ADR-010": {
        "title": "Future Capabilities",
        "status": "proposed",
        "related_specs": ["SPEC-006", "SPEC-014"],
    },
}

CONTRACT_META = {
    "CONTRACT-001": {
        "title": "Opportunity",
        "owner": "Fund Intel",
        "lifecycle_stage": "Opportunity",
        "schema": "../schemas/opportunity.json",
        "producer": "Fund Intel",
        "consumer": "Autonomous Giving",
        "related_specs": ["SPEC-003", "SPEC-007"],
        "related_events": ["EVENT-002"],
    },
    "CONTRACT-002": {
        "title": "Recommendation",
        "owner": "Fund Intel",
        "lifecycle_stage": "Recommendation",
        "schema": "../schemas/recommendation.json",
        "producer": "Fund Intel",
        "consumer": "Autonomous Giving",
        "related_specs": ["SPEC-003", "SPEC-007"],
        "related_events": ["EVENT-003"],
    },
    "CONTRACT-003": {
        "title": "Allocation",
        "owner": "Autonomous Giving",
        "lifecycle_stage": "Allocation",
        "schema": "../schemas/allocation.json",
        "producer": "Autonomous Giving",
        "consumer": "Impact Relay",
        "related_specs": ["SPEC-005", "SPEC-007"],
        "related_events": ["EVENT-005"],
    },
    "CONTRACT-004": {
        "title": "Evidence",
        "owner": "Impact Relay",
        "lifecycle_stage": "Evidence",
        "schema": "../schemas/evidence.json",
        "producer": "Impact Relay",
        "consumer": "Autonomous Giving",
        "related_specs": ["SPEC-005", "SPEC-007"],
        "related_events": ["EVENT-007"],
    },
    "CONTRACT-005": {
        "title": "Receipt",
        "owner": "Autonomous Giving",
        "lifecycle_stage": "Receipt",
        "schema": "../schemas/receipt.json",
        "producer": "Autonomous Giving",
        "consumer": "Impact Relay",
        "related_specs": ["SPEC-005", "SPEC-007"],
        "related_events": ["EVENT-008"],
    },
    "CONTRACT-006": {
        "title": "Notification",
        "owner": "Impact Relay",
        "lifecycle_stage": "Notification",
        "schema": "../schemas/notification.json",
        "producer": "Impact Relay",
        "consumer": "Channel adapter",
        "related_specs": ["SPEC-006", "SPEC-007"],
        "related_events": ["EVENT-010"],
    },
    "CONTRACT-007": {
        "title": "TimelineEvent",
        "owner": "Impact Relay",
        "lifecycle_stage": "Notification",
        "schema": "../schemas/timeline-event.json",
        "producer": "Ecosystem boundary",
        "consumer": "Impact Relay",
        "related_specs": ["SPEC-007", "SPEC-009"],
        "related_events": [],
    },
}

EVENT_META = {
    "EVENT-001": {
        "title": "SignalDetected",
        "owner": "Fund Intel",
        "lifecycle_stage": "Signal",
        "producer": "Fund Intel",
        "consumers": ["Fund Intel", "Impact Relay"],
        "schema": "../schemas/signal-detected.json",
        "contract": None,
        "idempotency": "eventId",
        "related_specs": ["SPEC-003", "SPEC-008"],
        "related_contracts": [],
    },
    "EVENT-002": {
        "title": "OpportunityCreated",
        "owner": "Fund Intel",
        "lifecycle_stage": "Opportunity",
        "producer": "Fund Intel",
        "consumers": ["Autonomous Giving", "Impact Relay"],
        "schema": "../schemas/opportunity.json",
        "contract": "CONTRACT-001",
        "idempotency": "eventId",
        "related_specs": ["SPEC-003", "SPEC-008"],
        "related_contracts": ["CONTRACT-001"],
    },
    "EVENT-003": {
        "title": "RecommendationGenerated",
        "owner": "Fund Intel",
        "lifecycle_stage": "Recommendation",
        "producer": "Fund Intel",
        "consumers": ["Autonomous Giving", "Impact Relay"],
        "schema": "../schemas/recommendation.json",
        "contract": "CONTRACT-002",
        "idempotency": "eventId",
        "related_specs": ["SPEC-003", "SPEC-008"],
        "related_contracts": ["CONTRACT-002"],
    },
    "EVENT-004": {
        "title": "ApprovalGranted",
        "owner": "Autonomous Giving",
        "lifecycle_stage": "Approval",
        "producer": "Autonomous Giving",
        "consumers": ["Autonomous Giving", "Impact Relay"],
        "schema": "../schemas/approval-granted.json",
        "contract": None,
        "idempotency": "eventId",
        "related_specs": ["SPEC-005", "SPEC-008"],
        "related_contracts": [],
    },
    "EVENT-005": {
        "title": "AllocationCreated",
        "owner": "Autonomous Giving",
        "lifecycle_stage": "Allocation",
        "producer": "Autonomous Giving",
        "consumers": ["Autonomous Giving", "Impact Relay"],
        "schema": "../schemas/allocation.json",
        "contract": "CONTRACT-003",
        "idempotency": "eventId",
        "related_specs": ["SPEC-005", "SPEC-008"],
        "related_contracts": ["CONTRACT-003"],
    },
    "EVENT-006": {
        "title": "ExecutionStarted",
        "owner": "Autonomous Giving",
        "lifecycle_stage": "Execution",
        "producer": "Autonomous Giving",
        "consumers": ["Impact Relay"],
        "schema": "../schemas/execution-started.json",
        "contract": None,
        "idempotency": "eventId",
        "related_specs": ["SPEC-006", "SPEC-008"],
        "related_contracts": [],
    },
    "EVENT-007": {
        "title": "EvidenceAttached",
        "owner": "Impact Relay",
        "lifecycle_stage": "Evidence",
        "producer": "Impact Relay",
        "consumers": ["Impact Relay", "Autonomous Giving"],
        "schema": "../schemas/evidence.json",
        "contract": "CONTRACT-004",
        "idempotency": "eventId",
        "related_specs": ["SPEC-005", "SPEC-008"],
        "related_contracts": ["CONTRACT-004"],
    },
    "EVENT-008": {
        "title": "ReceiptGenerated",
        "owner": "Autonomous Giving",
        "lifecycle_stage": "Receipt",
        "producer": "Autonomous Giving",
        "consumers": ["Impact Relay"],
        "schema": "../schemas/receipt.json",
        "contract": "CONTRACT-005",
        "idempotency": "eventId",
        "related_specs": ["SPEC-005", "SPEC-008"],
        "related_contracts": ["CONTRACT-005"],
    },
    "EVENT-009": {
        "title": "VerificationCompleted",
        "owner": "Impact Relay",
        "lifecycle_stage": "Verification",
        "producer": "Impact Relay",
        "consumers": ["Autonomous Giving", "Impact Relay"],
        "schema": "../schemas/verification-completed.json",
        "contract": None,
        "idempotency": "eventId",
        "related_specs": ["SPEC-005", "SPEC-008"],
        "related_contracts": [],
    },
    "EVENT-010": {
        "title": "NotificationSent",
        "owner": "Impact Relay",
        "lifecycle_stage": "Notification",
        "producer": "Impact Relay",
        "consumers": ["Channel adapter", "Autonomous Giving"],
        "schema": "../schemas/notification.json",
        "contract": "CONTRACT-006",
        "idempotency": "eventId",
        "related_specs": ["SPEC-006", "SPEC-008"],
        "related_contracts": ["CONTRACT-006"],
    },
}

# Complete fenced JSON examples for events (payload-level, schema-valid).
EVENT_EXAMPLES = {
    "EVENT-001": {
        "signalId": "a0c2e191-3000-4000-8000-000000000001",
        "needId": "need-community-ai-lab",
        "source": "community-needs-survey",
        "observedAt": "2026-08-03T15:50:00Z",
        "confidence": 0.92,
    },
    "EVENT-002": {
        "opportunityId": "a6c2e191-3000-4000-8000-000000000001",
        "needId": "need-community-ai-lab",
        "title": "Laptop access",
        "status": "open",
        "createdAt": "2026-08-03T16:00:00Z",
    },
    "EVENT-003": {
        "recommendationId": "b6c2e191-3000-4000-8000-000000000001",
        "opportunityId": "a6c2e191-3000-4000-8000-000000000001",
        "proposedAmount": 2500,
        "currency": "USD",
        "rationale": "Equip the lab",
        "createdAt": "2026-08-03T16:05:00Z",
    },
    "EVENT-004": {
        "approvalId": "approval-community-ai-lab",
        "recommendationId": "b6c2e191-3000-4000-8000-000000000001",
        "approvedBy": "human-reviewer",
        "approvedAt": "2026-08-03T16:08:00Z",
        "policyReference": "policy-human-approval-v1",
    },
    "EVENT-005": {
        "allocationId": "c6c2e191-3000-4000-8000-000000000001",
        "recommendationId": "b6c2e191-3000-4000-8000-000000000001",
        "approvalId": "approval-community-ai-lab",
        "amount": 2500,
        "currency": "USD",
        "createdAt": "2026-08-03T16:10:00Z",
    },
    "EVENT-006": {
        "executionId": "f0c2e191-3000-4000-8000-000000000001",
        "allocationId": "c6c2e191-3000-4000-8000-000000000001",
        "channel": "vendor-purchase",
        "startedAt": "2026-08-03T16:15:00Z",
    },
    "EVENT-007": {
        "evidenceId": "d6c2e191-3000-4000-8000-000000000001",
        "allocationId": "c6c2e191-3000-4000-8000-000000000001",
        "type": "delivery_photo",
        "uri": "https://evidence.example/community-ai-lab/delivery-1",
        "capturedAt": "2026-08-03T16:20:00Z",
        "source": "Community AI Lab",
    },
    "EVENT-008": {
        "receiptId": "e6c2e191-3000-4000-8000-000000000001",
        "allocationId": "c6c2e191-3000-4000-8000-000000000001",
        "amount": 2500,
        "currency": "USD",
        "issuedAt": "2026-08-03T16:25:00Z",
        "issuer": "Community Technology Supply",
    },
    "EVENT-009": {
        "verificationId": "e0c2e191-3000-4000-8000-000000000001",
        "allocationId": "c6c2e191-3000-4000-8000-000000000001",
        "evidenceIds": ["d6c2e191-3000-4000-8000-000000000001"],
        "outcome": "verified",
        "verifiedAt": "2026-08-03T16:28:00Z",
        "verifier": "impact-relay-reviewer",
    },
    "EVENT-010": {
        "notificationId": "f6c2e191-3000-4000-8000-000000000001",
        "timelineEventId": "a6c2e191-3000-4000-8000-000000000002",
        "channel": "in_app",
        "createdAt": "2026-08-03T16:30:00Z",
    },
}


def _dump_fm(data: dict) -> str:
    # Drop keys with None values for cleaner frontmatter.
    cleaned = {k: v for k, v in data.items() if v is not None}
    dumped = yaml.safe_dump(
        cleaned,
        sort_keys=False,
        allow_unicode=True,
        default_flow_style=False,
    )
    return f"---\n{dumped}---\n\n"


def _has_frontmatter(text: str) -> bool:
    return text.startswith("---\n") or text.startswith("---\r\n")


def inject(path: Path, meta: dict) -> bool:
    text = path.read_text(encoding="utf-8")
    if _has_frontmatter(text):
        return False
    path.write_text(_dump_fm(meta) + text, encoding="utf-8")
    return True


def ensure_event_example(path: Path, event_id: str) -> None:
    text = path.read_text(encoding="utf-8")
    if "```json" in text:
        return
    import json

    example = EVENT_EXAMPLES[event_id]
    block = (
        "\n## Example payload\n\n```json\n"
        + json.dumps(example, indent=2)
        + "\n```\n"
    )
    # Insert before Version history if present
    if "## Version history" in text:
        text = text.replace("## Version history", block + "\n## Version history", 1)
    else:
        text = text.rstrip() + "\n" + block
    path.write_text(text, encoding="utf-8")


def main() -> int:
    changed = 0
    for sid, meta in SPEC_META.items():
        matches = list((ROOT / "specs").glob(f"{sid}-*.md"))
        if not matches:
            print(f"WARN missing {sid}", file=sys.stderr)
            continue
        payload = {"id": sid, **meta}
        if inject(matches[0], payload):
            changed += 1
            print(f"frontmatter {matches[0].name}")

    for aid, meta in ADR_META.items():
        matches = list((ROOT / "adr").glob(f"{aid}-*.md"))
        if not matches:
            print(f"WARN missing {aid}", file=sys.stderr)
            continue
        payload = {
            "id": aid,
            "version": "1.0.0",
            "authority": "normative",
            "owner": "Platform Architecture",
            "date": "2026-08-03",
            **meta,
        }
        if inject(matches[0], payload):
            changed += 1
            print(f"frontmatter {matches[0].name}")

    for cid, meta in CONTRACT_META.items():
        matches = list((ROOT / "contracts").glob(f"{cid}-*.md"))
        if not matches:
            print(f"WARN missing {cid}", file=sys.stderr)
            continue
        payload = {
            "id": cid,
            "version": "1.0.0",
            "status": "accepted",
            "authority": "normative",
            **meta,
        }
        if inject(matches[0], payload):
            changed += 1
            print(f"frontmatter {matches[0].name}")

    for eid, meta in EVENT_META.items():
        matches = list((ROOT / "events").glob(f"{eid}-*.md"))
        if not matches:
            print(f"WARN missing {eid}", file=sys.stderr)
            continue
        payload = {
            "id": eid,
            "version": "1.0.0",
            "status": "accepted",
            "authority": "normative",
            **meta,
        }
        if inject(matches[0], payload):
            changed += 1
            print(f"frontmatter {matches[0].name}")
        ensure_event_example(matches[0], eid)
        print(f"example {matches[0].name}")

    print(f"Updated {changed} files with frontmatter")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
