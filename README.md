# Agent Bootstrap Management (Spec-444): An AI Agent Bootstrap Spec

**Spec-444** is the *onboard* contract of the agent triad: a declarative YAML (`bootstrap_profile` root
key) that, when processed by a runtime scaffolder, instantiates an AI agent as a runnable component —
runtime targeting, skill bindings to code/models, **tool & MCP server bindings**, protocol handlers,
security/secrets injection, deployment & observability, validation, and lifecycle hooks.

Spec-444 extensions over TM Forum **TMF444 v1.0.0** (alpha; delta in `spec/annexes/delta-vs-TMF44X.md`):
per-environment `environments[]` overrides, `model_bindings` resolved through the Model Management
Authority, and the **per-environment deployment/inventory record** (which agent version is live where).

- **Status:** Draft — `spec/SPEC-444.md` v1.0.0-alpha merged on `main` (PRs #1–#3); comms pack canonical in [agent-standard-docs](https://github.com/Agentic-Operation/agent-standard-docs). **License:** Apache-2.0

## The triad (sibling repos)

| Verb | Spec | Repo |
|---|---|---|
| Define | Spec-443 | [`agent-profile-management`](https://github.com/Agentic-Operation/agent-profile-management) |
| **Onboard** (this repo) | Spec-444 | `Agentic-Operation/agent-bootstrap-management` |
| Source | Spec-445 | [`agent-discovery-card`](https://github.com/Agentic-Operation/agent-discovery-card) |

Join keys across the triad: identity fields (`id`, `uuid`, `version`, `provider`, CID, `integrity_wrapper`),
`skill_id` string equality, bidirectional companion pointers — see the
[triad overview](https://github.com/Agentic-Operation/agent-standard-docs/blob/main/communication/00-triad-overview.md) in agent-standard-docs.

## Repository map

| Directory | Purpose |
|---|---|
| `spec/` | Normative Spec-444 text + annexes (incl. model-authority record schema) |
| `schemas/` | `bootstrap.schema.json` + environment-override schema + test vectors |
| `examples/loyalty-agent/` | Worked example `bootstrap.yaml` + per-env override files |
| `conformance-kit/` | YAML schema validator, Annex-E cross-check, CI templates, runtime integrity check |
| `api/openapi/` | Bootstrap validation + scaffold API |
| `tools/cli/` | `spec444 validate/scaffold/deploy --env <name>` CLI |
| `integrations/` | Model authority resolution, secrets backends, Sigstore hooks, per-env deploy targets |
| `user-tools/` | Scaffolded project skeletons, CI templates |
| `docs/communication/` | Pointer to the canonical comms pack in [agent-standard-docs](https://github.com/Agentic-Operation/agent-standard-docs) |
| `docs/guides/` `docs/architecture/` `docs/references/` | Quickstarts, diagrams, related sources |

## Quickstart

See [docs/guides/quickstart-write-a-bootstrap.md](docs/guides/quickstart-write-a-bootstrap.md) and the
[02-onboard-your-agent](https://github.com/Agentic-Operation/agent-standard-docs/blob/main/communication/02-onboard-your-agent.md) one-pager in agent-standard-docs.

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md). Branch convention `vibe/<slug>-5a1ad6`, draft PRs.

## Runtime services (this org)

| Service | Repo |
|---|---|
| Agent Card Registry | [Agent-Registry](https://github.com/Agentic-Operation/Agent-Registry) |
| Model Management Authority (this repo's schema annex) | [model-authority](https://github.com/Agentic-Operation/model-authority) |
| Rollout controller (this repo's bootstrap API deploy/inventory/rollback) | [agent-rollout-controller](https://github.com/Agentic-Operation/agent-rollout-controller) |
| Orchestrator (swarm/hierarchy) | [agent-orchestrator](https://github.com/Agentic-Operation/agent-orchestrator) |
| Tool & MCP manager (this repo's §3) | [tool-mcp-manager](https://github.com/Agentic-Operation/tool-mcp-manager) |
| Conformance kit | [agent-conformance](https://github.com/Agentic-Operation/agent-conformance) |
| Published docs / comms pack (canonical) | [agent-standard-docs](https://github.com/Agentic-Operation/agent-standard-docs) |
