# Cross-check manifest — Spec-444 side

The full triad manifest (C1–C20) is canonical in
`agent-profile-management/spec/annexes/cross-check-manifest.md`. Bootstrap-side joins enforced by
`conformance-kit/validators/bootstrap_validate.py` + `crosscheck.py`:

- C1–C6 identity/CID/integrity: bootstrap Front Matter ≡ profile ≡ card.
- C7/C8: `skill_bindings[*].skill_id` ⊇ profile §4.2 skill IDs (string equality, TMF prefix mandatory);
  `bound_core_task` matches profile §4.1.
- C9: `tool_bindings` keys join to profile §5.2 systems.
- C10: `protocol_handlers` keys ⊇ profile §6.1 protocol.
- C13: `security_config.auth.provider` consistent with profile §8.3.
- C16: `testing.acceptance_criteria` metric names + thresholds match profile §9.
- C17: `lifecycle_hooks.post_bootstrap` emits the autonomy case at L3+.
- C19 [EXT]: `model_bindings` ≡ profile §3.1/§9.2 model refs ≡ card `modelGovernance`.
- C20 [EXT]: `environments[*].name` ≡ profile §10.1a ≡ card `environment-instances`; `inventory[].environment` ∈ `environments[*].name`.
- C6 [EXT]: `inventory[].artifact_cid` must match the Sigstore-signed artifact in the transparency log (stage-3 runtime check).
