# Prompt for LLM Analysis of Oracle General Ledger Documentation

Analyze the attached Oracle General Ledger User's Guide (Release 12.2) and extract comprehensive technical requirements for designing a reliable, enterprise-grade accounting ledger system. Focus on the following dimensions:

## 1. Core Ledger Architecture
- Identify the fundamental data structures (chart of accounts, calendar, currency, accounting entities)
- Map the relationships between ledgers, ledger sets, and reporting hierarchies
- Document the multi-ledger architecture patterns (primary, secondary, reporting ledgers)
- Extract the accounting flexfield structure and segment configurations
- Define journal entry lifecycle (creation, approval, posting, reversal)

## 2. Chart of Accounts Requirements
For the accounting flexfield structure, document:
- **Segment Types**: Balancing, natural account, cost center, intercompany, management
- **Validation Rules**: Cross-validation rules, security rules, value set definitions
- **Hierarchies**: Rollup groups, parent-child relationships, summary accounts
- **Dynamic Insertion**: Rules for creating new combinations
- **Account Types**: Assets, liabilities, equity, revenue, expense, statistical

## 3. Journal Processing Framework
Extract requirements for:
- **Journal Sources**: Manual, subledger, automated, recurring, allocation
- **Journal Categories**: Standard categories and their purposes
- **Batch Processing**: Journal batch controls and validation
- **Approval Workflows**: Authorization limits, approval hierarchies
- **Posting Process**: Validation rules, period controls, error handling
- **Reversal Methods**: Switch sign, change period, matching rules

## 4. Period Management & Calendar
Document:
- **Calendar Types**: Accounting, transaction, adjustment periods
- **Period Statuses**: Never opened, future entry, open, closed, permanently closed
- **Year-End Processing**: Closing procedures, retained earnings, opening balances
- **Concurrent Programs**: Period-end processes, reconciliation reports
- **Multi-period Accounting**: Encumbrances, commitments, budgetary control

## 5. Multi-Currency Architecture
Identify requirements for:
- **Currency Types**: Functional, foreign, reporting, statistical
- **Conversion Types**: Spot, period average, historical, user-defined
- **Revaluation**: Unrealized gains/losses, realized gains/losses
- **Translation**: Balance sheet vs. income statement methods
- **Triangulation**: Cross-rate calculations, Euro considerations
- **Rate Management**: Daily rates, period rates, historical rates

## 6. Consolidation Framework
Extract:
- **Consolidation Methods**: Balance transfer, journal transfer
- **Elimination Entries**: Intercompany, investment, minority interest
- **Mapping Rules**: Subsidiary to parent account mappings
- **Translation Adjustments**: CTA calculations, equity pickups
- **Consolidation Sets**: Multi-level consolidations, partial ownership

## 7. Security & Data Access Model
Document:
- **Data Access Sets**: Ledger access, segment value security
- **Responsibility Model**: Function security, menu exclusions
- **Definition Access Sets**: Who can modify setup data
- **Journal Authorization**: Approval limits by amount/account
- **Cross-Validation Rules**: Preventing invalid combinations
- **Audit Trail**: Change tracking, journal history

## 8. Reporting & Analytics Requirements
For reporting capabilities, extract:
- **Financial Statement Generator (FSG)**: Row sets, column sets, content sets
- **Account Analysis**: Drilldown capabilities, T-accounts, account inquiry
- **Trial Balance**: Summary vs. detail, YTD vs. PTD
- **Management Reporting**: Responsibility reporting, variance analysis
- **Legal Reporting**: Statutory requirements, GAAP/IFRS compliance
- **Real-Time Balances**: Online inquiry, balance monitoring

## 9. Integration Architecture
Document integration requirements:
- **Subledger Accounting (SLA)**: Event model, accounting methods
- **Subledger Integration**: AP, AR, FA, Projects, Inventory
- **Journal Import**: Interface tables, validation rules, error correction
- **Web Services**: REST APIs, SOAP services, integration patterns
- **Data Exchange**: GL interface, open interfaces, APIs
- **External Systems**: Bank reconciliation, tax systems, reporting tools

## 10. Advanced Features
Identify sophisticated capabilities:
- **Allocations**: Fixed, variable, looping, step-down allocations
- **Recurring Journals**: Formula-based, skeleton, standard
- **Mass Allocations**: Cost allocations, overhead distributions
- **Budget Control**: Encumbrance accounting, funds checking
- **Statistical Accounts**: Quantities, headcount, metrics
- **Average Daily Balances**: Interest calculations, cash management
- **Suspense Posting**: Automatic offsetting, clearing accounts

