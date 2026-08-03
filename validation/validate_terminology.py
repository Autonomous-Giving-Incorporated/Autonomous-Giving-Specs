"""Scan normative artifacts for forbidden synonyms of glossary terms."""

from __future__ import annotations

import json
import re

from lib.constants import FORBIDDEN_SYNONYMS
from lib.documents import DocumentIndex
from lib.report import Report


def validate_terminology(index: DocumentIndex, report: Report) -> None:
    patterns = [(re.compile(pat, re.IGNORECASE), canonical) for pat, canonical in FORBIDDEN_SYNONYMS]

    for mapping in (index.specs, index.adrs, index.contracts, index.events):
        for art in mapping.values():
            body = art.body
            for regex, canonical in patterns:
                for match in regex.finditer(body):
                    report.error(
                        "FORBIDDEN_SYNONYM",
                        f"Found forbidden synonym '{match.group(0)}'; use canonical '{canonical}'",
                        art.rel_path,
                    )

    # Duplicate glossary terms already partially handled in CI; re-check.
    seen: dict[str, str] = {}
    for term_id, term in index.glossary_terms.items():
        key = term.casefold()
        if key in seen:
            report.error(
                "DUPLICATE_GLOSSARY_TERM",
                f"Duplicate glossary term '{term}' ({term_id} and {seen[key]})",
                "glossary/README.md",
            )
        else:
            seen[key] = term_id


def main() -> int:
    from lib.documents import load_repository

    report = Report()
    index = load_repository()
    validate_terminology(index, report)
    print(json.dumps(report.to_dict(), indent=2))
    return report.exit_code()


if __name__ == "__main__":
    raise SystemExit(main())
