import subprocess
import sys
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[2]
VAL = ROOT / "conformance-kit/validators/bootstrap_validate.py"
GOOD = ROOT / "examples/loyalty-agent/bootstrap.yaml"


def run(doc):
    tmp = Path("/tmp/_bootstrap_case.yaml")
    tmp.write_text(yaml.safe_dump(doc))
    return subprocess.run([sys.executable, str(VAL), str(tmp)], capture_output=True, text=True)


def test_valid_example_passes():
    r = subprocess.run([sys.executable, str(VAL), str(GOOD)], capture_output=True, text=True)
    assert r.returncode == 0, r.stderr


def test_local_platform_in_base_fails():
    doc = yaml.safe_load(open(GOOD))
    doc["bootstrap_profile"]["deployment"]["target_platform"] = "local"
    r = run(doc)
    assert r.returncode == 1 and "local" in r.stderr


def test_model_ref_without_binding_fails():
    doc = yaml.safe_load(open(GOOD))
    doc["bootstrap_profile"]["model_bindings"] = []
    r = run(doc)
    assert r.returncode == 1 and "model_bindings" in r.stderr


def test_inventory_env_not_in_environments_fails():
    doc = yaml.safe_load(open(GOOD))
    doc["bootstrap_profile"]["inventory"][0]["environment"] = "qa"
    r = run(doc)
    assert r.returncode == 1 and "not in environments" in r.stderr


def test_bad_skill_id_fails():
    doc = yaml.safe_load(open(GOOD))
    doc["bootstrap_profile"]["skill_bindings"][0]["skill_id"] = "OASF-3015"
    r = run(doc)
    assert r.returncode == 1 and "bad skill_id" in r.stderr


def test_warn_failure_policy_fails():
    doc = yaml.safe_load(open(GOOD))
    doc["bootstrap_profile"]["validation"]["failure_policy"] = "warn_only"
    r = run(doc)
    assert r.returncode == 1 and "fail_commit" in r.stderr
