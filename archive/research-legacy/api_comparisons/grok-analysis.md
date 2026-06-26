# STEP A — CONTEXT

- **Summarized API content to analyze**: Detailed comparison of APIs from Unit, Q2 Helix, Increase, and Column, covering authentication, customer/entity management, accounts, limits/controls, beneficiaries, cards, transfers (ACH, wire, RTP, checks), loans, FX, transactions, webhooks/events, bookkeeping, simulation/testing, reporting/statements, documents, and compliance/verification. Key differences include Increase's double-entry ledger and OAuth; Column's loans/FX/simulations; Q2 Helix's entitlements/beneficiaries/questionnaires; Unit's unified payments/DACA.

- **Business goals**: BaaS for fintechs enabling embedded retail banking, card issuing, payments (domestic/international), and basic lending; support multi-tenant fintech partners with white-labeling.

- **Compliance & region**: US-focused (ACH, Fedwire, RTP, FDIC); Reg E (electronic transfers), PCI-DSS (card data), BSA/AML/KYC (OFAC screening), GLBA (privacy).

- **Scale & SLAs**: 1M end-users across tenants, 500 TPS peak, 99.95% uptime (5-min downtime/month).

- **Tech stack preferences**: Go (for services/performance), PostgreSQL (ACID transactions/ledger), Kafka (event streaming/webhooks).

- **Security posture**: Zero trust (mTLS, JWT validation), encryption at rest (AES-256), per-tenant data isolation (row-level security in DB).

- **Non-negotiables**: Double-entry ledger (every txn debits/credits), immutable audit trail (append-only logs), ACID settlement (no partial txns).

# 1. Gap Analysis

After applying Elon's algorithm, the unified design retains core coverage from all providers (e.g., accounts, payments, KYC) but deletes redundant endpoints (e.g., separate domestic/international wires), simplifies to unified resources (e.g., single "transfers" endpoint), accelerates via Kafka for async events, and automates compliance checks in pipelines—reducing API surface by ~40% for faster iteration.

## Covered Capabilities
- **Authentication/Authorization**: All cover basics (Bearer/API keys); Increase's OAuth is retained as baseline.
  - *Questioned requirement*: Do we need full OAuth platform for third-party apps? Yes, for BaaS extensibility, but scoped to client credentials flow only.
  - *Delete/combine*: Delete Q2's Basic Auth (insecure); combine Unit/Increase Bearer with Column's keys into single JWT scheme.
  - *Simplify*: Use one token endpoint with scopes (read/write/transfer).
  - *Accelerate*: Shorten token expiry to 1h; use Kafka for revocation events to enable real-time invalidation.
  - *Automate*: Script token rotation via CI/CD hooks on deploy.

- **Customer/Entity Management**: Strong across all (CRUD, types: individual/business); Q2's tags/dormancy, Increase's entity types (trusts/gov), Unit's authorized users.
  - *Questioned requirement*: Separate person/business endpoints (Column/Q2)? No—unify for simplicity, as 80% use cases overlap.
  - *Delete/combine*: Delete Q2's separate createBusinessApplication (combine into POST /entities); delete email/tag lookups (use unified search).
  - *Simplify*: Single "entity" resource with type discriminator (natural/corp/trust); embed KYC status.
  - *Accelerate*: Index entity IDs in PostgreSQL for <1ms lookups at 500 TPS.
  - *Automate*: Auto-generate tokens on create (Q2-inspired) via event triggers.

- **Account Management**: Comprehensive CRUD/freezes/closes; Increase's multi-numbers/IntraFi, Q2's entitlements, Unit's DACA/reopen.
  - *Questioned requirement*: DACA/IntraFi as core? Questioned for retail focus—retain IntraFi optionally, delete DACA (niche lending).
  - *Delete/combine*: Delete separate reopen (use PATCH status); combine entitlements into entity relationships.
  - *Simplify*: Unified /accounts with sub-resources for numbers/limits; tags as metadata.
  - *Accelerate*: Async account creation via Kafka (sync balance query).
  - *Automate*: Auto-enroll IntraFi on high-balance thresholds via rules engine.

