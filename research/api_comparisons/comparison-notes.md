This is what GPT-5 thinking produced when comparing the open API spec or API docs from column, increase, Q2 and unit.

# Authentication / Authorization
- **Increase**
  - **Scheme:** HTTP Bearer.
- **Unit**
  - **Scheme:** HTTP Bearer (JWT).
- **Q2/Helix**
  - **Scheme:** HTTP Basic (program-level); also exposes a customer-scoped auth token endpoint.
- **Column (semantic map)**
  - **Scheme:** API key (inferred from semantic map; not a formal OpenAPI block).

**Differences:** Increase/Unit use bearer tokens; Helix uses basic auth plus customer tokens; Column’s map implies API-key auth (not authoritative).

---

## Customers / Applications / KYC
- **Unit**
  - **Endpoints:**
    - `GET/POST /customers`, `GET/PATCH /customers/{customerId}`
    - `POST /customers/{customerId}/archive`
    - `GET /customers/{customerId}/authorized-users`
    - Applications & documents: `/applications`, `/applications/{id}/cancel`, `/applications/{id}/documents/...` (upload/verify/download)
  - **Key parameters:** Person/business discriminator, SSN/Tax ID, addresses, application document payloads.
  - **Special:** First-class **Applications** with document upload/verification workflow.
- **Q2/Helix**
  - **Endpoints:**
    - `POST /customer/search`, `GET /customer/list`, `GET /customer/getByTag/{tag}`
    - `POST /customer/archive`, `GET /customer/notesList/{customerId}`
    - `GET /customer/generateToken/{customerId}` (customer-level token)
  - **Key parameters:** Search body supports name, identifiers, contact info; paginated (`pageNumber`, `pageSize`).
  - **Special:** Customer search via POST; customer notes; archival; customer-scoped tokens.
- **Increase**
  - **Endpoints:** Customer onboarding paths not prominent in the provided slice; rich **identification** schema (SSN/ITIN/passport/driver’s license).
  - **Special:** Detailed IDV schema coverage.
- **Column (semantic map)**
  - **Objects:** Document/Event/Program; explicit customer endpoints not fully specified.

**Differences:** Unit = full **applications + doc** flow; Helix = **search/notes/archive + customer tokens**; Increase = deep IDV schema; Column = inventory only.

---

## Accounts (Core)
- **Unit**
  - **Endpoints:**
    - `GET/POST /accounts`, `GET/PATCH /accounts/{accountId}`
    - **Actions:** `POST /accounts/{id}/freeze`, `.../unfreeze`, `.../close`, `.../reopen`
    - **DACA:** `POST /accounts/{id}/enter-daca`, `.../activate-daca`, `.../deactivate-daca`
    - Other: `/account-end-of-day`, `/accounts/{id}/limits`, `/accounts/{id}/deposit-products`, `/accounts/{id}/relationships/customers`
  - **Special:** Explicit lifecycle and control actions; EOD balances; DACA controls; relationships.
- **Q2/Helix**
  - **Endpoints:**
    - `GET /account/list/{customerId}`
    - Entitlements: `GET /account/listEntitlements/{customerId}/{accountId}`, `POST /account/addEntitlement`, `POST /account/removeEntitlement`
  - **Special:** Access/role control via entitlements.
- **Increase**
  - **Endpoints:** Not fully visible in slice; see **Account Numbers** as a separate resource (below).
- **Column (semantic map)**
  - **Endpoints:** `POST /bank-accounts/`, `PATCH /bank-accounts/`, `DELETE /bank-accounts/` (delete only at $0 balance).

**Differences:** Unit exposes stateful account actions and DACA; Helix focuses on entitlements; Increase surfaces account numbers separately; Column shows CRUD with a balance constraint (inferred).

---

## Account Numbers
- **Increase**
  - **Endpoints:** `GET /account_numbers`
  - **Key parameters:** Filters such as `status.in`, `ach_debit_status.in`, `account_id`, `created_at.after|before`, `idempotency_key`; cursor pagination.
  - **Special:** Dedicated resource with robust filtering + cursor pagination.
- **Unit / Q2/Helix / Column**
  - Not exposed as a separate top-level resource in the provided material.

**Differences:** Only Increase treats account numbers as a first-class listable resource with filters.

---

## External Accounts / Counterparties
- **Unit**
  - **Endpoints:** `GET/POST /counterparties`, `GET/PATCH /counterparties/{counterpartyId}`, `GET /counterparties/{id}/balance`
  - **Key parameters:** Manual routing details or Plaid processor token.
  - **Special:** Balance endpoint for counterparties; Plaid integration on create.
