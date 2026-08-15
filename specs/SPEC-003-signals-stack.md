---
id: SPEC-003
title: Signals Stack
version: 2.0.0
status: accepted
authority: normative
owner: Fund Intel
related_specs:
- SPEC-002A
- SPEC-004
- SPEC-005
- SPEC-006
- SPEC-017
- SPEC-023
- SPEC-026
related_adrs:
- ADR-003
- ADR-006
- ADR-015
related_contracts:
- CONTRACT-001
- CONTRACT-002
related_events:
- EVENT-001
- EVENT-002
- EVENT-003
---

# SPEC-003: Signals Stack
| Version | 2.0.0 | Owner | Fund Intel | Status | Accepted |
| --- | --- | --- | --- | --- | --- |
| Dependencies | SPEC-004, SPEC-005, SPEC-006, SPEC-026 | Related ADRs | ADR-003, ADR-006, ADR-015 | Related contracts | CONTRACT-001, CONTRACT-002 |

## Purpose

Define the Fund Intel **observation → recommendation** boundary: how a Signal is captured, how Signals group into an Opportunity, and how an Opportunity may yield a Recommendation. Recommendations are advisory. They are never Approval, never Allocation, and never a pot credit.

## Scope

Signals, Opportunities, and Recommendations produced under Fund Intel responsibility. Connector gift summaries ([SPEC-026](SPEC-026-donation-source-connectors.md)) may **inform** Signals. This specification is logical architecture only: no event bus, stream processor, or network hop is required.

## Non-goals

Source-connector product APIs beyond the gift-summary adapter, scoring-model training, transport, deployment topology, Approval, Allocation, Evidence, ImpactNotice, and AGI checkout are excluded. Pot credit remains the SPEC-026 observe path, not a Recommendation effect.

## Definitions and required meaning

| Concept | Meaning | Public contract / event |
| --- | --- | --- |
| **Signal** | Immutable observation relevant to a Need ([TERM-004](../glossary/README.md)) | [EVENT-001](../events/EVENT-001-signal-detected.md) / `signal-detected.json` |
| **Opportunity** | Actionable grouping of a Need and supporting Signals ([TERM-005](../glossary/README.md)) | [CONTRACT-001](../contracts/CONTRACT-001-opportunity.md) |
| **Recommendation** | Proposed, non-authorizing allocation response ([TERM-006](../glossary/README.md)) | [CONTRACT-002](../contracts/CONTRACT-002-recommendation.md) |

### Signal — required meaning

Fund Intel MUST retain the following for every Signal, even when a published event omits an optional field:

| Field | Rule |
| --- | --- |
| `signalId` | Stable identifier; never reused |
| `needId` | The Need this observation is about |
| `source` | Provenance of the observation (survey, operator note, connector identity, CSV twin, or equivalent) |
| `subject` | What was observed (program, campaign, org, or other non-PII subject). MUST NOT be a donor email or name |
| `observedAt` | When the underlying fact occurred (RFC 3339) |
| `capturedAt` | When Fund Intel recorded the Signal (RFC 3339). MAY equal `observedAt` when they coincide |
| `confidence` | Closed interval `0.0`–`1.0` |

[EVENT-001](../events/EVENT-001-signal-detected.md) v1.1 requires `signalId`, `needId`, `source`, `observedAt`, and `confidence` on the published payload. `subject` and `capturedAt` are optional on that schema and MUST still be stored by Fund Intel.

A Signal is append-only after publish. Corrections are new Signals, not in-place edits ([ADR-003](../adr/ADR-003-platform-canon.md)).

### Opportunity — required meaning

[CONTRACT-001](../contracts/CONTRACT-001-opportunity.md) required fields remain: `opportunityId`, `needId`, `title`, `status`, `createdAt`. Allowed `status`: `open`, `dismissed`, `converted`.

Fund Intel MUST also retain the **grouping**: the set of `signalId` values that support the Opportunity. `signalIds` MAY appear on the CONTRACT-001 payload (schema 1.1.0, optional). Absence on the public payload does not authorize an Opportunity with no supporting Signals.

`converted` means a Recommendation was published for this Opportunity. `dismissed` means Fund Intel closed it without recommending. Neither status is Approval.

### Recommendation — required meaning

[CONTRACT-002](../contracts/CONTRACT-002-recommendation.md) required fields remain: `recommendationId`, `opportunityId`, `proposedAmount`, `currency`, `rationale`, `createdAt`.

A Recommendation MUST reference an existing Opportunity. `proposedAmount` is a proposal, not a pot debit and not an Allocation. `rationale` MUST be non-empty and MUST remain reconcilable to the supporting Signals (via the Opportunity grouping).

CONTRACT-001 and CONTRACT-002 required fields are complete for the v1 public boundary. This specification does not add required contract fields.

## How Signals become Opportunities become Recommendations

```text
Need
  → Signal (immutable observation; EVENT-001)
  → Opportunity (group Signals under one Need; CONTRACT-001 / EVENT-002)
  → Recommendation (advisory proposal; CONTRACT-002 / EVENT-003)
       -- not Approval
       -- not Allocation
       -- not pot credit
```

