Generated using Claude Opus 4.1

Summary
I've thoroughly analyzed the Increase API documentation. Here's what I've learned:
API Overview

Platform: Increase (Modern Banking Infrastructure)
OpenAPI Version: 3.1.0
API Version: 0.0.1
Mission: "Anything that you can achieve with PDFs, presence, and persistence in a bank branch you can do with our API"
Environments:

Production: https://api.increase.com
Sandbox: https://sandbox.increase.com


Authentication: Bearer token (HTTP Bearer scheme)
Total Endpoints: 176
Total Schemas: 209
HTTP Methods: GET (100), POST (104), PATCH (9)

Core Banking Services
Accounts & Numbers (7 endpoints)

Multiple account and routing numbers per account
Support for 6 currencies (USD, EUR, GBP, CAD, CHF, JPY)
Interest-bearing accounts with account revenue rates
Partner banks: Core Bank, First Internet Bank, Grasshopper Bank

Payment Methods (Comprehensive Coverage)

ACH Transfers - Automated Clearing House transfers
Wire Transfers - Including wire drawdown requests (pull wires)
Check Transfers - Physical check mailing and deposits
Real-Time Payments (RTP) - Instant transfers on RTP network
Card Payments - Commercial credit cards with tokenization

Unique/Advanced Features
IntraFi Integration (Extended FDIC Coverage)

Account enrollment in IntraFi network
Automated fund sweeping across multiple banks
Balance management across institutions
Exclusion management for specific banks
Extends FDIC insurance beyond standard $250K limit

Double-Entry Bookkeeping System

Bookkeeping accounts (T-accounts)
Entry sets (transactionally applied entries)
Balance lookups
Compliance-ready accounting annotations
Programmatic ledger management

Physical Mail Handling

Lockboxes: Physical addresses for receiving checks
Inbound Mail Items: Tracking of physical mail
Automatic check deposit creation from lockbox mail

OAuth Platform Capabilities

Build third-party applications
OAuth applications, connections, and tokens
Multi-organization support
Platform-as-a-service capabilities

Real-Time Decision Engine

Real-time authorization decisions
Card authorization handling
Programmatic approval/decline logic
Webhook-based decision flows

Card Services
Card Types

Commercial credit cards
Physical and digital cards
Custom card artwork and profiles
Digital wallet integration (Apple Pay, Google Pay)

Card Features

Card tokenization for secure storage
Card push transfers (send funds to cards)
Card validation services
Purchase supplements (settlement/refund data)

Entity Management
Entity Types Supported:

Natural Person (individuals)
Corporation
Partnership
Government Authority
Trust
Joint entities

Compliance & Documentation

Supplemental documents upload
KYC/KYB support
Program-based compliance terms
Entity confirmation workflows

Transaction & Reporting
Transaction Types:

Standard transactions (immutable ledger)
Pending transactions (potential future)
Declined transactions (refused)

Reporting Features:

Account statements (monthly generation)
PDF generation and file management
Export capabilities (batch summaries)
Transaction search by various criteria

Developer Experience
Testing & Development:

Comprehensive sandbox environment
Idempotency key support for request safety
Event subscriptions and webhooks
Real-time event streaming

API Patterns:

Consistent RESTful design
Full CRUD operations for most resources
Action endpoints (approve, cancel, confirm, etc.)
Filtering and pagination support

Key Differentiators

IntraFi Integration: Unique extended FDIC insurance capability
Bookkeeping API: Built-in double-entry accounting system
Physical Mail: Lockbox and mail handling capabilities
Wire Drawdowns: Ability to request incoming wires
OAuth Platform: Build banking apps for other organizations
Real-Time Decisions: Programmatic authorization control
Multi-Bank Support: Choice of underlying partner banks
Comprehensive Payment Rails: All major payment types in one API

Operational Features
Approval Workflows:

Two-step approval for transfers (create → approve)
Cancel capabilities for pending operations
Stop payment functionality

Groups & Organizations:

Multi-organization support
Group-level management
OAuth-based multi-tenancy

This is an extremely comprehensive banking API that goes beyond typical BaaS offerings with unique features like IntraFi integration, built-in bookkeeping, physical mail handling, and OAuth platform capabilities. It's designed for both direct banking operations and building banking platforms for others.