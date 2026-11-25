# Spec-444 — AI Agent Bootstrap (normative draft v1.0.0-alpha)

**Status:** Draft. **Base:** TM Forum TMF444 v1.0.0 (alpha) — this document is TMF444 plus the
extensions in `annexes/delta-vs-TMF444.md` (marked **[EXT]**). TMF444 is an additive extension of an
IG1412-compliant agent specification: all fields live under a `bootstrap_profile` root key.
A bootstrap specification is a declarative YAML configuration that, processed by a runtime scaffolder,
instantiates an AI agent as a runnable software component.

## Front Matter [M]

Cover block (title `"{Agent Name} — AI Agent Bootstrap Specification"`, doc id, version+date, owner,
status, conformance class); **Identity & Integrity [M]** — `id`, `name`, `uuid`, `version`, `provider`,
`content_identifier_cid`, `integrity_wrapper`; MUST match the Spec-443 profile and Spec-445 card.
**Companion artifacts [M]** — `spec443_profile_ref`, `spec445_agent_card_ref`; bidirectional.
Conformance clause [M] — [M]/[R]/[O]/[M-cond], section-presence + field-level classes.

## §1 Generation & Runtime Targeting [M] — `bootstrap_profile.generation`

`target_framework` ∈ open-agent-spec | wayflow | langgraph | crewai | autogen | custom (MUST match the
profile §3.4 `execution_engine`); `framework_version_constraint` (closed range); `language` ∈ python |
typescript | go | java | rust; `output_structure` ∈ modular | monolithic | microservice; `include_tests`,
`generate_dockerfile` (booleans); `ci_cd_template` ∈ github-actions | gitlab-ci | jenkins | none;
`license_header` (SPDX).

## §2 Skill Bindings [M] — `bootstrap_profile.skill_bindings`

Per binding: `skill_id` [M] (string-equality join to profile §4.2 / card §5; TMF prefix mandatory),
`bound_core_task` [M] (join to profile §4.1), `source_taxonomy` [M], `description` [R],
`implementation.adapter` [M] ∈ huggingface_pipeline | mlflow_model | langgraph_subgraph | wayflow_node |
python_function | custom; `implementation.model_ref` [R, required for model adapters];
`implementation.entrypoint` [R]; `implementation.fallback_behavior` [O] ∈ cache_or_default |
retry_with_backoff | fail_closed | custom.

### §2.2 Model Bindings [EXT] [M-cond: any model-based adapter]

`bootstrap_profile.model_bindings` — one entry per model referenced by `skill_bindings`:

```yaml
model_bindings:
  - model_id: "churn-scorer"            # Model Management Authority record id
    version: "2.3.1"                    # pinned semver — resolved + signature-verified at deploy
    cid: "sha256:..."                   # content identifier from the authority record
    authority_endpoint: "https://models.example.com/v1/models"   # authority API
    eval_evidence_ref: "https://models.example.com/v1/models/churn-scorer/2.3.1/eval"
    risk_class: "medium"                # authority-assigned; constrains impact radius x autonomy
```

Cross-check C19: model id + version + CID must equal the profile §3.1/§9.2 refs and the card
`modelGovernance` extension. Re-registration or deprecation in the authority triggers re-validation +
autonomy re-certification. The authority record schema is normative in
`annexes/model-authority-record.schema.json`.

## §3 Tool & MCP Server Configuration [M] — `tool_bindings` + `mcp_servers`

`tool_bindings` maps tool name → binding (`type` ∈ mcp_tool | mcp_resource | rest_api | function;
`mcp_server`, `function_name`, `resource_path`, `auth_scope`; each binding corresponds to a profile §5.2
touchpoint). `mcp_servers[]`: `name` [M], `transport` ∈ stdio | sse | websocket | http [M], `command`/`args`
[R for stdio; `${ENV_VAR}` placeholders resolved at deploy time], `env_secrets` [M] (names only — values
come from the secrets manager; never embed secret values), `health_check.endpoint` [R].

## §4 Protocol Handlers [R] — `protocol_handlers`

Map protocol ∈ rep | a2a_jsonrpc | mcp | wo_a | custom → `handler_module` [M] + `config` [M]; joins to
profile §6.1 posture and §7.2 handshake (cross-check C10). Do not declare handlers the agent never uses.

## §5 Security & Configuration Injection [M] — `security_config`

`auth.provider` ∈ oauth2_oidc | keycloak | mtls | api_key | custom (must match profile §8.3 — cross-check
C13); `auth.issuer`, `auth.client_id_env` (resolved from secrets manager at deploy time),
`auth.token_validation` ∈ jwks_uri | introspection | static_jwk; `auth.scopes_required` [M];
`secrets_management.backend` ∈ aws_secrets | gcp_secret_manager | hashicorp_vault | kubernetes_secrets |
env_only, `kv_path`, `refresh_interval`; `sigstore_integration{enabled, issuer, rekor_url, sign_artifacts}`
— consistent with the `integrity_wrapper` (cross-check C6).

