# Lifecycle diagram

Canonical logical progression ([SPEC-005](../specs/SPEC-005-lifecycle.md)):

```text
Need → Signal → Opportunity → Recommendation → Approval → Allocation
  → Execution → Evidence → Receipt → Verification → Impact
```

Projections (not alternate stages): `TimelineEvent`, `Notification`, `ImpactNotice` (after Evidence or explicit human waive; [SPEC-027](../specs/SPEC-027-impact-loop.md)).

No transport or deployable is implied per stage.
