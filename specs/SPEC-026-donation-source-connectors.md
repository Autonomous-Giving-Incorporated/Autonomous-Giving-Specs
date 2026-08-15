---
id: SPEC-026
title: Donation-source Connectors
version: 1.0.0
status: accepted
authority: normative
owner: Fund Intel
related_specs:
- SPEC-006
- SPEC-017
- SPEC-022
- SPEC-023
- SPEC-024
related_adrs:
- ADR-006
- ADR-013
- ADR-015
related_contracts:
- CONTRACT-003
---

# SPEC-026: Donation-source Connectors
| Version | 1.0.0 | Owner | Fund Intel | Status | Accepted |
| --- | --- | --- | --- | --- | --- |
| Dependencies | SPEC-006, SPEC-023, SPEC-024 | Related ADRs | ADR-006, ADR-013, ADR-015 | Related contracts | CONTRACT-003 |

## Purpose

Define the inbound adapter so implementations can ingest gift summaries from third-party donation platforms, credit pots, and raise exceptions—without AGI checkout or a fifth capability.

## Scope

Connector adapter, verification, raw-payload persistence, idempotent `chargeId`, default `netAmount` credit, pot/slice auto-create, exception codes, and CSV import. Aligns with the informative [allocation middleware design](../docs/superpowers/specs/2026-08-03-allocation-middleware-design.md). Observed Worker/`am_*` shapes are cited as **OBSERVED** repo artifacts, not as a live production receipt.

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

| Rule | Requirement |
| --- | --- |
| P0 | **every.org** gift-completed webhooks |
| Offline twin | CSV import through the same normalize + idempotency path |
| P1 | Givebutter, Donorbox, same adapter |
| P2+ | Fundraise Up, Zeffy, GoFundMe Pro — reserved; MUST NOT block P0 |
| Checkout | AGI MUST NOT host checkout or invent a processor session to replace a connector |

OBSERVED product module names (`normalizeEveryOrgDonation`, `parseGiftCsv`) MAY realize this boundary. The constant `every.org` is the P0 `source` value.

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

## Verify and persist

1. Inbound webhooks MUST be verified (shared secret and/or signature) before side effects. OBSERVED Worker shape: `POST /webhooks/every-org` with `x-webhook-token` or `?token=`; other `/webhooks/*` paths return 404.
2. Implementations MUST persist the **raw payload** (or an equivalent webhook-event row plus payload) before or within the same transaction as pot credit ([SPEC-023](SPEC-023-financial-ledger-invariants.md)).
3. Unverified requests MUST NOT create gift summaries or pot credits.
4. Live pointing of the every.org nonprofit webhook is **operator-owned**. Specs MUST NOT invent a workers.dev or named-host URL.

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

Implementations MAY store exceptions as work items (OBSERVED: `am_exceptions`). Codes above are the v1 catalog; new codes require a SPEC-026 amendment.

## CSV import

12. CSV is the offline twin of the webhook. Required columns: `chargeId`, `netAmount`. Optional: `amount`, `campaignKey`, `programKey`, `currency`, `donatedAt`.
13. Each row MUST pass through the same normalize + `chargeId` idempotency + pot-credit rules as a webhook gift.
14. OBSERVED parser: `services/allocation-middleware/src/connectors/csv.mjs`. A Worker HTTP route for CSV was **not** OBSERVED on `run_worker_first`; exposing import on the Worker (or an equivalent operator path) remains implementation work.

## Donor PII

15. Donor identity fields are opt-in from the connector. Core credit UX MUST work with no name or email.
16. If the connector omits contactable identity, implementations MUST NOT invent email or push targets ([SPEC-017](SPEC-017-data-classification-and-privacy.md), [SPEC-027](SPEC-027-impact-loop.md)).

## Observed persistence (repo artifacts, not live inspect)

The following are **OBSERVED** in [Portfolio-Signals](https://github.com/Autonomous-Giving-Incorporated/Portfolio-Signals) files. This session did not inspect a live Cloudflare dashboard or live AGI Postgres.

| Artifact | OBSERVED fact |
| --- | --- |
| `wrangler.toml` | Worker name `portfolio-signals`; `main` `workers/portfolio-signals/src/index.js`; `workers_dev = true`; `run_worker_first` includes `/webhooks/*` and allocation API paths; `[vars] ORG_ID = "org_hacker_dojo"`; `PLATFORM_SUPABASE_URL = "https://utdioxwiskzatwoejgiu.supabase.co"` |
| Worker `index.js` | `/webhooks/every-org` → every-org handler; other `/webhooks/*` → 404; allocation API → allocation handler; else ASSETS |
| `202608030001_allocation_middleware.sql` | `am_gifts` (PK `charge_id`), `am_pots`, `am_allocations`, `am_proofs`, `am_exceptions`; RLS select for members; director insert on allocations/proofs; `client_id` e.g. `org_hacker_dojo` |
| Static surfaces | `allocation.html`, `allocation-login.html`, `allocation-setup.html`, `donor-impact.html` / `donor-impact.js` |

Durable state is platform Supabase `am_*` via service-role binding (comment OBSERVED in `wrangler.toml`). Named-host OBSERVED and live every.org pointing remain operator-owned.

## Non-goals

- AGI-hosted donation checkout or Stripe donation capture
- Bank, Plaid, QuickBooks, or a full general ledger
- A fifth capability
- Marking any host READY or inventing a workers.dev URL