## 11. Performance & Scalability
Extract requirements for:
- **Concurrent Processing**: Parallel posting, multi-threading
- **Summary Accounts**: Balance aggregation, performance optimization
- **Archiving**: Historical data management, purge programs
- **Indexing Strategies**: Key performance indexes
- **Partitioning**: Table partitioning strategies
- **Caching**: Balance caching, frequently accessed data

## 12. Audit & Compliance
Document:
- **Audit Trail Requirements**: Journal entry history, modification tracking
- **Segregation of Duties**: Incompatible functions, role separation
- **Compliance Features**: SOX, regulatory reporting
- **Account Reconciliation**: Manual vs. automated reconciliation
- **Exception Reporting**: Unusual transactions, variance thresholds
- **Documentation**: Supporting documents, attachments, references

## Output Format

Provide a structured technical specification with:

### 1. Entity Relationship Diagram (Mermaid syntax)
Show core entities: Ledger, Period, Journal, Account, Currency, etc.

### 2. Data Model Specification
```yaml
entities:
  ledger:
    attributes:
      - ledger_id (PK)
      - name
      - short_name
      - currency_code
      - calendar_name
      - chart_of_accounts_id
    relationships:
      - has_many: journals
      - belongs_to: ledger_set
```

### 3. State Machines
Define state transitions for:
- Journal lifecycle (draft → approved → posted → reversed)
- Period lifecycle (never opened → open → closed → permanently closed)
- Batch processing (pending → processing → completed → error)

### 4. API Specifications
```yaml
/api/v1/ledger:
  /journals:
    POST: Create journal entry
    GET: Retrieve journals
    PUT: Update journal
    DELETE: Reverse journal
  /accounts:
    GET: Account balances
  /periods:
    POST: Open/close period
```

### 5. Business Rules Engine
Document validation rules, calculations, and automated processes

### 6. Integration Patterns
Message formats, event schemas, webhook specifications

### 7. Performance Benchmarks
Expected transaction volumes, response times, batch processing windows

## Special Considerations for Modern Architecture

### Cloud-Native Design
- Microservices decomposition
- Event-driven architecture
- CQRS patterns for read/write separation
- Distributed transaction handling

### Real-Time Processing
- Streaming balance updates
- Event sourcing for audit trail
- Materialized views for reporting
- Cache strategies for hot data

### Multi-Entity Support
- Tenant isolation strategies
- Shared service models
- Cross-entity consolidation
- Transfer pricing

### Regulatory Adaptability
- Configurable compliance rules
- Multi-GAAP support
- Real-time regulatory reporting
- Automated compliance monitoring

## Key Areas to Focus On

1. **Double-Entry Integrity**: How Oracle ensures balanced journal entries
2. **Period Locking**: Mechanisms preventing post-period adjustments
3. **Currency Precision**: Handling of decimal places and rounding
4. **Intercompany Processing**: Automated balancing and settlements
5. **Tax Integration**: Sales tax, VAT, withholding tax handling
6. **Workflow Engine**: Approval routing and delegation rules
7. **Error Recovery**: Exception handling and correction procedures
8. **Reversibility**: Full audit trail and transaction reversal capabilities

## Expected Deliverables

1. **Core Ledger Design Document**: 
   - Complete data model with all entities and relationships
   - Detailed attribute specifications with data types and constraints

2. **Processing Flow Diagrams**:
   - Journal entry lifecycle from creation to posting
   - Period-end close procedures
   - Consolidation workflow

3. **API Specification**:
   - RESTful endpoints for all ledger operations
   - Event schemas for real-time notifications
   - Batch processing interfaces

4. **Validation Rule Catalog**:
   - All business rules extracted from Oracle GL
   - Cross-validation matrices
   - Authorization frameworks

5. **Integration Architecture**:
   - Subledger integration patterns
   - External system interfaces
   - Data synchronization strategies

6. **Implementation Roadmap**:
   - Prioritized feature list (MVP to advanced)
   - Technical dependencies
   - Risk mitigation strategies

Focus on extracting the essential capabilities that make Oracle GL a reliable, auditable, and scalable ledger system that can handle complex multi-national, multi-currency, multi-entity accounting requirements while maintaining data integrity and regulatory compliance.