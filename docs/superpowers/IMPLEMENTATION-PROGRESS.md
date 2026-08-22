# Implementation progress (informative)

**As of:** 2026-08-22  
**Normative SPECs are unchanged.** Docs pin remains **v2.0.0** (not READY). SPEC-028 / AGI login remain **PARKED**. C3 public-data policy remains **PROPOSED**. This page tracks how implementation repositories consume Specs products. Do not treat this file as operator acceptance, a freeze SHA, or product READY.

Authoritative **runtime evidence** lives in Portfolio-Signals [`docs/CURRENT-STATE.md`](https://github.com/Autonomous-Giving-Incorporated/Portfolio-Signals/blob/main/docs/CURRENT-STATE.md).  
Authoritative **continuation order** lives in Portfolio-Signals [`docs/PRODUCTION-READINESS-AND-CONTINUATION-2026-08-22.md`](https://github.com/Autonomous-Giving-Incorporated/Portfolio-Signals/blob/main/docs/PRODUCTION-READINESS-AND-CONTINUATION-2026-08-22.md) (`current_main_verdict: NO_GO`).

## Repositories

| Repo | Role |
| --- | --- |
| [Portfolio-Signals](https://github.com/Autonomous-Giving-Incorporated/Portfolio-Signals) | Workspace, allocation middleware, runtime SoT |
| [Impact-Relay](https://github.com/Autonomous-Giving-Incorporated/Impact-Relay) | Evidence library + empty public aggregate shell |
| [Autonomous-Giving-Incorporated](https://github.com/Autonomous-Giving-Incorporated/Autonomous-Giving-Incorporated) | Public static site (`output: "export"`) on `autogive.app` |
| [agi-cross-repo-harness](https://github.com/Autonomous-Giving-Incorporated/agi-cross-repo-harness) | Private pin + edge verifier. Not a production runtime |

Harness `refs/versions.json` (observed 2026-08-22, harness #20): `specs` `c089739` (v2.0.0 docs pin); `specsMain` `4aa680f` (this repo after #17; workflows unchanged through #18). This repo’s tip is now `dcf7f6b` after #18. Unmerged draft SHAs are not recorded in the harness pin file.

## Since 2026-08-17 (verified 2026-08-22)

| Item | State | Label |
| --- | --- | --- |
| Civic Forge synthetic v1 | In-repo join-key corpus. PS [#47](https://github.com/Autonomous-Giving-Incorporated/Portfolio-Signals/pull/47), IR [#12](https://github.com/Autonomous-Giving-Incorporated/Impact-Relay/pull/12), AGI [#18](https://github.com/Autonomous-Giving-Incorporated/Autonomous-Giving-Incorporated/pull/18) merged. Live `data/` untouched | SYNTHETIC_ONLY |
| C3 public-data policy | AGI `PUBLIC_DATA_POLICY.md` still PROPOSED. PS written deferral. IR restatement pointer. Chat is not the four seats | PROPOSED |
| SPEC-026 P1 Givebutter / Donorbox / CSV twin | Merged [PS #52](https://github.com/Autonomous-Giving-Incorporated/Portfolio-Signals/pull/52) `4c38323`. CODE_SHIPPED. Not live. Not READY. No invented `workers.dev` | CODE_SHIPPED |
| IR public shell | `data/public-impact.json` still `outcomes: []` / `gated:public_shell` | OBSERVED empty |
| Named Worker `portfolio-signals` | ABSENT on the connected Cloudflare account. Suite `/portfolio-signals` and `/impact-relay` still proxy GET/HEAD to Vercel | OBSERVED 2026-08-15; not re-listed |
| Live every.org gift | Still operator-owned | PENDING [#20](https://github.com/Autonomous-Giving-Incorporated/Portfolio-Signals/issues/20) |
| MFA onboarding-pack dry-run | Still operator-owned | PENDING [#18](https://github.com/Autonomous-Giving-Incorporated/Portfolio-Signals/issues/18) |
| Hosted isolated restore | Local-synthetic observed earlier; hosted drill still open | PENDING [#19](https://github.com/Autonomous-Giving-Incorporated/Portfolio-Signals/issues/19) reopened |
| Specs dependency pins | PyYAML `>=6.0.3,<7` (#14) and jsonschema `>=4.26.0,<5` (#15) still on main; tip is now `dcf7f6b` after #18 | OBSERVED in-repo |
| Optional IR doc hygiene | Merged [IR #17](https://github.com/Autonomous-Giving-Incorporated/Impact-Relay/pull/17) `59e3e8f`: 413 collected tests; personal/org Pages 404; host screens in Portfolio Signals | OBSERVED docs |

Do not un-PARK SPEC-028. Do not add AGI auth on the public site. Do not claim `source=live` until an authorized `VERIFIED` outcome exists. Do not copy Civic Forge into live `data/`.

## Allocation middleware (design 2026-08-03)

| Item | Status |
| --- | --- |
| MVP package (pots, allocate, proof, packet, every.org adapter, UI) | Shipped |
| Local Node pilot + unit tests | OBSERVED |
| Director JWT (`org_hacker_dojo`) | OBSERVED — Fund-Intel #72 closed |
| Public HTTPS (Cloudflare quick tunnel) | OBSERVED ephemeral — #71 closed |
| Seed-loop allocate→proof→packet | OBSERVED — `npm run accept:seed-loop` |
| Durable named host | Designed: Cloudflare Worker `portfolio-signals` + existing Supabase ([ADR-013](../../adr/ADR-013-cloudflare-workers-public-host.md)). Named Worker **ABSENT**. Do not invent a `workers.dev` URL. Render / Fly / Railway are not the path |
| Live every.org webhook + director browser sign-off | **Open** — [Portfolio-Signals #20](https://github.com/Autonomous-Giving-Incorporated/Portfolio-Signals/issues/20). Historical issue numbers #73 / #74 are not in this repository |
| SPEC-026 P1 Givebutter / Donorbox | Merged [PS #52](https://github.com/Autonomous-Giving-Incorporated/Portfolio-Signals/pull/52) `4c38323`. CODE_SHIPPED; operator-owned pointing; Stripe `/webhooks/stripe` stays 404 |

Specs: [design](specs/2026-08-03-allocation-middleware-design.md) · [MVP plan](plans/2026-08-03-allocation-middleware.md) · [pilot hosting](plans/2026-08-03-hacker-dojo-pilot-hosting.md).

## Suite commercial onboarding (Portfolio-Signals + IR)

**Hub:** Portfolio-Signals [`docs/SUITE-ONBOARDING.md`](https://github.com/Autonomous-Giving-Incorporated/Portfolio-Signals/blob/main/docs/SUITE-ONBOARDING.md) (done without login vs needs every.org/admin).

**Evidence SoT:** Portfolio-Signals [`docs/CURRENT-STATE.md`](https://github.com/Autonomous-Giving-Incorporated/Portfolio-Signals/blob/main/docs/CURRENT-STATE.md) (labels OBSERVED / PENDING / BLOCKED).

**This-repo continuation note (2026-08-08):** [plans/2026-08-08-suite-continuation.md](plans/2026-08-08-suite-continuation.md). Superseded for operator order by the 2026-08-22 Portfolio-Signals plan above. Historical issue numbers in that 08 August note (#73 / #74) do not exist on current Portfolio-Signals.

### Slices

| Slice | Topic | Runbook (Portfolio-Signals) | Status |
| --- | --- | --- | --- |
| C | Operator / director access | `docs/OPERATOR-ACCESS-ONBOARDING.md` | **People registered** (see matrix); MFA incomplete for Qi/Ed |
| B | Client provision → publish → activate | `docs/COMMERCIAL-CLIENT-LIFECYCLE.md` | Dry-run OBSERVED (`org_hacker_dojo`) |
| Doc pack | Private org-proof documents | `docs/CLIENT-ONBOARDING-PACK.md` | **Platform schema + Edge OBSERVED** 2026-08-08; MFA dry-run **PENDING** ([Portfolio-Signals #18](https://github.com/Autonomous-Giving-Incorporated/Portfolio-Signals/issues/18); historical #104/#113) |
| D | Second tenant + IR template clone | `docs/SECOND-TENANT-ONBOARDING.md` | Dry-run OBSERVED |
| Harden | Tenant chrome + HD data gate | — | **OBSERVED** on main #108, #111, #112 |

### People matrix (platform `utdioxwiskzatwoejgiu`)

Recorded 2026-08-08. This 2026-08-22 refresh did **not** re-verify MFA enrollment.

| Email | Role | Scope | MFA |
| --- | --- | --- | --- |
| `scrimshawlife@gmail.com` | `master_admin` | All clients + platform admin | Enforced |
| `qi@enkeyai.com` | `master_admin` | All clients + platform admin | Pending TOTP → then `set-mfa-enforced` |
| `ed@hackerdojo.org` | **director only** | **`org_hacker_dojo` only** — not `platform_administrators`; no other client memberships | Pending TOTP → then `set-mfa-enforced` (action_link regenerated operator-local 2026-08-08) |

**Access rule (Ed):** Hacker Dojo tenant dataset and tenant-scoped workspace/onboarding functions for that `client_id` only. Master admins bypass membership checks; Ed does not.

### Recent Portfolio-Signals merges (2026-08-08)

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

Those numbers are from the 08 August record. Dry-runs (C/B/D): OBSERVED. Document pack: tables REST 200 + Edge OPTIONS 200 / unauth 401 on `utdioxwiskzatwoejgiu` (2026-08-08). MFA workspace dry-run still PENDING before full pack OBSERVED.

**every.org setup wizard:** fixture chargeIds (`fixture-*`) do not mark Connected; only live (non-fixture) POSTs do (`counts.liveGifts` / `lastLiveGift`).

**Document pack (phase 1):** upload → `campaign-private` → suggest type → human confirm → pack ready. Never auto-promotes CRM; xlsx/csv parked for future list quarantine.

**Optional ops runbooks (code/docs ready; dashboards operator):** durable host preflight, custom SMTP, secret hygiene — see suite hub.

## Next operator actions

Ordered for least external dependency first. Detail: Portfolio-Signals [2026-08-22 continuation plan](https://github.com/Autonomous-Giving-Incorporated/Portfolio-Signals/blob/main/docs/PRODUCTION-READINESS-AND-CONTINUATION-2026-08-22.md) Wave 1.

1. **Wave 1.1:** MFA-enforced Client Onboarding Pack dry-run on `org_hacker_dojo` — [Portfolio-Signals #18](https://github.com/Autonomous-Giving-Incorporated/Portfolio-Signals/issues/18).  
2. **Wave 1.2:** hosted isolated restore drill — [#19](https://github.com/Autonomous-Giving-Incorporated/Portfolio-Signals/issues/19).  
3. **Wave 1.3:** sign or keep deferring C3. Still PROPOSED. Four-seat sign-off is human.  
4. **Wave 2:** durable named Worker + live every.org gift + director browser allocate — [#20](https://github.com/Autonomous-Giving-Incorporated/Portfolio-Signals/issues/20). Do not invent a Worker URL.  
5. **Do not:** unpark SPEC-028, add AGI `/login`, publish Civic Forge, or mark READY from this file.  
6. **Security:** revoke any PAT pasted into chat; regenerate if still needed.