- **Payments/Transfers (ACH/Wire/RTP/Checks)**: Unit's unified payments, Increase/Column's dedicated (prenotes/drawdowns/positive pay/tracking); Q2 minimal.
  - *Questioned requirement*: Separate endpoints per type (e.g., Column's domestic/intl wire)? No—unify to reduce cognitive load.
  - *Delete/combine*: Delete Q2's limited ACH; combine all into /transfers with type (ach/wire/rtp/check); delete inbound/outbound splits (use direction param).
  - *Simplify*: Single schema for transfers: type, amount, counterparty, metadata (e.g., prenote flag).
  - *Accelerate*: Batch approvals via Kafka streams for 500 TPS.
  - *Automate*: Auto-return failed ACH (Reg E) via cron jobs.

- **Card Issuance/Management**: Unit/Q2/Increase strong (freeze/lost/provision); Column none.
  - *Questioned requirement*: Separate physical/digital (Increase)? No—unify with status flag.
  - *Delete/combine*: Delete Q2 mocks (sandbox-only); combine lost/stolen into /cards/{id}/suspend.
  - *Simplify*: /cards with type (physical/virtual), embed limits/PIN status.
  - *Accelerate*: Async provisioning to wallets via Kafka.
  - *Automate*: Auto-freeze on fraud detection (Increase real-time engine).

- **Transaction Management**: Unit/Increase/Q2 unified lists; Increase's pending/declined.
  - *Questioned requirement*: Tag-based (Q2)? Useful but not core—embed in query params.
  - *Delete/combine*: Delete fee creation (use ledger entries); combine pending/declined into filtered /transactions.
  - *Simplify*: Unified /transactions?filter=status:pending with pagination.
  - *Accelerate*: Cache recent txns in Redis for sub-100ms queries.
  - *Automate*: Auto-categorize fees via ML rules.

- **Webhooks/Events**: All have basics; Column's 68 events/tracking, Increase's subscriptions/decisions.
  - *Questioned requirement*: 68 events? Overkill—consolidate to 20 core (e.g., txn.created, account.frozen).
  - *Delete/combine*: Delete event retrieval (use webhooks); combine subscriptions with deliveries.
  - *Simplify*: /webhooks with event_types array; idempotent via UUID.
  - *Accelerate*: Kafka for fan-out delivery (<50ms latency).
  - *Automate*: Auto-retry deliveries (3x) with exponential backoff.

- **Compliance/Verification (KYC/AML)**: Embedded (Q2 questionnaires, Increase confirm, Unit apps, Column validations).
  - *Questioned requirement*: Interactive Q2 questions? Yes for AML, but standardize to workflow states.
  - *Delete/combine*: Delete IBAN/Fedwire validates (use external service); combine docs/uploads into /entities/{id}/compliance.
  - *Simplify*: Workflow: pending/verified/rejected with auto-screening hooks.
  - *Accelerate*: Parallel doc verification via async Kafka.
  - *Automate*: Integrate OFAC screening on entity create.

- **Reporting/Statements/Documents**: Unit's formats, Increase exports, Q2 multi-lang.
  - *Questioned requirement*: Multi-format (HTML/PDF)? PDF only for compliance.
  - *Delete/combine*: Delete app-centric docs (Unit); combine into /files with links.
  - *Simplify*: /statements/{id}?format=pdf; bulk /exports.
  - *Accelerate*: Pre-generate statements nightly via Kafka jobs.
  - *Automate*: Auto-archive docs after 7y (GLBA).

## Missing Capabilities for Complete Banking Core/BaaS
- **Ledger/Bookkeeping**: Only Increase has double-entry; missing immutable audit, reconciliation.
  - *Questioned requirement*: Full T-accounts? Essential for non-negotiable double-entry.
  - *Delete/combine*: N/A (add new).
  - *Simplify*: Append-only /ledger_entries with debit/credit.
  - *Accelerate*: Sharded PostgreSQL for 1M txns/day.
  - *Automate*: Auto-reconcile daily via scripts.

- **Loan Management**: Only Column; missing for basic lending goal.
  - *Questioned requirement*: Full 19 endpoints? Scope to core (create/pay/schedule).
  - *Delete/combine*: N/A (add simplified).
  - *Simplify*: /loans with sub-resources for payments/disbs.
  - *Accelerate*: Async disbursements.
  - *Automate*: Auto-schedule payments.

- **FX**: Only Column; missing for intl payments.
  - *Questioned requirement*: Rate sheets? Use external oracle, expose quotes only.
  - *Delete/combine*: N/A.
  - *Simplify*: /fx/quotes?from=USD&to=EUR.
  - *Accelerate*: Cache rates 5min.
  - *Automate*: Auto-hedge on large transfers.

- **Beneficiaries**: Only Q2; missing for transfers.
  - *Questioned requirement*: Two-tier? Unify to entity-linked.
  - *Delete/combine*: N/A.
  - *Simplify*: /beneficiaries linked to entity/account.
  - *Accelerate*: Bulk add via CSV import.
  - *Automate*: Auto-verify beneficiaries on add.

- **Simulation/Testing**: Column/Q2 partial; missing unified mocks for BaaS onboarding.
  - *Questioned requirement*: 11 sim endpoints? Sandbox-only, delete from prod.
  - *Delete/combine*: Combine into /simulate/{type}.
  - *Simplify*: Single /simulate with payload.
  - *Accelerate*: Local dev mocks via Go stubs.
  - *Automate*: CI/CD integration tests.

# 2. Normalized Domain Model

Applying the algorithm pruned entities to essentials (questioned bloat like separate "mock" types, deleted duplicates like person/business, simplified relationships to many-to-one, accelerated with indexes, automated schema migrations via DB tools), yielding a minimal model supporting double-entry and isolation.

Key entities: Entity (unified customer), Account, Transaction (unified transfer/fee), LedgerEntry (double-entry), Card, Beneficiary, Loan (optional), File (docs), WebhookSubscription.

```yaml
Entity:  # Required by AML/KYC (BSA)
  id: string (UUID, required, PK)
  type: enum(natural, corp, trust, gov, required)  # Compliance: entity type for screening
  details: object(name: string, email: string, phone: string, address: object, ssn_ein: string(encrypted))  # GLBA privacy
  status: enum(pending, verified, dormant, archived, required)  # Internal: dormancy tracking
  kyc: object(status: enum(pending, verified, rejected), docs: array(ref File))  # BSA/AML
  created_at: timestamp (immutable, audit)
  updated_at: timestamp

Account:  # ACID balances
  id: string (UUID, PK)
  entity_id: string (ref Entity, required)
  type: enum(deposit, credit, loan, required)
  name: string
  balance: decimal(15,2)  # Internal: real-time via ledger
  numbers: array(object(routing: string, account: string))  # Increase-inspired
  status: enum(open, frozen, closed, required)
  limits: object(daily: decimal, type: enum(transfer, spend))  # Reg E
  intrafi_enrolled: boolean (optional)  # FDIC extension
  tags: array(string)  # Q2-inspired, metadata
  created_at: timestamp (immutable)

Transaction:  # Unified payments/fees
  id: string (UUID, PK)
  type: enum(ach, wire, rtp, check, fee, required)
  direction: enum(inbound, outbound, internal)
  amount: decimal(15,2, required)
  currency: string (default USD)
  status: enum(pending, completed, failed, declined, required)  # Increase tiers
  from_account_id: string (ref Account)
  to_account_id: string (ref Account)  # Or beneficiary/external
  beneficiary_id: string (ref Beneficiary, optional)
  metadata: object(prenote: boolean, tracking_id: string)  # Column-inspired
  created_at: timestamp (immutable, audit)

LedgerEntry:  # Double-entry, non-negotiable
  id: string (UUID, PK)
  txn_id: string (ref Transaction, required)
  account_id: string (ref Account, required)
  entry_type: enum(debit, credit, required)
  amount: decimal(15,2, required)
  balance_after: decimal(15,2)  # Internal: for reconciliation
  timestamp: timestamp (immutable, append-only)
  # Per-tenant isolation: row filter on tenant_id (hidden)

Card:
  id: string (UUID, PK)
  account_id: string (ref Account, required)
  type: enum(physical, virtual, debit, credit, required)
  status: enum(active, frozen, closed, required)
  limits: object(daily: decimal)
  pin_status: enum(set, unset)  # Unit-inspired, PCI-DSS
  wallet_tokens: array(string)  # Q2 provisioning

Beneficiary:  # Q2-inspired
  id: string (UUID, PK)
  entity_id: string (ref Entity, required)
  account_id: string (ref Account, optional)  # Two-tier support
  details: object(name: string, routing: string, account: string)
  verified: boolean (AML)

Loan:  # Column-inspired, optional for MVP
  id: string (UUID, PK)
  entity_id: string (ref Entity, required)
  account_id: string (ref Account, required)  # Linked credit account
  principal: decimal(15,2)
  rate: decimal(5,4)
  schedule: array(object(due_date: date, amount: decimal))  # Immutable

File:  # Docs/compliance
  id: string (UUID, PK)
  entity_id: string (ref Entity, required)
  type: enum(kyc, statement, check_image, required)  # BSA
  url: string (encrypted at rest)
  status: enum(uploaded, verified)
  created_at: timestamp

WebhookSubscription:
  id: string (UUID, PK)
  endpoint: string (required)
  events: array(enum(txn.created, account.frozen), required)
  tenant_id: string (per-tenant isolation)
  secret: string (for sig validation)
```

Relationships: Entity 1:M Account/Card/Beneficiary/Loan/File; Account 1:M Transaction/LedgerEntry/Card; Transaction 1:M LedgerEntry (double-entry: one debit, one credit per txn).

# 3. API Surface Blueprint

The blueprint consolidates ~200 endpoints across providers to ~50 (deleted type-specific paths, combined CRUD, simplified params to JSON bodies), using REST with OpenAPI 3.0; accelerates with async responses (202 Accepted + webhook); automates idempotency via client-provided UUID.

```yaml
openapi: 3.0.0
info:
  title: Unified BaaS API
  version: 1.0.0
servers:
  - url: https://api.baas.example.com/v1
security:
  - bearerAuth: []  # JWT, scopes: read, write, transfer
components:
  securitySchemes:
    bearerAuth:
      type: http
      scheme: bearer
      bearerFormat: JWT
  schemas:
    Entity: # Ref to YAML above
    TransactionRequest:
      type: object
      required: [type, amount, to_account_id]
      properties:
        type: {enum: [ach, wire, rtp, check]}
        amount: {type: number, format: decimal}
        idempotency_key: {type: string}  # UUID, automated retry
    Error: {type: object, properties: {code: string, message: string}}
paths:
  # Auth & Access Control
  /auth/tokens:
    post:
      summary: Create/refresh token
      parameters: [{name: grant_type, in: query, enum: [client_credentials]}]
      requestBody: {required: true, content: {application/json: {schema: {type: object, properties: {client_id: string, client_secret: string}}}}}
      responses:
        '200': {description: Token, content: {application/json: {schema: {type: object, properties: {access_token: string, expires_in: integer}}}}}
      notes: Idempotent via client_id; rate: 100/min; scope: write (OAuth-inspired, Increase).

  # Account Management
  /accounts:
    post:
      summary: Create account
      requestBody: {required: true, content: {application/json: {schema: {type: object, properties: {entity_id: string, type: string, name: string}}}}}
      responses:
        '201': {description: Account, content: {application/json: {schema: { $ref: '#/components/schemas/Account' }}}}
      notes: Async via Kafka; idempotent: true; rate: 50/min; security: write.
    get:
      summary: List accounts
      parameters: [{name: entity_id, in: query, schema: {type: string}}, {name: status, in: query, enum: [open, frozen]}]
      responses: {'200': {description: Array of Accounts}}
      notes: Paginated (?limit=100); rate: 200/min; security: read.

  /accounts/{account_id}:
    get:
      summary: Get account
      parameters: [{name: account_id, in: path, required: true, schema: {type: string}}]
      responses: {'200': {description: Account}}
      notes: Includes balance (ACID query); rate: unlimited; security: read.
    patch:
      summary: Update/freeze/close
      requestBody: {content: {application/json: {properties: {status: enum(open,frozen,closed), limits: object}}}}
      responses: {'200': {description: Updated Account}}
      notes: Idempotent; rate: 100/min; security: write.

  /accounts/{account_id}/numbers:
    post: {summary: Add routing/account number, responses: {'201': {description: Numbers array}}, notes: Increase-inspired; rate: 10/min; security: write}

  # Ledger Entries and Balances
  /ledger_entries:
    get:
      summary: List entries (audit trail)
      parameters: [{name: account_id, in: query}, {name: since, in: query, schema: {type: string, format: date-time}}]
      responses: {'200': {description: Array of LedgerEntry}}
      notes: Append-only, immutable; paginated; rate: 500/min; security: read (internal policy).

  /accounts/{account_id}/balance:
    get: {summary: Get current balance, responses: {'200': {properties: {available: decimal, pending: decimal}}}, notes: Real-time ACID; rate: unlimited; security: read}

  # Transfers and Settlements
  /transfers:
    post:
      summary: Create transfer (unified ACH/wire/RTP/check)
      requestBody: {content: {application/json: { $ref: '#/components/schemas/TransactionRequest' }}}
      responses:
        '202': {description: Accepted (async settlement), content: {application/json: {properties: {id: string, status: pending}}}}
        '400': {description: Invalid, $ref: '#/components/schemas/Error'}
      notes: Idempotent via key; approval workflow if >$10k; rate: 500 TPS; security: transfer; settles ACID via ledger.

  /transfers/{transfer_id}:
    get: {summary: Get transfer, responses: {'200': { $ref: '#/components/schemas/Transaction' }}, notes: Includes ledger entries; rate: 200/min; security: read}
    patch: {summary: Cancel/update (pre-settlement), responses: {'200': {description: Updated}}, notes: Only pending; rate: 100/min; security: write}

  /transfers/{transfer_id}/approve: {post: {summary: Two-step approve (Increase), responses: {'204': {description: No content}}, notes: Async Kafka; rate: 100/min; security: write}}

  # KYC/AML Lifecycle
  /entities:
    post:
      summary: Create entity
      requestBody: {content: {application/json: {properties: {type: string, details: object}}}}
      responses: {'201': { $ref: '#/components/schemas/Entity' }}
      notes: Triggers auto-KYC screen; rate: 50/min; security: write.
    get: {summary: List, parameters: [{name: status, in: query, enum: [pending,verified]}], responses: {'200': {description: Array<Entity>}}, notes: Paginated; security: read}

  /entities/{entity_id}/confirm:
    post:
      summary: Confirm KYC (questionnaire/docs)
      requestBody: {content: {application/json: {properties: {answers: array(object), docs: array(ref File)}}}}
      responses: {'200': {description: Updated Entity}}
      notes: Q2-inspired; auto-AML check; rate: 20/min; security: write.

  /entities/{entity_id}/compliance:
    get: {summary: Get KYC status/docs, responses: {'200': {properties: {status: string, docs: array}}}, notes: BSA audit; security: read}

  # Webhooks or Event Streams
  /webhooks:
    post:
      summary: Subscribe to events
      requestBody: {content: {application/json: {properties: {endpoint: string, events: array(string)}}}}
      responses: {'201': {description: Subscription}}
      notes: Column-inspired; sig validation; rate: 10/min; security: write.
    get: {summary: List subscriptions, responses: {'200': {description: Array<WebhookSubscription>}}, notes: Per-tenant; security: read}

  /events:  # For polling fallback
    get:
      summary: List recent events
      parameters: [{name: since, in: query}]
      responses: {'200': {description: Array of {id: string, type: string, payload: object, timestamp: timestamp}}}
      notes: Kafka-backed; rate: 100/min; security: read.
```

# 4. Service & Data Decomposition

Algorithm application: Questioned monolith needs (decomposed to microservices for scale); deleted cross-service coupling (use Kafka events); simplified to 6 services (from potential 12); accelerated with async boundaries (90% events); automated ownership via DB schemas with RLS.

| Service | Data Ownership | APIs (Sync/Async) | Boundaries |
|---------|----------------|-------------------|------------|
| **Auth** | Tokens, scopes (Redis cache) | Sync: /auth/tokens (JWT issue/validate). Async: revocation events to Kafka. | Sync for API gateway; async for expiry pushes. Per-tenant keys isolated. |
| **Entity/KYC** | Entities, Files (PostgreSQL blobs, encrypted) | Sync: /entities CRUD, /confirm. Async: verification complete -> Kafka (triggers account create). | Sync for compliance gates; async for doc processing (e.g., OCR). Owns KYC records. |
| **Account** | Accounts, Balances (PostgreSQL, sharded) | Sync: /accounts CRUD/balance. Async: freeze -> Kafka (notifies cards). | Sync queries (ACID); async updates for limits. Owns numbers/limits. |
| **Ledger** | LedgerEntries, Transactions (PostgreSQL append-only) | Sync: /ledger_entries GET (read-only). Async: txn create -> Kafka (settles double-entry). | Eventual consistency for reports; ACID for balances. Owns immutable trail. |
| **Payments** | Transfers (PostgreSQL + Kafka for orchestration) | Sync: /transfers POST/GET (idempotent). Async: approve/settle -> Kafka (to external networks). | Sync init; async settlement (e.g., RTP push). Owns txn metadata. |
| **Events** | Subscriptions, Deliveries (PostgreSQL + Kafka) | Sync: /webhooks CRUD. Async: All events published to Kafka (fan-out). | Fully async; retries automated. Owns webhook logs for SLAs. |
| **Cards** (Optional MVP) | Cards (PostgreSQL) | Sync: /cards CRUD/freeze. Async: provision -> Kafka (wallets). | Sync for auth; async for physical print. |
| **Loans/FX** (Post-MVP) | Loans/FX quotes (PostgreSQL + external oracle) | Sync: /loans CRUD, /fx/quotes. Async: disbursement -> Kafka (to ledger). | Sync quotes; async exec. |

Data: All in PostgreSQL (tenant_id RLS); Kafka for cross-service events (e.g., entity.verified -> account.create).

# 5. Ledger & Transaction Logic

Questioned per-provider txns (unified to double-entry); deleted reversals as direct ops (use compensating entries); simplified to append-only; accelerated with Kafka for parallelism; automated settlement via sagas—ensuring ACID for core (settlement) and eventual for reports.

**Recording**: Append-only LedgerEntry per Transaction: On create, pending txn posts no entries; on settle, create debit/credit pair (e.g., deposit: debit cash, credit account; amount matches, balances update atomically). Holds: Temp negative entry (reversible). Reversals: New compensating txn (e.g., return: credit original debit). Immutable: No updates/deletes; audit via txn_id chain.

**Consistency**: ACID for settlement (PostgreSQL txns: atomic double-entry, isolation via locks, durable writes). Eventual for aggregates (e.g., reports via Kafka streams). Rationale: ACID prevents balance errors (Reg E); eventual scales to 500 TPS without locking contention.

**Transaction Flows** (Sequences as Mermaid-like pseudocode):

- **Deposit (e.g., ACH inbound)**:
  1. POST /transfers (type=ach, direction=inbound) -> 202 Accepted, publish kafka:transfer.pending.
  2. External network confirms -> kafka:transfer.confirmed.
  3. Ledger service: BEGIN TXN; INSERT LedgerEntry (txn_id, account_id=to, debit, balance_after); UPDATE Account balance; COMMIT.
  4. Publish kafka:transfer.settled -> webhook.

- **Payout (e.g., Wire outbound)**:
  1. POST /transfers (type=wire, >$10k? -> /approve) -> pending.
  2. Approve -> kafka:transfer.approved.
  3. Payments: External send -> on success: Ledger debit from_account, credit external (or intermediary).
  4. If fail: Compensating credit back; publish failed.

- **Reversal (e.g., ACH return)**:
  1. POST /transfers (type=ach, reference=original_id, direction=return) -> auto-links.
  2. On settle: INSERT compensating entries (reverse signs); update statuses.
  3. Kafka: reversal.settled -> audit log.

# 6. Security & Compliance Blueprint

Questioned legacy auth (upgraded to zero trust); deleted manual verifs (automated); simplified controls to per-endpoint scopes; accelerated audits via Kafka logs; automated scans in CI—mapping directly to regs for auditability.

**Mapping**:
| Requirement | Control | Implementation |
|-------------|---------|----------------|
| **PCI-DSS** (Card data) | Tokenization, no storage | Cards: PAN encrypted/transient; limits via scopes; quarterly scans automated. |
| **SOC 2** (Availability/Confidentiality) | Encryption at rest/transit, access logs | AES-256 PostgreSQL; mTLS + JWT; immutable Kafka audit trail (all API calls logged). |
| **AML/KYC (BSA)** | Screening, docs verify | Auto-OFAC on /entities POST (external API hook); Q2-style confirm workflow; retain 5y. |
| **Reg E (Transfers)** | Error resolution, limits | 10-day dispute window (automated holds); limits enforced in Ledger pre-commit. |
| **GDPR/GLBA** (Privacy, US equiv.) | Consent, data isolation | Per-tenant RLS; delete on archive; consent flags in Entity. |

**Encryption**: At-rest: PostgreSQL TDE; in-transit: TLS 1.3. **Key Management**: AWS KMS (rotate 90d, HSM-backed). **Audit Logging**: Append-only Kafka topic (events: who/what/when); queryable via /audit?since=...; automated retention (7y BSA, purge after).

# 7. MVP BaaS Roadmap

Algorithm drove MVP to core only (questioned loans/FX—postponed; deleted sims from prod); simplified to auth/entity/account/transfers/ledger; accelerated cycles via Kafka prototypes (weekly deploys); automated testing/compliance early for 99.95% SLAs.

- **30 Days: Critical Path to Functional Core**
  - Week 1-2: Scaffold services (Auth, Entity, Account) in Go; PostgreSQL schemas; basic CRUD APIs. Integrate Kafka for entity create -> account.
  - Week 3: Add /transfers (ACH focus) with pending ACID ledger.
  - Week 4: Basic webhooks; unit/integration tests (80% coverage automated).
  - Milestone: Sandbox with 10 TPS; manual KYC flow.

- **60 Days: Accelerate Iteration**
  - Add cards (freeze/provision, sync to accounts); RTP/wire stubs.
  - Shrink cycles: CI/CD pipeline (GitHub Actions) for deploys (<1h); Kafka mocks for parallel dev (e.g., test transfers without DB).
  - Performance: Load test to 200 TPS; optimize queries (indexes).
  - Milestone: Beta with 1 fintech tenant; auto-KYC integration.

- **90 Days: Automate & Expand**
  - Full transfers (checks, approvals); double-entry reconciliation cron.
  - Automate: Compliance scans (SonarQube for PCI); e2e tests (Cypress for APIs); monitoring (Prometheus for 99.95% uptime alerts).
  - Post-MVP: Loans/FX as feature flags.
  - Milestone: Prod launch, 500 TPS certified; OAuth extensions.