# Delta annex — Spec-444 vs TMF444 v1.0.0

| Spec-444 location | Extension | TMF444 origin | Class | Rationale |
|---|---|---|---|---|
| Front Matter | companion refs renamed `spec443_profile_ref` / `spec445_agent_card_ref` | TMF444 Front Matter | [M] | align with Spec-44X |
| §2.2 | `model_bindings` resolved through the Model Management Authority (id+version+CID, eval evidence, risk class) | TMF444 §2 (`model_ref` was a free URI) | [M-cond: model adapter] | governed, pinned, signed models; re-cert triggers |
| §6.2 | `environments[]` per-environment override blocks | TMF444 §6 (single env-agnostic deployment; "local" warning) | [M-cond: mobility ≠ Static] | formal per-env rollout without polluting base YAML |
| §6.3 | per-environment deployment & **inventory record** (instance, CIDs, model versions, rollout state, health, metrics vs targets, per-env autonomy case) | TMF444 §6/§8 (no runtime inventory) | [M for production-bound] | answers "which agent version is live where" |
| §8 | per-environment `pre_deploy` signing hook | TMF444 §8 | [M-cond: production] | override-aware signing |
| Annex | `model-authority-record.schema.json` | none | [M] | the authority's record contract |
