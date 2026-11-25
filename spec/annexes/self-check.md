# Pre-submission self-check (Spec-444 instance)

- [ ] Identity fields match the Spec-443 profile / Spec-445 card (C1–C6).
- [ ] §1 `target_framework` matches profile §3.4 `execution_engine`; version constraint is a closed range.
- [ ] §2 every profile §4.2 skill has a binding with the exact `skill_id`; §2.2 `model_bindings` cover all model adapters.
- [ ] §3 tool bindings map 1:1 to profile §5.2; `env_secrets` are names only; health checks declared.
- [ ] §4 handlers match profile §6.1/§7.2; no speculative handlers.
- [ ] §5 auth provider consistent with profile §8.3; sigstore block consistent with `integrity_wrapper`.
- [ ] §6 base is env-agnostic (no `local` platform in VC); §6.2 `environments[]` present if Cross-Environment; §6.3 inventory populated for production.
- [ ] §7 three-stage workflow all enabled for production (`fail_commit`); acceptance criteria join to profile §9.
- [ ] §8 hooks present; post_bootstrap autonomy-case generator at L3+; pre_deploy signs artifacts.
- [ ] `bootstrap_validate.py` + `crosscheck.py` pass; deviation register records [R]/[O] deviations.
