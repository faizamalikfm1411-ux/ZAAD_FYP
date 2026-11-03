"""Loader and validator for the shared safety rules file (S1-FM-05).

Used by:
  * CI:      python shared/rules/validate_rules.py      (exit code 1 = broken file = failed build)
  * backend: from validate_rules import load_rules, build_name_index

No LLM, no network, no UI imports (NFR-ARCH-01, FR-ALG-08).
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

from jsonschema import Draft202012Validator

HERE = Path(__file__).resolve().parent
DEFAULT_RULES = HERE / "safety-rules.json"
DEFAULT_SCHEMA = HERE / "safety-rules.schema.json"


class RulesError(Exception):
    """The rules file is broken. The message lists every problem found."""

    def __init__(self, problems: list[str]):
        self.problems = problems
        super().__init__("\n".join(problems))


def _reject_duplicate_keys(pairs):
    seen = {}
    for key, value in pairs:
        if key in seen:
            raise ValueError(f"duplicate key {key!r}")
        seen[key] = value
    return seen


def _read_json(path: Path) -> object:
    try:
        text = path.read_text(encoding="utf-8")
    except OSError as exc:
        raise RulesError([f"cannot read {path}: {exc}"]) from exc
    try:
        return json.loads(text, object_pairs_hook=_reject_duplicate_keys)
    except ValueError as exc:  # includes JSONDecodeError and duplicate keys
        raise RulesError([f"{path.name}: invalid JSON: {exc}"]) from exc


def validate_rules(data: object, schema: object) -> list[str]:
    """Return a list of problems (empty list = valid)."""
    validator = Draft202012Validator(schema)
    problems = [
        f"schema: {'/'.join(str(p) for p in e.absolute_path) or '(root)'}: {e.message}"
        for e in sorted(validator.iter_errors(data), key=lambda e: list(map(str, e.absolute_path)))
    ]
    if problems:
        return problems  # semantic checks assume the structure is right

    allergens = data["allergens"]
    ids = [a["id"] for a in allergens]
    if len(set(ids)) != len(ids):
        dupes = sorted({i for i in ids if ids.count(i) > 1})
        problems.append(f"allergens: duplicate id(s): {', '.join(dupes)}")
    if len(set(ids)) != 10:
        problems.append(f"allergens: expected all 10 Appendix C ids, found {len(set(ids))}")

    owner: dict[str, str] = {}
    for a in allergens:
        both = set(a["hiddenNames"]) & set(a["directNames"])
        if both:
            problems.append(f"allergen {a['id']}: name(s) in both hiddenNames and directNames: {', '.join(sorted(both))}")
        for name in list(a["hiddenNames"]) + list(a["directNames"]):
            if name in owner and owner[name] != a["id"]:
                problems.append(
                    f"name {name!r} maps to two allergens ({owner[name]} and {a['id']}); decide one before merging"
                )
            owner.setdefault(name, a["id"])
        if data["contentStatus"] != "skeleton" and not a["hiddenNames"]:
            problems.append(f"allergen {a['id']}: contentStatus is {data['contentStatus']!r} but hiddenNames is empty")
        known = set(a["hiddenNames"]) | set(a["directNames"])
        stray = set(a["namesUr"]) - known
        if stray:
            problems.append(f"allergen {a['id']}: namesUr has entries for unknown names: {', '.join(sorted(stray))}")
        if data["contentStatus"] != "skeleton":
            # FR-ALG-11: Urdu names for each allergen and its hidden names
            if a["nameUr"] is None:
                problems.append(f"allergen {a['id']}: nameUr is missing (FR-ALG-11)")
            no_ur = [n for n in a["hiddenNames"] if n not in a["namesUr"]]
            if no_ur:
                problems.append(f"allergen {a['id']}: no Urdu text for hidden name(s): {', '.join(no_ur)} (FR-ALG-11)")

    diet_ids = [d["id"] for d in data["dietTypes"]]
    if len(set(diet_ids)) != len(diet_ids):
        problems.append("dietTypes: duplicate id")
    return problems


def warnings_for(data: dict) -> list[str]:
    missing = [a["id"] for a in data["allergens"] if a["nameUr"] is None]
    if missing:
        return [f"nameUr not set yet for: {', '.join(missing)} (Urdu names are supplied later, FR-ALG-11)"]
    return []


def load_rules(path: Path | str = DEFAULT_RULES, schema_path: Path | str = DEFAULT_SCHEMA) -> dict:
    """Load and validate the rules file. Raises RulesError if anything is wrong."""
    data = _read_json(Path(path))
    schema = _read_json(Path(schema_path))
    problems = validate_rules(data, schema)
    if problems:
        raise RulesError(problems)
    return data  # type: ignore[return-value]


def display_name(rules: dict, allergen_id: str, lang: str = "en") -> str:
    """Name to show a customer. lang is 'en' or 'ur'. Falls back to English if Urdu is missing."""
    for a in rules["allergens"]:
        if a["id"] == allergen_id:
            return (a["nameUr"] if lang == "ur" else None) or a["nameEn"]
    raise KeyError(allergen_id)


def build_name_index(rules: dict) -> dict[str, str]:
    """Map every hidden or direct ingredient name to its allergen id (lowercase keys)."""
    index: dict[str, str] = {}
    for a in rules["allergens"]:
        for name in list(a["hiddenNames"]) + list(a["directNames"]):
            index[name] = a["id"]
    return index


def main(argv: list[str]) -> int:
    path = Path(argv[1]) if len(argv) > 1 else DEFAULT_RULES
    try:
        rules = load_rules(path)
    except RulesError as exc:
        print(f"RULES FILE INVALID: {path}")
        for problem in exc.problems:
            print(f"  - {problem}")
        return 1
    for warning in warnings_for(rules):
        print(f"warning: {warning}")
    print(
        f"OK: {path.name} rulesVersion={rules['rulesVersion']} contentStatus={rules['contentStatus']} "
        f"allergens={len(rules['allergens'])} names={len(build_name_index(rules))}"
    )
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
