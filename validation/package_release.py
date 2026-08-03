#!/usr/bin/env python3
"""Build a versioned distributable specification package under dist/."""

from __future__ import annotations

import argparse
import hashlib
import json
import shutil
import sys
from datetime import datetime, timezone
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from lib.constants import PLATFORM_SPEC_VERSION
from lib.documents import load_repository
from generate_indexes import generate


def _sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as fh:
        for chunk in iter(lambda: fh.read(65536), b""):
            h.update(chunk)
    return h.hexdigest()


def package(version: str, root: Path | None = None) -> Path:
    index = load_repository(root)
    root = index.root
    generate(root)

    dist_root = root / "dist"
    dist_root.mkdir(parents=True, exist_ok=True)
    pkg_name = f"autonomous-giving-spec-v{version}"
    pkg_dir = dist_root / pkg_name
    if pkg_dir.exists():
        shutil.rmtree(pkg_dir)
    pkg_dir.mkdir(parents=True)

    # Copy core artifact trees
    for folder in ("contracts", "schemas", "events", "specs", "adr", "glossary", "demo"):
        src = root / folder
        if src.exists():
            shutil.copytree(src, pkg_dir / folder, ignore=shutil.ignore_patterns(".DS_Store"))

    # Generated indexes + glossary export
    gen = root / "generated"
    if gen.exists():
        shutil.copytree(gen, pkg_dir / "generated")

    glossary = {
        "platformSpecVersion": version,
        "terms": [
            {"id": tid, "term": term} for tid, term in index.glossary_terms.items()
        ],
    }
    (pkg_dir / "glossary.json").write_text(json.dumps(glossary, indent=2) + "\n", encoding="utf-8")

    # Traceability copy at package root for convenience
    trace_src = root / "generated" / "traceability.json"
    if trace_src.exists():
        shutil.copy2(trace_src, pkg_dir / "traceability.json")

    manifest = {
        "name": "autonomous-giving-spec",
        "version": version,
        "createdAt": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "repository": "scrimshawlife-ctrl/Autonomous-Giving-Specs",
        "counts": {
            "specifications": len(index.specs),
            "contracts": len(index.contracts),
            "events": len(index.events),
            "adrs": len(index.adrs),
            "schemas": len(
                [p for p in index.schema_by_filename.values() if p.parent.name != "meta"]
            ),
        },
        "schemaBaseIds": "https://autonomousgiving.org/schemas/",
        "contents": sorted(
            p.relative_to(pkg_dir).as_posix()
            for p in pkg_dir.rglob("*")
            if p.is_file()
        ),
    }
    (pkg_dir / "manifest.json").write_text(json.dumps(manifest, indent=2) + "\n", encoding="utf-8")

    # Checksums for package files
    checksum_lines = []
    for path in sorted(pkg_dir.rglob("*")):
        if path.is_file():
            rel = path.relative_to(pkg_dir).as_posix()
            checksum_lines.append(f"{_sha256(path)}  {pkg_name}/{rel}")
    checksums_path = dist_root / "checksums.txt"
    # Also include package-level relative paths for the release folder
    checksums_path.write_text("\n".join(checksum_lines) + "\n", encoding="utf-8")

    # Refresh contents after checksums not in package; re-write manifest without checksums file
    return pkg_dir


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--version", default=PLATFORM_SPEC_VERSION)
    parser.add_argument("--root", type=Path, default=None)
    args = parser.parse_args()
    pkg = package(args.version, args.root)
    print(f"packaged {pkg}")
    print(f"checksums {pkg.parent / 'checksums.txt'}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
