# Implementation plan: P1 donation-source connectors and CSV operator path

**Parent:** [SPEC-026](../../SPEC-026-donation-source-connectors.md) v1.1.0  
**Spec:** [spec.md](spec.md) (what / why)  
**Tasks:** [tasks.md](tasks.md)  
**Created:** 2026-08-22  
**Status:** Plan only — not READY  
**Runtime home:** Autonomous-Giving-Incorporated / Portfolio-Signals  
**Style:** [Google developer documentation style](https://developers.google.com/style)

This file states **how** later runtime SHOULD be shaped. It does not implement code in this repository. Path strings below are proposals or OBSERVED artifact paths. They are not live webhook URLs.

## Evidence labels

| Label | Meaning |
| --- | --- |
| **OBSERVED** | Cited from SPEC-026’s Portfolio-Signals artifact table or from public vendor docs retrieved 2026-08-22. Not a live inspect. |
| **INFERRED** | Follows from OBSERVED artifacts; not re-verified in this session. |
| **SPECULATIVE** | Design choice that is not evidenced. |
| **NOT_COMPUTABLE** | Cannot be determined here (including any live `workers.dev` URL). |

## Summary

You extend the existing Fund Intel adapter so Givebutter, Donorbox, and an operator CSV path share `verify_webhook`, `normalize_gift`, and `list_campaign_hints`. You keep `/webhooks/every-org`. You add proposed `/webhooks/givebutter` and `/webhooks/donorbox`. You expose an operator CSV import path. You fail closed on verify miss. You credit net by `chargeId` into platform Supabase `am_*`. You do not add Kubernetes, sharding, AGI checkout, or a fifth capability.

## Technical context

| Item | Value | Label |
| --- | --- | --- |
| Language | JavaScript Worker modules, matching the OBSERVED Portfolio-Signals Worker | OBSERVED in SPEC-026 |
| Host | Cloudflare Worker | OBSERVED preferred stack ([ADR-013](../../../adr/ADR-013-cloudflare-workers-public-host.md)) |
| Datastore | Platform Supabase PostgreSQL `am_*` | OBSERVED in SPEC-026 |
| Gift PK | `am_gifts.charge_id` | OBSERVED |
| Pots / exceptions | `am_pots`, `am_exceptions` | OBSERVED |
| Testing | Fixture tests for duplicate `chargeId`, bad signature, CSV row, currency mismatch, unmapped fundraiser | Required by this plan |
| Target platform | Cloudflare Worker + Supabase; no Kubernetes; no sharding | Required |
| Project type | Adapter modules inside the existing allocation-middleware / Worker package | INFERRED from SPEC-026 module names |
| Performance | Honor the Worker request budget; persist raw payload before or with credit; do not leave a partial pot credit | INFERRED from SPEC-023 |
| Scale | Single modular Worker; Queues only if deferred retry is later evidenced ([SPEC-025](../../SPEC-025-operations-deploy-and-scale.md)) | Informative |
| Numeric timeout | **NOT_COMPUTABLE** in this repository. Do not invent a milliseconds budget. Fail closed if verify or the store write cannot complete inside the Worker request. | NOT_COMPUTABLE |

## Constitution check

| Principle | Plan response |
| --- | --- |
| Intelligence never allocates | Fund Intel verifies, normalizes, and credits. Autonomous Giving allocates under human Approval. |
| Every allocation has Evidence | ImpactNotice still requires Evidence or an explicit waive ([SPEC-027](../../SPEC-027-impact-loop.md)). |
| Every capability owns one responsibility | No fifth capability. Connectors stay a Fund Intel adapter ([SPEC-014](../../SPEC-014-future-capabilities.md)). |
| Human approval gates allocations | Unchanged. |
| Deployment is not a mandate | Cloudflare + Supabase is the preferred path, not a conformance class. |

If a later change would process donations, host checkout, or debit pots from refunds, stop and amend SPEC-026 / SPEC-023 instead of stretching this plan.

## Architecture

```text
vendor dashboard (operator-owned pointing)
        │
        ▼
Cloudflare Worker
  POST /webhooks/every-org      (OBSERVED)
  POST /webhooks/givebutter     (proposal)
  POST /webhooks/donorbox       (proposal)
  POST /import/csv              (operator path; proposal / checklist)
  other /webhooks/*             → 404 (OBSERVED)
        │
        ├─ verify_webhook (fail closed)
        ├─ persist raw payload
        ├─ normalize_gift
        ├─ list_campaign_hints
        └─ idempotent credit net → am_gifts / am_pots / am_exceptions
```

### Worker paths

| Path | Role | Label |
| --- | --- | --- |
| `POST /webhooks/every-org` | P0 every.org | OBSERVED in SPEC-026 |
| `POST /webhooks/givebutter` | P1 Givebutter | Proposal. Not a live URL. |
| `POST /webhooks/donorbox` | P1 Donorbox | Proposal. Not a live URL. |
| `POST /import/csv` | Operator CSV | Proposal. SPEC-026 v1.0.0 did not OBSERVE this route. The informative sprint remaining work in this repo lists it as CODE_SHIPPED. Not a live inspect. |
| Other ` /webhooks/*` | Reject | OBSERVED 404 |

Do not publish a `workers.dev` or named-host URL in specs or product copy. The operator pastes the real URL in the vendor dashboard.

### Verification

| Source | How you verify | Label |
| --- | --- | --- |
| `every.org` | Shared token (`x-webhook-token` or `?token=`) | OBSERVED in SPEC-026 |
| `givebutter` | Compare the dashboard signing secret to the request header named `Signature` | OBSERVED from [Givebutter webhook help](https://help.givebutter.com/en/articles/8828428-how-to-automate-workflows-and-data-using-webhooks) on 2026-08-22; not in-repo |
| `donorbox` | Follow [Verify Donorbox webhook notifications](https://donorbox.zendesk.com/hc/en-us/articles/17982194843028-Verify-Donorbox-webhook-notifications). Public docs show `Donorbox-Signature` as `timestamp,hmac-sha256` | OBSERVED from that help article on 2026-08-22; not in-repo |
| `csv` | Operator authentication on the import path; not a vendor signature | INFERRED |

If the header name in current vendor docs differs at implement time, follow the vendor docs and record the delta. Do not invent a header that is not OBSERVED.

Unverified requests: no gift summary, no pot credit, no ImpactNotice side effects.

### Secrets

Store secrets in Worker bindings. Do not commit them.

| Binding (informative names) | Purpose | Label |
| --- | --- | --- |
| `WEBHOOK_TOKEN` | every.org shared secret | OBSERVED name in sprint remaining work; not a live inspect |
| Givebutter signing secret | `Signature` compare | Proposed binding; name is SPECULATIVE |
| Donorbox signature secret | HMAC key | Proposed binding; name is SPECULATIVE |
| `SUPABASE_SERVICE_ROLE_KEY` | `am_*` writes | OBSERVED name in sprint remaining work; not a live inspect |
| CSV operator credential | Authenticated import | SPECULATIVE name |

Rotate on leak. Never log raw secrets or unnecessary donor PII.

### Timeouts, retries, and idempotency

1. If you cannot finish verify, persist, and credit inside the Worker request, fail closed. Partial credit is forbidden.
2. Vendor redelivery is the retry. `chargeId` idempotency makes redelivery a no-op on credited.
3. After a verified request, if the store write fails, open `SYNC_FAILURE`. A later redelivery or operator retry MAY complete the write.
4. Do not retry unverified requests into credit.
5. Durable Queues are optional later ([SPEC-025](../../SPEC-025-operations-deploy-and-scale.md)). They are not required to start P1.
6. A specific millisecond timeout is **NOT_COMPUTABLE** here.

### Persistence

Write the raw payload (or webhook-event row plus payload) before or in the same transaction as `am_gifts` / `am_pots` credit. Gift PK is `charge_id`. Auto-create unmapped pots tagged for review. Same exception catalog as SPEC-026.

Stripe billing webhooks, if present, MUST NOT write `am_gifts`.

### Field mapping

Use the tables in SPEC-026. Summary:

- every.org: `fromFundraiser`, `designation`, `chargeId`, `netAmount` (already specified).
- Givebutter `transaction.succeeded`: `data.id` → `chargeId`; `data.donated` → `netAmount`; campaign id/code → campaign pot; email only if `communication_opt_in`.
- Donorbox `donation.created`: donation `id` → `chargeId`; INFERRED net from `amount` minus `processing_fee` when fee is present, else INFERRED net = `amount`; campaign → pot.
- CSV: required `chargeId`,`netAmount`; optional `amount`, `campaignKey`, `programKey`, `currency`, `donatedAt`.

If `netAmount` is **NOT_COMPUTABLE**, open `SYNC_FAILURE` and do not credit.

### Tenant onboarding fields

| Field | Rule |
| --- | --- |
| `source` | `every.org` \| `givebutter` \| `donorbox` \| `csv` |
| `donation_link` | Optional HTTPS tenant receiver. Missing is allowed. |
| Webhook secret | Per-source binding. Operator-owned. |

ImpactNotice still requires contactable identity, Evidence or waive, and `donation_link`.

## Tests you MUST add in the product repo

| Case | Expected |
| --- | --- |
| Duplicate `chargeId` | Success-equivalent; credited unchanged |
| Bad signature | No gift summary; no pot credit |
| CSV row | Same normalize + idempotency as webhook |
| Currency mismatch | `CURRENCY_MISMATCH`; no silent convert unless policy says so |
| Unmapped fundraiser | Auto-create tagged for review; MAY open `UNMAPPED_FUNDRAISER` |

Also cover: missing `donation_link` does not invent a URL; Donorbox `stripe_charge_id` is not `chargeId`; refund/chargeback events do not debit.

## What you do not build

- Kubernetes, service mesh, or sharding
- AGI checkout
- Stripe / PayPal / Square donation sources
- CRM, bank, Plaid, or QuickBooks connectors
- P2+ Fundraise Up, Zeffy, GoFundMe Pro as blockers
- Automatic pot debit
- Application code in this specifications repository

## Complexity tracking

No constitution violation is proposed. Residual complexity is vendor-field drift: treat mappings as INFERRED until you re-read current vendor docs at implement time.
