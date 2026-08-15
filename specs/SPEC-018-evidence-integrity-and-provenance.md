---
id: SPEC-018
title: Evidence Integrity and Provenance
version: 1.1.0
status: accepted
authority: normative
owner: Impact Relay
related_specs:
- SPEC-002
- SPEC-005
- SPEC-007
- SPEC-016
- SPEC-028
related_adrs:
- ADR-007
- ADR-014
related_contracts:
- CONTRACT-003
- CONTRACT-004
- CONTRACT-005
- CONTRACT-012
---

# SPEC-018: Evidence Integrity and Provenance
| Version | 1.1.0 | Owner | Impact Relay | Status | Accepted |
| --- | --- | --- | --- | --- | --- |
| Dependencies | SPEC-002, SPEC-005, SPEC-007 | Related ADRs | ADR-007, ADR-014 | Related contracts | CONTRACT-003–005, CONTRACT-012 |

## Purpose
Ensure Evidence, Receipt, and Verification form an attributable, append-only chain from Allocation to Impact.

## Scope
Contracts and events for Evidence, Receipt, Verification, and impact claims. Binary artifact storage backends are implementation concerns; integrity properties are normative.

## Requirements

### Append-only history
1. Evidence records are immutable after publish. Corrections are new Evidence linked to the same `allocationId`, never in-place edits.
2. Receipt records are immutable after publish. Amendments are new Receipts or separately governed amendment events, never silent mutation.
3. Verification outcomes are immutable; a new Verification may supersede interpretation for product display but prior Verification events remain in the log.

### Authenticity
1. Each Evidence item SHALL identify `source`, `capturedAt`, `type`, and resolvable `uri` (or equivalent content address in a future schema version).
2. Implementations SHOULD store a content hash of binary evidence alongside the URI for tamper detection; when present, the hash is part of verification input.
3. Producers MUST validate Evidence and Receipt payloads against their schemas before publish.

### Provenance for impact
1. An Impact claim SHALL reference the `allocationId` and the Verification (and thereby Evidence) that supports it.
2. Impact MUST NOT be asserted from Notification or TimelineEvent alone.
3. Public impact statements MUST remain reconcilable to the event chain in the Community AI Lab fixture pattern.

### Receipt integrity
1. Receipt `amount` and `currency` MUST be correlatable to the Allocation; exceeding Allocation without an explicit amendment is non-conformant.
2. Receipt `issuer` and `issuedAt` are required provenance fields.
3. Receipt identifiers are unique and never reused.

### Audit-log integrity
1. Authoritative lifecycle events form the audit log. Implementations MUST retain them for the retention period required by their operators, and at minimum long enough to support dispute review for active Allocations.
2. Audit storage SHOULD detect truncation or reordering (monotonic store, hash chain, or equivalent). Exact mechanism is implementation-defined but MUST be documented in the consumer’s conformance evidence.
3. Deletion of audit events for convenience is forbidden; legal erasure requests follow [SPEC-017](SPEC-017-data-classification-and-privacy.md) and MUST NOT destroy non-PII allocation integrity metadata required for institutional accountability without a recorded legal basis.

### Verification discipline
1. Verification MUST name one or more `evidenceIds` and an `outcome`.
2. Verification without Evidence is non-conformant.
3. Automated checks may assist but do not replace the Verification record requirements.

### Control-plane non-duplication
1. AGI MUST NOT duplicate Impact Relay evidence, verification, or public-projection records as a second system of record ([SPEC-028](SPEC-028-agi-control-plane.md), [ADR-014](../adr/ADR-014-agi-control-plane.md)).
2. Public projections ([CONTRACT-012](../contracts/CONTRACT-012-public-projection.md)) MUST remain reconcilable to Verification and MUST NOT become an editable evidence store.

## Non-goals
This specification does not require a particular blockchain, WORM appliance, or certificate authority. It does not define courtroom evidentiary standards.
