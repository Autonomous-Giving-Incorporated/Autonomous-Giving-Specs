---
id: SPEC-029
title: Mission Graph and Learning Feedback
version: 0.1.0
status: proposed
authority: normative
owner: Platform Architecture
related_specs:
- SPEC-003
- SPEC-004
- SPEC-005
- SPEC-006
- SPEC-017
- SPEC-018
- SPEC-027
- SPEC-028
related_adrs:
- ADR-003
- ADR-006
- ADR-007
related_contracts: []
---

# SPEC-029: Mission Graph and Learning Feedback
| Version | 0.1.0 | Owner | Platform Architecture | Status | Proposed |
| --- | --- | --- | --- | --- | --- |
| Dependencies | SPEC-003–006, SPEC-017, SPEC-018, SPEC-027, SPEC-028 | Related ADRs | ADR-003, ADR-006, ADR-007 | Related contracts | None |

## Purpose

Define the **Mission Graph** as a traceable projection over existing canonical artifacts, and define the governed feedback relationship by which verified Impact can inform a future Signal. This specification adds neither a lifecycle nor a system of record.

## Scope

Relationship projection, record ownership, learning-feedback provenance, epistemic classification, and projection privacy. It does not require a graph database, microservice, new event, or new capability.

## Canonical relationship model

The canonical lifecycle remains exactly as defined by [SPEC-005](SPEC-005-lifecycle.md):

```text
Need → Signal → Opportunity → Recommendation → Approval → Allocation
  → Execution → Evidence → Receipt → Verification → Impact
```

The Mission Graph may render traceable relationships over those artifacts:

```text
Need
 ├── Signal → source / provenance
 ├── Opportunity → supporting Signals
 ├── Recommendation → rationale / evidence references
 ├── Approval → human authority
 ├── Allocation → pot / fund / project
 ├── Execution → program / activity
 ├── Evidence → source artifact
 ├── Receipt → lineage
 ├── Verification → verifier
 └── Impact → outcome → Learning Feedback → new Signal
```

`Learning Feedback` is a relationship from a prior verified outcome into a **new** Signal. It is not a lifecycle stage, transition, or substitute for Fund Intel’s normal Signal → Opportunity → Recommendation boundary.

## Requirements

1. The Mission Graph MUST be a projection, not a lifecycle and not a second system of record.
2. A projection MUST link to the owner and canonical identifier of every underlying artifact it represents. Cross-capability traversal MUST NOT change record ownership.
3. Rendering, querying, or traversing the Mission Graph MUST NOT create authority, mutate canonical artifacts, or cause a consequential state change.
4. Learning Feedback MUST be derived from verified Impact or evidence explicitly classified with its epistemic state. It MUST preserve references to the available Impact, Verification, Evidence, and provenance records.
5. Learning Feedback MUST preserve `OBSERVED`, `INFERRED`, `SPECULATIVE`, or `NOT_COMPUTABLE` classification. Inferred or speculative feedback MUST NOT be presented as observed fact.
6. If required evidence is absent, weak, stale, conflicting, or unauthorized, the resulting learning output MUST be `NOT_COMPUTABLE`; an implementation MUST NOT invent learning.
7. A feedback-derived Signal MUST be a new immutable Signal owned by Fund Intel, with its own identifier, provenance, and references to the source Impact and Verification where available. It MUST NOT silently mutate a prior Signal, Opportunity, Recommendation, or Impact.
8. New Signals from learning feedback MUST re-enter through Fund Intel and follow the normal Signal → Opportunity → Recommendation path. Fund Intel retains advisory-only intelligence authority.
9. No direct `Impact → Recommendation`, `Impact → Approval`, `Impact → Allocation`, or `Impact → Execution` transition is allowed.
10. Autonomous Giving MAY render authorized Mission Graph projections but MUST NOT thereby become canonical owner of Fund Intel or Impact Relay records.
11. Public Mission Graph projections MUST comply with [SPEC-017](SPEC-017-data-classification-and-privacy.md), including aggregate-safe presentation and existing privacy rules.
12. AI may extract, classify, summarize, rank, score, forecast, and recommend only where evidence permits. AI MUST NOT independently approve, allocate, fabricate or waive Evidence, verify unsupported claims, or create irreversible organizational commitments.

## Conformance and non-goals

The graph may be implemented as linked records, a materialized read model, or another projection appropriate to a modular monolith. No graph database, separate microservice, direct Impact-to-action automation, or duplicate storage is required. The Mission Graph does not change contracts or event meaning.

## References

- [SPEC-003](SPEC-003-signals-stack.md) — Fund Intel Signal ownership and advisory boundary
- [SPEC-005](SPEC-005-lifecycle.md) — sole canonical lifecycle
- [SPEC-006](SPEC-006-capability-boundaries.md) — capability ownership
- [SPEC-018](SPEC-018-evidence-integrity-and-provenance.md) — provenance discipline
- [SPEC-027](SPEC-027-impact-loop.md) — verified outcomes and ImpactNotice projection
- [SPEC-028](SPEC-028-agi-control-plane.md) — authorized control-plane projections