- **Q2/Helix**
  - **Endpoints:** External Account sections exist (not fully expanded); documents for external accounts also present.
- **Increase**
  - **Notes:** External accounts appear in payment schemas; explicit top-level paths not shown in slice.
- **Column (semantic map)**
  - **Objects:** Counterparty listed; paths unclear.

**Differences:** Unit has the clearest counterparty surface + live balance and Plaid.

---

## Payments / Money Movement

### ACH
- **Unit**
  - **Endpoints:**
    - `GET/POST /payments`, `GET/PATCH /payments/{paymentId}`
    - Actions: `POST /payments/{id}/cancel`
    - Received: `/received-payments` (+ actions: `advance`, `reprocess`)
    - Returns: `/returns/{transactionId}`
    - Recurring ACH: `/recurring-payments` (+ enable/disable)
  - **Special:** Rich action set (cancel/reprocess/advance), recurring ACH management, returns by transaction.
- **Q2/Helix**
  - **Endpoints:** ACH modeled under a generalized **Transfer** surface (create/calc fees/void by type).
- **Increase**
  - **Notes:** ACH transfer list/object with detailed status and submission fields; paths not fully enumerated in slice.
- **Column (semantic map)**
  - **Endpoints:** `/transfers/ach` (list/details; returns concept present).

**Differences:** Unit has explicit **action endpoints** and **recurring** surface; Helix groups ACH under generalized transfers; Increase shows deep ACH semantics; Column offers inferred ACH list/details.

### Wires
- **Increase**
  - **Endpoints:** Wire transfer list/object (includes approval/cancel/reversal/submission fields).
- **Q2/Helix**
  - **Endpoints:** Wire create/void under Transfer category (e.g., `TransferWireCreate...` responses).
- **Unit / Column**
  - Not clearly exposed in the provided slice.

**Differences:** Increase carries full wire lifecycle semantics; Helix exposes wire operations as a category of transfer.

### Card Push / Network Flows
- **Increase**
  - **Endpoints:** `GET/POST /card_push_transfers`, `GET /card_push_transfers/{id}`
  - **Actions:** `POST /card_push_transfers/{id}/approve`, `.../cancel`
  - **Special:** Real-time decisioning + 3DS/auth flows for card network transactions.
- **Unit / Q2/Helix / Column**
  - Not shown in the provided material.

**Differences:** Only Increase provides explicit **card push** endpoints and real-time decision hooks.

---

## Cards / Card Controls
- **Unit**
  - **Endpoints:** `GET/POST /cards`, `GET/PATCH /cards/{cardId}`
  - **Actions:** `POST /cards/{id}/freeze`, `.../unfreeze`, `.../close`, `.../replace`, `.../report-lost`, `.../report-stolen`
  - **Other:** Card limits and PIN status endpoints.
  - **Special:** Full card lifecycle and incident actions.
- **Increase**
  - **Notes:** Card transaction/interchange/merchant data; real-time decision + 3DS.
- **Q2/Helix**
  - **Notes:** Card and Card Limits/Controls sections present (endpoints not expanded).
- **Column**
  - Not surfaced.

**Differences:** Unit emphasizes **operational card controls**; Increase emphasizes **network/auth semantics**.

---

## Transactions
- **Unit**
  - **Endpoints:** `GET /transactions`; per-account: `GET /accounts/{accountId}/transactions/{transactionId}`
  - **Special:** Rich transaction taxonomy (ACH variations, book transfers, purchases, etc.).
- **Q2/Helix**
  - **Endpoints:** Transaction list/detail via envelope responses.
- **Increase**
  - **Notes:** Payment/wire/ach objects link to transaction and pending_transaction ids.
- **Column**
  - **Notes:** Appears under reporting/history rather than as a separate uniform surface.

**Differences:** Unit provides the most granular typed transactions; Helix uses envelope wrappers; Increase links transactions from domain objects.

---

## Statements / Reporting / Exports
- **Increase**
  - **Endpoints:** `GET /statements`, `GET /statements/{id}/html`, `GET /statements/{id}/pdf`, `GET /statements/{accountId}/bank/pdf`
  - **Exports:** Programmatic exports (OFX/BAI2/CSV for statements, transactions, balances).
- **Unit**
  - **Endpoints:** `GET /tax-forms`, `GET /tax-forms/{id}`, `GET /tax-forms/{id}/pdf`; `GET /account-end-of-day`
- **Q2/Helix**
  - **Endpoints:** Statement and bank document list/download endpoints.
