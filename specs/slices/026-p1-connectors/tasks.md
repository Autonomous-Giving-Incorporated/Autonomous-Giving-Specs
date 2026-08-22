# Tasks: P1 donation-source connectors and CSV operator path

**Input:** [spec.md](spec.md), [plan.md](plan.md), [SPEC-026](../../SPEC-026-donation-source-connectors.md) v1.1.0  
**Runtime home:** Autonomous-Giving-Incorporated / Portfolio-Signals  
**This repository:** specs only — do not implement these tasks here  
**Status:** Ordered backlog. Do **not** mark READY. Do **not** claim HIPAA or live operations.

Before you map a vendor field, re-read the current Givebutter and Donorbox documentation. SPEC-026 labels product mappings **INFERRED** where this repository does not already record the vendor field name.

## Phase 1: Setup

**Goal:** Product-repo workspace can receive adapter work without changing the money boundary.

- [ ] T001 Confirm the runtime branch lives in Autonomous-Giving-Incorporated / Portfolio-Signals, not in Autonomous-Giving-Specs.
- [ ] T002 Confirm Constitution, [ADR-015](../../../adr/ADR-015-donation-tracking-money-boundary.md), and [SPEC-023](../../SPEC-023-financial-ledger-invariants.md) still forbid AGI checkout and Stripe-as-donation-source.
- [ ] T003 Add fixture directories for every.org, Givebutter, Donorbox, and CSV using **synthetic** payloads only. Do not copy live donor PII.
- [ ] T004 Document operator-owned pointing: the vendor dashboard receives the Worker URL from the operator. Specs do not invent a `workers.dev` URL.

## Phase 2: Foundational (adapter interface and fixtures)

**Goal:** One adapter boundary exists before any new source story.

**Depends on:** Phase 1

- [ ] T005 Keep the adapter as `verify_webhook`, `normalize_gift`, and `list_campaign_hints` only. Do not add a fourth function or a fifth capability.
- [ ] T006 Share gift-summary shape: `chargeId`, `netAmount`, optional `amount`, campaign/program hints, `currency`, `donatedAt`, opt-in identity.
- [ ] T007 Persist raw payload before or with pot credit into platform Supabase `am_gifts` / `am_pots` / `am_exceptions` (OBSERVED table names in SPEC-026).
- [ ] T008 Fail closed on verify miss: no gift summary, no pot credit.
- [ ] T009 Store secrets in Worker bindings. Do not commit secrets.
- [ ] T010 Add shared tests: duplicate `chargeId`, bad signature, currency mismatch, unmapped fundraiser.

## Phase 3: User story 1 — every.org pointing and docs

**Goal:** Close remaining P0 pointing and documentation gaps so P1 work does not block on every.org.

**Depends on:** Phase 2  
**Story:** [spec.md](spec.md) user story 1 (every.org path)

- [ ] T011 Keep `POST /webhooks/every-org` (OBSERVED). Do not rename it.
- [ ] T012 Confirm shared-token verify still matches SPEC-026 (`x-webhook-token` or `?token=`).
- [ ] T013 Write operator docs that explain how to paste the operator-owned URL into the every.org nonprofit webhook settings. Do not publish an invented host.
- [ ] T014 Confirm `fromFundraiser`, `designation`, `chargeId`, and `netAmount` still match the v1.0.0 mapping.
- [ ] T015 If pointing is still operator-owned and unverified live, leave it operator-owned. Do not mark READY.

## Phase 4: User story 2 — Givebutter

**Goal:** `transaction.succeeded` credits net after signature verify.

**Depends on:** Phase 2  
**Story:** [spec.md](spec.md) user story 2

- [ ] T016 Re-read current Givebutter webhook help and confirm field names before you code.
- [ ] T017 Add proposed Worker path `POST /webhooks/givebutter`. Other unknown `/webhooks/*` paths stay 404.
- [ ] T018 Implement `verify_webhook` using the Givebutter signing secret and the header named `Signature` if current docs still say that (OBSERVED 2026-08-22; verify again).
- [ ] T019 Map `data.id` → `chargeId`, `data.donated` → `netAmount`, campaign id/code → campaign pot. If `donated` is absent, INFERRED fallback is `payout`. If net is NOT_COMPUTABLE, open `SYNC_FAILURE` and do not credit.
- [ ] T020 Store email only when `communication_opt_in` is true. Do not invent PII.
- [ ] T021 After verify, persist `refund.created` without pot debit. Hold as `SYNC_FAILURE` or persist-and-ignore (not v1 debit).
- [ ] T022 Tests: happy-path fixture, duplicate `chargeId`, bad signature, missing opt-in, unmapped campaign.

## Phase 5: User story 3 — Donorbox

**Goal:** `donation.created` credits net after documented verification. Tenants without the webhook add-on use CSV.

**Depends on:** Phase 2  
**Story:** [spec.md](spec.md) user story 3

