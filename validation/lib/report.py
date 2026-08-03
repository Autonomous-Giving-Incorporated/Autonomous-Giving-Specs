"""Machine-readable validation report model."""

from __future__ import annotations

import json
from dataclasses import asdict, dataclass, field
from pathlib import Path
from typing import Any, Literal

from .constants import PLATFORM_SPEC_VERSION


Severity = Literal["error", "warning"]


@dataclass(frozen=True)
class Finding:
    code: str
    message: str
    path: str = ""
    severity: Severity = "error"

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass
class Report:
    platform_spec_version: str = PLATFORM_SPEC_VERSION
    specifications: int = 0
    contracts: int = 0
    events: int = 0
    schemas: int = 0
    adrs: int = 0
    manifests: int = 0
    findings: list[Finding] = field(default_factory=list)

    def error(self, code: str, message: str, path: str = "") -> None:
        self.findings.append(Finding(code=code, message=message, path=path, severity="error"))

    def warning(self, code: str, message: str, path: str = "") -> None:
        self.findings.append(Finding(code=code, message=message, path=path, severity="warning"))

    @property
    def errors(self) -> list[Finding]:
        return [f for f in self.findings if f.severity == "error"]

    @property
    def warnings(self) -> list[Finding]:
        return [f for f in self.findings if f.severity == "warning"]

    @property
    def result(self) -> str:
        return "PASS" if not self.errors else "FAIL"

    def to_dict(self) -> dict[str, Any]:
        return {
            "platformSpecVersion": self.platform_spec_version,
            "result": self.result,
            "specifications": self.specifications,
            "contracts": self.contracts,
            "events": self.events,
            "schemas": self.schemas,
            "adrs": self.adrs,
            "manifests": self.manifests,
            "errors": [e.to_dict() for e in self.errors],
            "warnings": [w.to_dict() for w in self.warnings],
        }

    def write_json(self, path: Path) -> None:
        path.write_text(json.dumps(self.to_dict(), indent=2, sort_keys=False) + "\n", encoding="utf-8")

    def exit_code(self) -> int:
        return 0 if self.result == "PASS" else 1
