# Executable specification validation

This directory is the **enforced** validation toolchain for the Autonomous Giving platform canon.

## Quick start

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements-validation.txt
python validation/validate_all.py
```

Exit code `0` means **PASS** (warnings allowed). Exit code `1` means **FAIL** (errors present). The default output is a deterministic JSON report:

```json
{
  "platformSpecVersion": "1.0.0",
  "result": "PASS",
  "specifications": 14,
  "contracts": 7,
  "events": 10,
  "schemas": 12,
  "errors": [],
  "warnings": []
}
```

Write the report to disk:

```bash
python validation/validate_all.py --output validation-report.json
```

## Validators

| Script | Enforces |
| --- | --- |
| `validate_metadata.py` | Required frontmatter; meta-schema compliance; ID↔path; duplicate IDs |
| `validate_references.py` | Relative links; known IDs; event→contract/schema; circular related refs |
| `validate_schemas.py` | Draft 2020-12; unique `$id`; catalog file existence |
| `validate_lifecycle.py` | Canonical stages on events/contracts; SPEC-005 completeness |
| `validate_ownership.py` | Exactly one contract owner from the service set |
| `validate_examples.py` | Fenced JSON examples validate against linked schemas |
| `validate_manifests.py` | Conformance manifests against `schemas/meta/conformance-manifest.schema.json` |
| `validate_terminology.py` | Forbidden synonyms; duplicate glossary terms |
| `validate_demo.py` | Community AI Lab fixture order, continuity, and payloads |
| `validate_all.py` | Orchestrates all of the above |

## Generated indexes

```bash
python validation/generate_indexes.py
```

Writes `generated/catalog.json`, `traceability.json`, `lifecycle.json`, `ownership.json`, `dependency-graph.json`, and `conformance-matrix.json`.

## Release package

```bash
python validation/package_release.py --version 1.0.0
```

Produces `dist/autonomous-giving-spec-v1.0.0/` and `dist/checksums.txt`.

## Meta-schemas

Frontmatter for SPEC / ADR / CONTRACT / EVENT documents is defined under `schemas/meta/`. Consumer manifests use `schemas/meta/conformance-manifest.schema.json`.

## CI

GitHub Actions workflow [`.github/workflows/spec-validation.yml`](../.github/workflows/spec-validation.yml) runs link checks, `validate_all.py`, index generation, and a packaging smoke test on every pull request and push to `main`.