- **Column (semantic map)**
  - **Endpoints:** `/reporting` (list); **SettlementReport** object; `/history` daily summaries.

**Differences:** Increase uniquely offers robust **exports**; Helix focuses on **bank document** retrieval; Unit includes **tax forms** and EOD; Column highlights **settlement reports**.

---

## Webhooks / Events
- **Unit**
  - **Endpoints:** `GET/POST /webhooks`, `GET/PATCH /webhooks/{id}`
  - **Actions:** `POST /webhooks/{id}/enable`, `.../disable`
  - **Events:** `GET /events`, `GET /events/{eventId}`
- **Increase**
  - **Special:** Real-time decision webhooks for card flows (approve/deny).
- **Q2/Helix**
  - **Notes:** Eventing exists but not fully expanded in the slice.
- **Column (semantic map)**
  - **Endpoints:** `POST /webhook-endpoints` (create); webhook object + event catalog.

**Differences:** Unit provides full webhook CRUD and enable/disable plus an events feed; Increase focuses on real-time card decision events.

---

## Checks / Stop Payments
- **Unit**
  - **Check deposits:** `GET/POST /check-deposits`, `GET/PATCH /check-deposits/{id}`, `POST /check-deposits/{id}/confirm`, images: `GET /check-deposits/{id}/front|back`
  - **Check payments:** `GET/POST /check-payments`, `GET/PATCH /check-payments/{id}`, actions: `.../approve|cancel|return`, images: `GET /check-payments/{id}/front|back`
  - **Stop payments:** `GET/POST /stop-payments`, `GET/PATCH /stop-payments/{id}`, `POST /stop-payments/{id}/disable`
- **Q2/Helix**
  - **Notes:** Stop Pay present as a category (details not expanded).
- **Column (semantic map)**
  - **Notes:** Check objects appear; exact endpoints not authoritative.

**Differences:** Unit exposes comprehensive **check** lifecycle and images; others are limited or implied.

---

## Fees / Disputes / Rewards
- **Unit**
  - **Endpoints:** `POST /fees`, `POST /fees/reverse`; `GET /disputes`, `GET /disputes/{id}`; `GET /rewards`, `GET /rewards/{id}`
  - **Special:** Programmatic fee reversal; dispute inquiry surface; rewards reporting.
- **Q2/Helix**
  - **Notes:** Fee operations exist; details not expanded.
- **Increase / Column**
  - Not shown in the provided slice.

**Differences:** Unit is the only one clearly exposing **fee reversal** and **disputes** here.

---

## Limits / Controls
- **Unit**
  - **Endpoints:** `GET /accounts/{id}/limits`, `GET /cards/{id}/limits`; account/card freeze/unfreeze actions.
- **Q2/Helix**
  - **Notes:** Dedicated “Account Limits” and “Card Limits and Controls” categories.
- **Increase**
  - **Special:** Enforcement via real-time decisioning (approve/decline with AVS/merchant context).
- **Column**
  - Not explicit.

**Differences:** Unit surfaces limits directly; Helix categorizes them; Increase applies controls via decision webhooks.

---

## Beneficiaries / Relationships
- **Q2/Helix**
  - **Endpoints:** Customer/account **beneficiaries**; **customer relationships** with roles; account **entitlements** add/remove/list.
- **Unit**
  - **Endpoints:** `/accounts/{id}/relationships/customers`
- **Increase / Column**
  - Not prominent in the provided slice.

**Differences:** Helix is strongest on **relationship modeling** and entitlements; Unit has simpler account–customer associations.

---

## Documents / Identity / Verification
- **Unit**
  - **Endpoints:** Application document upload (front/back), verify, download.
  - **Special:** End-to-end application doc workflow.
- **Q2/Helix**
  - **Endpoints:** Bank document list/download; customer document sections.
- **Increase**
  - **Special:** Detailed **identification** schema for individuals (SSN/ITIN/passport/driver’s license/etc.).
- **Column (semantic map)**
  - **Endpoints:** `GET /documents` (list); **Document** object present.

**Differences:** Unit operationalizes doc capture/verify; Helix emphasizes retrieval of bank/customer docs; Increase focuses on identity data structures.

---

## Search / Query / Pagination
- **Increase**
  - **Pattern:** Cursor-based lists (`cursor`, `limit`, `next_cursor`) across list endpoints (e.g., wires, ACH, exports).
- **Q2/Helix**
  - **Pattern:** Envelope responses; POST-based customer search; page-number pagination.
- **Unit**
  - **Pattern:** Conventional resource lists; filters per resource (details vary).
