# Hacker Dojo Pilot Hosting Implementation Plan

> **Status (2026-08-07):** Seed-on-boot, pilot scripts, director JWT, local Node host, ephemeral public HTTPS, and seed-loop acceptance are **landed in Fund-Intel**. Remaining operator steps: durable named host (optional), **live every.org webhook** ([Fund-Intel#73](https://github.com/scrimshawlife-ctrl/Fund-Intel/issues/73)), full director browser sign-off ([#74](https://github.com/scrimshawlife-ctrl/Fund-Intel/issues/74)).  
> Operator runbook: [Fund-Intel HACKER-DOJO-ALLOCATION-PILOT.md](https://github.com/scrimshawlife-ctrl/Fund-Intel/blob/main/docs/HACKER-DOJO-ALLOCATION-PILOT.md) · Evidence: [CURRENT-STATE.md](https://github.com/scrimshawlife-ctrl/Fund-Intel/blob/main/docs/CURRENT-STATE.md)

**Goal:** Make the Hacker Dojo allocation pilot runnable with seed-on-boot, deploy/smoke scripts, director auth, and a clear operator checklist—without requiring live every.org data for the first demo path.

**Architecture:** Single Node allocation-middleware process (`Fund-Intel/services/allocation-middleware`), durable `DATA_FILE`, Supabase director JWT (preferred), every.org webhook as a later ops step. Fixture seed fills pots until live gifts arrive.

**Tech Stack:** Node 22, existing middleware package, Local Node / Docker Compose / Render / Railway / optional Fly, shell scripts, platform Supabase Auth.

## Implementation status (2026-08-07)

| Capability | State | Notes |
| --- | --- | --- |
| Seed-on-boot + pilot fixtures | **Done** | `SEED_ON_BOOT`, `fixtures/hacker-dojo-pilot.json` |
| `pilot:smoke` / env checklist | **Done** | Local + HTTPS smoke PASS |
| Local Node host (no Docker) | **Done** | Phase 3a default |
| Docker Compose / Render / Railway / Fly recipes | **Done** | Durable host optional |
| Director JWT + membership (`org_hacker_dojo`) | **Done** | [Fund-Intel#72](https://github.com/scrimshawlife-ctrl/Fund-Intel/issues/72) closed |
| Public HTTPS (ephemeral cloudflared) | **Done** | [Fund-Intel#71](https://github.com/scrimshawlife-ctrl/Fund-Intel/issues/71) closed |
| Seed allocate → proof → packet | **Done** | `npm run accept:seed-loop` OBSERVED (#74 partial) |
| Durable named public host | Optional | Render/Railway/Fly when every.org needs stable URL |
| Live every.org webhook | **Open** | #73 |
| Full director browser acceptance | **Open** | #74 remaining after live gift |

## Global Constraints

- Tenant: `org_hacker_dojo` for this pilot (reference tenant, not product brand).
- Transaction-light pots; no bank/QuickBooks.
- every.org connect = webhook wizard, not OAuth.
- Director writes: Supabase membership `director` | `campaign_lead`; operator-token fallback emergency-only (`ALLOW_OPERATOR_TOKEN_FALLBACK=0` preferred).
- Do not block first pilot path on live every.org; seed fixtures first.
- Production boot fails closed without required secrets (existing guards).

## Related docs

- Design: [allocation middleware design](../specs/2026-08-03-allocation-middleware-design.md)
- MVP plan: [allocation middleware plan](2026-08-03-allocation-middleware.md) (historical checklist; MVP shipped)
- Fund-Intel: `docs/HACKER-DOJO-ALLOCATION-PILOT.md`, `docs/ALLOCATION-DIRECTOR-LOGIN.md`, `docs/ALLOCATION-HOSTING-OPTIONS.md`, `docs/CURRENT-STATE.md`
- Suite commercial onboarding (people / client / second tenant): Fund-Intel `OPERATOR-ACCESS-ONBOARDING`, `COMMERCIAL-CLIENT-LIFECYCLE`, `SECOND-TENANT-ONBOARDING`

---

## Historical task checklist (completed in Fund-Intel)

Tasks below were the original implementation sequence. They are retained for audit; **do not re-execute** unless regenerating the package.

### Task 1: Seed-on-boot — **done**

- `SEED_ON_BOOT` / `SEED_ALLOCATE` / fixture path  
- Idempotent gift chargeIds  

### Task 2: Deploy / smoke scripts — **done**

- `pilot-smoke.sh`, `print-env-checklist.sh`, optional Fly deploy helpers  
- Compose / Render / Railway configs  

### Task 3: Pilot runbook polish — **done**

- Fund-Intel pilot, director login, hosting options, production readiness docs  

### Task 4: Specs plan + cross-link — **done** (this file; status refreshed 2026-08-07)

---

## Operator success criteria

| Criterion | Status |
| --- | --- |
| `pilot:smoke` green (local and/or HTTPS) | **Met** |
| Seeded Available shows Community Hardware Fund | **Met** |
| Director JWT can authorize writes (config path) | **Met** |
| Allocate → proof → packet on seed | **Met** (`accept:seed-loop`) |
| Process restart keeps balances (`DATA_FILE`) | **Met** (file store) |
| `/setup.html` ready for every.org | **Met** (wizard shipped; live paste **open**) |
| Live gift credits Available without re-seed | **Open** (#73) |

## Out of scope (unchanged)

- Live every.org admin access automation  
- Multi-tenant multi-process fleet for pilot  
- Givebutter/Donorbox  
- Full Supabase store adapter (file volume OK for pilot)  
