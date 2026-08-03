# Community AI Lab — executable demo fixture

Deterministic conformance fixture for [SPEC-011](../../specs/SPEC-011-demo-specification.md).

## Files

| File | Purpose |
| --- | --- |
| `scenario.json` | Fixed identities, amounts, and invariants |
| `expected-events.jsonl` | Canonical event order and schema-valid payloads |
| `expected-state-transitions.json` | Lifecycle stage sequence and ordering rules |
| `expected-receipts.json` | Receipt provenance tied to `allocationId` |
| `invalid-cases/` | Negative vectors implementations must reject |

## Invariants validated by `validation/validate_demo.py`

1. **Event order** — Approval before Allocation; Evidence before Verification; Notification only after Verification.
2. **Contract payloads** — each event payload validates against its schema.
3. **Allocation identity continuity** — every `allocationId` matches `scenario.json`.
4. **Human approval before allocation** — `ApprovalGranted` precedes `AllocationCreated`.
5. **Evidence before verification** — `EvidenceAttached` precedes `VerificationCompleted`.
6. **Receipt provenance** — receipt amount and `allocationId` match the scenario.
7. **Notification after verified impact path** — `NotificationSent` follows verification.
8. **Replay determinism** — fixed UUIDs and timestamps; re-running the fixture yields identical artifacts.

## Consumer usage

Implementations should load these fixtures, drive their pipelines (or replay adapters), and assert identical event order, payloads (modulo transport envelope fields they add), and state transitions.
