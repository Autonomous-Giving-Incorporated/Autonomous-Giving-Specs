# Implementation progress (informative)

**As of:** 2026-08-08 (evening)  
**Normative SPECs are unchanged.** This page tracks how implementation repositories consume Specs products (especially allocation middleware and suite onboarding).

## Repositories

| Repo | Role |
| --- | --- |
| [Portofolio-Signals](https://github.com/scrimshawlife-ctrl/Portofolio-Signals) (Fund-Intel) | Portfolio Signals + allocation middleware pilot |
| [Impact-Relay](https://github.com/scrimshawlife-ctrl/Impact-Relay) | Evidence / tenant template clone |
| [Autonomous-Giving-Incorporated](https://github.com/scrimshawlife-ctrl/Autonomous-Giving-Incorporated) | Public suite narrative + GitHub Project #3 notes |

Authoritative **runtime evidence** lives in Portofolio-Signals / Fund-Intel [`docs/CURRENT-STATE.md`](https://github.com/scrimshawlife-ctrl/Portofolio-Signals/blob/main/docs/CURRENT-STATE.md)—not in this Specs repo.

## Allocation middleware (design 2026-08-03)

| Item | Status |
| --- | --- |
| MVP package (pots, allocate, proof, packet, every.org adapter, UI) | Shipped |
| Local Node pilot + unit tests | OBSERVED |
| Director JWT (`org_hacker_dojo`) | OBSERVED — Fund-Intel #72 closed |
| Public HTTPS (Cloudflare quick tunnel) | OBSERVED ephemeral — #71 closed |
| Seed-loop allocate→proof→packet | OBSERVED — `npm run accept:seed-loop` |
| Durable named host (Render/Fly/…) | Recipe READY in Portofolio-Signals; public deploy optional operator. **Platform preferred host for new work:** Cloudflare + Supabase ([ADR-013](../../adr/ADR-013-cloudflare-workers-public-host.md)); Render is historical |
| Live every.org webhook | **Open** — Portofolio-Signals #73 |
| Full director browser sign-off | **Open** — #74 remainder |

Specs: [design](specs/2026-08-03-allocation-middleware-design.md) · [MVP plan](plans/2026-08-03-allocation-middleware.md) · [pilot hosting](plans/2026-08-03-hacker-dojo-pilot-hosting.md).

## Suite commercial onboarding (Portofolio-Signals + IR)

**Hub:** Portofolio-Signals [`docs/SUITE-ONBOARDING.md`](https://github.com/scrimshawlife-ctrl/Portofolio-Signals/blob/main/docs/SUITE-ONBOARDING.md) (done without login vs needs every.org/admin).

**Evidence SoT:** Portofolio-Signals [`docs/CURRENT-STATE.md`](https://github.com/scrimshawlife-ctrl/Portofolio-Signals/blob/main/docs/CURRENT-STATE.md) (labels OBSERVED / PENDING / BLOCKED).

**Continuation plan (this repo):** [plans/2026-08-08-suite-continuation.md](plans/2026-08-08-suite-continuation.md).

### Slices

| Slice | Topic | Runbook (Portofolio-Signals) | Status |
| --- | --- | --- | --- |
| C | Operator / director access | `docs/OPERATOR-ACCESS-ONBOARDING.md` | **People registered** (see matrix); MFA incomplete for Qi/Ed |
| B | Client provision → publish → activate | `docs/COMMERCIAL-CLIENT-LIFECYCLE.md` | Dry-run OBSERVED (`org_hacker_dojo`) |
| Doc pack | Private org-proof documents | `docs/CLIENT-ONBOARDING-PACK.md` | **Platform schema + Edge OBSERVED** 2026-08-08; MFA dry-run **PENDING** ([#104](https://github.com/scrimshawlife-ctrl/Portofolio-Signals/pull/104), activate [#113](https://github.com/scrimshawlife-ctrl/Portofolio-Signals/pull/113)) |
| D | Second tenant + IR template clone | `docs/SECOND-TENANT-ONBOARDING.md` | Dry-run OBSERVED |
| Harden | Tenant chrome + HD data gate | — | **OBSERVED** on main [#108](https://github.com/scrimshawlife-ctrl/Portofolio-Signals/pull/108), [#111](https://github.com/scrimshawlife-ctrl/Portofolio-Signals/pull/111), [#112](https://github.com/scrimshawlife-ctrl/Portofolio-Signals/pull/112) |

### People matrix (platform `utdioxwiskzatwoejgiu`)

| Email | Role | Scope | MFA |
| --- | --- | --- | --- |
| `scrimshawlife@gmail.com` | `master_admin` | All clients + platform admin | Enforced |
| `qi@enkeyai.com` | `master_admin` | All clients + platform admin | Pending TOTP → then `set-mfa-enforced` |
| `ed@hackerdojo.org` | **director only** | **`org_hacker_dojo` only** — not `platform_administrators`; no other client memberships | Pending TOTP → then `set-mfa-enforced` (action_link regenerated operator-local 2026-08-08) |

**Access rule (Ed):** Hacker Dojo tenant dataset and tenant-scoped workspace/onboarding functions for that `client_id` only. Master admins bypass membership checks; Ed does not.

### Recent Portofolio-Signals merges (2026-08-08)

| PR | Topic |
| --- | --- |
| #104–#105 | Client Onboarding Pack code + suite hub sync |
| #106 | Suite subpath asset base (`/portfolio-signals/`) |
| #107 | Compliance disclaimers + legal footer |
| #108 | Tenant chrome only when signed in |
| #109 | Second master_admin Qi Diaz |
| #110 | HD director `ed@hackerdojo.org` |
| #111 | Canonical HD campaign data behind tenant login |
| #112 | Platform activate plan + residual HD fixture harden + `activate-onboarding-pack.sh` |

Dry-runs (C/B/D): OBSERVED. Document pack: tables REST 200 + Edge OPTIONS 200 / unauth 401 on `utdioxwiskzatwoejgiu` (2026-08-08). MFA workspace dry-run still PENDING before full pack OBSERVED.

**every.org setup wizard:** fixture chargeIds (`fixture-*`) do not mark Connected; only live (non-fixture) POSTs do (`counts.liveGifts` / `lastLiveGift`).

**Document pack (phase 1):** upload → `campaign-private` → suggest type → human confirm → pack ready. Never auto-promotes CRM; xlsx/csv parked for future list quarantine. Design: Portofolio-Signals [`docs/superpowers/specs/2026-08-08-client-onboarding-pack-design.md`](https://github.com/scrimshawlife-ctrl/Portofolio-Signals/blob/main/docs/superpowers/specs/2026-08-08-client-onboarding-pack-design.md) · plan: [`plans/2026-08-08-client-onboarding-pack.md`](https://github.com/scrimshawlife-ctrl/Portofolio-Signals/blob/main/docs/superpowers/plans/2026-08-08-client-onboarding-pack.md) · activate: [`plans/2026-08-08-platform-activate-and-tenant-harden.md`](https://github.com/scrimshawlife-ctrl/Portofolio-Signals/blob/main/docs/superpowers/plans/2026-08-08-platform-activate-and-tenant-harden.md).

**Optional ops runbooks (code/docs ready; dashboards operator):** durable host preflight, custom SMTP, secret hygiene — see suite hub.

## Next operator actions

Ordered for least external dependency first. Detail: [suite continuation plan](plans/2026-08-08-suite-continuation.md).

1. **People:** open operator-local action_links for Qi/Ed → enroll TOTP → `set-mfa-enforced`.  
2. **Pack dry-run:** MFA director (or master) → Workspace Onboarding pack → 5 required + park xlsx → mark CURRENT-STATE full OBSERVED.  
3. **Live every.org webhook** for Hacker Dojo (#73) — stable HTTPS URL recommended.  
4. **Director browser allocate** after live (or test) gift; sign off #74.  
5. **Optional:** durable Render/Railway/Fly host; custom SMTP for invite volume.  
6. **Security:** revoke any PAT pasted into chat; regenerate if still needed.
