# Allocation Middleware MVP Implementation Plan

> **Status (2026-08-07):** MVP **shipped** in Fund-Intel `services/allocation-middleware/` (domain, every.org webhook adapter, UI, file store, proof, director JWT, pilot seed, smoke, seed-loop accept). Pilot hosting progress: local Node + director auth + ephemeral public HTTPS OBSERVED; **live every.org webhook still open** — see [hacker-dojo-pilot-hosting](2026-08-03-hacker-dojo-pilot-hosting.md). Task checkboxes below are retained as historical execution checklist.

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Ship a transaction-light allocation middleware MVP: every.org gift summaries credit campaign/program pots; humans approve allocations; exceptions drive day-to-day ops; trail and board packet expose the story.

**Architecture:** Modular monolith package inside Fund-Intel (`services/allocation-middleware/`) with pure domain modules (pots, gifts, allocations, exceptions), an every.org connector adapter, HTTP API (webhook + operator endpoints), and a minimal static operator UI. Persistence starts as an in-memory repository behind an interface so unit tests need no database. Aligns with Specs SPEC-002A / SPEC-020 Profile B modular-monolith idea; **preferred durable path for new work** is Supabase PostgreSQL with Workers talking to Supabase ([ADR-013](../../../adr/ADR-013-cloudflare-workers-public-host.md), [SPEC-022](../../../specs/SPEC-022-postgresql-persistence.md)). [ADR-012](../../../adr/ADR-012-render-first-platform.md) Render PostgreSQL notes are historical.

**Tech Stack:** Node.js 22, ESM (`.mjs`), `node:test` + `node:assert/strict`, built-in `node:http`, no framework required for MVP. Optional later: Supabase tables + RLS (Fund-Intel already has tenant patterns).

**Spec:** [docs/superpowers/specs/2026-08-03-allocation-middleware-design.md](../specs/2026-08-03-allocation-middleware-design.md)

## Global Constraints

- Transaction-light: gift **summaries** and pot **balances** only — no bank/QuickBooks/Plaid.
- Canonical connector: **every.org**; credit default uses **`netAmount`**.
- Pot hierarchy: **campaign pot** (fundraiser | `General`) → **program slice** (designation | `Undesignated`).
- Idempotency key: every.org **`chargeId`**.
- Human gate: **allocation approve** before commit; no auto-allocate in MVP.
- Donor PII (name/email) not required for allocation UX; do not surface in default trail.
- Client UI language: pots / allocate / inbox / trail / packet — not platform lifecycle jargon.
- Package private; Node `>=22 <23`; ESM `"type": "module"`.
- TDD: failing test → implement → pass → commit per task.
- Do not implement Givebutter/Donorbox/portfolio in this plan (adapter interface only).

## File map (create unless noted)

```text
Fund-Intel/
  services/allocation-middleware/
    package.json
    README.md
    src/
      domain/
        types.mjs              # Org, pots, gifts, allocations, exceptions
        money.mjs              # parse/compare decimal amounts as strings
        pots.mjs               # resolve hierarchy, credit, available
        allocate.mjs           # propose/approve against available
        exceptions.mjs         # exception factory + codes
      connectors/
        everyorg.mjs           # normalize webhook → GiftSummaryDraft
        interface.mjs          # JSDoc Connector shape
      app/
        store.mjs              # InMemoryStore implementing repository ports
        service.mjs            # Application service orchestration
      http/
        server.mjs             # createServer routes
    test/
      money.test.mjs
      pots.test.mjs
      everyorg.test.mjs
      allocate.test.mjs
      service.test.mjs
      server.test.mjs
    public/
      index.html               # Minimal operator UI (Available / Allocate / Inbox)
  docs/ALLOCATION-MIDDLEWARE.md   # Modify: add implementation status + runbook link
```

---

### Task 1: Scaffold package + money helpers

**Files:**
- Create: `services/allocation-middleware/package.json`
- Create: `services/allocation-middleware/src/domain/money.mjs`
- Create: `services/allocation-middleware/test/money.test.mjs`
- Create: `services/allocation-middleware/README.md`

**Interfaces:**
- Produces: `parseAmount(str) → { cents: bigint }` (USD cents, 2 decimal places); `addCents(a,b)`, `subCents(a,b)`, `formatCents(cents) → string`; throws on invalid.

- [ ] **Step 1: Write the failing test**

```js
// services/allocation-middleware/test/money.test.mjs
import assert from 'node:assert/strict';
import { test } from 'node:test';
import { parseAmount, addCents, subCents, formatCents } from '../src/domain/money.mjs';

test('parseAmount accepts decimal dollars as cents', () => {
  assert.equal(parseAmount('1000.00').cents, 100000n);
  assert.equal(parseAmount('970.07').cents, 97007n);
});

test('add and sub cents', () => {
  assert.equal(addCents(100n, 50n), 150n);
  assert.equal(subCents(100n, 40n), 60n);
});

test('formatCents', () => {
  assert.equal(formatCents(97007n), '970.07');
});

test('parseAmount rejects garbage', () => {
  assert.throws(() => parseAmount('abc'));
});
```

- [ ] **Step 2: Run test to verify it fails**

Run: `cd services/allocation-middleware && npm test`  
Expected: FAIL (module not found / package missing)

- [ ] **Step 3: Write package.json + minimal implementation**

