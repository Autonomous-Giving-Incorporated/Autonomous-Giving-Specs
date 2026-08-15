---
id: SPEC-009
title: Design System
version: 2.0.0
status: accepted
authority: normative
owner: Platform Product
related_specs:
- SPEC-004
- SPEC-005
- SPEC-011
- SPEC-017
- SPEC-023
- SPEC-026
- SPEC-027
related_adrs:
- ADR-006
- ADR-009
- ADR-015
related_contracts:
- CONTRACT-007
- CONTRACT-013
---

# SPEC-009: Design System
| Version | 2.0.0 | Owner | Platform Product | Status | Accepted |
| --- | --- | --- | --- | --- | --- |
| Dependencies | SPEC-004, SPEC-005, SPEC-017 | Related ADRs | ADR-006, ADR-009, ADR-015 | Related contracts | CONTRACT-007, CONTRACT-013 |

## Purpose

Specify **audit-visible information design** so a reviewer or operator can see lifecycle state, follow Impact back to Evidence, Allocation, and tracked gifts, and never mistake an outbound Donation Link for AGI checkout. This is not a Figma kit, token file, or React component library.

## Scope

Required visible states, traceability, accessibility of state, tenant vs public vs donor surface content, Donation Link CTA, ImpactNotice content, and formatting rules for diagrams and specifications in this repository.

## Non-goals

- UI code, CSS, design tokens, component implementations, or brand artwork in this repository
- A mobile or web visual language beyond information requirements
- Inventing product screens, live tenants, or workers.dev URLs
- Replacing [SPEC-017](SPEC-017-data-classification-and-privacy.md) classification labels

## Required visible states (Need → Impact)

Every tenant-facing lifecycle surface that claims to show an Allocation MUST make the current stage explicit with a **text label** (not color alone). Required labels and when they apply:

| Stage / projection | Visible text MUST convey | Must not imply |
| --- | --- | --- |
| Need | Documented gap; not yet funded | That funds moved |
| Signal | Observation captured; source visible or reachable | Approval |
| Opportunity | Grouped Need; open / dismissed / converted | Authorization |
| Recommendation | Proposal + amount + currency; “not approved” | That allocation exists |
| Approval | Human principal + time; [ADR-006](../adr/ADR-006-human-approval.md) | That Evidence exists |
| Allocation | `allocationId` + amount + currency + stage | That Impact is verified |
| Execution | Fulfillment started | Receipt or Evidence |
| Evidence | Attached, or **waived** with actor + time ([SPEC-027](SPEC-027-impact-loop.md)) | That Verification passed |
| Receipt | Amount, currency, issuer, `allocationId` | A donation charge by AGI |
| Verification | Outcome (`verified` / `rejected` / `pending`) + verifier | That Notification equals Impact |
| Impact | Claim reconcilable to Verification + Evidence | A new lifecycle fork |
| Notification | Delivery attempt; not consent | That the donor was emailed if no contact exists |
| ImpactNotice | Use summary + same Donation Link CTA, or **not shown** when no contactable identity | Invented PII or AGI checkout |

`MISSING_PROOF` is an inbox/exception state ([SPEC-026](SPEC-026-donation-source-connectors.md)). It is not a waive. Surfaces MUST NOT label `MISSING_PROOF` as waived.

## Traceability (reviewer-testable)

A user on a tenant surface MUST be able to walk this chain without hidden client-only state:

```text
Impact → Verification → Evidence (or recorded waive)
      → Allocation → Approval → Recommendation
      → pot / gift summary (chargeId) when the Allocation is funded from tracked gifts
```

1. Every Impact statement MUST name or link `allocationId` and the Verification (and thereby Evidence or waive) that supports it ([SPEC-018](SPEC-018-evidence-integrity-and-provenance.md)).
2. Every Allocation row MUST show `allocationId` as copyable text.
3. When the Allocation is attributable to a pot, the pot identity and remaining available (credited − allocated) MUST be reachable from that row ([SPEC-023](SPEC-023-financial-ledger-invariants.md)). Gift summaries use connector `chargeId`, not a Stripe charge.
4. Public and donor surfaces MAY shorten the chain to aggregate-safe fields ([CONTRACT-012](../contracts/CONTRACT-012-public-projection.md), [CONTRACT-007](../contracts/CONTRACT-007-timeline-event.md)) but MUST NOT invent missing links.
5. Demo and screenshots MUST use synthetic identifiers only ([SPEC-011](SPEC-011-demo-specification.md)).

## Accessibility of state