1. A Signal MUST name a `needId`. Signals without a Need are not platform Signals.
2. An Opportunity MUST group one or more Signals for the same `needId`. Grouping MUST NOT mix Needs.
3. Fund Intel MAY publish an Opportunity only when at least one supporting Signal is retained and is not stale under the rules below.
4. A Recommendation MAY be published only for an `open` Opportunity. Publishing a Recommendation SHOULD set that Opportunity to `converted`.
5. Multiple Recommendations MAY exist for one Opportunity over time; each is a new `recommendationId`. A later Recommendation does not rewrite a prior one.
6. Absence of a Recommendation is a valid outcome (see Negative cases). Implementations MUST NOT mint a zero-rationale Recommendation to represent “do not recommend.”

## Advisory-only (hard boundary)

7. Intelligence MUST NOT grant Approval ([ADR-006](../adr/ADR-006-human-approval.md)).
8. Intelligence MUST NOT create Allocation, execute fulfillment, or issue Receipt.
9. A Recommendation MUST NOT credit, debit, or lock a pot. Pot credit is the [SPEC-026](SPEC-026-donation-source-connectors.md) gift-summary path, not a Recommendation side effect.
10. Intelligence MUST NOT attach Evidence, waive Evidence, or emit ImpactNotice ([SPEC-027](SPEC-027-impact-loop.md)).
11. Consumers MUST treat CONTRACT-002 as a proposal. Governance (Autonomous Giving) is the only capability that may turn a Recommendation into Approval and then Allocation ([SPEC-006](SPEC-006-capability-boundaries.md)).

## Gift summaries may inform Signals

Connector gift summaries are a distinct state family from Recommendations ([SPEC-023](SPEC-023-financial-ledger-invariants.md), [ADR-015](../adr/ADR-015-donation-tracking-money-boundary.md)):

```text
connector gift state  ≠  pot credit  ≠  Signal  ≠  Recommendation
```

12. A verified gift summary MAY produce a Signal whose `source` names the connector (P0: `every.org`) and whose `subject` is a non-PII campaign/program/pot key. The Signal MUST NOT copy donor email, name, or phone.
13. Applying a gift summary to a pot (`chargeId` idempotency, `netAmount` credit) follows SPEC-026 and MUST remain a separate write from publishing EVENT-001, EVENT-002, or EVENT-003.
14. Implementations MUST NOT collapse gift state into a Recommendation (for example: treating `chargeId` as `recommendationId`, or treating pot `available` as `proposedAmount` without a human-readable rationale).
15. Unverified webhooks MUST NOT create Signals, Opportunities, Recommendations, or pot credits ([SPEC-016](SPEC-016-security-and-trust-boundaries.md), SPEC-026).
16. Stripe billing webhooks MUST NOT create Signals or gift summaries.

## Provenance, confidence, and staleness

17. `source` and `observedAt` are provenance. Consumers MUST be able to evaluate source quality independently of recommendation policy ([ADR-003](../adr/ADR-003-platform-canon.md)).
18. `confidence` is an input to grouping and recommend/do-not-recommend policy. It is not authorization.
19. A Signal is **stale** when Fund Intel’s published policy says `observedAt` (or `capturedAt` if `observedAt` is absent) is older than the configured horizon for that `source` class. Stale Signals MUST NOT be the sole support for a new Recommendation.
20. Implementations MUST document their staleness horizon in conformance evidence. This specification does not invent a numeric TTL.
21. Re-using a stale Signal as historical context on an Opportunity is allowed if at least one non-stale supporting Signal remains, or if Fund Intel dismisses the Opportunity instead of recommending.

## Negative cases

| Outcome | Required behavior |
| --- | --- |
| Insufficient evidence | Fewer than one retained supporting Signal, or Signals that do not share `needId` → MUST NOT publish Opportunity; MUST NOT publish Recommendation |
| Stale signal | Sole remaining support is stale → MUST NOT publish Recommendation; Opportunity MAY be `dismissed` |
| Do-not-recommend | Policy or reviewer judgement against proposing funds → MUST NOT emit EVENT-003; Opportunity status `dismissed` or left `open` without conversion |
| Unverified connector input | MUST NOT create Signal or pot credit |
| Donor PII in the observation | MUST NOT place email, name, or phone on Signal `subject`, Opportunity `title`, or Recommendation `rationale` ([SPEC-017](SPEC-017-data-classification-and-privacy.md)) |
| Gift without a Need | MAY credit a pot (SPEC-026) and MUST NOT invent a Recommendation to “explain” the gift |

## Topology

22. Fund Intel MAY run as a module inside a modular monolith or as a separately deployed unit. Neither choice changes contract ownership ([SPEC-002A](SPEC-002A-architectural-principles.md)).
23. No event bus, stream processor, or network hop is required. In-process calls remain conformant when EVENT-001–003 payloads and ordering invariants hold ([SPEC-008](SPEC-008-events.md)).

## Rationale

Splitting observation from judgement lets consumers reject a Recommendation without discarding the Signal log. Keeping pot credit off the Recommendation path prevents the money-boundary regression that treated intelligence output as a ledger write.

## References

- [ADR-003](../adr/ADR-003-platform-canon.md) — signals as immutable observations
- [SPEC-005](SPEC-005-lifecycle.md) — Need → Signal → Opportunity → Recommendation
- [SPEC-026](SPEC-026-donation-source-connectors.md) — gift summaries and pot credit
- [EVENT-001](../events/EVENT-001-signal-detected.md), [EVENT-002](../events/EVENT-002-opportunity-created.md), [EVENT-003](../events/EVENT-003-recommendation-generated.md)