```json
{
  "name": "@agi/allocation-middleware",
  "private": true,
  "version": "0.1.0",
  "type": "module",
  "engines": { "node": ">=22 <23" },
  "scripts": {
    "test": "node --test",
    "start": "node src/http/server.mjs"
  }
}
```

```js
// services/allocation-middleware/src/domain/money.mjs
export function parseAmount(str) {
  if (typeof str !== 'string' || !/^-?\d+(\.\d{1,2})?$/.test(str.trim())) {
    throw new Error(`invalid amount: ${str}`);
  }
  const [w, f = ''] = str.trim().split('.');
  const frac = (f + '00').slice(0, 2);
  const sign = w.startsWith('-') ? -1n : 1n;
  const whole = BigInt(w.replace('-', '') || '0');
  return { cents: sign * (whole * 100n + BigInt(frac)) };
}

export function addCents(a, b) {
  return a + b;
}

export function subCents(a, b) {
  return a - b;
}

export function formatCents(cents) {
  const sign = cents < 0n ? '-' : '';
  const abs = cents < 0n ? -cents : cents;
  const whole = abs / 100n;
  const frac = (abs % 100n).toString().padStart(2, '0');
  return `${sign}${whole}.${frac}`;
}
```

README one-pager: purpose, `npm test`, design link to Specs.

- [ ] **Step 4: Run tests — expect PASS**

Run: `cd services/allocation-middleware && npm test`

- [ ] **Step 5: Commit**

```bash
cd /Users/appliedalchemylabs/Fund-Intel
git add services/allocation-middleware
git commit -m "feat(allocation-middleware): scaffold package and money helpers"
```

---

### Task 2: Domain types + pot credit with hierarchy

**Files:**
- Create: `services/allocation-middleware/src/domain/types.mjs`
- Create: `services/allocation-middleware/src/domain/pots.mjs`
- Create: `services/allocation-middleware/test/pots.test.mjs`

**Interfaces:**
- Produces:
  - `normalizeKey(s) → string` (trim + lowercase)
  - `resolvePotPath({ fundraiserKey, designationKey }) → { campaignKey, programKey }`
  - `creditGift(state, gift) → { state, created: boolean, exception? }`
- Gift shape: `{ chargeId, orgId, campaignKey, programKey, netCents, grossCents, currency, donatedAt, source: 'every.org' }`
- State shape (in-memory): `{ gifts: Map, pots: Map, allocations: Map, exceptions: [] }`  
  Pot key: `` `${orgId}|${campaignKey}|${programKey}` ``  
  Pot: `{ orgId, campaignKey, programKey, creditedCents, allocatedCents }`  
  `available = credited − allocated`

- [ ] **Step 1: Write the failing tests**

```js
// services/allocation-middleware/test/pots.test.mjs
import assert from 'node:assert/strict';
import { test } from 'node:test';
import { resolvePotPath, creditGift, availableCents, emptyState } from '../src/domain/pots.mjs';

test('resolvePotPath uses General and Undesignated defaults', () => {
  assert.deepEqual(resolvePotPath({}), {
    campaignKey: 'general',
    programKey: 'undesignated',
  });
  assert.deepEqual(
    resolvePotPath({ fundraiserKey: 'Hardware Drive', designationKey: 'Laptops' }),
    { campaignKey: 'hardware drive', programKey: 'laptops' },
  );
});

test('creditGift is idempotent on chargeId', () => {
  let state = emptyState();
  const gift = {
    chargeId: 'chg-1',
    orgId: 'org_1',
    campaignKey: 'hardware drive',
    programKey: 'laptops',
    netCents: 97007n,
    grossCents: 100000n,
    currency: 'USD',
    donatedAt: '2026-08-03T00:00:00Z',
    source: 'every.org',
  };
  const r1 = creditGift(state, gift);
  assert.equal(r1.created, true);
  const r2 = creditGift(r1.state, gift);
  assert.equal(r2.created, false);
  assert.equal(availableCents(r2.state, 'org_1', 'hardware drive', 'laptops'), 97007n);
});
```

- [ ] **Step 2: Run — expect FAIL**

Run: `cd services/allocation-middleware && node --test test/pots.test.mjs`

- [ ] **Step 3: Implement types.mjs + pots.mjs**

```js
// services/allocation-middleware/src/domain/types.mjs
/** @typedef {{ orgId: string, campaignKey: string, programKey: string, creditedCents: bigint, allocatedCents: bigint }} Pot */
/** @typedef {{ chargeId: string, orgId: string, campaignKey: string, programKey: string, netCents: bigint, grossCents: bigint, currency: string, donatedAt: string, source: string }} GiftSummary */
/** @typedef {{ id: string, orgId: string, campaignKey: string, programKey: string, amountCents: bigint, purpose: string, status: 'approved', approvedAt: string, approvedBy: string }} Allocation */
/** @typedef {{ id: string, orgId: string, code: string, message: string, open: boolean, createdAt: string, ref?: object }} ExceptionItem */

export const DEFAULT_CURRENCY = 'USD';
```

