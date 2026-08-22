# Feature specification: P1 donation-source connectors and CSV operator path

**Parent:** [SPEC-026](../../SPEC-026-donation-source-connectors.md) v1.1.0 (normative)  
**Slice:** `026-p1-connectors`  
**Created:** 2026-08-22  
**Status:** Specify only — not READY  
**Audience:** Later runtime in Autonomous-Giving-Incorporated / Portfolio-Signals  
**Style:** [Google developer documentation style](https://developers.google.com/style)

This file states **what** and **why**. It does not choose a stack. For how and architecture, see [plan.md](plan.md). For ordered implementer work, see [tasks.md](tasks.md).

## Evidence labels

| Label | Meaning |
| --- | --- |
| **OBSERVED** | Fact from a cited public vendor document (retrieved 2026-08-22) or from Portfolio-Signals artifacts already cited in SPEC-026. This session did not inspect a live host, live webhook, or live database. |
| **INFERRED** | Mapping that follows from an OBSERVED field but is not named as the product field in this repository. |
| **SPECULATIVE** | Possible, not evidenced, not required. |
| **NOT_COMPUTABLE** | Cannot be determined from evidence in this repository or the cited public docs. |

Do not invent evidence, hosts, or live webhook URLs. Re-read current vendor documentation at implement time.

## Why this slice exists

Pantry and rescue staff already run public fundraisers on every.org, Givebutter, or Donorbox. They need those completed gifts to become tracked pot credit so a human can allocate and, after Evidence or an explicit waive, send an ImpactNotice. AGI tracks gifts. It does not process donations ([ADR-015](../../../adr/ADR-015-donation-tracking-money-boundary.md)).

SPEC-026 v1.0.0 defined the adapter and the every.org P0 path. This slice tells a later implementer how to finish P1 sources and a CSV operator path without adding a fifth capability or AGI checkout.

## User stories

### User story 1 — Connect an existing fundraiser in one sitting (Priority: P1)

A pantry or rescue operator who already has a public fundraiser records `donation_link`, chooses `source`, stores the vendor webhook secret, and points the vendor dashboard at AGI’s operator-owned Worker path. After one sitting, a verified gift can credit a pot.

**Why this priority:** Without onboarding fields, P1 adapters have nowhere to attach tenant identity or verification material.

**Independent test:** A tenant record accepts `source`, optional HTTPS `donation_link`, and a webhook secret binding. A missing `donation_link` does not invent a URL and does not emit ImpactNotice ([SPEC-027](../../SPEC-027-impact-loop.md)).

**Acceptance scenarios:**

1. Given a tenant with an existing HTTPS fundraiser URL, when the operator pastes that URL as `donation_link` and chooses `every.org`, `givebutter`, or `donorbox`, then the tenant record stores the outbound link and the chosen source.
2. Given a tenant with no donation URL, when the operator leaves `donation_link` empty, then credit MAY still proceed and ImpactNotice MUST NOT emit.
3. Given an operator-owned Worker path, when the operator pastes that path into the vendor dashboard, then specs still do not record a `workers.dev` URL.

### User story 2 — Givebutter succeeded transaction (Priority: P1)

A tenant whose receiver is Givebutter receives `transaction.succeeded`. After verify, the adapter credits **net** by `chargeId`.

**Why this priority:** Givebutter is the first named P1 source.

**Independent test:** A fixture built from the public Givebutter sample maps `data.id` → `chargeId` and `data.donated` → `netAmount`, and it does not store email unless `communication_opt_in` is true.

**Acceptance scenarios:**

1. Given a verified `transaction.succeeded` payload, when `normalize_gift` runs, then pot credit uses net and campaign hints from campaign id/code.
2. Given `communication_opt_in` is false or absent, when normalize runs, then name and email are omitted and ImpactNotice stays ineligible.
3. Given `refund.created`, when the Worker receives it after verify, then v1 MUST NOT debit the pot.

### User story 3 — Donorbox created donation (Priority: P1)

A tenant whose receiver is Donorbox receives `donation.created`. After verify, the adapter credits **net** by donation `id`. Tenants without the Donorbox API/Zapier add-on or Premium plan use CSV.

**Why this priority:** Donorbox is the second named P1 source. Public docs state that custom webhooks need that add-on or Premium (**OBSERVED**, 2026-08-22).

**Independent test:** A fixture built from the public Donorbox sample maps donation `id` → `chargeId` and applies the SPEC-026 INFERRED net rule. `stripe_charge_id` is not `chargeId`.

**Acceptance scenarios:**

1. Given a verified `donation.created` payload, when `normalize_gift` runs, then campaign pot comes from `campaign` and slice from `designation` when present.
2. Given `join_mailing_list` is false, when normalize runs, then donor email is not treated as contactable.
3. Given `donation.chargeback_created` (or won/lost), when the Worker receives it after verify, then v1 MUST NOT debit the pot.

### User story 4 — CSV fallback (Priority: P1)

An operator without a vendor webhook, or a small Donorbox org without the webhook add-on, imports a CSV through the same normalize and idempotency path.

**Why this priority:** CSV is the offline twin. It unblocks tenants who cannot point a webhook.

**Independent test:** A row with `chargeId` and `netAmount` credits once. A second row with the same `chargeId` is a no-op.

**Acceptance scenarios:**

1. Given required columns `chargeId` and `netAmount`, when the operator imports the file on the authenticated path, then each new `chargeId` credits net.
2. Given optional `amount`, `campaignKey`, `programKey`, `currency`, or `donatedAt`, when those columns are present, then they follow the same rules as a webhook gift.
3. Given a missing required column, when import runs, then that row does not credit and MAY open `SYNC_FAILURE`.

### User story 5 — Redelivery and unverified requests are no-ops (Priority: P1)

Webhook redelivery and unverified requests must not corrupt pots.

**Why this priority:** Connectors retry. Fail-closed verify is the money-boundary gate.

**Independent test:** The same `chargeId` twice does not increase `credited`. A bad signature creates no gift summary and no pot credit.

**Acceptance scenarios:**

1. Given an already credited `chargeId`, when the vendor redelivers, then the outcome is success-equivalent and credited does not increase.
2. Given a missing or wrong signature, when the Worker handles the request, then it persists nothing as a gift and credits nothing.
3. Given an unknown `/webhooks/*` path, when a client POSTs, then the Worker returns 404.

## Requirements

### Functional requirements

- **FR-001.** Keep the SPEC-026 adapter: `verify_webhook`, `normalize_gift`, `list_campaign_hints`. Do not add a fifth capability or a fourth adapter function.
- **FR-002.** Accept tenant `source` values `every.org`, `givebutter`, `donorbox`, and `csv` only.
- **FR-003.** If `donation_link` is present, it MUST be HTTPS and MUST point at the tenant receiver. If it is absent, do not invent a URL and do not emit ImpactNotice.
- **FR-004.** Verify shared secret or signature before any gift summary or pot credit. Fail closed on verify miss.
- **FR-005.** Credit **net** by idempotent `chargeId`. Auto-create unmapped pots/slices tagged for review. Use the SPEC-026 exception catalog unchanged.
- **FR-006.** Persist the raw payload before or with pot credit.
- **FR-007.** Treat donor name and email as opt-in only. Emit ImpactNotice only when the connector supplied contactable identity **and** Evidence or an explicit human waive exists **and** `donation_link` exists.
- **FR-008.** Map Givebutter `transaction.succeeded` as specified in SPEC-026. Do not credit from Givebutter CSV-import events (vendor docs: that event does not fire on their CSV imports — **OBSERVED** 2026-08-22).
- **FR-009.** Map Donorbox `donation.created` as specified in SPEC-026. Do not use `stripe_charge_id` as `chargeId`.
- **FR-010.** CSV required columns: `chargeId`, `netAmount`. Optional: `amount`, `campaignKey`, `programKey`, `currency`, `donatedAt`. Same normalize and idempotency as webhooks.
- **FR-011.** A human still allocates. Do not let intelligence allocate.
- **FR-012.** Do not automatically debit pots for Givebutter `refund.created` or Donorbox chargeback events. Hold as `SYNC_FAILURE` or persist-and-ignore until a future SPEC-026 amendment.

### Out of scope

State these as non-goals so later runtime does not expand the slice:

- Stripe, PayPal, or Square as donation sources
- Stripe billing webhooks writing `am_gifts`
- Automatic refund or chargeback pot debit
- Fundraise Up, Zeffy, GoFundMe Pro (P2+; reserved; MUST NOT block)
- CRM (Salesforce, HubSpot, Mailchimp)
- Bank, Plaid, or QuickBooks
- Inventing donor PII
- Changing SPEC-023 ledger invariants
- AGI checkout
- A fifth capability
- HIPAA claims or live-operations claims

## Success criteria

- **SC-001.** A pantry or rescue operator can connect an existing fundraiser in one sitting without AGI hosting checkout.
- **SC-002.** Duplicate `chargeId` is a no-op on credited.
- **SC-003.** Unverified webhooks are a no-op.
- **SC-004.** CSV fallback produces the same gift-summary shape as a webhook.
- **SC-005.** Missing `donation_link` never becomes an invented URL.
- **SC-006.** This slice is not marked READY.

## Runtime home

Later implementation lives in Autonomous-Giving-Incorporated / Portfolio-Signals. This specifications repository stays specs-only.
