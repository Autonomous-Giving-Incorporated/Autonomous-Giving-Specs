# Schema library

JSON Schema Draft 2020-12 artifacts are normative under [SPEC-007](../specs/SPEC-007-contracts.md). Contract schemas define public boundary payloads; event-specific schemas define payloads where no public contract applies.

| ID | Schema | Contract | Version |
| --- | --- | --- | --- |
| SCHEMA-001 | [Opportunity](opportunity.json) | CONTRACT-001 | 1.1.0 |
| SCHEMA-002 | [Recommendation](recommendation.json) | CONTRACT-002 | 1.0.0 |
| SCHEMA-003 | [Allocation](allocation.json) | CONTRACT-003 | 1.0.0 |
| SCHEMA-004 | [Evidence](evidence.json) | CONTRACT-004 | 1.0.0 |
| SCHEMA-005 | [Receipt](receipt.json) | CONTRACT-005 | 1.0.0 |
| SCHEMA-006 | [Notification](notification.json) | CONTRACT-006 | 1.1.0 |
| SCHEMA-007 | [TimelineEvent](timeline-event.json) | CONTRACT-007 | 1.0.0 |
| SCHEMA-008 | [AGI Auth Context](auth-context.json) | CONTRACT-008 | 1.0.0 |
| SCHEMA-009 | [Tenant Project Context](tenant-project-context.json) | CONTRACT-009 | 1.0.0 |
| SCHEMA-010 | [Capability Route Intent](route-intent.json) | CONTRACT-010 | 1.0.0 |
| SCHEMA-011 | [Delegation Approval Policy](delegation-policy.json) | CONTRACT-011 | 1.0.0 |
| SCHEMA-012 | [Public Impact Projection](public-projection.json) | CONTRACT-012 | 1.0.0 |
| SCHEMA-013 | [ImpactNotice](impact-notice.json) | CONTRACT-013 | 1.0.0 |

[event-envelope.json](event-envelope.json) defines event metadata. `signal-detected`, `approval-granted`, `execution-started`, and `verification-completed` are event-specific payload schemas.