```js
// services/allocation-middleware/src/domain/pots.mjs
import { addCents, subCents } from './money.mjs';

export function emptyState() {
  return {
    gifts: new Map(),
    pots: new Map(),
    allocations: new Map(),
    exceptions: [],
  };
}

export function normalizeKey(s) {
  if (s == null || String(s).trim() === '') return '';
  return String(s).trim().toLowerCase();
}

export function resolvePotPath({ fundraiserKey, designationKey } = {}) {
  const campaignKey = normalizeKey(fundraiserKey) || 'general';
  const programKey = normalizeKey(designationKey) || 'undesignated';
  return { campaignKey, programKey };
}

function potId(orgId, campaignKey, programKey) {
  return `${orgId}|${campaignKey}|${programKey}`;
}

export function availableCents(state, orgId, campaignKey, programKey) {
  const p = state.pots.get(potId(orgId, campaignKey, programKey));
  if (!p) return 0n;
  return subCents(p.creditedCents, p.allocatedCents);
}

export function creditGift(state, gift) {
  if (state.gifts.has(gift.chargeId)) {
    return { state, created: false };
  }
  if (gift.currency !== 'USD') {
    const ex = {
      id: `ex_${gift.chargeId}_currency`,
      orgId: gift.orgId,
      code: 'CURRENCY_MISMATCH',
      message: `currency ${gift.currency} not USD`,
      open: true,
      createdAt: new Date().toISOString(),
      ref: { chargeId: gift.chargeId },
    };
    return {
      state: {
        ...state,
        exceptions: [...state.exceptions, ex],
      },
      created: false,
      exception: ex,
    };
  }
  const gifts = new Map(state.gifts);
  gifts.set(gift.chargeId, gift);
  const pots = new Map(state.pots);
  const id = potId(gift.orgId, gift.campaignKey, gift.programKey);
  const prev = pots.get(id) || {
    orgId: gift.orgId,
    campaignKey: gift.campaignKey,
    programKey: gift.programKey,
    creditedCents: 0n,
    allocatedCents: 0n,
  };
  pots.set(id, {
    ...prev,
    creditedCents: addCents(prev.creditedCents, gift.netCents),
  });
  return { state: { ...state, gifts, pots }, created: true };
}
```

- [ ] **Step 4: Run — expect PASS**

Run: `cd services/allocation-middleware && npm test`

- [ ] **Step 5: Commit**

```bash
git add services/allocation-middleware
git commit -m "feat(allocation-middleware): pot hierarchy and idempotent gift credit"
```

---

### Task 3: every.org webhook normalizer

**Files:**
- Create: `services/allocation-middleware/src/connectors/everyorg.mjs`
- Create: `services/allocation-middleware/src/connectors/interface.mjs`
- Create: `services/allocation-middleware/test/everyorg.test.mjs`

**Interfaces:**
- Produces: `normalizeEveryOrgDonation(payload, { orgId }) → GiftSummary`
- Uses: `resolvePotPath`, `parseAmount` on `netAmount` / `amount`

- [ ] **Step 1: Write failing test with sample payload from every.org docs**

```js
// services/allocation-middleware/test/everyorg.test.mjs
import assert from 'node:assert/strict';
import { test } from 'node:test';
import { normalizeEveryOrgDonation } from '../src/connectors/everyorg.mjs';

const sample = {
  chargeId: 'somerandomuuid',
  designation: 'Laptops',
  toNonprofit: { slug: 'community-ai-lab', name: 'Community AI Lab' },
  amount: '1000.00',
  netAmount: '970.07',
  currency: 'USD',
  frequency: 'One-time',
  donationDate: '2022-02-03T05:00:16.175Z',
  fromFundraiser: {
    id: 'fr_1',
    title: 'Hardware Drive',
    slug: 'hardware-drive',
  },
  // firstName/email present — must not be required on GiftSummary
  firstName: 'Jane',
  email: 'jane@example.org',
};

test('normalizeEveryOrgDonation maps fundraiser and designation', () => {
  const g = normalizeEveryOrgDonation(sample, { orgId: 'org_1' });
  assert.equal(g.chargeId, 'somerandomuuid');
  assert.equal(g.orgId, 'org_1');
  assert.equal(g.campaignKey, 'hardware drive'); // from title normalized
  assert.equal(g.programKey, 'laptops');
  assert.equal(g.netCents, 97007n);
  assert.equal(g.grossCents, 100000n);
  assert.equal(g.currency, 'USD');
  assert.equal(g.source, 'every.org');
  assert.equal('email' in g, false);
});

test('defaults General and Undesignated', () => {
  const g = normalizeEveryOrgDonation(
    {
      chargeId: 'c2',
      amount: '10.00',
      netAmount: '10.00',
      currency: 'USD',
      donationDate: '2026-01-01T00:00:00Z',
      toNonprofit: { slug: 'x', name: 'X' },
    },
    { orgId: 'org_1' },
  );
  assert.equal(g.campaignKey, 'general');
  assert.equal(g.programKey, 'undesignated');
});
```

- [ ] **Step 2: Run — FAIL**

- [ ] **Step 3: Implement**

```js
// services/allocation-middleware/src/connectors/interface.mjs
/**
 * @typedef {object} ConnectorContext
 * @property {string} orgId
 *
 * @typedef {object} DonationConnector
 * @property {string} id
 * @property {(payload: unknown, ctx: ConnectorContext) => import('../domain/types.mjs').GiftSummary} normalizeDonation
 */

export const CONNECTOR_EVERY_ORG = 'every.org';
```

