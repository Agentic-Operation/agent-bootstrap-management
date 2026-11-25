# spec444 CLI

`python tools/cli/spec444.py <subcommand>`:

- `validate <bootstrap.yaml>` — schema + structural rules (`conformance-kit/validators/bootstrap_validate.py`)
- `scaffold <bootstrap.yaml> --out DIR` — generate runnable repo skeleton per `generation` + `skill_bindings`
- `deploy <bootstrap.yaml> --env prod [--strategy canary] [--registry URL] [--authority URL]` — merge
  `environments[]` override, resolve `model_bindings` via the Model Management Authority, run lifecycle
  hooks, update the §6.3 inventory record and the card's environment instance
- `inventory <bootstrap.yaml>` — print the per-environment inventory record
- `rollback <bootstrap.yaml> --env prod` — roll back to `previous_version`
