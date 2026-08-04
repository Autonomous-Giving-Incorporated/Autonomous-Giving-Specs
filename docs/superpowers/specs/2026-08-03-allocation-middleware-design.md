# Allocation Middleware Product Design

**Date:** 2026-08-03  
**Status:** Approved (brainstorming)  
**Owner:** Product / Platform Architecture  
**Related:** Constitution, SPEC-002A, SPEC-006, SPEC-013, SPEC-020, implementation-guidance.md  

## 1. Problem

Nonprofit directors, foundation staff, and board/campaign leads need a trustworthy path from **money raised → allocation → proof** without operating a second finance system. Day-to-day work must be **mostly automated**. Deep transaction and accounting integration is explicitly out of scope.

## 2. Goals

| Goal | Measure |
| --- | --- |
| Easy for clients | Allocate in under ~2 minutes; daily habit = exception inbox |
| Transaction-light | Decision-grade numbers (pots, balances, gift summaries)—not a GL |
| Middleware | Sit between donation platforms and human governance |
| Small team | Modular monolith; one primary connector first |
| Automation-first | Humans approve allocations and resolve exceptions only |

## 3. Non-goals

- Payment processing / checkout replacement  
- Bank, Plaid, QuickBooks, or full transaction warehouses  
- Multi-service deployment as the MVP shape  
- Full multi-grantee funder portfolio (later phase)  
- Exposing platform lifecycle jargon as the primary UI language  

## 4. Personas (priority order)

| ID | Role | Primary need |
| --- | --- | --- |
| A | Nonprofit / program director | Allocate and prove use without re-entry |
| B | Foundation / funder staff | Trustworthy trail without chasing PDFs |
| C | Board / campaign director | Defendable packet and campaign clarity |

All three share **one product** with role-based views—not three client apps.

## 5. Wedge priority

1. **Automated use-of-funds trail** (gift summary → pot → allocation → proof)  
2. **Exception-only ops inbox**  
3. **Board / campaign decision packet**  
4. **Funder multi-grantee portfolio** (later)  

## 6. Approach

**Pot hierarchy middleware** (Approach A):

```text
Donation platform (canonical: every.org)
        ↓ gift summaries (webhook)
Campaign pot (parent) ← fundraiser
   └── Program slice (child) ← designation | Undesignated
        ↓
Human allocates from available (approval gate)
        ↓
Trail + exceptions + board packet
```

## 7. Canonical integration: every.org

### 7.1 Why first

- Nonprofit donation webhook on completed gifts  
- Fields map cleanly to pots without a full ledger  
- Zero platform-fee positioning common with mission-aligned clients  
- Donor PII may be omitted—compatible with privacy-minimizing UX  

### 7.2 Field mapping

| every.org field | Product mapping |
| --- | --- |
| `fromFundraiser` | Campaign pot (parent); else **General** |
| `designation` | Program slice (child); else **Undesignated** under parent |
| `chargeId` | Gift summary id (idempotent) |
| `netAmount` (default policy) | Credit to slice / roll up to campaign |
| `amount` | Secondary display (gross) |
| `currency` | Must match org default or raise exception |
| Donor name/email | Not required for allocation; drop or restricted store |

### 7.3 Connector roadmap

| Phase | Connectors |
| --- | --- |
| P0 | **every.org** + manual pots + CSV gift-summary import |
| P1 | Givebutter, Donorbox (same adapter interface) |
| P2 | Fundraise Up, Zeffy |
| P3 | GoFundMe Pro (enterprise demand) |

Marketing may list a “top 5”; **engineering priority is every.org first**.

## 8. Domain model (client language)

| Object | Definition |
| --- | --- |
| Organization | Tenant |
| Campaign pot | Parent balance bucket (fundraiser-backed) |
| Program slice | Child balance under a campaign (designation-backed) |
| Gift summary | Opaque credit event from a connector (not a bank transaction UI) |
| Allocation | Human-approved commitment against available balance |
| Proof | Evidence artifact linked to an allocation |
| Exception | Work item requiring human resolution |

Platform vocabulary (Need, Allocation, Evidence, …) remains authoritative in Specs; **product UI uses the table above**.

## 9. Mapping and automation rules

1. On gift webhook: resolve campaign pot → resolve program slice → credit if new `chargeId`.  
2. Unknown fundraiser/designation: **auto-create** pot/slice tagged “New — review” and optionally open exception.  
3. Duplicate `chargeId`: no double credit; may log `DUPLICATE_GIFT` if anomalous.  
4. Available balance = credited − allocated (per pot/slice policy; allocations reserve from slice and roll up).  
5. Allocation cannot exceed available; violation → block or `OVER_ALLOCATION` exception.  

## 10. Exception catalog

