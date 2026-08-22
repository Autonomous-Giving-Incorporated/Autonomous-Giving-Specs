---
id: SPEC-026
title: Donation-source Connectors
version: 1.1.0
status: accepted
authority: normative
owner: Fund Intel
related_specs:
- SPEC-006
- SPEC-017
- SPEC-022
- SPEC-023
- SPEC-024
- SPEC-027
related_adrs:
- ADR-006
- ADR-013
- ADR-015
related_contracts:
- CONTRACT-003
- CONTRACT-013
---

# SPEC-026: Donation-source Connectors
| Version | 1.1.0 | Owner | Fund Intel | Status | Accepted |
| --- | --- | --- | --- | --- | --- |
| Dependencies | SPEC-006, SPEC-023, SPEC-024, SPEC-027 | Related ADRs | ADR-006, ADR-013, ADR-015 | Related contracts | CONTRACT-003, CONTRACT-013 |

## Purpose

Define the inbound adapter so implementations can ingest gift summaries from third-party donation platforms, credit pots, and raise exceptions—without AGI checkout or a fifth capability.

Version **1.1.0** is a MINOR amendment ([SPEC-012](SPEC-012-versioning.md)): it adds tenant onboarding fields and P1 Givebutter / Donorbox mappings behind the same adapter. It does not change ledger invariants ([SPEC-023](SPEC-023-financial-ledger-invariants.md)) and does not add exception codes.

Implementer specify → plan → tasks for later runtime work live in [specs/slices/026-p1-connectors/](slices/026-p1-connectors/spec.md). Those files are informative. This specification remains the normative authority. This repository MUST NOT implement Workers or claim READY.

## Scope

Connector adapter, verification, raw-payload persistence, idempotent `chargeId`, default `netAmount` credit, pot/slice auto-create, exception codes, CSV import, tenant onboarding fields (`source`, `donation_link`, webhook secret), and P1 source mappings. Aligns with the informative [allocation middleware design](../docs/superpowers/specs/2026-08-03-allocation-middleware-design.md). Observed Worker/`am_*` shapes are cited as **OBSERVED** repo artifacts, not as a live production receipt.

## Evidence labels

| Label | Meaning |
| --- | --- |
| **OBSERVED** | Fact recorded from a cited public vendor document (retrieved 2026-08-22) or from Portfolio-Signals artifacts already cited in this specification. This session did not inspect a live Cloudflare dashboard, live webhook, or live AGI Postgres. |
| **INFERRED** | Mapping or behavior that follows from an OBSERVED field or rule but is not named in this repository or in the cited vendor sample as the product field. |
| **SPECULATIVE** | Possible design that is not evidenced. Implementations MUST NOT treat it as required. |
| **NOT_COMPUTABLE** | Cannot be determined from evidence in this repository or the cited public docs. |

Vendor field names that are not already recorded in this repository are labeled **INFERRED** at the product-mapping edge even when the vendor document is OBSERVED. Implementers MUST re-read current vendor documentation at implement time.

## Capability split

| Step | Capability |
| --- | --- |
| Verify, normalize, persist, credit pot | Fund Intel (observe) |
| Human allocate against available | Autonomous Giving |
| Attach Evidence, notify | Impact Relay |

Intelligence never allocates ([ADR-006](../adr/ADR-006-human-approval.md)).

## Adapter

Implementations SHALL expose one adapter boundary for every donation source:

```text
normalize_gift(payload) → gift summary
list_campaign_hints(payload) → fundraiser / designation keys
verify_webhook(request) → accept | reject
```

Do not add a fourth or fifth function to this boundary. Do not add a fifth capability.

| Rule | Requirement |
| --- | --- |
| P0 | **every.org** gift-completed webhooks |
| Offline twin | CSV import through the same normalize + idempotency path |
| P1 | Givebutter, Donorbox, same adapter |
| P2+ | Fundraise Up, Zeffy, GoFundMe Pro — reserved; MUST NOT block P0 or P1 |
| Checkout | AGI MUST NOT host checkout or invent a processor session to replace a connector |
| Source values | `every.org` (P0), `givebutter` (P1), `donorbox` (P1), `csv` (offline twin) |

OBSERVED product module names (`normalizeEveryOrgDonation`, `parseGiftCsv`) MAY realize this boundary. The constant `every.org` is the P0 `source` value.

## Tenant onboarding

These rules apply to a tenant that already has a public fundraiser on a third-party receiver. Numbered requirements 17–24 appear after Donor PII.

