---
id: SPEC-006
title: Capability Boundaries
version: 1.3.0
status: accepted
authority: normative
owner: Platform Architecture
related_specs:
- SPEC-002
- SPEC-002A
- SPEC-005
- SPEC-020
- SPEC-029
- SPEC-030
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
| Version | 1.3.0 | Owner | Platform Architecture | Status | Accepted |
| --- | --- | --- | --- | --- | --- |
| Dependencies | SPEC-002, SPEC-002A, SPEC-005 | Related ADRs | ADR-010 | Related contracts | CONTRACT-001–007, CONTRACT-013 |

## Purpose
Assign ecosystem **capability** responsibilities without prescribing deployment topology.

## Scope
Fund Intel, Autonomous Giving, Impact Relay, and future capabilities. Logical architecture only.

## Capabilities (not deployables)

| Capability | Responsibility | Must not |
| --- | --- | --- |
| **Fund Intel** | Observe, normalize, produce Signals, group Opportunities, generate advisory Recommendations, ingest valid learning feedback as new evidence-backed Signals, and credit pots from gift summaries | Allocate or grant Approval |
| **Autonomous Giving** | Govern, authorize, approve, allocate, execute authorized fulfillment, operate the authenticated control plane, and project authorized cross-capability mission state | Fabricate Evidence, Verification, or downstream records |
| **Impact Relay** | Collect Evidence, generate receipts/provenance, verify Impact, project timeline/public state, issue permitted ImpactNotice, and expose verified outcome data for future intelligence | Create Recommendations, Approval, Allocation, or edit authoritative history |

These are **logical** boundaries. They MAY execute inside one process (modules in a modular monolith) or across many processes. Deployment choice does not change ownership of contracts or events.

## Requirements
1. Fund Intel observes, normalizes, produces Signals, groups Opportunities, and generates advisory Recommendations. It MAY ingest verified downstream outcomes only as provenance-bearing new Signals; it MUST NOT grant Approval or allocate resources.
2. Autonomous Giving governs, authorizes, approves, allocates, executes authorized fulfillment, and may display authorized Mission Graph and mission-intelligence projections. Projection does not transfer canonical ownership.
3. Impact Relay collects Evidence, generates receipts/provenance, verifies Impact, and notifies only (including ImpactNotice). It MAY expose verified outcome and provenance data for future Fund Intel Signals; it MUST NOT independently generate or authorize Recommendations.
4. There is no fifth capability for payments or checkout. AGI does not process donations ([ADR-015](../adr/ADR-015-donation-tracking-money-boundary.md)).
5. Cross-capability data exchange uses versioned contracts and events, whether invoked as a function call or over a network.
6. Capability boundaries SHALL NOT be read as requirements for separate repositories, containers, databases, or orchestrators.
7. Derived mission-intelligence metrics and Mission Graph traversal MUST NOT create new authority. They remain evidence-bounded projections and derived artifacts.

## Non-goals
Repository layout of product monorepos, network topology, container orchestration, and operational ownership of hosting are excluded. See [SPEC-020](SPEC-020-reference-deployment-profiles.md) for informative deployment profiles.
