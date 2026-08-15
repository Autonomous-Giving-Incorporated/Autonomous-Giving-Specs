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
| TERM-021 | Preferred Stack | Informative physical architecture for new product work: Cloudflare (Workers, static assets/Pages, Durable Objects if needed, Queues/Cron Triggers) + Supabase (Auth, PostgreSQL, Storage) per ADR-013. every.org is the P0 donation-source connector. Stripe is tenant/SaaS billing only. Resend, OpenAI, and Clerk only if still required. ADR-012 (Render-first) is superseded. Not a conformance mandate. |
| TERM-022 | Ledger Entry | Append-oriented internal tracking record used to reconstruct pot, allocation, and Evidence state (distinct from connector gift state). Not a donation-processor settlement record. |
| TERM-023 | Webhook Event | Persisted inbound provider event used for verification, idempotency, and replay. |
| TERM-024 | Job | Durable unit of async work with idempotency key and lifecycle queued→running→terminal. |
| TERM-025 | Gift Summary | Opaque credit event from a donation-source connector (not a bank transaction UI and not an AGI charge). |
| TERM-026 | Pot | Balance bucket for tracked gifts: campaign parent and program slice. Available = credited − allocated. |
| TERM-027 | Donation-source Connector | Adapter that verifies and normalizes third-party gift-completed events (P0: every.org) or the CSV twin. |
| TERM-028 | ImpactNotice | Notification projection that tells a contactable donor where/what allocated funds were used for and CTAs to the tenant Donation Link. |
| TERM-029 | Donation Link | Outbound HTTPS URL on the tenant record pointing at the tenant’s own receiver. Not a checkout session. |

No synonym may substitute for an identified term. A proposed new concept requires a glossary identifier and a review against existing terms.

**Note:** Platform vocabulary for lifecycle and domain concepts is unchanged. Capability/deployment terms, preferred-stack terms, and tracking terms (Gift Summary, Pot, Donation-source Connector, Donation Link) clarify the product without renaming Need, Allocation, Evidence, Impact, or other lifecycle terms. Product UI MAY say “proof” for Evidence. ImpactNotice is a Notification projection, not a new lifecycle stage.
