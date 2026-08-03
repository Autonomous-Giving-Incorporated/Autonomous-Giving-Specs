"""Validate deterministic demo fixtures when present."""

from __future__ import annotations

import json
from pathlib import Path

from jsonschema import Draft202012Validator, FormatChecker

from lib.constants import CANONICAL_LIFECYCLE
from lib.documents import DocumentIndex, load_json_schema, resolve_schema_path
from lib.report import Report

DEMO_DIR = Path("demo/community-ai-lab")


def validate_demo(index: DocumentIndex, report: Report) -> None:
    demo = index.root / DEMO_DIR
    if not demo.exists():
        report.warning("DEMO_DIR_MISSING", f"{DEMO_DIR} not present", str(DEMO_DIR))
        return

    scenario_path = demo / "scenario.json"
    events_path = demo / "expected-events.jsonl"
    transitions_path = demo / "expected-state-transitions.json"
    receipts_path = demo / "expected-receipts.json"

    required = [scenario_path, events_path, transitions_path, receipts_path]
    for path in required:
        if not path.exists():
            report.error("DEMO_FIXTURE_MISSING", f"Missing {path.relative_to(index.root)}", path.as_posix())
            return

    scenario = json.loads(scenario_path.read_text(encoding="utf-8"))
    allocation_id = scenario.get("allocationId")
    if not allocation_id:
        report.error("DEMO_ALLOCATION_ID", "scenario.json missing allocationId", scenario_path.as_posix())

    # Events order and schemas
    events: list[dict] = []
    for line_no, line in enumerate(events_path.read_text(encoding="utf-8").splitlines(), 1):
        line = line.strip()
        if not line:
            continue
        try:
            events.append(json.loads(line))
        except json.JSONDecodeError as exc:
            report.error(
                "DEMO_EVENT_JSON",
                f"expected-events.jsonl line {line_no}: {exc}",
                events_path.as_posix(),
            )

    if not events:
        report.error("DEMO_EVENTS_EMPTY", "expected-events.jsonl has no events", events_path.as_posix())
        return

    # Must include Approval before AllocationCreated
    types = [e.get("eventType") for e in events]
    if "ApprovalGranted" not in types:
        report.error("DEMO_APPROVAL_REQUIRED", "Demo must include ApprovalGranted", events_path.as_posix())
    if "AllocationCreated" not in types:
        report.error("DEMO_ALLOCATION_REQUIRED", "Demo must include AllocationCreated", events_path.as_posix())
    if "ApprovalGranted" in types and "AllocationCreated" in types:
        if types.index("ApprovalGranted") > types.index("AllocationCreated"):
            report.error(
                "DEMO_APPROVAL_ORDER",
                "ApprovalGranted must precede AllocationCreated",
                events_path.as_posix(),
            )

    # Evidence before Verification; Notification only after Verification
    if "EvidenceAttached" in types and "VerificationCompleted" in types:
        if types.index("EvidenceAttached") > types.index("VerificationCompleted"):
            report.error(
                "DEMO_EVIDENCE_ORDER",
                "EvidenceAttached must precede VerificationCompleted",
                events_path.as_posix(),
            )
    if "NotificationSent" in types and "VerificationCompleted" in types:
        if types.index("NotificationSent") < types.index("VerificationCompleted"):
            report.error(
                "DEMO_NOTIFICATION_ORDER",
                "NotificationSent must follow VerificationCompleted",
                events_path.as_posix(),
            )

    # Continuity of allocationId
    for i, event in enumerate(events):
        payload = event.get("payload") or {}
        if "allocationId" in payload and payload["allocationId"] != allocation_id:
            report.error(
                "DEMO_ALLOCATION_CONTINUITY",
                f"Event[{i}] allocationId mismatch",
                events_path.as_posix(),
            )

    # Validate event payloads against schemas via event catalog meta when possible
    event_type_to_id = {
        "SignalDetected": "EVENT-001",
        "OpportunityCreated": "EVENT-002",
        "RecommendationGenerated": "EVENT-003",
        "ApprovalGranted": "EVENT-004",
        "AllocationCreated": "EVENT-005",
        "ExecutionStarted": "EVENT-006",
        "EvidenceAttached": "EVENT-007",
        "ReceiptGenerated": "EVENT-008",
        "VerificationCompleted": "EVENT-009",
        "NotificationSent": "EVENT-010",
    }
    format_checker = FormatChecker()
    for i, event in enumerate(events):
        et = event.get("eventType")
        eid = event_type_to_id.get(et)
        if not eid or eid not in index.events:
            continue
        art = index.events[eid]
        schema_path = resolve_schema_path(index, str(art.meta.get("schema") or art.meta.get("contract") or ""))
        if not schema_path:
            continue
        schema = load_json_schema(schema_path)
        payload = event.get("payload")
        validator = Draft202012Validator(schema, format_checker=format_checker)
        for err in sorted(validator.iter_errors(payload), key=lambda e: list(e.absolute_path)):
            loc = "/".join(str(p) for p in err.absolute_path) or "(root)"
            report.error(
                "DEMO_PAYLOAD_INVALID",
                f"Event[{i}] {et} payload {loc}: {err.message}",
                events_path.as_posix(),
            )

    transitions = json.loads(transitions_path.read_text(encoding="utf-8"))
    stages = transitions.get("stages") or transitions.get("sequence") or []
    if stages:
        # Must be subsequence of canonical lifecycle (+ Notification optional)
        canonical = CANONICAL_LIFECYCLE + ["Notification"]
        positions = []
        for stage in stages:
            if stage not in canonical:
                report.error(
                    "DEMO_TRANSITION_STAGE",
                    f"Non-canonical stage in transitions: {stage}",
                    transitions_path.as_posix(),
                )
            else:
                positions.append(canonical.index(stage))
        if positions != sorted(positions):
            report.error(
                "DEMO_TRANSITION_ORDER",
                "State transitions are not in canonical order",
                transitions_path.as_posix(),
            )

    receipts = json.loads(receipts_path.read_text(encoding="utf-8"))
    receipt_list = receipts if isinstance(receipts, list) else receipts.get("receipts", [])
    for i, receipt in enumerate(receipt_list):
        if receipt.get("allocationId") != allocation_id:
            report.error(
                "DEMO_RECEIPT_ALLOCATION",
                f"Receipt[{i}] allocationId mismatch",
                receipts_path.as_posix(),
            )
        if scenario.get("amount") is not None and receipt.get("amount") != scenario.get("amount"):
            report.error(
                "DEMO_RECEIPT_AMOUNT",
                f"Receipt[{i}] amount must equal scenario amount",
                receipts_path.as_posix(),
            )

    # Invalid cases: each must fail schema or invariant markers
    invalid_dir = demo / "invalid-cases"
    if invalid_dir.exists():
        for path in sorted(invalid_dir.glob("*.json")):
            try:
                case = json.loads(path.read_text(encoding="utf-8"))
            except json.JSONDecodeError as exc:
                report.error("DEMO_INVALID_CASE_JSON", str(exc), path.as_posix())
                continue
            if "expect_error" not in case and "expectError" not in case:
                report.warning(
                    "DEMO_INVALID_CASE_NO_EXPECT",
                    "Invalid case should declare expect_error",
                    path.relative_to(index.root).as_posix(),
                )


def main() -> int:
    from lib.documents import load_repository

    report = Report()
    index = load_repository()
    validate_demo(index, report)
    print(json.dumps(report.to_dict(), indent=2))
    return report.exit_code()


if __name__ == "__main__":
    raise SystemExit(main())
