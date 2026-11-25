# Agent Bootstrap Management (Spec-444): An AI Agent Bootstrap Spec

**Spec-444** is the *onboard* contract of the agent triad: a declarative YAML (`bootstrap_profile` root
key) that, when processed by a runtime scaffolder, instantiates an AI agent as a runnable component —
runtime targeting, skill bindings to code/models, **tool & MCP server bindings**, protocol handlers,
security/secrets injection, deployment & observability, validation, and lifecycle hooks.

Spec-444 extensions over TM Forum **TMF444 v1.0.0** (alpha; delta in `spec/annexes/delta-vs-TMF44X.md`):
per-environment `environments[]` overrides, `model_bindings` resolved through the Model Management
Authority, and the **per-environment deployment/inventory record** (which agent version is live where).

- **Status:** Draft — Phase 0 comms pack pending; **Phase 1**: normative `spec/SPEC-444.md` v1.0.0-alpha on `vibe/spec-draft-5a1ad6`. **License:** Apache-2.0

## The triad (sibling repos)

| Verb | Spec | Repo |
|---|---|---|
| Define | Spec-443 | [`agent-profile-management`](https://github.com/Agentic-Operation/agent-profile-management) |
| **Onboard** (this repo) | Spec-444 | `Agentic-Operation/agent-bootstrap-management` |
| Source | Spec-445 | [`agent-discovery-card`](https://github.com/Agentic-Operation/agent-discovery-card) |

Join keys across the triad: identity fields (`id`, `uuid`, `version`, `provider`, CID, `integrity_wrapper`),
`skill_id` string equality, bidirectional companion pointers — see
[docs/communication/00-triad-overview.md](docs/communication/00-triad-overview.md).

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
| `docs/communication/` | Audience one-pagers (onboard one-pager here; canonical triad pack in agent-profile-management) |
| `docs/guides/` `docs/architecture/` `docs/references/` | Quickstarts, diagrams, related sources |

## Quickstart

See [docs/guides/quickstart-write-a-bootstrap.md](docs/guides/quickstart-write-a-bootstrap.md) and
[docs/communication/02-onboard-your-agent.md](docs/communication/02-onboard-your-agent.md).

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md). Branch convention `vibe/<slug>-5a1ad6`, draft PRs.
