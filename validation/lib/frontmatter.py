"""Parse YAML frontmatter and extract document body."""

from __future__ import annotations

import re
from datetime import date, datetime
from pathlib import Path
from typing import Any

import yaml

FRONTMATTER_RE = re.compile(r"\A---\s*\n(.*?)\n---\s*\n?", re.DOTALL)


def _normalize(value: Any) -> Any:
    """Coerce YAML-native types into JSON-schema-friendly values."""
    if isinstance(value, datetime):
        return value.date().isoformat()
    if isinstance(value, date):
        return value.isoformat()
    if isinstance(value, dict):
        return {str(k): _normalize(v) for k, v in value.items()}
    if isinstance(value, list):
        return [_normalize(v) for v in value]
    return value


def parse_frontmatter(text: str) -> tuple[dict[str, Any] | None, str]:
    """Return (metadata, body). Metadata is None when no frontmatter block exists."""
    match = FRONTMATTER_RE.match(text)
    if not match:
        return None, text
    raw = match.group(1)
    data = yaml.safe_load(raw)
    if data is None:
        data = {}
    if not isinstance(data, dict):
        raise ValueError("frontmatter must be a YAML mapping")
    return _normalize(data), text[match.end() :]


def read_document(path: Path) -> tuple[dict[str, Any] | None, str]:
    text = path.read_text(encoding="utf-8")
    return parse_frontmatter(text)


def extract_fenced_json_blocks(body: str) -> list[str]:
    """Return contents of ```json fenced blocks."""
    pattern = re.compile(r"```json\s*\n(.*?)```", re.DOTALL | re.IGNORECASE)
    return [m.group(1).strip() for m in pattern.finditer(body)]


def extract_inline_json_objects(body: str) -> list[str]:
    """Best-effort extraction of Example: `{...}` inline JSON objects."""
    results: list[str] = []
    for match in re.finditer(r"Example:\s*`(\{.*?\})`", body):
        results.append(match.group(1))
    return results


def markdown_links(body: str) -> list[tuple[str, str]]:
    """Return (label, target) for markdown links."""
    return re.findall(r"\[([^\]]+)\]\(([^)]+)\)", body)


def id_references(body: str) -> set[str]:
    """Stable platform IDs mentioned in prose or links."""
    return set(
        re.findall(
            r"\b(?:SPEC-\d{3}[A-Z]?|ADR-\d{3}|EVENT-\d{3}|CONTRACT-\d{3}|SCHEMA-\d{3}|TERM-\d{3})\b",
            body,
        )
    )
