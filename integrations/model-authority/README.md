# Model Management Authority (reference implementation)

Implements the record contract in `spec/annexes/model-authority-record.schema.json` (Spec-444 §2.2):
model registration with schema validation, versioned lookup, `POST /v1/resolve` for pinning
`model_ref` → id+version+CID (used by `spec444 deploy`), deprecation with webhook callbacks that
trigger agent re-validation + autonomy re-certification (cross-check C19).

Run: `python integrations/model-authority/model_authority.py --port 8090 --store models.json`
