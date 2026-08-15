---
id: SPEC-006
title: Capability Boundaries
version: 1.2.0
status: accepted
authority: normative
owner: Platform Architecture
related_specs:
- SPEC-002
- SPEC-002A
- SPEC-005
- SPEC-020
related_adrs:
- ADR-010
- ADR-015
related_contracts:
- CONTRACT-001
- CONTRACT-002
- CONTRACT-003
- CONTRACT-004
- CONTRACT-005
- CONTRACT-006
- CONTRACT-007
- CONTRACT-013
---

# SPEC-006: Capability Boundaries
| Version | 1.2.0 | Owner | Platform Architecture | Status | Accepted |
| --- | --- | --- | --- | --- | --- |
| Dependencies | SPEC-002, SPEC-002A, SPEC-005 | Related ADRs | ADR-010 | Related contracts | CONTRACT-001–007, CONTRACT-013 |

## Purpose
Assign ecosystem **capability** responsibilities without prescribing deployment topology.

## Scope
Fund Intel, Autonomous Giving, Impact Relay, and future capabilities. Logical architecture only.

## Capabilities (not deployables)

| Capability | Responsibility | Must not |
| --- | --- | --- |
| **Fund Intel** | Observe, normalize, recommend; ingest gift summaries and credit pots | Allocate or grant Approval |
| **Autonomous Giving** | Govern, approve, allocate, execute authorized fulfillment | Fabricate Evidence or Verification |
| **Impact Relay** | Collect evidence, verify, project timeline, notify (including ImpactNotice) | Edit authoritative history or allocate |

These are **logical** boundaries. They MAY execute inside one process (modules in a modular monolith) or across many processes. Deployment choice does not change ownership of contracts or events.

## Requirements
1. Fund Intel observes, normalizes, recommends, and credits gift summaries only.
2. Autonomous Giving governs, approves, and allocates only.
3. Impact Relay collects evidence, verifies, and notifies only (including ImpactNotice).
4. There is no fifth capability for payments or checkout. AGI does not process donations ([ADR-015](../adr/ADR-015-donation-tracking-money-boundary.md)).
5. Cross-capability data exchange uses versioned contracts and events, whether invoked as a function call or over a network.
6. Capability boundaries SHALL NOT be read as requirements for separate repositories, containers, databases, or orchestrators.

## Non-goals
Repository layout of product monorepos, network topology, container orchestration, and operational ownership of hosting are excluded. See [SPEC-020](SPEC-020-reference-deployment-profiles.md) for informative deployment profiles.