- Operators MUST be able to record an outbound `donation_link` that is an HTTPS URL on the tenant’s own receiver ([SPEC-024](SPEC-024-integration-boundaries.md), [TERM-029](../glossary/README.md)).
- A missing `donation_link` is allowed. If the tenant has no `donation_link`, ImpactNotice MUST NOT emit and implementations MUST NOT invent a URL ([SPEC-027](SPEC-027-impact-loop.md)).
- Operators MUST choose exactly one `source` from `every.org`, `givebutter`, `donorbox`, or `csv`.
- Operators MUST point the vendor webhook at AGI’s operator-owned Worker path. Specs MUST NOT invent a `workers.dev` URL or a named-host URL. Live pointing remains operator-owned.

## every.org field mapping

| every.org field | Product mapping |
| --- | --- |
| `fromFundraiser` (title, slug, or id) | Campaign pot (parent); else **General** |
| `designation` | Program slice (child); else **Undesignated** under parent |
| `chargeId` | Gift summary id (idempotent) |
| `netAmount` | Default credit to slice; roll up to campaign |
| `amount` | Secondary display (gross) |
| `currency` | MUST match org default or raise `CURRENCY_MISMATCH` |
| `donationDate` | Gift `donatedAt`; if omitted, server time MAY be used |
| Donor name/email | Opt-in only; not required to credit; MUST NOT be invented |

## Givebutter field mapping (P1)

