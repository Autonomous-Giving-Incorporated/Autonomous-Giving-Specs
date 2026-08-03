"""Load and index repository artifacts."""

from __future__ import annotations

import json
import re
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Literal

from .frontmatter import extract_fenced_json_blocks, id_references, read_document

ArtifactKind = Literal["spec", "adr", "contract", "event", "schema", "manifest"]


@dataclass
class Artifact:
    kind: ArtifactKind
    path: Path
    rel_path: str
    meta: dict[str, Any]
    body: str
    artifact_id: str

    @property
    def json_examples(self) -> list[str]:
        return extract_fenced_json_blocks(self.body)

    @property
    def referenced_ids(self) -> set[str]:
        return id_references(self.body) | id_references(json.dumps(self.meta, default=str))


@dataclass
class DocumentIndex:
    root: Path
    specs: dict[str, Artifact] = field(default_factory=dict)
    adrs: dict[str, Artifact] = field(default_factory=dict)
    contracts: dict[str, Artifact] = field(default_factory=dict)
    events: dict[str, Artifact] = field(default_factory=dict)
    schemas: dict[str, Path] = field(default_factory=dict)  # filename stem or SCHEMA-id
    schema_files: dict[str, Path] = field(default_factory=dict)  # relative path -> path
    schema_by_filename: dict[str, Path] = field(default_factory=dict)
    manifests: dict[str, Artifact] = field(default_factory=dict)
    schema_catalog: dict[str, dict[str, Any]] = field(default_factory=dict)  # SCHEMA-NNN
    glossary_terms: dict[str, str] = field(default_factory=dict)

    def all_document_ids(self) -> set[str]:
        ids: set[str] = set()
        ids.update(self.specs)
        ids.update(self.adrs)
        ids.update(self.contracts)
        ids.update(self.events)
        ids.update(self.schema_catalog)
        ids.update(self.glossary_terms)
        return ids


def _repo_root_from_here() -> Path:
    return Path(__file__).resolve().parents[2]


def _load_markdown_artifacts(
    root: Path,
    directory: str,
    kind: ArtifactKind,
    id_prefix: str,
) -> dict[str, Artifact]:
    result: dict[str, Artifact] = {}
    base = root / directory
    if not base.exists():
        return result
    for path in sorted(base.glob(f"{id_prefix}-*.md")):
        meta, body = read_document(path)
        if meta is None:
            # Placeholders: validator will report missing frontmatter.
            meta = {}
        artifact_id = str(meta.get("id") or _id_from_filename(path.name, id_prefix))
        rel = path.relative_to(root).as_posix()
        result[artifact_id] = Artifact(
            kind=kind,
            path=path,
            rel_path=rel,
            meta=meta,
            body=body,
            artifact_id=artifact_id,
        )
    return result


def _id_from_filename(name: str, prefix: str) -> str:
    match = re.match(rf"({prefix}-\d{{3}})", name)
    return match.group(1) if match else name


def _load_schema_catalog(root: Path) -> dict[str, dict[str, Any]]:
    """Parse schemas/README.md table for SCHEMA-NNN mapping."""
    readme = root / "schemas" / "README.md"
    catalog: dict[str, dict[str, Any]] = {}
    if not readme.exists():
        return catalog
    text = readme.read_text(encoding="utf-8")
    # | SCHEMA-001 | [Opportunity](opportunity.json) | CONTRACT-001 | 1.0.0 |
    row = re.compile(
        r"\|\s*(SCHEMA-\d{3})\s*\|\s*\[([^\]]+)\]\(([^)]+)\)\s*\|\s*([^|]+)\|\s*([^|]+)\|"
    )
    for match in row.finditer(text):
        schema_id, title, file_name, contract, version = match.groups()
        catalog[schema_id] = {
            "id": schema_id,
            "title": title.strip(),
            "file": file_name.strip(),
            "contract": contract.strip(),
            "version": version.strip(),
        }
    return catalog


def _load_glossary(root: Path) -> dict[str, str]:
    path = root / "glossary" / "README.md"
    terms: dict[str, str] = {}
    if not path.exists():
        return terms
    for match in re.finditer(
        r"\|\s*(TERM-\d{3})\s*\|\s*([^|]+)\|\s*([^|]+)\|",
        path.read_text(encoding="utf-8"),
    ):
        term_id, term, _definition = match.groups()
        if term_id == "ID":
            continue
        terms[term_id] = term.strip()
    return terms


def _load_manifests(root: Path) -> dict[str, Artifact]:
    result: dict[str, Artifact] = {}
    for base in (root / "conformance" / "examples", root / "validation" / "manifests"):
        if not base.exists():
            continue
        for path in sorted(base.glob("*.yml")) + sorted(base.glob("*.yaml")):
            import yaml

            data = yaml.safe_load(path.read_text(encoding="utf-8")) or {}
            service_id = (
                data.get("service", {}).get("id")
                if isinstance(data.get("service"), dict)
                else path.stem
            )
            key = str(service_id or path.stem)
            rel = path.relative_to(root).as_posix()
            result[key] = Artifact(
                kind="manifest",
                path=path,
                rel_path=rel,
                meta=data if isinstance(data, dict) else {},
                body="",
                artifact_id=key,
            )
    return result


def load_repository(root: Path | None = None) -> DocumentIndex:
    root = (root or _repo_root_from_here()).resolve()
    index = DocumentIndex(root=root)
    index.specs = _load_markdown_artifacts(root, "specs", "spec", "SPEC")
    index.adrs = _load_markdown_artifacts(root, "adr", "adr", "ADR")
    index.contracts = _load_markdown_artifacts(root, "contracts", "contract", "CONTRACT")
    index.events = _load_markdown_artifacts(root, "events", "event", "EVENT")
    index.schema_catalog = _load_schema_catalog(root)
    index.glossary_terms = _load_glossary(root)
    index.manifests = _load_manifests(root)

    schemas_dir = root / "schemas"
    if schemas_dir.exists():
        for path in sorted(schemas_dir.glob("*.json")):
            rel = path.relative_to(root).as_posix()
            index.schema_files[rel] = path
            index.schema_by_filename[path.name] = path
        # Exclude meta schemas from payload schema count later via path prefix.
        for path in sorted((schemas_dir / "meta").glob("*.json")) if (schemas_dir / "meta").exists() else []:
            rel = path.relative_to(root).as_posix()
            index.schema_files[rel] = path

    return index


def load_json_schema(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def resolve_schema_path(index: DocumentIndex, ref: str) -> Path | None:
    """Resolve a schema field value to a filesystem path."""
    if not ref:
        return None
    # Strip markdown link wrappers if present.
    m = re.search(r"\(([^)]+)\)", ref)
    candidate = m.group(1) if m else ref
    candidate = candidate.strip()
    # CONTRACT-NNN → contract's schema
    if re.fullmatch(r"CONTRACT-\d{3}", candidate):
        contract = index.contracts.get(candidate)
        if not contract:
            return None
        return resolve_schema_path(index, str(contract.meta.get("schema", "")))
    # Relative or bare filename
    name = Path(candidate).name
    if name in index.schema_by_filename:
        return index.schema_by_filename[name]
    # Path relative to repo
    direct = index.root / candidate
    if direct.exists():
        return direct
    # Path relative to schemas/
    under = index.root / "schemas" / name
    if under.exists():
        return under
    return None