```js
// services/allocation-middleware/src/connectors/everyorg.mjs
import { parseAmount } from '../domain/money.mjs';
import { resolvePotPath, normalizeKey } from '../domain/pots.mjs';

export function normalizeEveryOrgDonation(payload, { orgId }) {
  if (!payload || typeof payload !== 'object') throw new Error('invalid payload');
  const p = /** @type {Record<string, any>} */ (payload);
  if (!p.chargeId) throw new Error('chargeId required');
  const fundraiserKey =
    p.fromFundraiser?.title || p.fromFundraiser?.slug || p.fromFundraiser?.id || '';
  const { campaignKey, programKey } = resolvePotPath({
    fundraiserKey,
    designationKey: p.designation,
  });
  const net = parseAmount(String(p.netAmount ?? p.amount));
  const gross = parseAmount(String(p.amount ?? p.netAmount));
  return {
    chargeId: String(p.chargeId),
    orgId,
    campaignKey,
    programKey,
    netCents: net.cents,
    grossCents: gross.cents,
    currency: String(p.currency || 'USD'),
    donatedAt: String(p.donationDate || new Date().toISOString()),
    source: 'every.org',
  };
}
```

- [ ] **Step 4: PASS + commit**

```bash
git commit -am "feat(allocation-middleware): every.org donation normalizer"
```

---

### Task 4: Allocate + approve against available

**Files:**
- Create: `services/allocation-middleware/src/domain/allocate.mjs`
- Create: `services/allocation-middleware/test/allocate.test.mjs`

**Interfaces:**
- Produces: `approveAllocation(state, { orgId, campaignKey, programKey, amountCents, purpose, approvedBy, id, approvedAt }) → { state } | throws`
- On success: increase pot `allocatedCents`; store allocation `status: 'approved'`
- Throws `OVER_ALLOCATION` if amount > available

- [ ] **Step 1: Failing tests**

```js
import assert from 'node:assert/strict';
import { test } from 'node:test';
import { emptyState, creditGift, availableCents } from '../src/domain/pots.mjs';
import { approveAllocation } from '../src/domain/allocate.mjs';

function fundedState() {
  let state = emptyState();
  ({ state } = creditGift(state, {
    chargeId: 'c1',
    orgId: 'org_1',
    campaignKey: 'general',
    programKey: 'undesignated',
    netCents: 50000n,
    grossCents: 50000n,
    currency: 'USD',
    donatedAt: '2026-08-03T00:00:00Z',
    source: 'every.org',
  }));
  return state;
}

test('approveAllocation reserves available funds', () => {
  let state = fundedState();
  ({ state } = approveAllocation(state, {
    id: 'alloc_1',
    orgId: 'org_1',
    campaignKey: 'general',
    programKey: 'undesignated',
    amountCents: 20000n,
    purpose: 'Laptops',
    approvedBy: 'director@example.org',
    approvedAt: '2026-08-03T12:00:00Z',
  }));
  assert.equal(availableCents(state, 'org_1', 'general', 'undesignated'), 30000n);
  assert.equal(state.allocations.get('alloc_1').status, 'approved');
});

test('approveAllocation blocks over-allocation', () => {
  const state = fundedState();
  assert.throws(
    () =>
      approveAllocation(state, {
        id: 'alloc_2',
        orgId: 'org_1',
        campaignKey: 'general',
        programKey: 'undesignated',
        amountCents: 999999n,
        purpose: 'Nope',
        approvedBy: 'director@example.org',
        approvedAt: '2026-08-03T12:00:00Z',
      }),
    /OVER_ALLOCATION/,
  );
});
```

- [ ] **Step 2–4: Implement, pass, commit**

```js
// services/allocation-middleware/src/domain/allocate.mjs
import { addCents, subCents } from './money.mjs';
import { availableCents } from './pots.mjs';

function potId(orgId, campaignKey, programKey) {
  return `${orgId}|${campaignKey}|${programKey}`;
}

export function approveAllocation(state, input) {
  const avail = availableCents(
    state,
    input.orgId,
    input.campaignKey,
    input.programKey,
  );
  if (input.amountCents <= 0n) throw new Error('INVALID_AMOUNT');
  if (input.amountCents > avail) throw new Error('OVER_ALLOCATION');
  if (state.allocations.has(input.id)) throw new Error('DUPLICATE_ALLOCATION');

  const pots = new Map(state.pots);
  const id = potId(input.orgId, input.campaignKey, input.programKey);
  const pot = pots.get(id);
  if (!pot) throw new Error('POT_NOT_FOUND');
  pots.set(id, {
    ...pot,
    allocatedCents: addCents(pot.allocatedCents, input.amountCents),
  });
  const allocations = new Map(state.allocations);
  allocations.set(input.id, {
    id: input.id,
    orgId: input.orgId,
    campaignKey: input.campaignKey,
    programKey: input.programKey,
    amountCents: input.amountCents,
    purpose: input.purpose,
    status: 'approved',
    approvedAt: input.approvedAt,
    approvedBy: input.approvedBy,
  });
  return { state: { ...state, pots, allocations } };
}
```

```bash
git commit -am "feat(allocation-middleware): human allocation approval against available"
```

---

### Task 5: Application service (ingest + list + allocate + exceptions)

**Files:**
- Create: `services/allocation-middleware/src/domain/exceptions.mjs`
- Create: `services/allocation-middleware/src/app/service.mjs`
- Create: `services/allocation-middleware/test/service.test.mjs`

**Interfaces:**
- Produces class or factory `createService({ orgId, now, idgen })`:
  - `ingestEveryOrg(payload) → { created, gift?, exception? }`
  - `listAvailable() → [{ campaignKey, programKey, credited, allocated, available }]`
  - `allocate({ campaignKey, programKey, amount, purpose, approvedBy }) → allocation`
  - `listExceptions({ openOnly }) → ExceptionItem[]`
  - `resolveException(id) → void`
  - `getTrail() → { gifts, allocations, pots }`
  - `getPacket() → { generatedAt, orgId, pots, allocations, totals }`