## §6 Deployment, Observability & Environments [R] — `deployment` (+ [EXT] below)

Base `deployment` (environment-agnostic — never commit `target_platform: "local"` to version control):
`target_platform` ∈ kubernetes | serverless | vm_bare | container; `resource_constraints`
(memory/cpu request+limit, gpu_optional); `scaling` (min_replicas — 0 for L4+, ≥1 below to keep surfaces
warm — max_replicas, metric ∈ cpu_utilization | request_rate | queue_depth | custom);
`observability` (logging format json for production; metrics exporter prometheus | otel | cloudwatch |
stackdriver | none; tracing otel | jaeger | zipkin | none).

### §6.2 Environment overrides [EXT] [M-cond: mobility ≠ Static]

`bootstrap_profile.environments[]` — one entry per environment; the base spec stays env-agnostic and the
scaffolder merges the matching override at deploy time:

```yaml
environments:
  - name: "prod"
    target_platform: "kubernetes"
    resource_constraints: {memory_request: "4Gi", memory_limit: "8Gi", cpu_request: "2000m"}
    scaling: {min_replicas: 2, max_replicas: 10, metric: "request_rate", target_utilization: 70}
    endpoints: {base_url: "https://agents.example.com"}
    secrets_management: {kv_path: "secret/data/agents/loyalty-management-agent/prod"}
    feature_flags: {adaptive_layer: true}
```

Schema: `schemas/environment-override.schema.json`. Cross-check C20: environment names must match the
profile §10.1a and the card `environment-instances` extension.

### §6.3 Deployment & inventory record [EXT] [M for production-bound]

`bootstrap_profile.inventory` (or a standalone `inventory-record.yaml`, schema
`schemas/inventory-record.schema.json`) — the per-environment record of what is actually running:

```yaml
inventory:
  - environment: "prod"
    instance_id: "lma-prod-7f3c9d"        # runtime instance identifier
    agent_id: "loyalty-management-agent-v1"
    agent_uuid: "9e3b2f5d-..."
    deployed_version: "1.0.0-stable"
    artifact_cid: "sha256:..."             # signed image/package CID (stage-3 check)
    bootstrap_cid: "sha256:..."            # this YAML's CID
    card_cid: "sha256:..."                 # Spec-445 card CID
    model_versions: [{model_id: "churn-scorer", version: "2.3.1", cid: "sha256:..."}]
    rollout: {strategy: canary, state: active, previous_version: "0.9.2"}
    health: {status: healthy, last_check: "2026-11-25T00:00:00Z"}
    metrics_vs_targets: [{metric: "redemption_validation_p95_latency_ms", target: "<= 500", actual: 412}]
    autonomy_case_ref: "https://grc.example.com/autonomy-cases/loyalty-management-agent-v1/prod"
    last_deployed: "2026-11-20T10:00:00Z"
    owner: "loyalty-platform-team"
```

Cross-checks: joins to all three triad artifacts on identity/CID fields (C1–C6); `artifact_cid` must match
the signed artifact in the transparency log at runtime (stage 3); environment names match C20.

## §7 Validation & Testing [M] — `validation` + `testing`

`validation`: `spec_schema_uri` [M], `strict_mode` [M], `pre_commit_hooks` [M] (≥1 schema validator + 1
secret-leak detector), `failure_policy` ∈ fail_commit | warn_only | log_only (production MUST
fail_commit). `testing`: `unit_test_framework` [M], `integration_test_config{mock_services, test_data_path}`,
`acceptance_criteria` (metric + threshold; join to profile §9 — cross-check C16). Minimum workflow:
stage 1 pre-commit (yamllint + schema + secret scan), stage 2 CI gate (schema + triad cross-check +
tests), stage 3 runtime (integrity_wrapper vs transparency log; aborts startup).

## §8 Lifecycle Hooks [M] — `lifecycle_hooks`

`pre_bootstrap` [R] (SHOULD include secret-resolution check), `post_bootstrap` [R] (SHOULD include
autonomy-case generator — **required at L3+**, cross-check C17), `pre_deploy` [M] (MUST include artifact
signing for production). Each entry: `script`, `fail_on_error` [M]. **[EXT]** hooks run per environment:
`pre_deploy` signing verifies the `environments[]` override applied for the target environment.

## Annexes

- `annexes/delta-vs-TMF444.md`, `annexes/cross-check-manifest.md`, `annexes/self-check.md`
- `annexes/model-authority-record.schema.json` — normative Model Management Authority record schema
- Worked example: `../examples/loyalty-agent/` (bootstrap.yaml + environments/ + inventory-record.yaml)
