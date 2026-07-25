## Cassandra BaaS-centric Banking Core — archive of record

**The live work moved to [cassandra-platform](https://github.com/Cassandra-Labs-Foundation/cassandra-platform) in July 2026.**

This repo is kept for what only exists here: `archive/` — 344 files of POC and legacy
implementations that were deliberately not carried forward.

| moved to cassandra-platform | where it landed |
|---|---|
| `architecture-decisions.md` | `core/architecture-decisions.md` |
| `research/` | `core/research/` (the NCUA 5300 analysis went to `analytics/reference/`) |
| `verifier/` | `core/verifier/` |
| `compliance-floor.yaml` | `core/compliance-floor.yaml` |

The decision log moved because the core cites it — `-- per D4`, `(D23)` — nearly 400 times,
and while it lived here those citations resolved to nothing. cassandra-platform now enforces
them in CI (`scripts/check_decision_refs.py --strict`).

`compliance-system-architecture.md` was **not** carried forward, on purpose. It sits under
`archive/research-legacy/` and is a 2024 sketch: right about the shape, wrong about every name
(Kafka, `openapi.yaml`, `vocabulary.json` — all superseded, Kafka by decision D4) and the count
(223 controls; there are now 333). Its successor is cassandra-platform's top-level `README.md`.

### Still here, and why

- `archive/` — tiger-beetle-core (Go), core-ui (Next.js), blnk-core, stablecoin-core, plus
  `archive/research-legacy/` (283 files). POCs, archived June 2026. Not carried forward.
- `controls.json`, `core-api.yaml`, `core-vocabulary.json` — the version-pinned snapshot that
  `verifier/targets.json` was enumerated from (529 targets, 75 resources, 143 endpoints).
  Kept deliberately: `core-api.yaml` here is the **original bespoke flat format**, while
  cassandra-platform's spec is OpenAPI 3.0.3. The verifier's `parse_core_api` still reads the
  bespoke format only, so this file is both the reference for porting that parser and the
  provenance of the last valid enumeration. See `core/README.md` over there.

### Note on core-ui

`archive/core-ui/` is byte-identical to the standalone
[core-ui](https://github.com/Cassandra-Labs-Foundation/core-ui) repo's HEAD (2025-05-14) apart
from three `.DS_Store` files, and the same 32 files are now also at `ui/` in
cassandra-platform. Three copies; this is the archival one.
