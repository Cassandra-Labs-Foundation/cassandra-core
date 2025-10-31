Generated using Claude Opus 4.1

Summary
I've thoroughly read and analyzed the Unit API documentation. Here's what I've learned:
API Overview

OpenAPI Version: 3.0.2
Unit API Version: 0.2.3
Base URL: https://api.s.unit.sh
Authentication: Bearer token (JWT format)
Total Endpoints: 116 endpoints across 33 categories

Core Entity Categories
The API is organized around these main resource types:

Applications (9 endpoints) - Customer onboarding and KYC
Customers (6 endpoints) - Individual and business customer management
Accounts (14 endpoints) - Deposit and credit account operations
Cards (10 endpoints) - Debit and credit card issuance and management
Payments (Multiple categories):

Regular payments (3 endpoints)
Received payments (4 endpoints)
Recurring payments (4 endpoints)
Check payments (7 endpoints)
Wire transfers (embedded in payment schemas)


Transactions - Transaction records and history
Authorizations (6 endpoints) - Card authorization handling
Webhooks (4 endpoints) - Event notifications
Statements (4 endpoints) - Account statements
Disputes (2 endpoints) - Transaction dispute handling

Key Features
Account Types:

Deposit Accounts
Credit Accounts
Support for DACA (Deposit Account Control Agreements)

Customer Types:

Individual Customers
Business Customers
Business Wallet Customers

Payment Methods:

ACH payments (incoming and outgoing)
Wire transfers
Book payments (internal transfers)
Check deposits and payments
Cash deposits (with barcode generation)

Card Features:

Physical and virtual cards
Individual and business cards
Debit and credit cards
Card controls (freeze/unfreeze, limits, PIN management)
Lost/stolen card reporting

Additional Services:

Stop payments (ACH and check)
Recurring payments and repayments
Rewards program
Tax forms generation
ATM and store location lookups
Sandbox environment for testing

Data Model Structure
All entities follow a consistent JSON:API structure with:

type: Entity type identifier
id: Unique identifier
attributes: Entity properties
relationships: Links to related entities

The API uses comprehensive schema definitions (503 total schemas) covering:

Create/Update/Response models for each entity
Relationship definitions
Status enumerations
Transaction types
Event types for webhooks

Security & Compliance

JWT-based authentication
Support for document verification and KYC
Beneficial owner tracking for businesses
Risk rating capabilities
Archive functionality with reason codes for compliance

This is a comprehensive banking-as-a-service API that provides full functionality for building financial products, from customer onboarding through account management, payments, and card issuance.