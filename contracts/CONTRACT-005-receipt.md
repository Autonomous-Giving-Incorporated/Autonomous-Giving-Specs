# CONTRACT-005: Receipt

| Field | Value |
| --- | --- |
| Version | 1.0.0 |
| Owner | Execution |
| Producer / consumer | Execution / Verification, Transparency |
| Schema | [receipt.json](../schemas/receipt.json) |

A transaction record for an execution. Required: `receiptId`, `allocationId`, `amount`, `currency`, `issuedAt`, `issuer`. The total cannot exceed the allocation without an explicit, separately governed amendment. Published by [EVENT-008](../events/EVENT-008-receipt-generated.md).
