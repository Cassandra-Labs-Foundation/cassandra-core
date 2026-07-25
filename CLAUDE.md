# Cassandra Core - Project Guide

> ## ⚠ This repo is an archive. The live work is in [cassandra-platform](https://github.com/Cassandra-Labs-Foundation/cassandra-platform).
>
> Moved there in July 2026: `architecture-decisions.md` → `core/architecture-decisions.md`,
> `research/` → `core/research/`, `verifier/` → `core/verifier/`, `compliance-floor.yaml` →
> `core/compliance-floor.yaml`. The banking core itself lives at `core/supabase/` there, and
> the compliance policies at `compliance/policies/`.
>
> What remains here is `archive/` — the POCs documented below — plus the version-pinned
> spec snapshot the verifier's `targets.json` was enumerated from. Everything below this
> banner describes those archived POCs and is accurate for them.

## What This Is

Cassandra is a **BaaS-centric banking core** built for **Pynthia Credit Union**. It provides a vertically integrated core banking system with the ability to white-label to other credit unions. Each credit union hosts its own instance, and each fintech partner operates on a fully isolated instance with an aggregator layer providing cross-fintech visibility for compliance and Fed settlement.

## Repository Structure

```
cassandra-core/
├── controls.json               # pinned snapshot (321 controls) — provenance for verifier/targets.json
├── core-api.yaml               # pinned spec in the ORIGINAL bespoke format (not OpenAPI)
├── core-vocabulary.json        # pinned, derived from the above
└── archive/                    # Archived implementation POCs (legacy — not active)
    ├── tiger-beetle-core/      # Go backend API server (the BaaS API)
    ├── core-ui/                # Next.js frontend (credit union staff console)
    ├── blnk-core/              # Blnk Finance ledger integration (POC)
    └── stablecoin-core/        # Stablecoin-based ledger exploration (early R&D)
```

> **Note:** `tiger-beetle-core`, `core-ui`, `blnk-core`, and `stablecoin-core` were moved under `archive/`. Path references in the sections below (e.g. `cd tiger-beetle-core`) are now relative to `archive/`.

## Architecture Overview

**Instance-per-fintech isolation** with a centralized **aggregator layer** per credit union:

- **Aggregator Layer**: Origination API (stateless decision maker), Payment Hub, BSA Approver, BSA Reporter, 5300 Reporter
- **Fintech Instance**: Blnk Deploy (managed ledger) + BaaS API + Control Engine + Supabase + DuckDB
- **Event Architecture**: PostgreSQL append-only event log with cursor-based consumers (no Kafka)
- **Infrastructure**: Blnk Deploy + Supabase (managed PostgreSQL) + DuckDB (analytics)

Key invariant: `Sum(all fintech customer balances) == Fed Master Account balance`

## tiger-beetle-core (Go Backend)

**Language**: Go 1.22.5
**Framework**: Gin
**Module**: `github.com/Cassandra-Labs-Foundation/core`

### Tech Stack
- **gin-gonic/gin** - HTTP framework
- **golang-jwt/jwt/v4** - Authentication
- **Supabase** - Entity storage (REST API client)
- **TigerBeetle** - Ledger (stub/mock currently)

### Directory Layout
```
tiger-beetle-core/
├── cmd/
│   ├── server/main.go            # Entry point
│   ├── mock-tigerbeetle/main.go  # Mock ledger for testing
│   └── tbtest/main.go            # Real TigerBeetle client test
├── internal/
│   ├── api/                      # HTTP handlers
│   │   ├── auth/handler.go
│   │   ├── person/handler.go
│   │   ├── business/handler.go
│   │   ├── ledger/handler.go
│   │   └── middleware/auth.go
│   ├── service/                  # Business logic
│   │   ├── auth/service.go
│   │   ├── person/service.go
│   │   ├── business/service.go
│   │   └── ledger/service.go
│   ├── repository/               # Data access (Supabase REST)
│   │   ├── person.go
│   │   ├── business.go
│   │   └── ledger.go
│   ├── clients/                  # External integrations
│   │   ├── supabase/client.go
│   │   └── tigerbeetle/client.go
│   └── config/config.go
├── pkg/jwt/jwt.go                # Reusable JWT package
└── development-notes.md
```

### API Endpoints (base: `/api/v1`)
- `POST /auth/login`, `POST /auth/refresh`, `GET /auth/validate`
- `POST|GET /entities/person`, `GET|PATCH /entities/person/{id}`
- `POST|GET /entities/business`, `GET|PATCH /entities/business/{id}`
- `POST /ledger/account`, `POST /ledger/transfer`

### Patterns
- **Layered architecture**: Handler -> Service -> Repository -> Client
- **Dependency injection**: Services receive repos via constructor, repos receive clients
- **JWT auth middleware**: Bearer token validation on all routes except login/refresh
- **Supabase tables**: `person_entities`, `business_entities`
- **Error variables**: Defined per service package (e.g., `ErrPersonNotFound`)

### Config (environment variables)
- `SERVER_PORT` (default: 8080), `JWT_SECRET`, `JWT_EXPIRY_MINUTES` (default: 60)
- `SUPABASE_URL`, `SUPABASE_API_KEY` (required)
- `DB_HOST`, `DB_PORT`, `DB_USER`, `DB_PASSWORD`, `DB_NAME`

### Running Tests
```bash
cd tiger-beetle-core
# Integration test scripts:
./auth-and-person-test.sh
./auth-and-business-test.sh
./auth-and-ledger-test.sh
```

