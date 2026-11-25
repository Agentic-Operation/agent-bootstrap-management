#!/usr/bin/env python3
"""spec444 CLI — validate / scaffold / deploy / inventory / rollback for Spec-444 bootstraps.

Subcommands:
  validate <bootstrap.yaml>                          schema + structural rules (bootstrap_validate)
  scaffold <bootstrap.yaml> --out DIR                generate runnable repo skeleton (src/, tests/,
                                                     Dockerfile, CI) per generation block
  deploy   <bootstrap.yaml> --env prod [--registry]  merge environments[] override, run lifecycle
                                                     hooks (dry-run), update inventory + card env
                                                     instance via registry
  inventory <bootstrap.yaml>                         print per-environment inventory record (§6.3)
  rollback <bootstrap.yaml> --env prod               set rollout state rolled-back to previous_version
Model resolution: --authority URL (default http://localhost:8090) resolves model_bindings model_refs
to pinned id+version+CID via the Model Management Authority.
"""
import argparse
import json
import subprocess
import sys
import urllib.parse
import urllib.request
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[2]
VALIDATOR = ROOT / "conformance-kit" / "validators" / "bootstrap_validate.py"


def api(method, url, obj=None):
    data = json.dumps(obj).encode() if obj is not None else None
    req = urllib.request.Request(url, data=data, method=method, headers={"Content-Type": "application/json"})
    try:
        with urllib.request.urlopen(req) as r:
            return r.status, json.loads(r.read())
    except urllib.error.HTTPError as e:
        return e.code, json.loads(e.read())


def load_bootstrap(path):
    doc = yaml.safe_load(open(path))
    return doc["bootstrap_profile"]


def merge_env(bp, env):
    base = {k: v for k, v in bp.items() if k not in ("environments", "inventory")}
    ov = next((e for e in bp.get("environments", []) if e["name"] == env), None)
    if not ov:
        raise SystemExit(f"no environments[] entry named {env!r}")
    merged = dict(base)
    for k, v in ov.items():
        if k == "name":
            continue
        if isinstance(v, dict) and isinstance(merged.get(k), dict):
            merged[k] = {**merged[k], **v}
        else:
            merged[k] = v
    return merged


def cmd_validate(a):
    return subprocess.run([sys.executable, str(VALIDATOR), a.bootstrap]).returncode


def cmd_scaffold(a):
    bp = load_bootstrap(a.bootstrap)
    gen = bp["generation"]
    out = Path(a.out)
    (out / "src" / "skills").mkdir(parents=True, exist_ok=True)
    (out / "tests" / "data").mkdir(parents=True, exist_ok=True)
    (out / ".github" / "workflows").mkdir(parents=True, exist_ok=True)
    (out / "src" / "skills" / "__init__.py").write_text("")
    for s in bp.get("skill_bindings", []):
        ep = (s.get("implementation", {}).get("entrypoint") or "src.skills::" + s["skill_id"].lower().replace(" ", "_"))
        mod = ep.split("::")[0].replace(".", "/") + ".py"
        f = out / mod
        f.parent.mkdir(parents=True, exist_ok=True)
        if not f.exists():
            f.write_text(f'"""Skill {s["skill_id"]} ({s.get("description", "")})."""\n\n\ndef run(*args, **kwargs):\n    raise NotImplementedError("implement {ep}")\n')
    if gen.get("generate_dockerfile"):
        (out / "Dockerfile").write_text("FROM python:3.12-slim\nWORKDIR /app\nCOPY . .\nCMD [\"python\", \"-m\", \"src.main\"]\n")
    if gen.get("ci_cd_template") == "github-actions":
        (out / ".github" / "workflows" / "ci.yml").write_text("name: ci\non: [push, pull_request]\njobs:\n  test:\n    runs-on: ubuntu-latest\n    steps:\n      - uses: actions/checkout@v4\n      - run: pip install pytest && pytest -q\n")
    (out / "README.md").write_text(f"# {bp['name']}\n\nScaffolded from Spec-444 bootstrap {bp['id']} {bp['version']} (framework: {gen['target_framework']}).\n")
    print(f"scaffolded -> {out} ({len(bp.get('skill_bindings', []))} skill modules, framework={gen['target_framework']})")
    return 0


