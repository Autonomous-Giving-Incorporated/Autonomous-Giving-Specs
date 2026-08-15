# Recovery runbook (preferred Supabase PostgreSQL path)

Informative operational placeholder for product teams. Customize RPO/RTO, contacts, and exact Supabase / Cloudflare console steps in the product repository runbook. Platform expectations: [SPEC-025](../specs/SPEC-025-operations-deploy-and-scale.md), financial invariants: [SPEC-023](../specs/SPEC-023-financial-ledger-invariants.md). [ADR-012](../adr/ADR-012-render-first-platform.md) Render recovery notes are **historical**.

## Objectives (set per product)

| Objective | MVP placeholder | Notes |
| --- | --- | --- |
| RPO | ≤ 24 hours | Tighten when backup tier allows |
| RTO | ≤ 8 hours | Depends on restore testing |
| Data integrity | Reconstructable ledger | Prefer compensating entries over destructive fixes |

## Backup expectations

1. Confirm Supabase PostgreSQL automatic backups are enabled for the environment tier.
2. Document whether point-in-time recovery (PITR) is available on the plan.
3. Periodically test restore to a **non-production** instance (schedule quarterly or after major schema changes).

## Restore procedure (outline)

1. **Declare incident** — freeze non-essential writes if corruption is active.
2. **Identify restore point** — time of last known good state; note in-flight Stripe events.
3. **Restore Postgres** — use Supabase backup/PITR to a new database instance (prefer not overwriting until verified).
4. **Point staging/canary Worker** at restored DB; run integrity checks:
   - row counts for donations, ledger_entries, webhook_events
   - sample reconciliation vs Stripe test/live as appropriate
5. **Cut over** production `DATABASE_URL` only after checks pass.
6. **Replay webhooks** — for gaps since restore point:
   - re-fetch events from Stripe API, or
   - reprocess stored `webhook_events` that were unprocessed
   - handlers MUST remain idempotent
7. **Reconcile** — run payment reconciliation job; open operator queue for mismatches.
8. **Communications** — notify stakeholders; never claim PCI or financial closure without reconciliation evidence.

## Migration recovery

| Situation | Response |
| --- | --- |
| Failed migration mid-deploy | Stop traffic if needed; fix forward with a new migration; avoid hand-editing prod schema |
| Bad migration applied | Forward-fix migration; restore from backup only if data loss/corruption is severe |
| Schema/app version skew | Deploy app version matching applied migration set |

## Accidental deletion response

| Data class | Response |
| --- | --- |
| Financial history | Do **not** hard-delete; use compensating entries; restore if bulk destruction |
| PII erasure request | Follow SPEC-017; retain non-PII integrity metadata |
| Jobs / notifications | Recreate from source events if possible |

## Webhook replay strategy

1. Identify missing or failed `webhook_events` by provider event id.
2. Fetch from Stripe (or re-deliver via Stripe dashboard/CLI in non-prod).
3. Process through the same verified, idempotent Worker / Worker+Queue path as live webhooks.
4. Confirm no duplicate ledger credits.

## Financial reconciliation after recovery

1. Export processor settlements for the incident window.
2. Compare to `payment_transactions`, `donations`, and `ledger_entries`.
3. Classify gaps: missing webhook, double apply (should be impossible), amount mismatch.
4. Record compensating entries and audit_events for every manual correction.
5. Sign off with operator identity and timestamp.

## Contacts (fill in product repo)

| Role | Contact |
| --- | --- |
| On-call engineer | |
| Finance/ops owner | |
| Cloudflare account admin | |
| Supabase project admin | |
| Stripe account admin | |

## Related

- [onboarding.md](onboarding.md)
- [SPEC-023](../specs/SPEC-023-financial-ledger-invariants.md)
- [SPEC-025](../specs/SPEC-025-operations-deploy-and-scale.md)
- [ADR-013](../adr/ADR-013-cloudflare-workers-public-host.md)