## core-ui (Next.js Frontend)

**Framework**: Next.js 15.3 (Pages Router, JavaScript)
**Styling**: Tailwind CSS 4
**Icons**: Lucide React

### Structure
```
core-ui/src/
├── pages/                    # Routes
│   ├── index.jsx             # Dashboard (home)
│   ├── teller.jsx            # Teller operations (most built-out)
│   ├── member-services.jsx   # Placeholder
│   ├── lending.jsx           # Placeholder
│   ├── accounting.jsx        # Placeholder
│   ├── reports.jsx           # Placeholder
│   └── administrator.jsx     # Placeholder
├── components/
│   ├── layout/MainLayout.jsx # Sidebar + header shell
│   ├── dashboard/Dashboard.jsx
│   └── teller/
│       ├── Teller.jsx
│       ├── TellerDrawer.jsx
│       └── MemberQuickEdit.jsx
├── lib/
│   ├── context/SessionContext.js  # Global state (user, drawer, notifications)
│   └── mock.js                    # Mock data layer (800ms latency)
└── styles/globals.css
```

### Commands
```bash
cd core-ui
npm run dev      # Development server
npm run build    # Production build
npm run lint     # ESLint
```

### What's Built
- Responsive sidebar navigation (7 sections, collapses on mobile)
- Dashboard with account cards and transaction table
- Full teller module: cash drawer (buy/sell/balance), member quick-edit with tabs (account info, quick transaction, transaction history), transaction journal with filters
- Mock data layer simulating API delays
- Session context with user info, permissions, and teller drawer state

### What's Placeholder
- Member Services, Lending, Accounting, Reports, Administrator pages
- Real API integration (everything uses mock.js currently)
- Authentication hardening

## Key Architecture Decisions

These are documented in `core/architecture-decisions.md` in **cassandra-platform** (28
decisions; the file moved out of this repo). Critical ones:

1. **Entity Hierarchy**: Unified `/entities` namespace, separate creation endpoints per type (person, business, trust, joint)
2. **Account Model**: 1:Many account-to-account-number (one ledger account, multiple external numbers)
3. **Ledger**: Blnk (double-entry) + shadow bookkeeping layer for 5300/FBO tagging
4. **Events**: PostgreSQL append-only log + cursor-based consumers (NOT Kafka)
5. **Multi-Tenancy**: Instance-per-fintech with aggregator layer
6. **Control Engine**: 321 base controls, `compliance_floor` controls cannot be disabled
7. **Idempotency**: Header-based (`Idempotency-Key`), never expires, 409 on reuse with different args
8. **Error Format**: Increase-style with `request_id` and `doc_url`
9. **Pagination**: Transparent cursor (ID-based, `?after=transfer_789`)
10. **Infrastructure**: Blnk Deploy + Supabase (managed) + DuckDB (analytics)

## Compliance

- **321 controls** across 14 categories (BSA/AML, CDD, Fair Lending, Collections, Cybersecurity, etc.)
- Controls are first-class API primitives, not afterthoughts
- `compliance_floor: true` controls are always enforced (e.g., OFAC screening)
- Controls defined in `controls.json`
- Compliance system architecture: `archive/research-legacy/compliance-system-architecture.md` — STALE (Kafka, openapi.yaml, vocabulary.json all superseded). The current description is cassandra-platform's top-level README.md. `decision-process.md` moved to `core/research/` there.

## Research Directory

Contains extensive competitive analysis and design work:

- `api_analysis_summaries/` - Summaries of Galileo, Unit, Increase, Column, Moov, Helix, Mambu APIs
- `api_comparisons/` - Cross-provider comparison analyses
- `endpoint_comparisons/` - CSV-based endpoint and property comparisons
- `jacob-design/` - Early architecture design (ARCHITECTURE.md, core-spec.md, modules.md)
- `compliance-system-architecture.md`, `decision-process.md` - Compliance system architecture + control-authoring decision process
- `increase/`, `lead-bank/` - Provider-specific flow charts and schemas
- Python scripts: `api_crawler.py`, `semantic_extractor.py`, `semantic_verifier.py`, `api_validation.py`

## Conventions

- **Go**: Standard Go project layout (`cmd/`, `internal/`, `pkg/`), interface-based dependency injection
- **Frontend**: Next.js Pages Router (not App Router), React functional components with hooks, Tailwind utility classes
- **API Design**: RESTful, Increase-style error responses, cursor pagination, HMAC-SHA256 webhook signatures
- **Database**: Supabase PostgreSQL via REST API (not direct SQL connections from Go)
- **Naming**: Entity types are `person`, `business`, `trust`, `joint`; accounts have types like `DDA`, `SDA`, `IRA`, `HSA`
- **State Machines**: Minimal states with controls as gates (e.g., Entity: PENDING -> ACTIVE <-> DISABLED -> ARCHIVED)

## Development Status

| Component | Status |
|-----------|--------|
| Architecture decisions (28) | Complete (v1.1) |
| Compliance controls (321) | Defined |
| Go API (auth, entities) | Working MVP |
| Go API (ledger) | Stub/mock |
| Core UI (dashboard, teller) | Working MVP |
| Core UI (other modules) | Placeholder |
| Blnk integration | POC phase |
| Stablecoin exploration | Early R&D |
| Real API integration (UI <-> Go) | Not started |
