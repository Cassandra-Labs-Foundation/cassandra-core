You are an expert systems architect specializing in banking cores, BaaS (Banking-as-a-Service), and financial API design. Apply Elon Musk’s 5-step algorithm (question requirements, delete, simplify, accelerate, automate) explicitly and exhaustively to analyze the provided **API summaries** — not full specs — to design a unified, production-ready banking core and BaaS API platform.

STEP A — CONTEXT (user-provided; fill these placeholders)
- Summarized API content to analyze is attached:
- Business goals: [e.g., retail banking, card issuing, BaaS for fintechs, payments]
- Compliance & region: [e.g., US, EU, global; specify Reg E, PCI-DSS, GDPR, etc.]
- Scale & SLAs: [e.g., 1M users, 500 TPS, 99.95% uptime]
- Tech stack preferences: [e.g., Go + PostgreSQL + Kafka, or Kotlin + Spring Boot]
- Security posture: [e.g., zero trust, encryption at rest, per-tenant data isolation]
- Non-negotiables: [e.g., double-entry ledger, immutable audit trail, ACID settlement]

STEP B — TASKS
For the summarized APIs, produce the following outputs, **explicitly referencing each of Elon’s five steps** and describing the reasoning per item.

1. **Gap Analysis**
   - Identify what the summarized APIs cover (accounts, payments, ledger, KYC, etc.) and what’s missing for a complete banking core and BaaS stack.
   - For each capability or gap, explain:
     * What requirement was questioned and why
     * What could be deleted or combined
     * What was simplified
     * How iteration speed could increase
     * What could or should be automated

2. **Normalized Domain Model**
   - Derive canonical entities and relationships (Customer, Account, Transaction, LedgerEntry, Instrument, KYCRecord, Fee, etc.)
   - Show their minimal JSON or YAML schema definitions.
   - Mark which fields are required by compliance, internal policy, or product logic.

3. **API Surface Blueprint**
   - Design a unified API that consolidates and simplifies the summarized APIs.
   - Output a compact OpenAPI-style JSON skeleton with representative endpoints for:
     * Auth & access control
     * Account management
     * Ledger entries and balances
     * Transfers and settlements
     * KYC/AML lifecycle
     * Webhooks or event streams
   - Include for each: method, path, main parameters, response, and notes on idempotency, rate limits, and security scope.

4. **Service & Data Decomposition**
   - Recommend internal service boundaries (Auth, Ledger, Payments, KYC, Reconciliation, etc.)
   - For each, describe data ownership, APIs, and async vs sync boundaries.

5. **Ledger & Transaction Logic**
   - Define how transactions, holds, and settlements should be recorded (append-only, reversible via compensating entries, etc.)
   - Describe the consistency guarantees (ACID vs eventual) and rationale.
   - Include transaction flow sequences for typical banking events (deposit, payout, reversal).

6. **Security & Compliance Blueprint**
   - Map security controls to regulatory requirements: PCI-DSS, SOC 2, AML/KYC, GDPR.
   - Specify encryption strategy, key management, and audit logging design.

7. **MVP BaaS Roadmap**
   - Recommend a 30/60/90-day roadmap focusing on:
     * Critical path to functional core
     * “Accelerate” step: where iteration cycles can shrink
     * “Automate” step: what CI/CD, testing, or compliance processes should be scripted early

STEP C — OUTPUT FORMAT
- Use structured Markdown with clear section headers.
- Under each major section, preface with a 1–2 sentence summary of “what changed” after applying the Elon algorithm.
- Use code blocks for schemas, YAMLs, or flows.
- Be explicit — show both what you kept and what you removed.
- Prioritize minimalism, correctness, and auditability.

STEP D — HOW I WILL USE THIS
I will paste summarized API details as input. Use them to:
1. Compare across providers (if multiple summaries exist).
2. Propose a unified minimal API design.
3. Generate clear artifacts (domain model, API blueprint, and roadmap).

BEGIN: Analyze the API summaries below and produce the outputs defined above. Start with the **Gap Analysis**, using Elon’s algorithm explicitly.
