# research

Competitor API research that informs (but does not generate) `architecture-decisions.md`.
This directory was reset around the **pipeline** — see **[PIPELINE.md](./PIPELINE.md)** for the
full diagram, per-stage commands, and the confidence-pass procedure.

## Layout

```
research/
├── PIPELINE.md                 # pipeline diagram + stage commands + confidence procedure
├── run_pipeline.py             # orchestrator (crawl→extract→verify→minify→compare)
├── providers.json              # declarative provider config (specs in specs/)
├── specs/                      # OpenAPI input specs the compare stage minifies
├── api_crawler.py              # stage 1 (crawl) — note: SPA limits, see PIPELINE.md
├── semantic_extractor.py       # stage 2 (regex extract)
├── semantic_verifier.py        # stage 2b (advisory)
├── api_validation.py           # crawl QA utility
├── openapi_minifier.py         # stage 3 (minify)
├── api_comparisons.py          # stage 4 (mechanical cross-provider diff)
├── api_analysis_summaries/     # prompts + refresh-2026-06/ (per-provider summaries + comparison)
├── autonomous-compliance/      # compliance system architecture + control-authoring prompts
├── 5300-call-report.md         # NCUA 5300 reporting analysis
├── 5300-call-report-prompt.md  # prompt for the 5300 analysis
└── build/                      # pipeline outputs (gitignored, regenerable)
```

## Quick start

```bash
cd research
python run_pipeline.py --dry-run    # see the plan
python run_pipeline.py              # run all providers
```

## Legacy

Earlier raw provider crawls, vendored SDKs, hand-written analyses, prompts, and source docs were
moved to **`../archive/research-legacy/`** when this directory was reset. They remain for provenance.
