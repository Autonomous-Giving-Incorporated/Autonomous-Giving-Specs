---
id: SPEC-019
title: Identity and Authorization
version: 1.3.0
status: proposed
authority: normative
owner: Platform Architecture
related_specs:
- SPEC-002A
- SPEC-006
- SPEC-016
- SPEC-017
- SPEC-024
related_adrs:
- ADR-004
- ADR-006
- ADR-012
- ADR-013
related_contracts:
- CONTRACT-003
- CONTRACT-006
---

# SPEC-019: Identity and Authorization
| Version | 1.3.0 | Owner | Platform Architecture | Status | Proposed |
| --- | --- | --- | --- | --- | --- |
| Dependencies | SPEC-002A, SPEC-006, SPEC-016 | Related ADRs | ADR-004, ADR-006, ADR-012, ADR-013 | Related contracts | CONTRACT-003, CONTRACT-006 |

## Purpose
Define identity and authorization expectations at platform trust boundaries without requiring a single vendor IAM stack for conformance. The **preferred** identity provider for new hosted-platform work is **Supabase Auth** ([SPEC-024](SPEC-024-integration-boundaries.md), [ADR-013](../adr/ADR-013-cloudflare-workers-public-host.md)). Clerk remains allowed only if a product still requires it. [ADR-012](../adr/ADR-012-render-first-platform.md) Clerk-default notes are **historical**.

## Scope
Human and workload principals that produce or consume platform events and contracts. End-user UI session design is out of scope except where it produces Approval or Notification side effects.

## Principal types

| Principal | Examples | Typical authority |
| --- | --- | --- |
| Human reviewer | Governance approver | Grant Approval |
| Workload identity | fund-intel, autonomous-giving, impact-relay module or process | Produce/consume declared contracts |
| Organization operator | Program staff | Submit Need context, operational evidence |
| Donor | Funding party | View permitted projections; consent for notifications |
| Auditor | Internal/external review | Read audit chain within entitlement |

## Identity vs authorization (preferred split)

| Concern | Owner |
| --- | --- |
| Authentication, sessions, OAuth, IdP MFA | **Supabase Auth** (preferred) or Clerk / equivalent IdP if still required |
| Authorization, roles, org membership policy, financial permissions, admin scope | **AGI application** (PostgreSQL-backed policies) |

Implementations MUST NOT treat “authenticated with IdP” as sufficient for financial or administrative actions. Map stable IdP subject identifiers (e.g. `supabase_user_id`, or `clerk_user_id` if Clerk is still required) to application principals; do **not** use mutable email as the sole foreign key for domain records ([SPEC-024](SPEC-024-integration-boundaries.md)).

## Requirements
1. Every Approval record MUST identify `approvedBy` as a human principal reference suitable for audit ([EVENT-004](../events/EVENT-004-approval-granted.md)).
2. When capability edges cross process boundaries, both parties MUST authenticate (mutual TLS, signed tokens, or equivalent). In-process module calls rely on process identity and module authorization checks.
3. Authorization is **deny by default**: a principal may only produce or consume artifacts listed in its conformance manifest and role policies.
4. Role separation follows [SPEC-006](SPEC-006-capability-boundaries.md): intelligence principals MUST NOT be authorized to create Allocation; evidence principals MUST NOT be authorized to create Approval.
5. Impersonation of human approvers by workload identities is forbidden for MVP Allocation gates.
6. Correlation identifiers in events are not authentication credentials.
7. Access to `pii` and `restricted` data requires an entitled principal and SHOULD be audit-logged ([SPEC-017](SPEC-017-data-classification-and-privacy.md)).
8. Notification channel credentials are held by channel adapters, not embedded in Notification contracts.
9. Implementations SHALL document their principal model and how it maps to platform capabilities in conformance evidence.
10. Application authorization decisions SHALL be enforceable without trusting client-supplied role claims alone; verify session with the IdP and evaluate server-side policy.

## Authorization checkpoints (minimum)

| Action | Required principal class |
| --- | --- |
| Publish Recommendation | Intelligence capability |
| Grant Approval | Human reviewer under governance |
| Create Allocation | Governance/execution capability after Approval |
| Attach Evidence | Evidence capability or entitled organization operator via evidence path |
| Complete Verification | Entitled verifier under evidence domain |
| Send Notification | Transparency/evidence capability with consent basis |

## Non-goals
This specification does not standardize OAuth grant types, enterprise SSO onboarding beyond the preferred Supabase Auth profile, Kubernetes service accounts, or service meshes. Conformance does not require Supabase Auth or Clerk; the preferred hosted path uses Supabase Auth.
