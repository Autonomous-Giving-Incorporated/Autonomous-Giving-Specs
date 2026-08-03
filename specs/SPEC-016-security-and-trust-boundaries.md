---
id: SPEC-016
title: Security and Trust Boundaries
version: 1.0.0
status: proposed
authority: normative
owner: Platform Architecture
related_specs:
- SPEC-002
- SPEC-006
- SPEC-017
- SPEC-018
- SPEC-019
related_adrs:
- ADR-004
- ADR-006
- ADR-007
related_contracts:
- CONTRACT-003
- CONTRACT-004
- CONTRACT-005
- CONTRACT-006
---

# SPEC-016: Security and Trust Boundaries
| Version | 1.0.0 | Owner | Platform Architecture | Status | Proposed |
| --- | --- | --- | --- | --- | --- |
| Dependencies | SPEC-002, SPEC-006 | Related ADRs | ADR-004, ADR-006, ADR-007 | Related contracts | CONTRACT-003–006 |

## Purpose
Define shared trust boundaries so implementations do not invent incompatible security controls at platform edges.

## Scope
Logical trust domains for Fund Intel (intelligence), Autonomous Giving (governance and allocation), Impact Relay (evidence and transparency), and external parties (donors, organizations, verifiers, channel adapters).

## Trust domains

| Domain | Trust posture | Must not |
| --- | --- | --- |
| Intelligence | Observes and recommends | Allocate funds or mint Approval |
| Governance | Authorizes allocation | Fabricate Evidence or Verification |
| Execution | Fulfils authorized Allocation | Bypass Approval or rewrite Receipt history |
| Evidence | Attests and verifies | Edit prior Evidence or Receipt records |
| Transparency | Projects TimelineEvent and Notification | Mutate authoritative lifecycle history |
| External donor | Views permitted projections | Access other donors’ private identity linkage without authorization |
| External organization | Supplies Need and operational evidence | Self-approve Allocation |

## Requirements
1. Each service boundary in [SPEC-006](SPEC-006-service-boundaries.md) is a trust boundary: cross-boundary data moves only through versioned contracts and events.
2. Authentication and authorization decisions SHALL be attributable to a principal (human or service identity) per [SPEC-019](SPEC-019-identity-and-authorization.md).
3. Human Approval remains a hard gate before Allocation for the MVP ([ADR-006](../adr/ADR-006-human-approval.md)).
4. Audit-relevant actions (approval, allocation, verification, receipt issuance) SHALL emit durable events suitable for independent review.
5. Implementations SHALL assume hostile or compromised peers outside their trust domain and MUST validate inbound payloads against pinned schemas.
6. Secrets, credentials, and signing keys NEVER appear in contract payloads, events, demo fixtures, or this repository.
7. Public projections (TimelineEvent, Notification content) SHALL apply data classification and redaction rules from [SPEC-017](SPEC-017-data-classification-and-privacy.md).
8. Threat assumptions for the platform MVP include: forged events without authz, replay of stale approvals, evidence substitution, notification leakage, and confused-deputy calls across services. Mitigations are schema validation, authz checks, idempotent `eventId`, append-only evidence, and least-privilege service roles.

## Trust-boundary diagram (logical)

```text
[External sources] -> (Intelligence) -> Recommendation
                              |
                              v
                         (Governance) --Approval--> Allocation/Execution
                              |                         |
                              v                         v
                         audit events            Receipt + operational data
                                                       |
                                                       v
                                                  (Evidence) --> Verification
                                                       |
                                                       v
                                                 (Transparency) --> Notification
```

## Non-goals
This specification does not mandate a particular IdP, KMS, network mesh, or cloud provider. It does not replace product threat models for each implementation repository.
