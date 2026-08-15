---
id: SPEC-016
title: Security and Trust Boundaries
version: 1.4.0
status: accepted
authority: normative
owner: Platform Architecture
related_specs:
- SPEC-002
- SPEC-006
- SPEC-017
- SPEC-018
- SPEC-019
- SPEC-023
- SPEC-024
- SPEC-025
- SPEC-028
related_adrs:
- ADR-004
- ADR-006
- ADR-007
- ADR-012
- ADR-013
- ADR-014
- ADR-015
related_contracts:
- CONTRACT-003
- CONTRACT-004
- CONTRACT-005
- CONTRACT-006
- CONTRACT-008
---

# SPEC-016: Security and Trust Boundaries
| Version | 1.4.0 | Owner | Platform Architecture | Status | Accepted |
| --- | --- | --- | --- | --- | --- |
| Dependencies | SPEC-002, SPEC-006, SPEC-019, SPEC-028 | Related ADRs | ADR-004, ADR-006, ADR-007, ADR-013, ADR-014, ADR-015 | Related contracts | CONTRACT-003–006, CONTRACT-008 |

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
1. Each **capability** boundary in [SPEC-006](SPEC-006-capability-boundaries.md) is a trust boundary: cross-boundary data moves only through versioned contracts and events (including in-process module calls).
2. Authentication and authorization decisions SHALL be attributable to a principal (human or workload identity) per [SPEC-019](SPEC-019-identity-and-authorization.md).
3. Human Approval remains a hard gate before Allocation for the MVP ([ADR-006](../adr/ADR-006-human-approval.md)).
4. Audit-relevant actions (approval, allocation, verification, receipt issuance) SHALL emit durable events suitable for independent review.
5. Implementations SHALL assume hostile or compromised peers outside their trust domain and MUST validate inbound payloads against pinned schemas. In a modular monolith, module boundaries still enforce validation at capability edges.
6. Secrets, credentials, and signing keys NEVER appear in contract payloads, events, demo fixtures, or this repository.
7. Public projections (TimelineEvent, Notification content) SHALL apply data classification and redaction rules from [SPEC-017](SPEC-017-data-classification-and-privacy.md).
8. Threat assumptions for the platform MVP include: forged events without authz, replay of stale approvals, evidence substitution, notification leakage, and confused-deputy calls across capabilities. Mitigations are schema validation, authz checks, idempotent `eventId`, append-only evidence, and least-privilege roles. Network-level controls apply only when deployment separates processes.
9. Inbound donation-source and identity webhooks MUST verify provider signatures (or shared secrets) before side effects; gift-summary application MUST follow [SPEC-023](SPEC-023-financial-ledger-invariants.md) idempotency rules. Stripe webhooks, if present, are tenant-billing only ([ADR-015](../adr/ADR-015-donation-tracking-money-boundary.md)).
10. Secrets (API keys, webhook secrets, database credentials) MUST live in environment/secret stores, never in contracts, fixtures, client bundles intended to be private, or this repository.
11. SQL access MUST use parameterized queries or an ORM that parameterizes; string-concatenated SQL with untrusted input is forbidden.
12. AGI does not take donation cards. Using Stripe for **tenant/SaaS billing** reduces card-data handling scope when card data remains with Stripe; implementations MUST NOT claim PCI compliance solely because Stripe is integrated. Document residual responsibilities for keys, webhooks, and server surfaces ([SPEC-024](SPEC-024-integration-boundaries.md)).
13. AI/agent tools MUST NOT hold unconstrained authority to move money; financial actions require deterministic application gates or authorized human/system actors ([SPEC-023](SPEC-023-financial-ledger-invariants.md)).
14. Production database access SHOULD be least-privilege, authenticated, and auditable. Backup and recovery expectations for the preferred path are in [SPEC-025](SPEC-025-operations-deploy-and-scale.md).
15. At capability edges, inbound AGI control-plane context MUST be verified before financial or administrative side effects: issuer, signature (published JWKS), audience, expiry, `client_id` / `tenant_id` equality and authorization, project scope when required, and requested capability ([SPEC-028](SPEC-028-agi-control-plane.md), [CONTRACT-008](../contracts/CONTRACT-008-auth-context.md), [ADR-014](../adr/ADR-014-agi-control-plane.md)). Unverified context is deny-by-default.
16. Donation-source connector webhooks MUST verify provider signatures or shared secrets before side effects (requirement 9). That webhook verify is independent of CONTRACT-008: a valid capability JWT does not replace connector signature checks, and a valid connector signature does not replace capability-edge token verification.

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

## Preferred deployment security notes (informative)

When following [ADR-013](../adr/ADR-013-cloudflare-workers-public-host.md): Cloudflare hosts Workers / Pages / static assets (Durable Objects and Queues/Cron Triggers only as needed); Supabase provides Auth, PostgreSQL, and Storage; AGI authorizes; every.org (or the CSV twin) is the donation-source connector; Stripe processes **tenant billing** only if tenants are charged ([ADR-015](../adr/ADR-015-donation-tracking-money-boundary.md)); Resend delivers email if still required. Clerk authenticates only if a product still requires it. CSRF/XSS mitigations follow Next.js and framework defaults plus secure cookie/session practices from the IdP. Rate limiting SHOULD protect auth and webhook endpoints as practical. [ADR-012](../adr/ADR-012-render-first-platform.md) Render hosting notes are **historical**.

## Non-goals
This specification does not mandate a particular IdP, KMS, network mesh, service mesh, Kubernetes, or cloud provider for conformance. It does not replace product threat models for each implementation repository.