- [ ] T023 Re-read current Donorbox Custom Webhooks and Verify notifications help before you code.
- [ ] T024 Add proposed Worker path `POST /webhooks/donorbox`.
- [ ] T025 Implement `verify_webhook` from the current verify-notifications article. Do not invent a header name. Public docs on 2026-08-22 showed `Donorbox-Signature`.
- [ ] T026 Map donation `id` → `chargeId`. Do not use `stripe_charge_id` as `chargeId`.
- [ ] T027 Apply the SPEC-026 net rule: INFERRED `amount` − `processing_fee` when fee is present; INFERRED `netAmount` = `amount` when fee is absent. If amount is not numeric, NOT_COMPUTABLE → `SYNC_FAILURE`.
- [ ] T028 Map `campaign` → campaign pot and `designation` → program slice when present.
- [ ] T029 Store email only when `join_mailing_list` is true (INFERRED opt-in analog). Do not invent PII.
- [ ] T030 After verify, persist chargeback events without pot debit. Hold as `SYNC_FAILURE` or persist-and-ignore.
- [ ] T031 Record in operator docs that custom webhooks need the Donorbox API/Zapier add-on or Premium (OBSERVED 2026-08-22). Other tenants use Story 4.
- [ ] T032 Tests: happy-path fixture, fee-absent net, bad signature, `stripe_charge_id` ignored as PK, unmapped campaign.

## Phase 6: User story 4 — CSV Worker / operator path

**Goal:** Authenticated CSV import uses the same normalize and idempotency path.

**Depends on:** Phase 2  
**Story:** [spec.md](spec.md) user story 4

- [ ] T033 Expose an operator-authenticated CSV import path. Proposed Worker path: `POST /import/csv`. Do not treat that string as a live URL.
- [ ] T034 Require columns `chargeId` and `netAmount`. Accept optional `amount`, `campaignKey`, `programKey`, `currency`, `donatedAt`.
- [ ] T035 Run each row through the same `normalize_gift` + `chargeId` idempotency + pot-credit rules as webhooks.
- [ ] T036 Reject anonymous public CSV POST. This is not a vendor webhook.
- [ ] T037 Tests: valid row, duplicate `chargeId`, missing required column, currency mismatch, unmapped `campaignKey`.

## Phase 7: User story 5 — Tenant onboarding fields

**Goal:** A tenant that already has a public fundraiser can finish setup in one sitting.

**Depends on:** Phases 3–6 for source-specific secrets; Phase 2 for persistence  
**Story:** [spec.md](spec.md) user stories 1 and 5

- [ ] T038 Persist tenant `source` as `every.org` \| `givebutter` \| `donorbox` \| `csv`.
- [ ] T039 Persist optional `donation_link` as HTTPS. If missing, do not invent a URL and do not emit ImpactNotice.
- [ ] T040 Persist or bind the per-source webhook secret. Pointing stays operator-owned.
- [ ] T041 Confirm ImpactNotice still requires contactable identity, Evidence or explicit waive, and `donation_link` ([SPEC-027](../../SPEC-027-impact-loop.md)).
- [ ] T042 Tests: missing link skips ImpactNotice; unverified webhook is a no-op; redelivery is a no-op.

## Phase 8: Polish

**Goal:** Conformance notes only. No READY claim.

**Depends on:** Phases 3–7

- [ ] T043 Run adapter conformance against SPEC-026 v1.1.0: same adapter, same exception catalog, no new capability, no AGI checkout.
- [ ] T044 Confirm Stripe billing webhooks (if any) do not write `am_gifts`.
- [ ] T045 Confirm P2+ sources (Fundraise Up, Zeffy, GoFundMe Pro) are not required and do not block merge.
- [ ] T046 Confirm CRM, bank, Plaid, and QuickBooks work is absent.
- [ ] T047 Write a short product-repo conformance note that lists implemented SPECs. Do **not** mark READY. Do **not** claim HIPAA. Do **not** claim live operations.

## Dependency graph

```text
Phase 1 Setup
    → Phase 2 Foundational
        → Phase 3 every.org pointing/docs
        → Phase 4 Givebutter
        → Phase 5 Donorbox
        → Phase 6 CSV
        → Phase 7 Onboarding fields (uses 3–6)
            → Phase 8 Polish
```

Phases 3–6 MAY proceed in parallel after Phase 2 if staffing allows. Phase 7 needs the source-specific secret bindings from 3–6.

## Parallel opportunities

- T016–T022 (Givebutter) and T023–T032 (Donorbox) can proceed in parallel after T010.
- T033–T037 (CSV) can proceed in parallel with the webhook stories after T010.
- T011–T015 (every.org docs) can proceed in parallel with P1 adapters.

## Stop conditions

Stop and return to specs if you need a new exception code, automatic pot debit, a new adapter function, AGI checkout, or a Stripe/PayPal/Square donation source.