- [ ] **Step 1: Failing integration-style unit test**

```js
import assert from 'node:assert/strict';
import { test } from 'node:test';
import { createService } from '../src/app/service.mjs';

test('ingest every.org then allocate and build packet', () => {
  let n = 0;
  const svc = createService({
    orgId: 'org_1',
    now: () => '2026-08-03T12:00:00Z',
    idgen: () => `id_${++n}`,
  });
  const r = svc.ingestEveryOrg({
    chargeId: 'chg-9',
    amount: '100.00',
    netAmount: '100.00',
    currency: 'USD',
    donationDate: '2026-08-01T00:00:00Z',
    designation: 'Lab',
    fromFundraiser: { title: 'Spring', slug: 'spring' },
    toNonprofit: { slug: 'x', name: 'X' },
  });
  assert.equal(r.created, true);
  const avail = svc.listAvailable();
  assert.ok(avail.some((p) => p.programKey === 'lab' && p.available === '100.00'));
  const alloc = svc.allocate({
    campaignKey: 'spring',
    programKey: 'lab',
    amount: '40.00',
    purpose: 'Equipment',
    approvedBy: 'director@example.org',
  });
  assert.equal(alloc.status, 'approved');
  const packet = svc.getPacket();
  assert.equal(packet.totals.available, '60.00');
  assert.equal(packet.allocations.length, 1);
});
```

- [ ] **Step 2–4: Implement service wrapping domain, PASS, commit**

```js
// services/allocation-middleware/src/app/service.mjs
import { normalizeEveryOrgDonation } from '../connectors/everyorg.mjs';
import { emptyState, creditGift, availableCents } from '../domain/pots.mjs';
import { approveAllocation } from '../domain/allocate.mjs';
import { parseAmount, formatCents } from '../domain/money.mjs';

export function createService({ orgId, now = () => new Date().toISOString(), idgen = () => crypto.randomUUID() }) {
  let state = emptyState();

  return {
    ingestEveryOrg(payload) {
      const gift = normalizeEveryOrgDonation(payload, { orgId });
      const result = creditGift(state, gift);
      state = result.state;
      return result;
    },
    listAvailable() {
      return [...state.pots.values()]
        .filter((p) => p.orgId === orgId)
        .map((p) => ({
          campaignKey: p.campaignKey,
          programKey: p.programKey,
          credited: formatCents(p.creditedCents),
          allocated: formatCents(p.allocatedCents),
          available: formatCents(availableCents(state, orgId, p.campaignKey, p.programKey)),
        }));
    },
    allocate({ campaignKey, programKey, amount, purpose, approvedBy }) {
      const amountCents = parseAmount(amount).cents;
      const id = idgen();
      const result = approveAllocation(state, {
        id,
        orgId,
        campaignKey,
        programKey,
        amountCents,
        purpose,
        approvedBy,
        approvedAt: now(),
      });
      state = result.state;
      return state.allocations.get(id);
    },
    listExceptions({ openOnly = true } = {}) {
      return state.exceptions.filter((e) => e.orgId === orgId && (!openOnly || e.open));
    },
    resolveException(id) {
      state = {
        ...state,
        exceptions: state.exceptions.map((e) =>
          e.id === id ? { ...e, open: false } : e,
        ),
      };
    },
    getTrail() {
      return {
        gifts: [...state.gifts.values()].filter((g) => g.orgId === orgId),
        allocations: [...state.allocations.values()].filter((a) => a.orgId === orgId),
        pots: [...state.pots.values()].filter((p) => p.orgId === orgId),
      };
    },
    getPacket() {
      const pots = this.listAvailable();
      const allocations = [...state.allocations.values()].filter((a) => a.orgId === orgId);
      let credited = 0n;
      let allocated = 0n;
      for (const p of state.pots.values()) {
        if (p.orgId !== orgId) continue;
        credited += p.creditedCents;
        allocated += p.allocatedCents;
      }
      return {
        generatedAt: now(),
        orgId,
        pots,
        allocations: allocations.map((a) => ({
          id: a.id,
          campaignKey: a.campaignKey,
          programKey: a.programKey,
          amount: formatCents(a.amountCents),
          purpose: a.purpose,
          approvedAt: a.approvedAt,
        })),
        totals: {
          credited: formatCents(credited),
          allocated: formatCents(allocated),
          available: formatCents(credited - allocated),
        },
      };
    },
    /** @internal test helper */
    _state: () => state,
  };
}
```

```bash
git commit -am "feat(allocation-middleware): application service for ingest allocate packet"
```

---

### Task 6: HTTP server — webhook + operator API

**Files:**
- Create: `services/allocation-middleware/src/http/server.mjs`
- Create: `services/allocation-middleware/test/server.test.mjs`

**Interfaces:**
- Produces: `createServer({ service, webhookSecret? }) → http.Server`
- Routes:
  - `POST /webhooks/every-org` — body JSON → `ingestEveryOrg`; 200 `{ created }`
  - `GET /available` — listAvailable JSON
  - `POST /allocations` — JSON `{ campaignKey, programKey, amount, purpose, approvedBy }`
  - `GET /exceptions`
  - `POST /exceptions/:id/resolve`
  - `GET /trail`
  - `GET /packet`
  - `GET /` or static from `public/` if present

