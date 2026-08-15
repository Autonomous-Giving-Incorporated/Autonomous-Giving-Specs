---
id: SPEC-014
title: Future Capabilities
version: 2.0.0
status: accepted
authority: normative
owner: Platform Architecture
related_specs:
- SPEC-002A
- SPEC-006
- SPEC-013
- SPEC-020
- SPEC-026
- SPEC-028
related_adrs:
- ADR-006
- ADR-010
- ADR-014
- ADR-015
related_contracts:
- CONTRACT-001
- CONTRACT-002
- CONTRACT-003
- CONTRACT-004
- CONTRACT-005
- CONTRACT-006
- CONTRACT-007
---

# SPEC-014: Future Capabilities
| Version | 2.0.0 | Owner | Platform Architecture | Status | Accepted |
| --- | --- | --- | --- | --- | --- |
| Dependencies | SPEC-002A, SPEC-006, SPEC-013, SPEC-028 | Related ADRs | ADR-010, ADR-014, ADR-015 | Related contracts | CONTRACT-001–007 |

## Purpose

Define admission rules for a future platform **capability** beyond Fund Intel, Autonomous Giving, and Impact Relay—so implementers do not invent a fourth capability for payments, connectors, or login.

## Scope

New logical responsibilities that would exchange platform contracts or alter lifecycle participation. Applies regardless of whether code is co-located or extracted.

## Non-goals

This does not require distributed processes, orchestrators, or a specific host. It does not admit AGI checkout.

## The three capabilities (closed set until admission)

| Capability | Observes / does | Must not |
| --- | --- | --- |
| Fund Intel | Observe, recommend, ingest gift summaries, credit pots | Allocate, approve, process donations |
| Autonomous Giving | Govern, approve, allocate, execute; **AGI control plane** ([SPEC-028](SPEC-028-agi-control-plane.md)) | Fabricate Evidence; host donation checkout |
| Impact Relay | Evidence, verification, timeline, Notification, ImpactNotice | Allocate; invent PII |

There is **no** payments/checkout capability. Tracking stays in these three ([SPEC-006](SPEC-006-capability-boundaries.md), [ADR-015](../adr/ADR-015-donation-tracking-money-boundary.md)).

## What is not a new capability

| Candidate | Classification | Why |
| --- | --- | --- |
| AGI control plane (login, session, authz, capability JWTs) | Autonomous Giving’s **edge** | [SPEC-028](SPEC-028-agi-control-plane.md), [ADR-014](../adr/ADR-014-agi-control-plane.md) |
| every.org / CSV connector | Fund Intel **adapter** | [SPEC-026](SPEC-026-donation-source-connectors.md) |
| Givebutter, Donorbox (P1) | Same SPEC-026 **adapter**, not a capability | Same normalize / verify / `chargeId` path |
| Fundraise Up, Zeffy, GoFundMe Pro (P2+) | Reserved adapters; MUST NOT block P0 | Still SPEC-026 |
| Stripe tenant/SaaS billing | External billing integration | [SPEC-024](SPEC-024-integration-boundaries.md); MUST NOT credit pots |
| Extracting Fund Intel to its own Worker | **Deployment** | [ADR-010](../adr/ADR-010-future-services.md) |
| Private integration harness | Out-of-repo verifier | Not a capability; not Specs-owned |
| Notion, Slack, or a project board | Coordination | Not architecture authority |

Extracting an existing capability into a separate deployable does **not** create a new capability. It changes deployment only ([SPEC-002A](SPEC-002A-architectural-principles.md)).

## When a fourth capability would be allowed

A new capability MAY be admitted only when **all** of the following hold:

1. It owns **one** new responsibility that is not already assigned in SPEC-006.
2. It does **not** capture, charge, refund, or host checkout for donations.
3. It does **not** take Approval, Allocation, Evidence, or Verification away from the existing owners.
4. It declares consumed and produced contracts/events, and names an owner in the known owner set.
5. An **ADR** records the admission (why the responsibility cannot live in an existing capability or adapter).
6. A **lifecycle impact assessment** states whether SPEC-005 stages change. Adding a lifecycle stage is a MAJOR platform change ([SPEC-012](SPEC-012-versioning.md), [SPEC-015](SPEC-015-compatibility-and-evolution.md)).
7. New cross-boundary contracts, if any, land with schemas, examples, and a SPEC amendment in the same change.
8. Conformance ([SPEC-013](SPEC-013-repository-conformance.md)) remains topology-agnostic. Preferred host stays [ADR-013](../adr/ADR-013-cloudflare-workers-public-host.md) unless a superseding ADR says otherwise.

## When a fourth capability is forbidden

9. A “payments,” “checkout,” “Stripe donations,” or “processor adjacency” capability — **forbidden**. Donations are tracked via SPEC-026 adapters.
10. A “Fund Intel 2” that allocates — **forbidden**. Intelligence never allocates ([ADR-006](../adr/ADR-006-human-approval.md)).
11. A second control plane or competing login that splits `client_id` / `tenant_id` — **forbidden** without superseding ADR-014.
12. Treating P1/P2 connectors as capabilities — **forbidden**.
13. Treating the control plane as a fourth capability — **forbidden**.
14. Inventing a capability to hold secrets, Wrangler config, or the private harness in this repository — **forbidden**.

## Required artifacts for an admission proposal

| Artifact | Required |
| --- | --- |
| ADR (Nygard) | Yes — context, decision, consequences, alternatives |
| SPEC-006 amendment | Yes — new row in the capability table |
| SPEC-014 checklist below | Yes — completed in the proposing PR |
| New CONTRACTs + schemas + examples | If the capability exchanges new cross-boundary data |
| Lifecycle assessment | Yes — no silent SPEC-005 change |
| Glossary terms | If a new TERM is required ([SPEC-004](SPEC-004-domain-model.md)) |
| RFC | When [docs/rfc-process.md](../docs/rfc-process.md) thresholds apply |

## Acceptance checklist (reviewer-testable)

A proposal is complete enough to review when:

- [ ] Responsibility statement is one sentence and does not overlap SPEC-006 “must not” rows
- [ ] Explicitly not a payments/checkout capability
- [ ] P1 connectors, if mentioned, are adapters under SPEC-026
- [ ] Control plane, if mentioned, remains Autonomous Giving’s edge (SPEC-028)
- [ ] Extraction vs capability is distinguished
- [ ] ADR + lifecycle impact + contract list are attached
- [ ] No invented live URLs, READY marks, or deployables in this repo
- [ ] `python3 validation/validate_all.py` still PASSes

## Rationale

The constitution allows three capabilities. Pressure to add a fourth usually means “we need checkout” or “we need another login.” Those are product mistakes, not admission candidates. Adapters and edges keep the set closed without blocking Givebutter or Cloudflare topology.

## References

- [SPEC-006](SPEC-006-capability-boundaries.md), [SPEC-028](SPEC-028-agi-control-plane.md), [ADR-010](../adr/ADR-010-future-services.md), [ADR-015](../adr/ADR-015-donation-tracking-money-boundary.md)
