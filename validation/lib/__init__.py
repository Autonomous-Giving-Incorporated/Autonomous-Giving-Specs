"""Shared validation helpers for Autonomous Giving Specs."""

from .constants import (
    CANONICAL_LIFECYCLE,
    EVENT_STAGES,
    FORBIDDEN_SYNONYMS,
    PLATFORM_SPEC_VERSION,
    SERVICE_OWNERS,
)
from .documents import DocumentIndex, load_repository
from .report import Finding, Report

__all__ = [
    "CANONICAL_LIFECYCLE",
    "EVENT_STAGES",
    "FORBIDDEN_SYNONYMS",
    "PLATFORM_SPEC_VERSION",
    "SERVICE_OWNERS",
    "DocumentIndex",
    "load_repository",
    "Finding",
    "Report",
]