| Code | Trigger | Human action |
| --- | --- | --- |
| UNMAPPED_FUNDRAISER | Policy requires confirm | Name / merge pot |
| UNMAPPED_DESIGNATION | Policy requires confirm | Name / merge slice |
| DUPLICATE_GIFT | Anomalous redelivery | Dismiss / investigate |
| CURRENCY_MISMATCH | Non-default currency | Hold or policy convert |
| OVER_ALLOCATION | Commit > available | Reduce / reallocate |
| SYNC_FAILURE | Connector error | Retry / reconnect |
| MISSING_PROOF | Allocation without evidence past SLA | Attach or waive |
| STALE_POT | Inactive pot threshold | Archive |

## 11. Product surfaces (MVP)

| Screen | Purpose |
| --- | --- |
| Available | Raised / allocated / remaining by campaign & program |
| Allocate | Propose amount; human approve |
| Inbox | Exceptions only |
| Trail | Gift → pot → allocation → proof |
| Packet | One-click board/funder snapshot |
| Settings | every.org connect + mapping tables |

### Role defaults

| Role | Home |
| --- | --- |
| Director | Available, Allocate, Inbox |
| Funder | Trail, Packet (read-mostly) |
| Board / campaign | Packet, Available |

## 12. Architecture

Modular monolith (SPEC-020 Profile B):

```text
GitHub Pages / web UI
        ↓
Single backend
  Connectors | Pots | Allocations | Exceptions | Proof | Packet | Auth
        ↓
PostgreSQL + object storage (proof files)
```

| Module | Responsibility |
| --- | --- |
| Connectors | Webhooks, idempotency, adapter interface |
| Pots | Hierarchy, credits, balances |
| Allocations | Create, approve, enforce available |
| Exceptions | Queue and resolution |
| Proof | Attach and link evidence |
| Packet | Export/share snapshot |
| Auth | Org tenant + roles |

Capability alignment (logical only):

- Observe/credit ≈ Fund Intel  
- Approve allocate ≈ Autonomous Giving  
- Proof/trail/packet ≈ Impact Relay  

## 13. Automation vs human

| System | Human |
| --- | --- |
| Ingest gift summaries | Connect every.org; review new maps |
| Credit pots | Approve allocations |
| Detect exceptions | Resolve inbox |
| Roll up packet numbers | Share/publish packet |
| Idempotent replay | Attach proof when required |

## 14. MVP scope

### In

- every.org webhook + mapping UI  
- Campaign pot / program slice balances  
- Allocate + approve  
- Exception inbox  
- Trail  
- Board packet  
- Manual adjust + CSV import  

### Out

- Additional donation platforms (interface reserved)  
- Funder multi-org portfolio  
- Accounting/bank integrations  
- Distributed multi-service deploy  

### Success criteria (first client)

1. every.org gifts increase **Available** without re-keying  
2. Allocation path under ~2 minutes with one approval  
3. Inbox is the daily operator surface  
4. Board packet without spreadsheet rebuild  

## 15. Risks and mitigations

| Risk | Mitigation |
| --- | --- |
| Clients expect full finance | Explicit messaging: middleware, not QuickBooks |
| Designation string chaos | Normalize + merge aliases in inbox |
| Webhook reliability | Persist raw payload; retry; SYNC_FAILURE |
| PII leakage in trail | Never require donor identity for core UX |
| Scope creep to multi-connector | every.org + CSV until one client is green |

## 16. Implementation notes (for planning)

- Prefer single product repository or modular monolith workspace; Specs remain pinable authority.  
- Connector interface: `normalize_gift()`, `list_campaign_hints()`, webhook verify.  
- Align allocation identity with platform `allocationId` when emitting platform events later.  
- Do not require full EVENT-001…010 producers on day one; grow conformance as modules harden.  

## 17. Open items (resolved in brainstorm)

| Item | Decision |
| --- | --- |
| Primary personas | A, B, C |
| Wedge order | 1 → 4 → 2 → 3 |
| Financial depth | Transaction-light |
| Product type | Middleware + necessary connectors |
| Canonical client platform | every.org |
| Pot model | Fundraiser parent + designation child (C) |
| Amount policy | Default credit **netAmount** |

## 18. Doc index (suite)

| Repo | Doc |
| --- | --- |
| Autonomous-Giving-Specs | This design; implementation-guidance cross-link |
| Autonomous-Giving-Incorporated | PRODUCT-ALLOCATION-MIDDLEWARE.md; ROADMAP pointer |
| Fund-Intel | docs/ALLOCATION-MIDDLEWARE.md (intelligence/observe role) |
| Impact-Relay | docs/ALLOCATION-MIDDLEWARE.md (proof/trail role) |

## 19. Implementation plan

[docs/superpowers/plans/2026-08-03-allocation-middleware.md](../plans/2026-08-03-allocation-middleware.md)

## 20. Pilot hosting plan

[docs/superpowers/plans/2026-08-03-hacker-dojo-pilot-hosting.md](../plans/2026-08-03-hacker-dojo-pilot-hosting.md)
