# Changelog

Format: [Keep a Changelog](https://keepachangelog.com/en/1.1.0/). Versions follow SemVer.

## [Unreleased]

### Added

- Phase 0 communication package: triad overview, audience one-pagers, model management authority
  overview, glossary, FAQ, conformance cheat sheet, worked-example walkthrough, references index,
  architecture diagrams (mermaid).
- Repo scaffolding: `docs/`, `spec/`, `schemas/`, `examples/`, `conformance-kit/`, `api/`, `tools/`,
  `integrations/`, `user-tools/`, `tests/`, GitHub templates and docs-lint workflow, pre-commit config.

### Added (Phase 1)

- `spec/SPEC-444.md` normative draft v1.0.0-alpha with extensions: §2.2 `model_bindings`, §6.2
  `environments[]` overrides, §6.3 per-environment deployment/inventory record, §8 per-env pre_deploy;
  annexes incl. `model-authority-record.schema.json`.
- `schemas/`: bootstrap, environment-override, inventory-record JSON Schemas.
- Worked example: `examples/loyalty-agent/bootstrap.yaml` + `environments/prod.yaml`.
- `conformance-kit/`: `bootstrap_validate.py`, `crosscheck.py`, pytest suite, CI gate; active
  `.github/workflows/ci-gate.yml`.
- `api/openapi/bootstrap-api.yaml` (validate / scaffold / deploy / inventory / rollback).

### Added (Phase 2)

- `integrations/model-authority/model_authority.py`: reference Model Management Authority implementing
  `spec/annexes/model-authority-record.schema.json` — register/resolve (pinned id+version+CID)/deprecate
  with re-certification webhooks (C19).
- `tools/cli/spec444.py`: validate / scaffold / deploy (env override merge + model resolution + hooks +
  inventory + registry env-instance update) / inventory / rollback.
- CI: ci-gate runs validate + scaffold smoke; new `cross-triad` job runs crosscheck.py across siblings.

### Changed (Phase 2 reshape)

- `integrations/model-authority/` moved to **model-authority** repo (schema annex stays canonical in
  `spec/annexes/model-authority-record.schema.json`); `spec444 deploy/inventory` delegate to
  **agent-rollout-controller** service.
- Comms pack moved to **agent-standard-docs**; `docs/communication/` is now a pointer.
- `cross-triad` CI job uses **agent-conformance** validators; README/REFERENCES link all service repos.
