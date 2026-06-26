# Overview

This directory is where we are iterating on our documentation. It serves as a design document just as much as a central place to answer user questions. 

# Pipeline

See [PIPELINE.md](./PIPELINE.md) for how the API research is crawled, extracted, and compared
(diagram + per-stage commands). The pipeline informs but does **not** generate
`architecture-decisions.md`, which is hand-authored.

# Structure

We have diagrammed the API documentation for [Column](./column.md), [Increase](./increase.md), and [Lead](./lead-bank.md)

[core-providers-analysis](./core-providers-analysis.md) is the original notes from Lorenzo analyzing both core providers as well as Baas layers 

# To Do 
- [x] [Helix by Q2](https://helix.q2.com/developers) — summary + OpenAPI + CSV diff done
- [x] [Unit](https://www.unit.co/docs/api/) — summary + OpenAPI + CSV diff done
- [ ] [Green Dot](https://www.greendot.com/business-solutions/developer) — never crawled
- [ ] Setup the TigerBeetle mock server
- [ ] Add an orchestrator script to chain the pipeline stages reproducibly