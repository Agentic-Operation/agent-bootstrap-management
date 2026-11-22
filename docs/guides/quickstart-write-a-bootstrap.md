# Quickstart: write your first Spec-444 bootstrap

1. Start from `examples/loyalty-agent/bootstrap.yaml` (Phase 1) — it joins to the Spec-443 profile and
   Spec-445 card of the same agent.
2. Fill `generation` to match the profile's declared `execution_engine` (Spec-443 §3.4).
3. List every profile §4.2 skill in `skill_bindings` with the exact `skill_id`; set
   `implementation.model_ref` to a model registered in the Model Management Authority.
4. Declare `tool_bindings`/`mcp_servers` for each profile §5.2 system; put secret **names** in
   `env_secrets` only.
5. Add `protocol_handlers` matching the profile §6.1 coordination posture.
6. Configure `security_config` (auth provider must match profile §8.3) and enable Sigstore signing for
   production.
7. Add `environments[]` overrides (dev/stage/prod) and the inventory record entries.
8. Validate: `pre-commit run --all-files`, then `spec444 validate` and the CI gate (Phase 1).
9. Scaffold and deploy: `spec444 scaffold` → `spec444 deploy --env dev` (Phase 2 tooling).
