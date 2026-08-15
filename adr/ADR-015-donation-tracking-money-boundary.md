---
id: ADR-015
version: 1.0.0
authority: normative
owner: Platform Architecture
date: '2026-08-15'
title: Donation Tracking versus Tenant Billing
status: accepted
related_specs:
- SPEC-006
- SPEC-023
- SPEC-024
- SPEC-026
- SPEC-027
---

# ADR-015: Donation Tracking versus Tenant Billing

| Status | Accepted |
| --- | --- |
| Date | 2026-08-15 |
| Related specs | SPEC-006, SPEC-023, SPEC-024, SPEC-026, SPEC-027 |

## Context

SPEC-023 v1 and SPEC-024 v1.1 described Stripe as the donation/payment processor and stated that AGI “handles money movement adjacent to processors.” That model contradicts the locked product (owner, 2026-08-15 PT):

- AGI never processes donations. It tracks gifts completed on third-party donation platforms.
- The canonical inbound connector is every.org gift-completed webhooks. CSV import is the offline twin. P1 later: Givebutter and Donorbox behind the same adapter.
- Stripe MAY exist only for tenant/SaaS billing (tenants paying AGI).
- Tenant pages MAY show outbound donation links to the tenant’s own receiver. AGI does not host checkout.
- The loop is: donate on third party → webhook gift summary → pot credit → human allocate → attach Evidence → ImpactNotice → CTA back to the same outbound donation link.

[ADR-013](ADR-013-cloudflare-workers-public-host.md) remains the preferred host (Cloudflare Workers + Supabase). Its residual “Stripe — payment processing, if the product still requires card/processor flows” line is **refined** by this ADR: those flows are tenant billing only, never donation capture. [ADR-012](ADR-012-render-first-platform.md) stays superseded.

An informative pot-hierarchy design already exists ([allocation middleware design](../docs/superpowers/specs/2026-08-03-allocation-middleware-design.md)). This ADR does not replace that design; it freezes the money boundary so SPECs cannot reintroduce AGI checkout.

## Decision

1. **Donations are tracked, not processed.** Gift summaries arrive through donation-source connectors ([SPEC-026](../specs/SPEC-026-donation-source-connectors.md)). AGI MUST NOT capture, charge, refund, or host checkout for donations.
2. **every.org is the P0 connector.** Givebutter and Donorbox are P1 behind the same adapter. CSV import uses the same normalize/idempotency path.
3. **Stripe is tenant billing only.** Stripe webhooks MUST NOT credit pots or create donation allocations. Absence of Stripe does not block the donation-tracking product.
4. **`donation_link` is an outbound URL on the tenant record**, not a Checkout Session. After Evidence (or explicit human waive), ImpactNotice CTA is that same URL ([SPEC-027](../specs/SPEC-027-impact-loop.md)).
5. **Capability split is unchanged.** Fund Intel observes and credits gift summaries. Autonomous Giving allocates under human Approval ([ADR-006](ADR-006-human-approval.md)). Impact Relay attaches Evidence and notifies. No fifth capability.
6. **Donor PII is opt-in from the connector.** If omitted, no ImpactNotice and no invented email.

## Consequences

- SPEC-023 v2.0.0 is a tracking ledger: connector gift state ≠ pot credit ≠ allocation ≠ Evidence. Stripe donation lifecycle text is withdrawn.
- SPEC-024 preferred integrations list every.org first; Stripe is billing-only; Resend (or equivalent) and `push` serve ImpactNotice.
- Implementers treat the OBSERVED Portfolio-Signals Worker (`/webhooks/every-org`, `am_*` tables) as the tracking core, not as a payment processor and not as a live production receipt.
- PCI scope for donations is not AGI’s: cards stay on the third-party receiver. Stripe PCI notes apply only if tenants are charged for SaaS.
- Historical Render/Fly/Railway host files in product repos remain non-canonical ([ADR-013](ADR-013-cloudflare-workers-public-host.md)).

## Alternatives considered

| Alternative | Why not |
| --- | --- |
| AGI hosts Stripe Checkout for donations | Owner lock: AGI never processes donations |
| Stripe as a donation-source connector | Would reintroduce processor adjacency and checkout temptation |
| Keep SPEC-023 v1 and “fix in product only” | Implementers would keep building the wrong money path |
| Fifth “payments” capability | Constitution and SPEC-006 allow three capabilities; tracking fits Fund Intel / Autonomous Giving / Impact Relay |

## Status

**Accepted** (2026-08-15). Refines ADR-013 externals for money movement. Does not supersede ADR-013’s host decision. Does not supersede ADR-006.