- **Column**
  - **Pattern:** Not clearly defined (semantic map).

**Differences:** Increase prefers **cursor** pagination; Helix uses **POST search** with explicit page controls; Unit is conventional list+filter.

---

## Simulation / Sandbox
- **Unit**
  - **Endpoints:** `/sandbox/atm-deposits`, `/sandbox/cards/{cardId}/activate`, `/sandbox/received-payments`, `/sandbox/received-ach-payment`
  - **Special:** Simulators for card activation and inbound payments.
- **Q2/Helix / Increase / Column**
  - Not explicitly shown in the provided slice.

**Differences:** Only Unit exposes explicit **sandbox simulators** here.

---

# Quick Capability Gaps
- **Relationship modeling/beneficiaries:** Strong in Helix; simpler in Unit; not prominent in Increase/Column.
- **Card push + 3DS/real-time decisions:** Only Increase shows an explicit surface.
- **Checks:** Only Unit provides full deposit/payment/imagery and stop-pay actions.
- **Exports/Statements:** Increase uniquely supports programmatic exports; Unit includes tax forms and EOD; Helix focuses on bank docs.
- **Sandbox:** Only Unit exposes simulators in the provided material.
- **Column file:** Semantic inventory—treat endpoints as hints, not canonical.

---

## Organizational Notes (Architecture & Workflow)
- **Increase:** Deep network/payment semantics (ACH status, wire lifecycle, card auth/3DS), real-time decisioning; cursor lists.
- **Unit:** Operational action endpoints (accounts/cards/payments), applications + doc workflows, comprehensive checks, sandbox simulators.
- **Q2/Helix:** Program/customer/account/transfer framing with envelope responses, POST search, entitlements, bank docs, stop pay.
- **Column:** Objects/reports/webhooks inventoried; patterns present but not authoritative.


API comparison prompt:

TASK: Analyze the provided OpenAPI specification(s) and create a comprehensive object catalog in the following format.
OUTPUT FORMAT:
For each major object/capability, use this structure:
## [Object/Capability Name]
- **[Provider A]:**
  - Endpoints: [List all endpoints with HTTP methods]
  - Key parameters: [Required and notable optional parameters]
  - [Any special features, sub-resources, or unique capabilities]
- **[Provider B]:**
  - Endpoints: [List all endpoints]
  - Key parameters: [Key parameters]
  - [Special features]
- **Differences:** [Concise comparison highlighting implementation differences, capabilities present in one but not another, and architectural distinctions]
ANALYSIS SCOPE:
Systematically extract and document:

Authentication/Authorization - How API access is secured
Core Resources - Primary business objects (customers, accounts, transactions, etc.)
Lifecycle Operations - Create, read, update, delete, archive, close, reopen, etc.
Sub-Resources - Objects nested under primary resources (account numbers under accounts, beneficiaries under customers, etc.)
Actions - State transitions and operations (approve, cancel, freeze, reverse, etc.)
Relationships - How objects connect (explicit relationship endpoints vs embedded references)
Supporting Resources - Documents, notes, events, webhooks, etc.
Search/Query Capabilities - List, search, filter, pagination patterns
Compliance/Verification - KYC, document management, verification workflows
Financial Operations - All money movement types (transfers, payments, fees, etc.)
Reporting/Analytics - Statements, exports, balance history, etc.
Configuration/Metadata - Program settings, product definitions, limits, etc.
Simulation/Testing - Sandbox endpoints if present

EXTRACTION RULES:

For each endpoint, show the full path pattern and HTTP method
List parameters as they appear in the spec (required first, then notable optionals)
Note when data is handled through embedded objects vs separate endpoints
Highlight unique capabilities (tags for search, custom fields, special workflows)
Identify missing capabilities explicitly (e.g., "Provider B: No beneficiary management")
For arrays/collections, note pagination and filtering options
Include both operational endpoints (GET, POST, PATCH) and action endpoints (approve, cancel, etc.)

ORGANIZATIONAL HIERARCHY:
Group related endpoints logically:

Main object operations first
Sub-resources and relationships next
Actions and state transitions last
Note when operations are nested vs flat (e.g., /loans/{id}/payments vs /payments?loan_id={id})

DIFFERENCES SECTION GUIDELINES:
Focus on:

Architectural differences (dedicated endpoints vs embedded data)
Capability gaps (present in one, absent in another)
Workflow differences (approval steps, state machines)
Data model differences (required fields, additional metadata)
Avoid generic statements; be specific about what differs

APPLY THIS ANALYSIS TO THE PROVIDED OPENAPI SPECIFICATION(S).