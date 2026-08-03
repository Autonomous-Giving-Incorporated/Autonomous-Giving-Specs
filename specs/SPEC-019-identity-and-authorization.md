---
id: SPEC-019
title: Identity and Authorization
version: 1.0.0
status: proposed
authority: normative
owner: Platform Architecture
related_specs:
- SPEC-006
- SPEC-016
- SPEC-017
related_adrs:
- ADR-004
- ADR-006
related_contracts:
- CONTRACT-003
- CONTRACT-006
---

# SPEC-019: Identity and Authorization
| Version | 1.0.0 | Owner | Platform Architecture | Status | Proposed |
| --- | --- | --- | --- | --- | --- |
| Dependencies | SPEC-006, SPEC-016 | Related ADRs | ADR-004, ADR-006 | Related contracts | CONTRACT-003, CONTRACT-006 |

## Purpose
Define identity and authorization expectations at platform trust boundaries without prescribing a single vendor IAM stack.

## Scope
Human and service principals that produce or consume platform events and contracts. End-user UI session design is out of scope except where it produces Approval or Notification side effects.

## Principal types

| Principal | Examples | Typical authority |
| --- | --- | --- |
| Human reviewer | Governance approver | Grant Approval |
| Service identity | fund-intel, autonomous-giving, impact-relay | Produce/consume declared contracts |
| Organization operator | Program staff | Submit Need context, operational evidence |
| Donor | Funding party | View permitted projections; consent for notifications |
| Auditor | Internal/external review | Read audit chain within entitlement |

## Requirements
1. Every Approval record MUST identify `approvedBy` as a human principal reference suitable for audit ([EVENT-004](../events/EVENT-004-approval-granted.md)).
2. Service-to-service calls across trust boundaries MUST authenticate both parties (mutual TLS, signed tokens, or equivalent).
3. Authorization is **deny by default**: a principal may only produce or consume artifacts listed in its conformance manifest and role policies.
4. Role separation follows [SPEC-006](SPEC-006-service-boundaries.md): intelligence principals MUST NOT be authorized to create Allocation; evidence principals MUST NOT be authorized to create Approval.
5. Impersonation of human approvers by service identities is forbidden for MVP Allocation gates.
6. Correlation identifiers in events are not authentication credentials.
7. Access to `pii` and `restricted` data requires an entitled principal and SHOULD be audit-logged ([SPEC-017](SPEC-017-data-classification-and-privacy.md)).
8. Notification channel credentials are held by channel adapters, not embedded in Notification contracts.
9. Implementations SHALL document their principal model and how it maps to platform roles in conformance evidence.

## Authorization checkpoints (minimum)

| Action | Required principal class |
| --- | --- |
| Publish Recommendation | Intelligence service |
| Grant Approval | Human reviewer under governance |
| Create Allocation | Governance/execution service after Approval |
| Attach Evidence | Evidence service or entitled organization operator via evidence service |
| Complete Verification | Entitled verifier under evidence domain |
| Send Notification | Transparency/evidence service with consent basis |

## Non-goals
This specification does not standardize OAuth grant types, RBAC product configuration, or enterprise SSO onboarding flows.
