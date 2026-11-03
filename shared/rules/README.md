# Shared safety rules

One JSON file holds the hidden-allergen map (SRS Appendix C) and the diet types (SRS Table 4.7).
The Python backend (authoritative) and the TypeScript mirror in the browser both read this file,
so they cannot disagree (NFR-ARCH-01, 02). No LLM is involved (FR-ALG-08).

| File | Purpose |
|---|---|
| `safety-rules.json` | The rules. Content owner: Khansa. Served by `GET /rules`. |
| `safety-rules.schema.json` | JSON Schema. Defines the allowed shape. |
| `validate_rules.py` | Loader and validator. `load_rules()` and `build_name_index()` for the backend. |
| `test_rules.py` | Tests, including broken files that must be rejected. |

## Check the file locally

```bash
pip install -r shared/rules/requirements-dev.txt
python shared/rules/validate_rules.py     # exit code 1 if the file is broken
pytest shared/rules -q
```

CI runs both commands on every pull request, so a broken rules file fails the build.

## Rules for editing the file

- Allergen ids are fixed (FR-ALG-11). Never rename one.
- Names are lowercase and trimmed. A name may belong to one allergen only.
- Urdu (FR-ALG-11): every allergen needs `nameUr`, and every hidden name needs an entry in `namesUr`. Both are drafts until a native speaker verifies them. The loader fails the build if any are missing.
- Keep the Python and TypeScript engines on this one file. Never copy the rules into code.