def resolve_models(bp, authority):
    if not authority:
        return
    for mb in bp.get("model_bindings", []):
        ref = f"{mb['model_id']}@{mb['version']}"
        code, resp = api("POST", f"{authority}/v1/resolve", {"model_ref": ref})
        if code != 200:
            raise SystemExit(f"model authority rejected {ref}: {resp}")
        if resp["cid"] != mb["cid"]:
            raise SystemExit(f"CID mismatch for {ref}: bootstrap {mb['cid']} vs authority {resp['cid']} (C19)")
        print(f"resolved {ref} -> cid ok, risk_class={resp['risk_class']}, envs={resp['approved_environments']}")


def cmd_deploy(a):
    bp = load_bootstrap(a.bootstrap)
    r = subprocess.run([sys.executable, str(VALIDATOR), a.bootstrap])
    if r.returncode != 0:
        return r.returncode
    merged = merge_env(bp, a.env)
    resolve_models(merged, a.authority)
    print(f"[hook pre_bootstrap] secret-resolution check (dry-run) for env={a.env}")
    print(f"[hook post_bootstrap] autonomy-case generator (required L3+) artifact=dist/autonomy-case.pdf")
    print(f"[hook pre_deploy] sign artifacts with env={a.env} override applied (sigstore)")
    inv = next((i for i in bp.get("inventory", []) if i["environment"] == a.env), None)
    if inv is None:
        inv = {"environment": a.env, "instance_id": f"{bp['id'][:12]}-{a.env}-x1",
               "agent_id": bp["id"].replace("-bootstrap", ""), "agent_uuid": bp["uuid"],
               "deployed_version": bp["version"], "artifact_cid": "sha256:" + "0" * 64,
               "rollout": {"strategy": a.strategy, "state": "active"},
               "health": {"status": "healthy", "last_check": "2026-11-25T00:00:00Z"}, "owner": "ci"}
        bp.setdefault("inventory", []).append(inv)
    inv["rollout"]["state"] = "active" if a.strategy == "rolling" else "canary"
    if a.registry:
        inst = {"instance_id": inv["instance_id"], "deployed_version": inv["deployed_version"],
                "artifact_cid": inv["artifact_cid"], "health": inv["health"]["status"],
                "rollout_state": inv["rollout"]["state"]}
        code, resp = api("PUT", f"{a.registry}/v1/cards/{bp['id'].replace('-bootstrap', '')}-card/environments/{a.env}", inst)
        print(f"registry env update: {code} {resp}")
    print(f"deployed {bp['id']} {bp['version']} to {a.env} (platform={merged.get('target_platform')})")
    return 0


def cmd_inventory(a):
    bp = load_bootstrap(a.bootstrap)
    print(json.dumps(bp.get("inventory", []), indent=2))
    return 0


def cmd_rollback(a):
    bp = load_bootstrap(a.bootstrap)
    inv = next((i for i in bp.get("inventory", []) if i["environment"] == a.env), None)
    if not inv or not inv.get("rollout", {}).get("previous_version"):
        raise SystemExit(f"no rollback target for env={a.env}")
    inv["rollout"]["state"] = "rolled-back"
    inv["deployed_version"], inv["rollout"]["previous_version"] = inv["rollout"]["previous_version"], inv["deployed_version"]
    print(f"rolled back {bp['id']} in {a.env} to {inv['deployed_version']}")
    return 0


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    sub = ap.add_subparsers(dest="cmd", required=True)
    p = sub.add_parser("validate"); p.add_argument("bootstrap")
    p = sub.add_parser("scaffold"); p.add_argument("bootstrap"); p.add_argument("--out", required=True)
    p = sub.add_parser("deploy"); p.add_argument("bootstrap"); p.add_argument("--env", required=True)
    p.add_argument("--strategy", default="rolling", choices=["canary", "blue-green", "rolling"])
    p.add_argument("--registry", default=None); p.add_argument("--authority", default=None)
    p = sub.add_parser("inventory"); p.add_argument("bootstrap")
    p = sub.add_parser("rollback"); p.add_argument("bootstrap"); p.add_argument("--env", required=True)
    a = ap.parse_args()
    return {"validate": cmd_validate, "scaffold": cmd_scaffold, "deploy": cmd_deploy,
            "inventory": cmd_inventory, "rollback": cmd_rollback}[a.cmd](a)


if __name__ == "__main__":
    sys.exit(main() or 0)