- [ ] **Step 1: Failing HTTP test** (listen on port 0, fetch)

```js
import assert from 'node:assert/strict';
import { afterEach, test } from 'node:test';
import { createService } from '../src/app/service.mjs';
import { createAllocationServer } from '../src/http/server.mjs';

const servers = [];
afterEach(async () => {
  await Promise.all(servers.splice(0).map((s) => new Promise((r) => s.close(r))));
});

async function start() {
  const service = createService({ orgId: 'org_1', idgen: () => 'fixed-id', now: () => '2026-08-03T12:00:00Z' });
  const server = createAllocationServer({ service });
  await new Promise((r) => server.listen(0, '127.0.0.1', r));
  servers.push(server);
  const { port } = server.address();
  return `http://127.0.0.1:${port}`;
}

test('webhook credits and available reflects gift', async () => {
  const base = await start();
  const wh = await fetch(`${base}/webhooks/every-org`, {
    method: 'POST',
    headers: { 'content-type': 'application/json' },
    body: JSON.stringify({
      chargeId: 'wh-1',
      amount: '25.00',
      netAmount: '25.00',
      currency: 'USD',
      donationDate: '2026-08-03T00:00:00Z',
      toNonprofit: { slug: 'x', name: 'X' },
    }),
  });
  assert.equal(wh.status, 200);
  const body = await wh.json();
  assert.equal(body.created, true);
  const av = await (await fetch(`${base}/available`)).json();
  assert.ok(av.some((p) => p.available === '25.00'));
});
```

- [ ] **Step 2–4: Implement minimal `node:http` router, pass, commit**

```js
// services/allocation-middleware/src/http/server.mjs
import http from 'node:http';
import { readFile } from 'node:fs/promises';
import path from 'node:path';
import { fileURLToPath } from 'node:url';

const __dirname = path.dirname(fileURLToPath(import.meta.url));

async function readJson(req) {
  const chunks = [];
  for await (const c of req) chunks.push(c);
  const raw = Buffer.concat(chunks).toString('utf8') || '{}';
  return JSON.parse(raw);
}

function send(res, status, data) {
  const body = JSON.stringify(data);
  res.writeHead(status, {
    'content-type': 'application/json',
    'content-length': Buffer.byteLength(body),
  });
  res.end(body);
}

export function createAllocationServer({ service }) {
  return http.createServer(async (req, res) => {
    try {
      const url = new URL(req.url || '/', 'http://localhost');
      if (req.method === 'POST' && url.pathname === '/webhooks/every-org') {
        const payload = await readJson(req);
        const result = service.ingestEveryOrg(payload);
        return send(res, 200, { created: result.created });
      }
      if (req.method === 'GET' && url.pathname === '/available') {
        return send(res, 200, service.listAvailable());
      }
      if (req.method === 'POST' && url.pathname === '/allocations') {
        const body = await readJson(req);
        const alloc = service.allocate(body);
        return send(res, 201, {
          id: alloc.id,
          status: alloc.status,
          amountCents: alloc.amountCents.toString(),
        });
      }
      if (req.method === 'GET' && url.pathname === '/exceptions') {
        return send(res, 200, service.listExceptions());
      }
      if (req.method === 'POST' && url.pathname.startsWith('/exceptions/') && url.pathname.endsWith('/resolve')) {
        const id = url.pathname.split('/')[2];
        service.resolveException(id);
        return send(res, 200, { ok: true });
      }
      if (req.method === 'GET' && url.pathname === '/trail') {
        const t = service.getTrail();
        return send(res, 200, {
          gifts: t.gifts.map((g) => ({ ...g, netCents: g.netCents.toString(), grossCents: g.grossCents.toString() })),
          allocations: t.allocations.map((a) => ({ ...a, amountCents: a.amountCents.toString() })),
        });
      }
      if (req.method === 'GET' && url.pathname === '/packet') {
        return send(res, 200, service.getPacket());
      }
      if (req.method === 'GET' && (url.pathname === '/' || url.pathname === '/index.html')) {
        const htmlPath = path.join(__dirname, '../../public/index.html');
        try {
          const html = await readFile(htmlPath, 'utf8');
          res.writeHead(200, { 'content-type': 'text/html; charset=utf-8' });
          return res.end(html);
        } catch {
          return send(res, 200, { service: 'allocation-middleware', ok: true });
        }
      }
      send(res, 404, { error: 'not_found' });
    } catch (err) {
      const message = err instanceof Error ? err.message : 'error';
      const status = message === 'OVER_ALLOCATION' ? 409 : 400;
      send(res, status, { error: message });
    }
  });
}

