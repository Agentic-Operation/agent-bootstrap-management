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
