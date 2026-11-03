"""Tests for the shared rules loader. A broken rules file must fail (S1-FM-05)."""
import copy
import json
import subprocess
import sys
from pathlib import Path

import pytest

from validate_rules import DEFAULT_RULES, DEFAULT_SCHEMA, RulesError, build_name_index, display_name, load_rules

HERE = Path(__file__).resolve().parent
GOOD = json.loads(DEFAULT_RULES.read_text(encoding="utf-8"))


def write(tmp_path, data, name="rules.json"):
    p = tmp_path / name
    p.write_text(data if isinstance(data, str) else json.dumps(data), encoding="utf-8")
    return p


def mutated(fn):
    data = copy.deepcopy(GOOD)
    fn(data)
    return data


def test_committed_rules_file_is_valid():
    rules = load_rules(DEFAULT_RULES, DEFAULT_SCHEMA)
    assert [a["id"] for a in rules["allergens"]] == [a["id"] for a in GOOD["allergens"]]
    assert len(rules["allergens"]) == 10
    assert rules["riskLevels"] == ["SAFE", "CAUTION", "DANGER"]


def test_name_index_maps_every_name_to_one_allergen():
    index = build_name_index(load_rules())
    total = sum(len(a["hiddenNames"]) + len(a["directNames"]) for a in GOOD["allergens"])
    assert len(index) == total


BROKEN = {
    "missing allergen": lambda d: d["allergens"].pop(),
    "unknown allergen id": lambda d: d["allergens"][0].update(id="peanut"),
    "duplicate allergen id": lambda d: d["allergens"][1].update(id=d["allergens"][0]["id"]),
    "uppercase hidden name": lambda d: d["allergens"][0]["hiddenNames"].append("Semolina"),
    "untrimmed hidden name": lambda d: d["allergens"][0]["hiddenNames"].append(" malt"),
    "empty hidden name": lambda d: d["allergens"][0]["hiddenNames"].append(""),
    "name under two allergens": lambda d: (
        d["allergens"][0]["hiddenNames"].append("tahini"),
        d["allergens"][6]["hiddenNames"].append("tahini"),
    ),
    "name in hidden and direct": lambda d: (
        d["allergens"][0]["hiddenNames"].append("flour"),
        d["allergens"][0]["directNames"].append("flour"),
    ),
    "wrong risk levels": lambda d: d.update(riskLevels=["SAFE", "DANGER"]),
    "risk levels reordered": lambda d: d.update(riskLevels=["DANGER", "CAUTION", "SAFE"]),
    "unknown top-level field": lambda d: d.update(price=1),
    "missing field": lambda d: d.pop("traceFlags"),
    "bad rulesVersion": lambda d: d.update(rulesVersion="one"),
    "bad schemaVersion": lambda d: d.update(schemaVersion=2),
    "non-snake trace flag": lambda d: d["traceFlags"].append("Shared Fryer"),
    "diet type missing": lambda d: d["dietTypes"].pop(),
    "nameUr missing in v0": lambda d: d["allergens"][0].update(nameUr=None),
    "nameUr in English letters": lambda d: d["allergens"][0].update(nameUr="Gluten"),
    "namesUr value in English letters": lambda d: d["allergens"][0]["namesUr"].update(maida="flour"),
    "hidden name without Urdu": lambda d: d["allergens"][0]["namesUr"].pop("maida"),
    "namesUr entry for unknown name": lambda d: d["allergens"][0]["namesUr"].update(cheese="پنیر"),
    "namesUr missing field": lambda d: d["allergens"][0].pop("namesUr"),
    "nameUr empty string": lambda d: d["allergens"][0].update(nameUr=""),
}


@pytest.mark.parametrize("label", BROKEN)
def test_broken_file_is_rejected(tmp_path, label):
    path = write(tmp_path, mutated(BROKEN[label]))
    with pytest.raises(RulesError):
        load_rules(path, DEFAULT_SCHEMA)


def test_invalid_json_is_rejected(tmp_path):
    with pytest.raises(RulesError):
        load_rules(write(tmp_path, '{"schemaVersion": 1,'), DEFAULT_SCHEMA)


def test_duplicate_json_key_is_rejected(tmp_path):
    text = json.dumps(GOOD)[:-1] + ', "rulesVersion": "9.9.9"}'
    with pytest.raises(RulesError):
        load_rules(write(tmp_path, text), DEFAULT_SCHEMA)


def test_missing_file_is_rejected(tmp_path):
    with pytest.raises(RulesError):
        load_rules(tmp_path / "nope.json", DEFAULT_SCHEMA)


def test_non_skeleton_requires_hidden_names(tmp_path):
    def blank(d):
        d["contentStatus"] = "v0"
        d["allergens"][0]["hiddenNames"] = []
    with pytest.raises(RulesError):
        load_rules(write(tmp_path, mutated(blank)), DEFAULT_SCHEMA)


def test_command_line_exit_codes(tmp_path):
    script = str(HERE / "validate_rules.py")
    ok = subprocess.run([sys.executable, script], capture_output=True, text=True)
    assert ok.returncode == 0, ok.stdout + ok.stderr
    bad = write(tmp_path, mutated(BROKEN["missing allergen"]), "bad.json")
    fail = subprocess.run([sys.executable, script, str(bad)], capture_output=True, text=True)
    assert fail.returncode == 1
    assert "INVALID" in fail.stdout


def test_every_allergen_has_urdu_name_and_urdu_for_every_hidden_name():
    rules = load_rules()
    for a in rules["allergens"]:
        assert a["nameUr"], a["id"]
        assert set(a["hiddenNames"]) <= set(a["namesUr"]), a["id"]


def test_display_name_in_both_languages():
    rules = load_rules()
    assert display_name(rules, "dairy", "en") == "Dairy"
    assert display_name(rules, "dairy", "ur") == "دودھ سے بنی اشیاء"
    with pytest.raises(KeyError):
        display_name(rules, "peanut")
