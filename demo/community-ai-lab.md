# Canonical demo: Community AI Lab

Values match [`demo/community-ai-lab/scenario.json`](community-ai-lab/scenario.json). This is a synthetic fixture, not a live tenant.

| Field | Fixed value |
| --- | --- |
| Organization | Community AI Lab |
| Need | 25 laptops for a neighborhood AI learning lab |
| Recommendation | $2,500 USD for equipment purchase |
| Approval | `approval-community-ai-lab`, human reviewer |
| Allocation | `c6c2e191-3000-4000-8000-000000000001` |
| Execution | Purchase of 25 laptops |
| Evidence | Delivery image and inventory attestation |
| Receipt | Vendor receipt for $2,500 USD |
| Verification | Independent evidence review: verified |
| Impact | Lab can provide 25 learner workstations |
| Gift | Tracked synthetic every.org `chargeId` (`synthetic-charge-community-ai-lab`); AGI did not process a donation; no Stripe donation |
| ImpactNotice | Not issued — no contactable donor (correct skip) |
| Donation Link | `https://example.com/tenant-fundraiser` (documentary outbound CTA) |

## Required narrative

The demo begins with the Need, shows the Fund Intel Recommendation as a proposal, visibly records Human Approval, then walks the Allocation through purchase, evidence, receipt, verification, impact, and Notification. Every rendered claim links backwards through the chain. Amounts are **2500 USD**.

## Acceptance checks

- No allocation exists before the approval event.
- The receipt equals the allocation amount (2500 USD).
- The impact claim names the verification and evidence identifiers.
- Re-running the demo produces the same IDs, ordering, amounts, and states.
- Gift is tracked, not processed. No Stripe donation path.
- ImpactNotice is absent because `contactableDonor` is false.

See [SPEC-011](../specs/SPEC-011-demo-specification.md).
