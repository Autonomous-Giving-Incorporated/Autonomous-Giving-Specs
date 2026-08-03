"""Canonical constants for platform validation."""

from __future__ import annotations

PLATFORM_SPEC_VERSION = "1.0.0"

# SPEC-005 lifecycle sequence (exclusive of projections).
CANONICAL_LIFECYCLE: list[str] = [
    "Need",
    "Signal",
    "Opportunity",
    "Recommendation",
    "Approval",
    "Allocation",
    "Execution",
    "Evidence",
    "Receipt",
    "Verification",
    "Impact",
]

# Events may also use Notification as a projection stage (not a lifecycle alternative).
EVENT_STAGES: frozenset[str] = frozenset(CANONICAL_LIFECYCLE + ["Notification"])

# Contract-owning services (exactly one owner per contract).
SERVICE_OWNERS: frozenset[str] = frozenset(
    {
        "Fund Intel",
        "Autonomous Giving",
        "Impact Relay",
        "Platform Architecture",
        "Platform Product",
        "Governance",
    }
)

# Documented forbidden synonyms for canonical glossary terms.
# Matched case-insensitively as whole phrases in normative prose (excluding frontmatter).
FORBIDDEN_SYNONYMS: list[tuple[str, str]] = [
    (r"\bImpactClaim\b", "Impact"),
    (r"\bfunding commitment\b", "Allocation"),
    (r"\bgrant award\b", "Allocation"),
    (r"\bapproval decision ID\b", "approvalId"),
    (r"\ballocation key\b", "allocationId"),
]

ID_PATTERNS = {
    "spec": r"^SPEC-\d{3}$",
    "adr": r"^ADR-\d{3}$",
    "event": r"^EVENT-\d{3}$",
    "contract": r"^CONTRACT-\d{3}$",
    "schema": r"^SCHEMA-\d{3}$",
    "term": r"^TERM-\d{3}$",
}

META_SCHEMAS = {
    "spec": "schemas/meta/spec-document.schema.json",
    "adr": "schemas/meta/adr-document.schema.json",
    "contract": "schemas/meta/contract-document.schema.json",
    "event": "schemas/meta/event-document.schema.json",
    "manifest": "schemas/meta/conformance-manifest.schema.json",
}