6. Approval, Allocation, Evidence, Verification, waive, and ImpactNotice eligibility MUST NOT be communicated by color alone. A text label (and, where an icon is used, the same text) is required.
7. Identifiers and amounts MUST be distinguishable and copyable. Do not truncate `allocationId` or `chargeId` to an unrecoverable fragment on audit surfaces.
8. Motion, if any, MUST preserve temporal order and MUST respect reduced-motion preferences. Motion MUST NOT be the only indication that Approval occurred.
9. Contrast and focus are implementation concerns; the information requirement is that state remains readable as text when color and motion are removed.

## Surfaces and classification ([SPEC-017](SPEC-017-data-classification-and-privacy.md))

| Surface | Default labels allowed | Must not show |
| --- | --- | --- |
| **Tenant** (operators, directors) | `tenant` fields: amounts, `allocationId`, pot balances, exception codes, Approval actor | Other tenants’ data; raw webhook secrets |
| **Public** | `public` TimelineEvent / CONTRACT-012 aggregate only | `pii`, `restricted`, private evidence URLs, donor identity |
| **Donor** (ImpactNotice or donor-facing page) | Use summary + outbound Donation Link; channel resolved from opt-in contact | Invented email; other donors’ gifts; service credentials |

10. Donor personal identifiers SHALL NOT be required on Allocation, Evidence, Receipt, or Recommendation displays.
11. Public impact narratives MUST NOT reveal donor identity unless the donor granted publicity consent (tracked outside core lifecycle contracts).
12. `sensitive-financial` payment-instrument data is out of band. AGI does not take donation cards ([ADR-015](../adr/ADR-015-donation-tracking-money-boundary.md)).

## Donation CTA

13. The donate call-to-action on tenant pages and on ImpactNotice MUST be the tenant outbound `donation_link` (Donation Link). It MUST be an HTTPS URL to the tenant’s own receiver.
14. Surfaces MUST NOT present AGI-hosted checkout, a Stripe Checkout Session, or a “pay with Stripe” control as a donation path.
15. If `donation_link` is missing, omit the CTA. MUST NOT invent a URL.

## ImpactNotice content

16. When an ImpactNotice is shown or sent, required visible meaning is: what the money was used for (`useSummary`) and the same Donation Link CTA ([CONTRACT-013](../contracts/CONTRACT-013-impact-notice.md), [SPEC-027](SPEC-027-impact-loop.md)).
17. ImpactNotice MUST NOT include donor email, name, or phone in the payload or in a public transcript.
18. If the connector omitted contactable identity, surfaces MUST NOT show a “notice sent” state and MUST NOT invent an address. Skip is the correct design.

## Diagram and documentation formatting (this repository)

19. Diagrams that explain lifecycle or capabilities MUST use editable source (Mermaid under `diagrams/` or fenced `text` trees). Do not commit opaque diagram-only binaries as the sole explanation.
20. Diagrams MUST use glossary terms (Need, Signal, Allocation, Evidence, ImpactNotice) and MUST NOT draw a fifth capability or AGI checkout.
21. Specifications MUST use stable identifiers, a purpose / scope / requirements / non-goals structure, tables for ownership or field rules, and RFC 2119 keywords in requirements ([SPEC-010](SPEC-010-documentation-standard.md), [docs/standards.md](../docs/standards.md)).
22. Color in diagrams MAY reinforce grouping. State transitions in diagrams MUST also be named in text.

## Component naming (when products build UI)

23. If an implementation names UI units, it SHOULD name them by domain role (`AllocationTimeline`, `EvidenceRecord`, `ImpactNoticeCard`), not by appearance (`BlueCard`, `PrettyBadge`). This repository does not ship those components.

## Reviewer checklist

A design or implementation review PASSES this specification when:

- [ ] Each required state in the table has a text label on the tenant surface that shows that Allocation
- [ ] Impact can be walked to Evidence (or waive) and Allocation without a hidden store
- [ ] Allocation can be walked to pot / `chargeId` when funded from tracked gifts
- [ ] Color-only state is absent for Approval, Evidence, Verification, and ImpactNotice
- [ ] Donate CTA is `donation_link` or omitted; no AGI checkout
- [ ] ImpactNotice (if any) has use summary + same CTA and no invented PII
- [ ] Public surface has no `pii` / private evidence URL

## Rationale

Audit visibility is a platform property. A component library would rot in this repository and would violate “no application code.” Information requirements can be tested on any host.

## References

- [design-system/README.md](../design-system/README.md) — short restatement
- [SPEC-005](SPEC-005-lifecycle.md), [SPEC-011](SPEC-011-demo-specification.md), [SPEC-017](SPEC-017-data-classification-and-privacy.md), [SPEC-027](SPEC-027-impact-loop.md)
