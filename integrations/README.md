# integrations

Runtime services live in their own repos in this org — the contracts stay canonical here:

- **model-authority** — Model Management Authority service implementing
  `spec/annexes/model-authority-record.schema.json` (moved from `integrations/model-authority/`):
  <https://github.com/Agentic-Operation/model-authority>
- **agent-rollout-controller** — deploy/inventory/rollback service implementing
  `api/openapi/bootstrap-api.yaml` (default <http://localhost:8091>): <https://github.com/Agentic-Operation/agent-rollout-controller>
- **tool-mcp-manager** — MCP servers/tool bindings from §3: <https://github.com/Agentic-Operation/tool-mcp-manager>
- **agent-conformance** — canonical validators used by the `cross-triad` CI job:
  <https://github.com/Agentic-Operation/agent-conformance>

Secrets backends (Vault/AWS/GCP/K8s) and Sigstore signing hooks plug in here.
