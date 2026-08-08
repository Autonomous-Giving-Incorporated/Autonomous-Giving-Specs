# Implementation progress (informative)

**As of:** 2026-08-08  
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
| Durable named host (Render/Fly/…) | Optional operator |
| Live every.org webhook | **Open** — Fund-Intel #73 |
| Full director browser sign-off | **Open** — #74 remainder |

Specs: [design](specs/2026-08-03-allocation-middleware-design.md) · [MVP plan](plans/2026-08-03-allocation-middleware.md) · [pilot hosting](plans/2026-08-03-hacker-dojo-pilot-hosting.md).

## Suite commercial onboarding (Fund-Intel + IR)

**Hub:** Portofolio-Signals [`docs/SUITE-ONBOARDING.md`](https://github.com/scrimshawlife-ctrl/Portofolio-Signals/blob/main/docs/SUITE-ONBOARDING.md) (done without login vs needs every.org/admin).

Implementation runbooks (not Spec SPECs):

| Slice | Topic | Runbook (Portofolio-Signals / Fund-Intel) | Status |
| --- | --- | --- | --- |
| C | Operator / director access | `docs/OPERATOR-ACCESS-ONBOARDING.md` | Dry-run OBSERVED |
| B | Client provision → publish → activate | `docs/COMMERCIAL-CLIENT-LIFECYCLE.md` | Dry-run OBSERVED |
| Doc pack | Private org-proof documents | `docs/CLIENT-ONBOARDING-PACK.md` | **Code MERGED** #104; platform apply **PENDING** |
| D | Second tenant + IR template clone | `docs/SECOND-TENANT-ONBOARDING.md` | Dry-run OBSERVED |

Dry-runs (C/B/D): OBSERVED (see CURRENT-STATE). Document pack: code on main; OBSERVED only after platform migrate + Edge deploy + MFA dry-run.

**every.org setup wizard:** fixture chargeIds (`fixture-*`) do not mark Connected; only live (non-fixture) POSTs do (`counts.liveGifts` / `lastLiveGift`).

**Document pack (phase 1):** upload → private storage → suggest type → human confirm → pack ready. Never auto-promotes CRM; xlsx/csv parked for future list quarantine. Design: Fund-Intel `docs/superpowers/specs/2026-08-08-client-onboarding-pack-design.md`.

## Next operator actions

1. **Doc pack platform:** apply migrations + deploy `upload-onboarding-document` / `onboarding-document-url` on `utdioxwiskzatwoejgiu`; MFA dry-run → OBSERVED.  
2. Live every.org webhook for Hacker Dojo (#73) — stable HTTPS URL recommended for production webhook.  
3. Director browser allocate after a live (or test) gift; sign off #74.  
4. Optional: durable Render/Railway host if tunnel URL is too ephemeral for every.org.
