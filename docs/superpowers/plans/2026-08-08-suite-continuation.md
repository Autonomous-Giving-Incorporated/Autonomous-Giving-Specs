# Suite continuation plan (informative)

> **Status:** Draft 2026-08-08. Tracks operator- and implementation-facing work after Portofolio-Signals #104–#112.  
> **Not a normative SPEC.** Runtime evidence remains Portofolio-Signals [`docs/CURRENT-STATE.md`](https://github.com/scrimshawlife-ctrl/Portofolio-Signals/blob/main/docs/CURRENT-STATE.md).  
> **Map:** [IMPLEMENTATION-PROGRESS](../IMPLEMENTATION-PROGRESS.md) · suite hub [SUITE-ONBOARDING](https://github.com/scrimshawlife-ctrl/Portofolio-Signals/blob/main/docs/SUITE-ONBOARDING.md).

**Goal:** Finish commercial onboarding activation on platform Supabase, complete people MFA, and close the allocation pilot operator path (every.org + director sign-off)—without reopening `production_import` or outreach.

**Architecture:** Platform project `utdioxwiskzatwoejgiu` only. Tenant isolation via `client_memberships` + `platform_administrators`. Hacker Dojo (`org_hacker_dojo`) is reference tenant; Ed is director **only** on that client. Onboarding pack stays campaign-private until human confirm; pack `ready` ≠ import authorized.

**Tech stack:** Supabase CLI / Management API, Deno Edge Functions, Portfolio Signals workspace, allocation-middleware Node pilot.

---

## Where we are (snapshot)

| Area | State |
| --- | --- |
| Suite rewrites + PS subpath assets | OBSERVED (#106) |
| Legal / compliance chrome | OBSERVED (#107) |
| Tenant chrome only when logged in | OBSERVED (#108) |
| Master admins: primary + Qi | OBSERVED (Qi MFA pending) (#109) |
| HD director Ed | OBSERVED membership; MFA pending (#110) |
| HD canonical data behind login | OBSERVED (#111, residual fixtures #112) |
| Onboarding pack **code** | MERGED (#104); activate script on main (#112) |
| Onboarding pack **platform** | Schema + Edge OBSERVED 2026-08-08; MFA dry-run PENDING |
| C/B/D dry-runs | OBSERVED |
| Allocation pilot local/ephemeral HTTPS / seed-loop | OBSERVED |
| every.org live webhook + full #74 | OPEN |

### Access model (do not confuse)

| Principal | Platform admin | Clients |
| --- | --- | --- |
| `scrimshawlife@gmail.com` | Yes (`master_admin`) | All (bypass) |
| `qi@enkeyai.com` | Yes (`master_admin`) | All (bypass) |
| `ed@hackerdojo.org` | **No** | **`org_hacker_dojo` director only** |

Ed sees Hacker Dojo dataset and tenant-scoped functions (workspace, onboarding pack for that `client_id` when deployed). He does **not** get other tenants or platform admin surfaces.

---

## Workstream A — Platform activate onboarding pack (highest leverage)

**Owner:** operator with Supabase access to `utdioxwiskzatwoejgiu`  
**Blocked on:** `supabase login` or `SUPABASE_ACCESS_TOKEN`  
**Implementation plan:** Portofolio-Signals [`plans/2026-08-08-platform-activate-and-tenant-harden.md`](https://github.com/scrimshawlife-ctrl/Portofolio-Signals/blob/main/docs/superpowers/plans/2026-08-08-platform-activate-and-tenant-harden.md)  
**Script:** `scripts/platform/activate-onboarding-pack.sh`

- [x] **A1.** `supabase login` (or export access token); `supabase link --project-ref utdioxwiskzatwoejgiu`
- [x] **A2.** Apply migrations `202608080001_client_onboarding_pack.sql`, `202608080002_onboarding_pack_mime_types.sql` (via activate script or `apply-migrations.sh remote-linked` with `PLATFORM_CONFIRM_PROJECT_REF=utdioxwiskzatwoejgiu`)
- [x] **A3.** Deploy Edge: `upload-onboarding-document`, `onboarding-document-url`
- [x] **A4.** Probe: REST `client_onboarding_packs` → 200; Edge OPTIONS/POST without JWT → not 404 (expect 401)
- [x] **A5.** (CURRENT-STATE PLATFORM_SCHEMA_AND_EDGE_OBSERVED; full pack OBSERVED after C) Update CURRENT-STATE: tables + Edge **OBSERVED**; pack dry-run still PENDING until MFA session

**Exit:** PostgREST no longer PGRST205 for pack tables; Edge functions respond.

---

## Workstream B — People completion (Qi + Ed)

**Owner:** platform master_admin + each user for TOTP  
**Blocked on:** Supabase Auth email rate limits (invite/magic-link)

- [x] **B1.** Action links regenerated 2026-08-08 via Admin `generate_link` → operator-local file (never commit); humans still must open links
- [ ] **B2.** Qi: first workspace login → enroll TOTP → operator `set-mfa-enforced` for Qi
- [ ] **B3.** Ed: first workspace login → enroll TOTP → operator `set-mfa-enforced` for Ed
- [ ] **B4.** Verify Ed: `get_workspace_context` shows active director on `org_hacker_dojo` only; `is_master_admin=false`
- [ ] **B5.** Verify Qi: `is_master_admin=true`; can open HD data without HD membership (master path)

**Exit:** Both non-primary people can sign in with MFA enforced; CURRENT-STATE people lines updated.

---

## Workstream C — Onboarding pack MFA dry-run

**Depends on:** A + MFA for at least one director or master_admin  
**Runbook:** Portofolio-Signals `docs/CLIENT-ONBOARDING-PACK.md`

- [ ] **C1.** Workspace → Onboarding pack for `org_hacker_dojo`
- [ ] **C2.** Upload five required document types (suggest → human confirm)
- [ ] **C3.** Park one xlsx/csv (list quarantine path; no CRM promote)
- [ ] **C4.** Confirm pack `ready` semantics: **does not** enable production_import / outreach / auto-activate
- [ ] **C5.** Mark CURRENT-STATE `client_onboarding_pack.status: OBSERVED`

**Exit:** Documented dry-run PASS; production_import remains BLOCKED.

---

## Workstream D — Allocation pilot close (#73 / #74)

**Depends on:** director login; preferably durable HTTPS for production webhook  
**Issues:** [Portofolio-Signals #73](https://github.com/scrimshawlife-ctrl/Portofolio-Signals/issues/73), [#74](https://github.com/scrimshawlife-ctrl/Portofolio-Signals/issues/74)

- [ ] **D1.** (Optional but recommended) Durable named host — `ALLOCATION-DURABLE-HOST.md` + `npm run preflight:durable`; set `PUBLIC_BASE_URL`, `ALLOW_OPERATOR_TOKEN_FALLBACK=0`
- [ ] **D2.** Or temporary cloudflared tunnel for a controlled test window
- [ ] **D3.** every.org HD nonprofit admin: register webhook URL from `/setup.html`
- [ ] **D4.** Live (non-fixture) test gift → setup shows **Connected** (`liveGifts` ≥ 1)
- [ ] **D5.** Director browser allocate → proof → packet; comment sign-off on #74
- [ ] **D6.** Close #73 / remaining #74 with evidence pointers (no secrets)

**Exit:** Live gift path OBSERVED; full director acceptance recorded.

---

## Workstream E — Optional hygiene (parallel anytime)

| Item | When |
| --- | --- |
| Custom SMTP ([PLATFORM-AUTH-SMTP.md](https://github.com/scrimshawlife-ctrl/Portofolio-Signals/blob/main/docs/PLATFORM-AUTH-SMTP.md)) | Invite volume / rate limits painful |
| Secret rotation ([OPERATOR-SECRET-HYGIENE.md](https://github.com/scrimshawlife-ctrl/Portofolio-Signals/blob/main/docs/OPERATOR-SECRET-HYGIENE.md)) | After share or offboard |
| Synthetic full B provision (non-HD client) | Sales path practice; do not re-activate HD |
| Paired FI + IR second-tenant exercise | After D dry-run if sales needs demo clone |
| AGI Project #3 / PLATFORM.md narrative sync | After pack OBSERVED or pilot close |

---

## Explicit non-goals (this plan)

- Production CRM / workbook import (`production_import: BLOCKED`)
- Outreach authority
- `service_role` on Vercel or browser
- Treating Ed as platform master_admin
- New normative SPECs for suite onboarding (stay informative here)

---

## Recommended execution order

```text
A (platform pack)  ──┬──►  C (pack dry-run)
B (people / MFA)   ──┘
        │
        ▼
D (every.org + director)   // may run after B even if C delayed
E (optional) anytime
```

If Supabase token is available **today**, do **A** first (unblocks product surface). If only humans are available, do **B1–B3**. Do not block D on C if allocation demo is the priority—pack is orthogonal to live gifts.

---

## Success criteria (suite “continuation complete”)

1. Pack tables + Edge OBSERVED on platform; MFA dry-run recorded.  
2. Qi and Ed MFA enforced; Ed scoped to `org_hacker_dojo` only.  
3. #73 live webhook path and #74 director sign-off closed or explicitly deferred with owner.  
4. CURRENT-STATE and this Specs progress map agree; no secrets in git.  
5. `production_import` still BLOCKED; outreach NOT_GRANTED.

---

## Related

| Doc | Role |
| --- | --- |
| [IMPLEMENTATION-PROGRESS.md](../IMPLEMENTATION-PROGRESS.md) | Status map |
| Portofolio-Signals `docs/SUITE-ONBOARDING.md` | Operator hub |
| Portofolio-Signals `docs/CURRENT-STATE.md` | Evidence SoT |
| [2026-08-03-hacker-dojo-pilot-hosting.md](2026-08-03-hacker-dojo-pilot-hosting.md) | Pilot host status |
| Portofolio-Signals `plans/2026-08-08-platform-activate-and-tenant-harden.md` | A checklist detail |
| Portofolio-Signals `plans/2026-08-08-client-onboarding-pack.md` | Pack implementation history |
