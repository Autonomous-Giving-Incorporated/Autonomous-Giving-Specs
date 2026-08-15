---
id: SPEC-017
title: Data Classification and Privacy
version: 1.1.0
status: accepted
authority: normative
owner: Platform Architecture
related_specs:
- SPEC-004
- SPEC-016
- SPEC-019
- SPEC-027
- SPEC-028
related_adrs:
- ADR-004
- ADR-007
- ADR-014
- ADR-015
related_contracts:
- CONTRACT-003
- CONTRACT-004
- CONTRACT-005
- CONTRACT-006
- CONTRACT-007
- CONTRACT-012
- CONTRACT-013
---

# SPEC-017: Data Classification and Privacy
| Version | 1.1.0 | Owner | Platform Architecture | Status | Accepted |
| --- | --- | --- | --- | --- | --- |
| Dependencies | SPEC-004, SPEC-016, SPEC-027 | Related ADRs | ADR-004, ADR-007, ADR-014, ADR-015 | Related contracts | CONTRACT-003–007, CONTRACT-012, CONTRACT-013 |

## Purpose
Classify platform data so public, tenant, and private fields are handled consistently across capabilities.

## Scope
Data at rest and in events/contracts for the Autonomous Giving Platform. Legal jurisdiction mapping is left to operators; classification labels are platform-normative.

## Classification labels

| Label | Meaning | Default handling |
| --- | --- | --- |
| `public` | Safe for unrestricted timeline projection | May appear in TimelineEvent and public demos |
| `tenant` | Visible to the operating organization and authorized capabilities | Not donor-public by default |
| `restricted` | Need-to-know within a capability or role | Not placed in Notification bodies without purpose |
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
3. Channel adapters MUST honor suppression/unsubscribe signals from the owning transparency capability.

### Redaction
1. Public TimelineEvent projections MUST redact `pii` and `restricted` fields.
2. Redaction is a projection concern: authoritative events retain full authorized payload for entitled auditors.
3. Export and support tooling MUST apply the same redaction rules as public APIs when the audience is public.

### Tenant boundaries
1. Data for one organization/tenant MUST NOT be readable by another tenant’s principals by default.
2. Cross-tenant analytics require explicit product authority and aggregation that removes `pii`.
3. Control-plane context ([SPEC-028](SPEC-028-agi-control-plane.md)) MUST fail closed on `client_id` / `tenant_id` mismatch so classification labels cannot leak across tenants.

### ImpactNotice and no invented PII
1. [CONTRACT-013](../contracts/CONTRACT-013-impact-notice.md) MUST NOT require or include donor email, name, or phone ([SPEC-027](SPEC-027-impact-loop.md)).
2. If the donation-source connector omits opt-in contactable identity, implementations MUST NOT emit ImpactNotice, MUST NOT send email, and MUST NOT invent an address or push target.
3. ImpactNotice CTA is the tenant outbound Donation Link, not a checkout session ([ADR-015](../adr/ADR-015-donation-tracking-money-boundary.md)).
4. Public projections ([CONTRACT-012](../contracts/CONTRACT-012-public-projection.md)) MUST remain aggregate-safe: no donor identity, private evidence URL, or service credential.

## Non-goals
This specification does not implement GDPR/CCPA compliance programs, cookie banners, or marketing consent UX. It does not store personal data in this repository.
