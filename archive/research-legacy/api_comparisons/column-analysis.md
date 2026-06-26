Generated using Claude Opus 4.1

Summary
I've thoroughly analyzed the Column API semantic map. Here's what I've learned:
API Overview

Provider: Column (Banking-as-a-Service)
Source: https://column.com/docs/api
Data Format: Semantic Map (not OpenAPI spec)
Extraction Date: September 26, 2025
Authentication: API Key
Total Endpoints: 114
Data Models: 54
Webhook Events: 68

HTTP Methods Distribution

GET: 62 endpoints (54%)
POST: 39 endpoints (34%)
PATCH: 9 endpoints (8%)
DELETE: 4 endpoints (4%)

Core Banking Infrastructure
Entity Management

Person Entities (individuals)
Business Entities (corporations)
Full CRUD operations for entity lifecycle
KYC/KYB document management

Account Services

Bank Accounts (6 endpoints)
Account Numbers management
Counterparty management (3 endpoints)
Institution information (2 endpoints)

Comprehensive Transfer Capabilities (43 total endpoints)

ACH Transfers (6 endpoints)

Standard ACH operations
ACH Positive Pay Rules (fraud prevention)
ACH returns handling


Wire Transfers (11 endpoints)

Domestic wires
Wire drawdown requests
Wire return requests


International Wires (7 endpoints)

International wire transfers
Wire tracking
Multi-currency support


Real-Time Payments (11 endpoints)

RTP network integration
Instant payment processing


Book Transfers (4 endpoints)

Internal account-to-account transfers


Check Transfers (8 endpoints)

Check issuance
Check returns
Check processing



Advanced Financial Features
Loan Management System (19 endpoints)

Loan creation and updates
Loan disbursements
Loan payments
Payment schedules
Loan statements

Foreign Exchange Capabilities

FX Quote generation
Exchange rate sheets
Multi-currency rate management
International wire FX integration

Risk Management

ACH Positive Pay Rules
Transaction fraud prevention
IBAN validation
Counterparty verification

Developer & Testing Tools
Simulation Environment (11 endpoints)

Receive ACH debit simulation
Receive wire simulation
International wire simulation
Wire drawdown request simulation
Wire return request simulation
Check deposit simulation
RTP receipt simulation

Webhook Infrastructure

68 distinct webhook events
Webhook endpoint management (6 endpoints)
Webhook delivery tracking (2 endpoints)
Event streaming and notifications

Reporting & Compliance

Transaction history tracking
Reporting endpoints (2)
Document management system
PDF preview generation
Market rates access

Data Model Architecture (54 models)
Core Models:

Entity models (Person, Business, generic Entity)
Bank Account and Account Number models
Counterparty and Financial Institution models

Transfer Models:

ACH, Wire, International Wire, Book, Check, Real-time
Admin transfers (Column-initiated)
Transfer returns and tracking

Financial Models:

Loan, Loan Payment, Loan Disbursement
Foreign Exchange Quote, Rate, Rate Sheet
Market rates and pricing

Supporting Models:

Documents and validation
Events and webhooks
Error handling structures

Key Differentiators

Comprehensive Loan Management: Full lending platform with 19 dedicated endpoints
International Capabilities: Strong international wire and FX support
ACH Positive Pay: Advanced fraud prevention for ACH transactions
Simulation Suite: 11 endpoints for testing various transaction types
Multi-Rail Payments: Support for 6 different payment rails
Real-time Payments: Full RTP network integration
Wire Drawdown: Ability to request incoming wires

Business Use Cases
This API is designed for:

Lending Platforms: Complete loan lifecycle management
International Banking: FX and international wire capabilities
Business Banking: Entity management with person/business distinction
Payment Processing: Multi-rail payment support
Treasury Management: Market rates, FX, and reporting
Testing & Development: Comprehensive simulation environment

Notable Gaps/Limitations
Based on the semantic map:

No card issuance capabilities mentioned
No explicit multi-bank support (unlike Increase)
No bookkeeping/accounting features (unlike Increase)
No physical mail/lockbox services

Column appears to be a sophisticated BaaS platform with particularly strong capabilities in lending, international payments, and multi-rail domestic transfers, making it well-suited for fintech companies building lending products or requiring international payment capabilities.