---
id: SPEC-017
title: Data Classification and Privacy
version: 1.0.0
status: proposed
authority: normative
owner: Platform Architecture
related_specs:
- SPEC-004
- SPEC-016
- SPEC-019
related_adrs:
- ADR-004
- ADR-007
related_contracts:
- CONTRACT-003
- CONTRACT-004
- CONTRACT-005
- CONTRACT-006
- CONTRACT-007
---

# SPEC-017: Data Classification and Privacy
| Version | 1.0.0 | Owner | Platform Architecture | Status | Proposed |
| --- | --- | --- | --- | --- | --- |
| Dependencies | SPEC-004, SPEC-016 | Related ADRs | ADR-004, ADR-007 | Related contracts | CONTRACT-003–007 |

## Purpose
Classify platform data so public, tenant, and private fields are handled consistently across services.

## Scope
Data at rest and in events/contracts for the Autonomous Giving Platform. Legal jurisdiction mapping is left to operators; classification labels are platform-normative.

## Classification labels

| Label | Meaning | Default handling |
| --- | --- | --- |
| `public` | Safe for unrestricted timeline projection | May appear in TimelineEvent and public demos |
| `tenant` | Visible to the operating organization and authorized services | Not donor-public by default |
| `restricted` | Need-to-know within a service or role | Not placed in Notification bodies without purpose |
| `pii` | Identifies or reasonably links to a person | Minimized; access logged; redacted in public views |
| `sensitive-financial` | Amounts linked to account or payment instruments | Amounts on Allocation/Receipt may be tenant-visible; payment instrument data is out of band |

## Requirements

### Donor identity separation
1. Donor personal identifiers (name, email, payment account, government ID) SHALL NOT be required fields on Allocation, Evidence, Receipt, or Recommendation contracts.
2. Donor identity, when processed by an implementation, SHALL be stored in an identity-bounded store and linked to lifecycle records only by opaque references not defined as public contract fields in v1.
3. Public impact narratives MUST NOT reveal donor identity unless the donor has granted notification/publicity consent.

### Allocation data visibility
1. `allocationId`, stage, and non-identifying program context may be `tenant` or `public` according to product policy.
2. Detailed recommendation rationale may be `tenant` or `restricted`.
3. Implementations MUST document which Allocation fields they project publicly.

### PII minimization
1. New contract fields that introduce `pii` require SPEC amendment, classification note, and privacy review by the artifact owner.
2. Demo fixtures SHALL use synthetic identifiers only (as in Community AI Lab).
3. Logs and notifications SHOULD prefer stable opaque IDs over display names.

### Notification consent
1. Notification delivery presupposes a lawful basis or consent tracked outside the core lifecycle contracts.
2. `NotificationSent` records delivery attempts; they are not consent records.
3. Channel adapters MUST honor suppression/unsubscribe signals from the owning transparency service.

### Redaction
1. Public TimelineEvent projections MUST redact `pii` and `restricted` fields.
2. Redaction is a projection concern: authoritative events retain full authorized payload for entitled auditors.
3. Export and support tooling MUST apply the same redaction rules as public APIs when the audience is public.

### Tenant boundaries
1. Data for one organization/tenant MUST NOT be readable by another tenant’s principals by default.
2. Cross-tenant analytics require explicit product authority and aggregation that removes `pii`.

## Non-goals
This specification does not implement GDPR/CCPA compliance programs, cookie banners, or marketing consent UX. It does not store personal data in this repository.
