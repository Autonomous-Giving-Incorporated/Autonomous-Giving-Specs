# Implementation progress (informative)

**As of:** 2026-08-07  
**Normative SPECs are unchanged.** This page tracks how implementation repositories consume Specs products (especially allocation middleware and suite onboarding).

## Repositories

| Repo | Role |
| --- | --- |
| [Fund-Intel](https://github.com/scrimshawlife-ctrl/Fund-Intel) | Portfolio Signals + allocation middleware pilot |
| [Impact-Relay](https://github.com/scrimshawlife-ctrl/Impact-Relay) | Evidence / tenant template clone |
| [Autonomous-Giving-Incorporated](https://github.com/scrimshawlife-ctrl/Autonomous-Giving-Incorporated) | Public suite narrative + GitHub Project #3 notes |

Authoritative **runtime evidence** lives in Fund-Intel [`docs/CURRENT-STATE.md`](https://github.com/scrimshawlife-ctrl/Fund-Intel/blob/main/docs/CURRENT-STATE.md)—not in this Specs repo.

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

Implementation runbooks (not Spec SPECs):

| Slice | Topic | Runbook (Fund-Intel) |
| --- | --- | --- |
| C | Operator / director access | `docs/OPERATOR-ACCESS-ONBOARDING.md` |
| B | Client provision → publish → activate | `docs/COMMERCIAL-CLIENT-LIFECYCLE.md` |
| D | Second tenant + IR template clone | `docs/SECOND-TENANT-ONBOARDING.md` |

Dry-runs: OBSERVED (see Fund-Intel CURRENT-STATE).

## Next operator actions

1. Live every.org webhook for Hacker Dojo (#73) — stable HTTPS URL recommended for production webhook.  
2. Director browser allocate after a live (or test) gift; sign off #74.  
3. Optional: durable Render/Railway host if tunnel URL is too ephemeral for every.org.
