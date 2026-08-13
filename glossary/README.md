# Canonical glossary

The glossary is normative under [SPEC-004](../specs/SPEC-004-domain-model.md). Every specification SHALL use these identifiers when referring to a major concept.

| ID | Term | Definition |
| --- | --- | --- |
| TERM-001 | Organization | Entity that operates or receives platform-supported programs. |
| TERM-002 | Program | Bounded initiative operated by an Organization. |
| TERM-003 | Need | Documented gap or desired outcome. |
| TERM-004 | Signal | Immutable observation relevant to a Need. |
| TERM-005 | Opportunity | Actionable grouping of a Need and supporting Signals. |
| TERM-006 | Recommendation | Proposed, non-authorizing allocation response to an Opportunity. |
| TERM-007 | Approval | Explicit governance decision authorizing a Recommendation. |
| TERM-008 | Allocation | Authorized commitment of funds, identified by `allocationId`. |
| TERM-009 | Execution | Fulfillment activity for an Allocation. |
| TERM-010 | Evidence | Attributable artifact or claim supporting what occurred. |
| TERM-011 | Receipt | Transaction record issued during Execution. |
| TERM-012 | Verification | Assessment of Evidence and Receipt against a claim. |
| TERM-013 | Impact | Verified outcome claim attributable to an Allocation. |
| TERM-014 | Notification | Delivery request or record for a lifecycle update. |
| TERM-015 | TimelineEvent | Immutable human-readable projection of an authoritative lifecycle event. |
| TERM-016 | Capability | Logical responsibility with owned contracts and boundaries (e.g. Fund Intel). Not a deployment unit. |
| TERM-017 | Module | Implementation unit that realizes a Capability inside a codebase (may share a process). |
| TERM-018 | Deployment | Operational topology: how modules are packaged, hosted, and operated. |
| TERM-019 | Service | Optional deployment model in which one or more capabilities run as a separately operable unit. Not required by the platform. |
| TERM-020 | Modular Monolith | Reference implementation shape: one primary deployable containing multiple capability modules with clear boundaries. |
| TERM-021 | Preferred Stack | Informative physical architecture for new product work: Cloudflare Workers/Pages for public static and edge surfaces (ADR-013); Render (or similar) plus PostgreSQL for optional durable application hosting (ADR-012); Clerk, Stripe, Resend, OpenAI, and existing Supabase as externals. Not a conformance mandate. |
| TERM-022 | Ledger Entry | Append-oriented internal financial record used to reconstruct AGI book state (distinct from processor payment state). |
| TERM-023 | Webhook Event | Persisted inbound provider event used for verification, idempotency, and replay. |
| TERM-024 | Job | Durable unit of async work with idempotency key and lifecycle queued→running→terminal. |

No synonym may substitute for an identified term. A proposed new concept requires a glossary identifier and a review against existing terms.

**Note:** Platform vocabulary for lifecycle and domain concepts is unchanged. Capability/deployment terms and preferred-stack terms clarify architecture without renaming Need, Allocation, Impact, or other lifecycle terms.