**OBSERVED** from the Givebutter Help Center article [How to automate workflows and data using webhooks](https://help.givebutter.com/en/articles/8828428-how-to-automate-workflows-and-data-using-webhooks) (retrieved 2026-08-22; article dated 16 June 2026). **Not** OBSERVED from a live payload or from code in this repository.

Credit only `transaction.succeeded`. Givebutter documents that this event does not fire during Givebutter CSV imports.

| Givebutter field (OBSERVED in public sample) | Product mapping | Label |
| --- | --- | --- |
| `data.id` | `chargeId` | OBSERVED field; product mapping INFERRED |
| `data.donated` | `netAmount` | OBSERVED field; product mapping INFERRED (no vendor field named `net`) |
| `data.payout` | Fallback `netAmount` if `donated` is absent | INFERRED |
| `data.amount` | Secondary display (gross) | OBSERVED field; product mapping INFERRED |
| `data.campaign_code` | Campaign pot key (preferred when present) | OBSERVED field; product mapping INFERRED |
| `data.campaign_id` | Campaign pot key if `campaign_code` is absent | OBSERVED field; product mapping INFERRED |
| `data.fund_code` / `data.fund_id` | Program slice if present; else **Undesignated** | INFERRED |
| `data.currency` | MUST match org default or raise `CURRENCY_MISMATCH` | OBSERVED field |
| `data.transacted_at` | Gift `donatedAt`; if omitted, server time MAY be used | OBSERVED field; product mapping INFERRED |
| `data.email` | Contactable identity **only** when `data.communication_opt_in` is true | OBSERVED fields |
| `data.first_name` / `data.last_name` | Opt-in display only with communication opt-in; MUST NOT be invented | OBSERVED fields |

If `donated` and `payout` are both absent, `netAmount` is **NOT_COMPUTABLE**. Do not invent a net. Open `SYNC_FAILURE` and do not credit.

## Donorbox field mapping (P1)

**OBSERVED** from Donorbox Help articles *Custom Webhooks* and *Verify Donorbox webhook notifications* (retrieved 2026-08-22). **Not** OBSERVED from a live payload or from code in this repository.

Credit only `donation.created`. Prefer payload version v2 when the operator can choose it (v2 includes `event_name`). v1 array samples remain acceptable if they still carry donation `id`.

Donorbox custom webhooks require the **API & Zapier** add-on or the **Premium** plan (**OBSERVED** from that Custom Webhooks article). Tenants without that add-on MUST use the CSV twin.

| Donorbox field (OBSERVED in public sample) | Product mapping | Label |
| --- | --- | --- |
| donation `id` | `chargeId` | OBSERVED field; product mapping INFERRED |
| `amount` | Gross display; see net rule below | OBSERVED field |
| `processing_fee` | Used only in the INFERRED net rule | OBSERVED field |
| `campaign.id` / `campaign.name` | Campaign pot | OBSERVED fields; product mapping INFERRED |
| `designation` | Program slice; else **Undesignated** | OBSERVED field; mapping INFERRED as the every.org analog |
| `currency` | MUST match org default or raise `CURRENCY_MISMATCH` | OBSERVED field |
| `donation_date` | Gift `donatedAt`; if omitted, server time MAY be used | OBSERVED field; product mapping INFERRED |
| `donor.email` | Contactable identity **only** when `join_mailing_list` is true | OBSERVED fields; opt-in mapping INFERRED |
| `donor.name` / first / last | Opt-in display only with mailing-list opt-in; MUST NOT be invented | OBSERVED fields |
| `stripe_charge_id` | MUST NOT be `chargeId` | OBSERVED field; processor id, not the donation id |

Net rule for Donorbox:

1. No vendor field named `net` or `netAmount` is OBSERVED in the public samples.
2. If `processing_fee` is present and numeric, **INFERRED** `netAmount` = `amount` − `processing_fee`.
3. If `processing_fee` is absent, **INFERRED** `netAmount` = `amount`.
4. If `amount` is absent or not numeric, `netAmount` is **NOT_COMPUTABLE**. Open `SYNC_FAILURE` and do not credit.

Implementers MUST verify this net rule against current Donorbox documentation at implement time. Do not treat the INFERRED arithmetic as a live settlement receipt.

## Verify and persist

1. Inbound webhooks MUST be verified (shared secret and/or signature) before side effects.
   - every.org: OBSERVED Worker shape `POST /webhooks/every-org` with `x-webhook-token` or `?token=`.
   - Givebutter: verify the dashboard signing secret against the request header named `Signature` (**OBSERVED** from the Givebutter help article retrieved 2026-08-22; not OBSERVED in this repository).
   - Donorbox: verify using the Donorbox verify-notifications help. The public article documents header `Donorbox-Signature` as timestamp, HMAC-SHA256 (**OBSERVED** from that help article retrieved 2026-08-22; not OBSERVED in this repository). Do not invent a different header name.
   - Other `/webhooks/*` paths return 404 (OBSERVED Worker shape). Proposed P1 paths are `/webhooks/givebutter` and `/webhooks/donorbox`. Those paths are proposals, not live URLs.
2. Implementations MUST persist the **raw payload** (or an equivalent webhook-event row plus payload) before or within the same transaction as pot credit ([SPEC-023](SPEC-023-financial-ledger-invariants.md)).
3. Unverified requests MUST NOT create gift summaries or pot credits.
4. Live pointing of any vendor webhook is **operator-owned**. Specs MUST NOT invent a workers.dev or named-host URL.

## Idempotent `chargeId`

5. Gift summary primary key SHALL be connector `chargeId` (OBSERVED: `am_gifts.charge_id`).
6. A second delivery with the same `chargeId` MUST NOT increase pot `credited` and MUST return a success-equivalent outcome (no-op create).
7. Anomalous redelivery MAY open `DUPLICATE_GIFT` without reversing the original credit.

## Pot credit and auto-create

8. On a new `chargeId`: resolve campaign pot → resolve program slice → credit **net** amount.
9. Unknown fundraiser or designation: **auto-create** pot/slice tagged for review (product language: “New — review”) and MAY open `UNMAPPED_FUNDRAISER` or `UNMAPPED_DESIGNATION` when policy requires confirm.
10. Available balance = credited − allocated (slice, rolled up to campaign). Allocation MUST NOT exceed available; violation is `OVER_ALLOCATION` and MUST block the commit.
11. Default currency is the organization default (typically `USD`). OBSERVED pot row identity: `(client_id, campaign_key, program_key)`.

## Exception catalog

| Code | Trigger | Human action |
| --- | --- | --- |
| `UNMAPPED_FUNDRAISER` | Policy requires confirm of a new/unknown fundraiser | Name / merge pot |
| `UNMAPPED_DESIGNATION` | Policy requires confirm of a new/unknown designation | Name / merge slice |
| `DUPLICATE_GIFT` | Anomalous redelivery of `chargeId` | Dismiss / investigate |
| `CURRENCY_MISMATCH` | Non-default currency | Hold or policy convert |
| `OVER_ALLOCATION` | Commit greater than available | Reduce / reallocate |
| `SYNC_FAILURE` | Connector or store error after verify | Retry / reconnect |
| `MISSING_PROOF` | Allocation without Evidence past SLA | Attach or waive ([SPEC-027](SPEC-027-impact-loop.md)) |
| `STALE_POT` | Inactive pot threshold | Archive |

Implementations MAY store exceptions as work items (OBSERVED: `am_exceptions`). Codes above are the v1 catalog; new codes require a SPEC-026 amendment. Version 1.1.0 does **not** add a refund or chargeback code.

## CSV import

12. CSV is the offline twin of the webhook. Required columns: `chargeId`, `netAmount`. Optional: `amount`, `campaignKey`, `programKey`, `currency`, `donatedAt`.
13. Each row MUST pass through the same normalize + `chargeId` idempotency + pot-credit rules as a webhook gift.
14. OBSERVED parser: `services/allocation-middleware/src/connectors/csv.mjs`. Version 1.0.0 recorded that a Worker HTTP route for CSV was **not** OBSERVED on `run_worker_first`. The informative [sprint remaining work](../docs/sprint-remaining-work-donation-tracking.md) in this repository later lists `POST /import/csv` as CODE_SHIPPED in Portfolio-Signals artifacts. This amendment does **not** treat that checklist as a live inspect. Implementations SHALL expose an operator-authenticated CSV import path. The proposed Worker path is `POST /import/csv`. That path MUST NOT be an anonymous public webhook.

## Donor PII

15. Donor identity fields are opt-in from the connector. Core credit UX MUST work with no name or email.
16. If the connector omits contactable identity, implementations MUST NOT invent email or push targets ([SPEC-017](SPEC-017-data-classification-and-privacy.md), [SPEC-027](SPEC-027-impact-loop.md)).
17. Operators MUST be able to record tenant `source` (`every.org` \| `givebutter` \| `donorbox` \| `csv`) and an optional HTTPS `donation_link`.
18. If `donation_link` is missing, ImpactNotice MUST NOT emit and implementations MUST NOT invent a URL.
19. Implementations MUST verify a shared secret or signature **before** any gift summary or pot credit. Unverified requests are a no-op.
20. Credit **net** by idempotent `chargeId`. Auto-create unmapped pots/slices tagged for review. Use the same exception catalog as this specification.
21. Donor name and email remain opt-in only. ImpactNotice is eligible only if the connector (or CSV twin) supplied contactable identity.
22. A human still allocates. Evidence is still required, or an explicit human waive, before ImpactNotice.
23. Live vendor pointing is operator-owned. Specs MUST NOT invent a `workers.dev` or named-host URL.
24. Stripe billing webhooks MUST NOT write `am_gifts` or credit pots.

## Refunds and chargebacks (not v1)

Givebutter documents `refund.created`. Donorbox documents `donation.chargeback_created`, `donation.chargeback_won`, and `donation.chargeback_lost` (**OBSERVED** from the vendor help articles retrieved 2026-08-22).

This specification does **not** define automatic pot debit for refunds or chargebacks. Implementations MUST NOT reverse pot credit from those events in v1. After verify, hold the payload as `SYNC_FAILURE` (or ignore after persist) until a future SPEC-026 amendment adds a catalog code and compensating-entry rules that preserve [SPEC-023](SPEC-023-financial-ledger-invariants.md). Version 1.1.0 does not add that code.

## Observed persistence (repo artifacts, not live inspect)

The following are **OBSERVED** in [Portfolio-Signals](https://github.com/Autonomous-Giving-Incorporated/Portfolio-Signals) files. This session did not inspect a live Cloudflare dashboard or live AGI Postgres.

| Artifact | OBSERVED fact |
| --- | --- |
| `wrangler.toml` | Worker name `portfolio-signals`; `main` `workers/portfolio-signals/src/index.js`; `workers_dev = true`; `run_worker_first` includes `/webhooks/*` and allocation API paths; `[vars] ORG_ID = "org_hacker_dojo"`; `PLATFORM_SUPABASE_URL = "https://utdioxwiskzatwoejgiu.supabase.co"` |
| Worker `index.js` | `/webhooks/every-org` → every-org handler; other `/webhooks/*` → 404; allocation API → allocation handler; else ASSETS |
| `202608030001_allocation_middleware.sql` | `am_gifts` (PK `charge_id`), `am_pots`, `am_allocations`, `am_proofs`, `am_exceptions`; RLS select for members; director insert on allocations/proofs; `client_id` e.g. `org_hacker_dojo` |
| Static surfaces | `allocation.html`, `allocation-login.html`, `allocation-setup.html`, `donor-impact.html` / `donor-impact.js` |

Durable state is platform Supabase `am_*` via service-role binding (comment OBSERVED in `wrangler.toml`). Named-host OBSERVED and live vendor pointing remain operator-owned.

## Non-goals

- AGI-hosted donation checkout or Stripe donation capture
- Stripe, PayPal, or Square as donation sources. Stripe billing webhooks MUST NOT write `am_gifts` or credit pots ([ADR-015](../adr/ADR-015-donation-tracking-money-boundary.md))
- Automatic pot debit for refunds or chargebacks
- Fundraise Up, Zeffy, or GoFundMe Pro as required P1 work (P2+, reserved; MUST NOT block)
- CRM (Salesforce, HubSpot, Mailchimp)
- Bank, Plaid, QuickBooks, or a full general ledger
- Inventing donor PII
- Changing SPEC-023 ledger invariants
- A fifth capability
- Marking any host READY or inventing a workers.dev URL
- Claiming HIPAA or live operations

## Revision history

| Version | Date | Change |
| --- | --- | --- |
| 1.0.0 | 2026-08-15 | Accepted: every.org P0 adapter, verify, raw payload, idempotent `chargeId`, `netAmount`, auto-create, exception catalog, CSV twin |
| 1.1.0 | 2026-08-22 | MINOR amendment: tenant onboarding; Givebutter and Donorbox P1 mappings; operator CSV path; refunds/chargebacks held out of v1 |
