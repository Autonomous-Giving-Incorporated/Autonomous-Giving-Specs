# Validation

Normative changes must pass the **executable** validation toolchain before merge.

## Automated (required)

```bash
pip install -r requirements-validation.txt
python validation/validate_all.py --output validation-report.json
```

The command **fails closed**: any error yields a non-zero exit code and `"result": "FAIL"`.

CI also runs Markdown link validation and inventory floors. See [validation/README.md](../validation/README.md).

### What is enforced

- Required metadata (frontmatter) for every SPEC, ADR, EVENT, and CONTRACT
- Stable identifier-to-path correspondence
- Every event references an existing schema (and contract when applicable)
- Every contract has exactly one owning service
- Lifecycle stages are canonical
- Every fenced JSON example validates against its schema
- No broken relative normative links or unknown artifact IDs
- No forbidden synonyms for canonical domain terms
- No missing version or status declarations
- Consumer conformance manifests (when present) match the catalog
- Community AI Lab demo fixtures preserve ordering and identity invariants

## Manual review (still required)

Automation does not replace human judgment for:

- [ ] Semantic correctness of new requirements language
- [ ] Whether a change is major / minor / patch under [SPEC-012](../specs/SPEC-012-versioning.md)
- [ ] Consumer impact and migration notes
- [ ] Constitution alignment for responsibility separation

## Reviewer checklist (supplement)

- [ ] `python validation/validate_all.py` reports `PASS`
- [ ] Generated indexes updated if metadata changed (`python validation/generate_indexes.py`)
- [ ] Breaking changes include ADR + changelog entry + migration template instance under `docs/migrations/`
