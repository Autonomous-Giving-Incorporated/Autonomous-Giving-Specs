# Schema library

JSON Schema Draft 2020-12 validation artifacts for [contracts](../contracts/README.md). Schemas are normative; descriptions explain fields but do not relax `required`, type, or format constraints.

The contract schemas are public boundary contracts. The additional event payload schemas (`signal-detected`, `approval-granted`, `execution-started`, and `verification-completed`) define event-specific data where no public contract applies. [event-envelope.json](event-envelope.json) defines the common event metadata.