// CLI entry when run as main
const isMain = process.argv[1] && fileURLToPath(import.meta.url) === path.resolve(process.argv[1]);
if (isMain) {
  const { createService } = await import('../app/service.mjs');
  const orgId = process.env.ORG_ID || 'org_demo';
  const service = createService({ orgId });
  const server = createAllocationServer({ service });
  const port = Number(process.env.PORT || 8787);
  server.listen(port, () => {
    console.log(`allocation-middleware on http://127.0.0.1:${port} org=${orgId}`);
  });
}
```

```bash
git commit -am "feat(allocation-middleware): HTTP webhook and operator API"
```

---

### Task 7: Minimal operator UI (easy client surface)

**Files:**
- Create: `services/allocation-middleware/public/index.html`

**Interfaces:**
- Single page: sections Available, Allocate form, Inbox (exceptions), Packet JSON preview
- Calls same-origin API with `fetch`

- [ ] **Step 1: Add HTML that loads `/available` on boot** (manual browser check OK; optional smoke test that `/` returns 200 with `Available`)

```html
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="utf-8" />
  <title>Allocation — Available</title>
  <style>
    body { font-family: system-ui, sans-serif; margin: 1.5rem; max-width: 52rem; }
    h1,h2 { font-weight: 600; }
    table { border-collapse: collapse; width: 100%; margin: 0.5rem 0 1.5rem; }
    th, td { border: 1px solid #ccc; padding: 0.4rem 0.6rem; text-align: left; }
    label { display: block; margin: 0.4rem 0; }
    input, button { font: inherit; }
    .row { display: flex; gap: 1rem; flex-wrap: wrap; }
    section { margin-bottom: 2rem; }
    pre { background: #f6f6f6; padding: 0.75rem; overflow: auto; }
  </style>
</head>
<body>
  <h1>Allocation</h1>
  <p>Transaction-light pots · every.org credits · approve to allocate · inbox for exceptions</p>

  <section>
    <h2>Available</h2>
    <div id="available">Loading…</div>
  </section>

  <section>
    <h2>Allocate</h2>
    <form id="alloc-form">
      <label>Campaign key <input name="campaignKey" required placeholder="general" /></label>
      <label>Program key <input name="programKey" required placeholder="undesignated" /></label>
      <label>Amount <input name="amount" required placeholder="40.00" /></label>
      <label>Purpose <input name="purpose" required placeholder="Equipment" /></label>
      <label>Approved by <input name="approvedBy" required placeholder="director@example.org" /></label>
      <button type="submit">Approve allocation</button>
    </form>
    <p id="alloc-msg"></p>
  </section>

  <section>
    <h2>Inbox</h2>
    <div id="exceptions">—</div>
  </section>

  <section>
    <h2>Board packet</h2>
    <button type="button" id="btn-packet">Refresh packet</button>
    <pre id="packet">{}</pre>
  </section>

  <script type="module">
    async function loadAvailable() {
      const rows = await (await fetch('/available')).json();
      if (!rows.length) {
        document.getElementById('available').textContent = 'No pots yet. Send an every.org webhook or wait for gifts.';
        return;
      }
      const table = document.createElement('table');
      table.innerHTML = `<thead><tr><th>Campaign</th><th>Program</th><th>Credited</th><th>Allocated</th><th>Available</th></tr></thead>`;
      const tb = document.createElement('tbody');
      for (const r of rows) {
        const tr = document.createElement('tr');
        tr.innerHTML = `<td>${r.campaignKey}</td><td>${r.programKey}</td><td>${r.credited}</td><td>${r.allocated}</td><td><strong>${r.available}</strong></td>`;
        tb.appendChild(tr);
      }
      table.appendChild(tb);
      document.getElementById('available').replaceChildren(table);
    }

    async function loadExceptions() {
      const rows = await (await fetch('/exceptions')).json();
      document.getElementById('exceptions').textContent = rows.length
        ? rows.map((e) => `${e.code}: ${e.message}`).join('\n')
        : 'No open exceptions';
    }

    document.getElementById('alloc-form').addEventListener('submit', async (ev) => {
      ev.preventDefault();
      const fd = new FormData(ev.target);
      const body = Object.fromEntries(fd.entries());
      const res = await fetch('/allocations', {
        method: 'POST',
        headers: { 'content-type': 'application/json' },
        body: JSON.stringify(body),
      });
      const data = await res.json();
      document.getElementById('alloc-msg').textContent = res.ok
        ? `Approved ${data.id}`
        : `Error: ${data.error}`;
      await loadAvailable();
    });

    document.getElementById('btn-packet').addEventListener('click', async () => {
      const data = await (await fetch('/packet')).json();
      document.getElementById('packet').textContent = JSON.stringify(data, null, 2);
    });

    await loadAvailable();
    await loadExceptions();
  </script>
</body>
</html>
```

- [ ] **Step 2: Manual verify**

Run: `cd services/allocation-middleware && ORG_ID=org_demo npm start`  
POST sample webhook with curl; open `http://127.0.0.1:8787/`; allocate; refresh packet.

```bash
curl -s -X POST http://127.0.0.1:8787/webhooks/every-org \
  -H 'content-type: application/json' \
  -d '{"chargeId":"demo-1","amount":"100.00","netAmount":"100.00","currency":"USD","donationDate":"2026-08-03T00:00:00Z","toNonprofit":{"slug":"x","name":"X"},"fromFundraiser":{"title":"Spring","slug":"spring"},"designation":"Lab"}'
```

- [ ] **Step 3: Commit**

```bash
git add services/allocation-middleware/public
git commit -m "feat(allocation-middleware): minimal operator UI for pots and allocate"
```

---

### Task 8: CSV gift-summary import (MVP escape hatch)

**Files:**
- Create: `services/allocation-middleware/src/connectors/csv.mjs`
- Create: `services/allocation-middleware/test/csv.test.mjs`
- Modify: `services/allocation-middleware/src/app/service.mjs` — add `importCsv(text)`
- Modify: `services/allocation-middleware/src/http/server.mjs` — `POST /import/csv` body text/plain or JSON `{ csv: "..." }`

**Interfaces:**
- Produces: `parseGiftCsv(text) → Array<{ chargeId, netAmount, amount?, campaignKey?, programKey?, currency?, donatedAt? }>`
- Header row required: `chargeId,netAmount,campaignKey,programKey,currency,donatedAt` (campaignKey/programKey optional → general/undesignated)

- [ ] **Step 1: Failing test**

```js
import assert from 'node:assert/strict';
import { test } from 'node:test';
import { parseGiftCsv } from '../src/connectors/csv.mjs';
import { createService } from '../src/app/service.mjs';

test('parseGiftCsv reads header rows', () => {
  const rows = parseGiftCsv(
    'chargeId,netAmount,campaignKey,programKey,currency,donatedAt\n' +
      'c-csv-1,50.00,spring,lab,USD,2026-08-01T00:00:00Z\n',
  );
  assert.equal(rows.length, 1);
  assert.equal(rows[0].chargeId, 'c-csv-1');
  assert.equal(rows[0].netAmount, '50.00');
});

test('importCsv credits pots', () => {
  const svc = createService({ orgId: 'org_1', idgen: () => 'x' });
  const result = svc.importCsv(
    'chargeId,netAmount,campaignKey,programKey,currency,donatedAt\n' +
      'c-csv-2,10.00,,,USD,2026-08-01T00:00:00Z\n',
  );
  assert.equal(result.created, 1);
  assert.ok(svc.listAvailable().some((p) => p.available === '10.00'));
});
```

- [ ] **Step 2: Implement parse + service.importCsv (loop creditGift with constructed gift), HTTP route, tests PASS**

```js
// parseGiftCsv: split lines, first line headers, map columns; skip empty lines
// importCsv: for each row build GiftSummary via resolvePotPath + parseAmount; creditGift; count created
```

- [ ] **Step 3: Commit**

```bash
git commit -am "feat(allocation-middleware): CSV gift-summary import escape hatch"
```

---

### Task 9: Docs + suite pointer update

**Files:**
- Modify: `Fund-Intel/docs/ALLOCATION-MIDDLEWARE.md`
- Modify: `Fund-Intel/services/allocation-middleware/README.md`
- Modify: `Autonomous-Giving-Specs/docs/superpowers/specs/2026-08-03-allocation-middleware-design.md` (add “Implementation home” note) — only if Specs PR acceptable; else Fund-Intel README only

- [ ] **Step 1: Document runbook**

In `services/allocation-middleware/README.md`:

```markdown
# Allocation middleware

MVP package for AGI allocation middleware (every.org → pots → allocate → packet).

## Commands

npm test
ORG_ID=org_demo npm start   # http://127.0.0.1:8787

## every.org setup

1. Nonprofit admin → Advanced settings → webhook URL: `https://<host>/webhooks/every-org`
2. Map fundraisers/designations via first gifts (auto keys) or future mapping UI
3. Operators use Available / Allocate / Inbox / Packet

## Design

https://github.com/Autonomous-Giving-Incorporated/Autonomous-Giving-Specs/blob/main/docs/superpowers/specs/2026-08-03-allocation-middleware-design.md
```

Update `docs/ALLOCATION-MIDDLEWARE.md` with **Implementation status: MVP package at `services/allocation-middleware/`**.

- [ ] **Step 2: Commit**

```bash
git commit -am "docs(allocation-middleware): runbook and implementation status"
```

---

### Task 10: Plan self-check smoke (full test suite)

- [ ] **Step 1: Run full tests**

```bash
cd /Users/appliedalchemylabs/Fund-Intel/services/allocation-middleware && npm test
```

Expected: all PASS

- [ ] **Step 2: Open PR to Fund-Intel**

```bash
git push -u origin HEAD
gh pr create --title "feat: allocation middleware MVP (every.org pots)" --body "Implements approved allocation middleware design: domain, every.org normalizer, HTTP API, minimal UI."
```

---

## Spec coverage checklist (self-review)

| Design requirement | Task |
| --- | --- |
| every.org mapping | 3, 5, 6 |
| Campaign pot + program slice | 2 |
| netAmount credit | 3 |
| Idempotent chargeId | 2 |
| Human allocate approve | 4, 5 |
| Available balances | 2, 5, 7 |
| Exception codes (currency) | 2 |
| Exception list/resolve API | 5, 6 |
| Trail | 5, 6 |
| Board packet | 5, 6, 7 |
| Easy UI | 7 |
| Modular monolith package | 1–7 |
| No bank/QuickBooks | Global constraints |
| CSV import | 8 |
| Supabase persistence | In-memory MVP shipped; durable path for new work prefers Supabase PostgreSQL + Workers ([ADR-013](../../../adr/ADR-013-cloudflare-workers-public-host.md)). ADR-012 Render PostgreSQL notes are historical. |
| Multi-connector | interface.mjs only |

### Optional follow-on (not blocking first demo)

**Task 11 (later): Supabase pots/gifts/allocations tables + RLS** using Fund-Intel `clients.id` as `orgId`.  
**Task 12 (later): Auth** — wire director session before public internet.  
**Task 13 (later): Proof upload + MISSING_PROOF SLA.**

---

## Out of scope for this plan (explicit)

- Givebutter/Donorbox adapters  
- Funder multi-tenant portfolio  
- Proof file upload UI (packet without binary proof is OK for first demo; `MISSING_PROOF` can be stubbed later)  
- Kubernetes / multi-service split  
