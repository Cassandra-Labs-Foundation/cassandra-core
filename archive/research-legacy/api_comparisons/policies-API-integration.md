# Pynthia Federal Credit Union API Specification

**Version:** 1.0.0  
**Date:** 2025-01-14  
**Purpose:** Canonical API specification integrating BaaS provider patterns (Unit, Q2 Helix, Increase, Column) with Pynthia FCU policy & procedure requirements

---

## Table of Contents

1. [Architecture Overview](#architecture-overview)
2. [Authentication & Authorization](#authentication--authorization)
3. [Core Domain Objects](#core-domain-objects)
4. [Member & Entity Management](#member--entity-management)
5. [Account Management](#account-management)
6. [Payments & Transfers](#payments--transfers)
7. [Cards](#cards)
8. [Compliance & Risk](#compliance--risk)
9. [Events & Webhooks](#events--webhooks)
10. [Policy Integration Matrix](#policy-integration-matrix)

---

## Architecture Overview

### Design Principles

1. **Policy-First**: Every endpoint maps to specific policy controls (e.g., `CD-04`, `FL-05`, `BA-03`)
2. **Event-Driven**: All state changes emit events that policies reference (e.g., `application.created`, `decision.recorded`)
3. **Audit-Native**: Every mutation produces immutable audit logs per policy requirements
4. **BaaS-Inspired**: Adopts best patterns from Unit, Q2 Helix, Increase, and Column while maintaining credit union specificity
5. **Credit Union Extensions**: Adds membership, share accounts, dividends, and governance features missing from commercial BaaS

### Base URL

```
Production: https://api.pynthia.coop/v1
Sandbox: https://sandbox-api.pynthia.coop/v1
```

### Request/Response Format

- **Content-Type**: `application/json`
- **Charset**: `UTF-8`
- **Date Format**: ISO 8601 (`YYYY-MM-DDTHH:MM:SSZ`)
- **Currency**: USD (amounts in cents unless specified)
- **Idempotency**: All mutations support `Idempotency-Key` header (24hr window)

---

## Authentication & Authorization

### Pattern: OAuth 2.0 + API Keys (inspired by Increase)

**Rationale from BaaS Analysis:**
- **Increase** offers the most sophisticated auth with full OAuth platform capabilities
- **Unit** uses JWT tokens which we'll adopt for internal services
- **Q2 Helix** HTTP Basic Auth is too weak
- **Column** simple API keys work for low-risk integrations

### Endpoints

#### `POST /oauth/token`
Create OAuth access token (for partner integrations)

**Policy Integration:** `VM-05` (vendor contracts require OAuth where feasible)

**Request:**
```json
{
  "grant_type": "client_credentials",
  "client_id": "string",
  "client_secret": "string",
  "scope": "members:read accounts:read transactions:write"
}
```

**Response:**
```json
{
  "access_token": "eyJ...",
  "token_type": "Bearer",
  "expires_in": 3600,
  "scope": "members:read accounts:read transactions:write"
}
```

**Events:** `oauth.token.created`

#### `GET /oauth/applications`
List OAuth applications (for audit/governance)

**Policy Integration:** `VM-02` (vendor inventory), `IS-06` (access control)

---

## Core Domain Objects

### Member vs Customer vs Entity

**Credit Union Distinction:**
- **Member**: Natural person with membership share and voting rights (credit union specific)
- **Customer**: Used only for non-member accounts (e.g., non-qualified accounts)
- **Entity**: Legal entities (businesses, trusts, government) that can be members or customers

**BaaS Mapping:**
- Unit: "Customer" → we use "Member/Entity"
- Q2 Helix: "Customer" → "Member/Entity"
- Increase: "Entity" (includes natural persons) → we separate "Member" from "Entity"
- Column: Person/Business separation → we adopt this but add membership layer

### Object: Member

```json
{
  "id": "mbr_01h2x...",
  "type": "member",
  "membership": {
    "number": "123456",
    "join_date": "2024-01-15T10:00:00Z",
    "share_balance_cents": 500,
    "eligibility_basis": "community_charter",
    "voting_status": "active"
  },
  "person": {
    "first_name": "Jane",
    "last_name": "Doe",
    "date_of_birth": "1985-03-20",
    "ssn_last_4": "1234",
    "email": "jane@example.com",
    "phone": "+15555551234",
    "address": {
      "line1": "123 Main St",
      "line2": "Apt 4B",
      "city": "San Jose",
      "state": "CA",
      "postal_code": "95110",
      "country": "US"
    }
  },
  "kyc_status": "verified",
  "risk_rating": "low",
  "status": "active",
  "created_at": "2024-01-15T10:00:00Z",
  "updated_at": "2024-06-10T14:30:00Z"
}
```

**Policy Fields:**
- `kyc_status`: Maps to `CD-04` (CIP)
- `risk_rating`: Maps to `CD-03` (Member Risk Profiling)
- `membership.voting_status`: Credit union specific (not in BaaS)

### Object: Entity (Business/Trust/Government)

```json
{
  "id": "ent_01h2x...",
  "type": "entity",
  "entity_type": "corporation",
  "membership": {
    "is_member": true,
    "number": "987654",
    "join_date": "2023-05-10T00:00:00Z",
    "share_balance_cents": 2500,
    "eligibility_basis": "community_charter"
  },
  "business_details": {
    "legal_name": "Acme Corp",
    "dba": "Acme",
    "ein": "12-3456789",
    "formation_state": "CA",
    "formation_date": "2020-01-01",
    "industry_code": "5411",
    "website": "https://acme.example"
  },
  "beneficial_owners": [
    {
      "person_id": "mbr_01h2y...",
      "ownership_percentage": 35,
      "control_person": true
    }
  ],
  "kyc_status": "verified",
  "risk_rating": "medium",
  "status": "active",
  "created_at": "2023-05-10T08:00:00Z",
  "updated_at": "2024-11-01T12:00:00Z"
}
```

**Policy Fields:**
- `beneficial_owners`: Maps to `CD-05` (Beneficial Ownership)
- `industry_code`: Maps to `CD-07` (ECDD triggers for high-risk industries)

---

## Member & Entity Management

### Pattern: Hybrid Unit + Increase Approach

**From BaaS Analysis:**
- **Unit**: Combines individual/business in one endpoint (we'll separate)
- **Q2 Helix**: Most customer-centric features (tokens, dormancy) — we adopt tokens
- **Increase**: "Entities" with broad type support — we adopt type flexibility
- **Column**: Separates person/business endpoints — we adopt separation + add membership

### `POST /members`
Create individual member

**Policy Integration:** 
- `CD-04` CIP verification required before activation
- `CD-03` Initial risk profiling
- `BA-03` BSA/AML CIP program

**Request:**
```json
{
  "person": {
    "first_name": "Jane",
    "last_name": "Doe",
    "date_of_birth": "1985-03-20",
    "ssn": "123-45-6789",
    "email": "jane@example.com",
    "phone": "+15555551234",
    "address": { ... }
  },
  "membership": {
    "eligibility_basis": "community_charter",
    "initial_share_deposit_cents": 500
  },
  "expected_activity": {
    "monthly_deposit_cents": 500000,
    "monthly_withdrawal_cents": 300000,
    "primary_use": "personal_banking"
  },
  "idempotency_key": "unique-key-123"
}
```

**Response:**
```json
{
  "member": { ... },
  "kyc_result": {
    "status": "verified",
    "provider": "alloy",
    "session_id": "alloy_01h...",
    "verification_timestamp": "2024-01-15T10:00:05Z"
  }
}
```

**Events Emitted:**
- `application.created` (FL-05)
- `kyc.started` (CD-04)
- `kyc.passed` (CD-04)
- `member.onboarded` (CD-01)
- `cip.verified` (BA-03)

**Audit Logs:**
- `member.created`
- `kyc.verification.completed`
- `membership.share.funded`

### `POST /entities`
Create business/trust/government entity

**Policy Integration:**
- `CD-05` Beneficial ownership collection
- `CD-07` Enhanced due diligence triggers
- `BA-04` CDD/EDD for legal entities

**Request:**
```json
{
  "entity_type": "corporation",
  "business_details": {
    "legal_name": "Acme Corp",
    "ein": "12-3456789",
    "formation_state": "CA",
    "industry_code": "5411"
  },
  "beneficial_owners": [
    {
      "first_name": "John",
      "last_name": "Smith",
      "date_of_birth": "1975-06-15",
      "ssn": "987-65-4321",
      "ownership_percentage": 35,
      "control_person": true,
      "address": { ... }
    }
  ],
  "membership": {
    "requested": true,
    "eligibility_basis": "community_charter",
    "initial_share_deposit_cents": 2500
  },
  "expected_activity": {
    "monthly_transaction_volume_cents": 5000000,
    "primary_use": "operating_account",
    "international_activity": false
  }
}
```

**Events Emitted:**
- `business.application.submitted` (CD-05)
- `bo.form_submitted` (CD-05)
- `kyb.started` (CD-04)
- `entity.onboarded`
- `risk.trigger.ecdd` (if high-risk industry, CD-07)

### `GET /members/:id`
Retrieve member details

**Policy Integration:**
- `IS-06` Access control enforcement
- `CD-12` Recordkeeping

**Response:** (see Member object above)

### `PATCH /members/:id`
Update member information

**Policy Integration:**
- `CD-09` Ongoing monitoring triggers
- `BA-04` Event-driven profile updates

**Request:**
```json
{
  "person": {
    "email": "newemail@example.com",
    "phone": "+15555559999",
    "address": { ... }
  }
}
```

**Events Emitted:**
- `member.profile.updated`
- `profile.refresh_due` (if material change triggers CD-09 review)

### `POST /members/:id/tokens`
Generate secure token for member operations (inspired by Q2 Helix)

**Policy Integration:**
- `IS-06` Authentication controls
- `CD-04` Identity verification before token issuance

**Request:**
```json
{
  "purpose": "password_reset",
  "expires_in_seconds": 900,
  "scope": "password:reset"
}
```

**Response:**
```json
{
  "token": "tok_01h...",
  "expires_at": "2024-01-15T10:15:00Z"
}
```

---

## Account Management

### Pattern: Increase + Q2 Helix Hybrid

**From BaaS Analysis:**
- **Q2 Helix**: Best entitlements system for multi-user access — we adopt
- **Increase**: Multiple account numbers per account + IntraFi FDIC extension — we adopt
- **Unit**: DACA support for lending — we adopt for loan accounts
- **Column**: Simplest model — too simple for credit union needs

### Account Types (Credit Union Specific)

```typescript
enum AccountType {
  // Share Accounts (Credit Union Specific)
  SHARE_REGULAR = "share_regular",           // Primary savings
  SHARE_DRAFT = "share_draft",               // Checking equivalent
  SHARE_CERTIFICATE = "share_certificate",    // Term deposit (CD)
  SHARE_SPECIAL = "share_special",           // Special purpose savings
  
  // Loan Accounts
  LOAN_AUTO = "loan_auto",
  LOAN_PERSONAL = "loan_personal",
  LOAN_MORTGAGE = "loan_mortgage",
  LOAN_CREDIT_CARD = "loan_credit_card",
  LOAN_LINE_OF_CREDIT = "loan_line_of_credit",
  
  // Special Accounts
  IRA_TRADITIONAL = "ira_traditional",
  IRA_ROTH = "ira_roth",
  CHARITABLE_DONATION = "charitable_donation",  // Per CDA policy
  BUSINESS_CHECKING = "business_checking",
  BUSINESS_SAVINGS = "business_savings"
}
```

### Object: Account

```json
{
  "id": "acct_01h2x...",
  "account_number": "1234567890",
  "routing_numbers": [
    {
      "routing_number": "321081669",
      "type": "ach",
      "status": "active"
    }
  ],
  "type": "share_draft",
  "member_id": "mbr_01h2x...",
  "entity_id": null,
  "name": "Primary Checking",
  "status": "active",
  "balance_cents": 125043,
  "available_balance_cents": 125043,
  "currency": "USD",
  "interest_rate": 0.0075,
  "dividend_rate": 0.0075,
  "opened_date": "2024-01-15",
  "closed_date": null,
  "product_id": "prod_share_draft_basic",
  "entitlements": [
    {
      "user_id": "mbr_01h2x...",
      "permissions": ["view", "transfer", "bill_pay"],
      "limits": {
        "daily_transfer_cents": 100000,
        "daily_bill_pay_cents": 50000
      }
    }
  ],
  "intrafi_enrolled": false,
  "daca_status": null,
  "created_at": "2024-01-15T10:00:00Z",
  "updated_at": "2024-12-15T08:30:00Z"
}
```

**Policy Fields:**
- `dividend_rate` vs `interest_rate`: Credit unions pay dividends, not interest (key distinction)
- `entitlements`: Q2 Helix-inspired multi-user access (maps to IS-06)
- `intrafi_enrolled`: Increase IntraFi FDIC extension (maps to LP-06 concentration limits)
- `daca_status`: Unit DACA support (maps to lending policies)

### `POST /accounts`
Open new account

**Policy Integration:**
- `CD-04` Member must have verified KYC status
- `LP-06` Funding concentration limits
- `CA-06` Reconciliation to GL

**Request:**
```json
{
  "member_id": "mbr_01h2x...",
  "type": "share_draft",
  "name": "Primary Checking",
  "product_id": "prod_share_draft_basic",
  "initial_deposit": {
    "amount_cents": 10000,
    "source_account_id": "acct_existing...",
    "source_type": "internal_transfer"
  },
  "entitlements": [
    {
      "user_id": "mbr_01h2x...",
      "permissions": ["view", "transfer", "bill_pay"]
    }
  ]
}
```

**Events Emitted:**
- `account.created`
- `account.funded`
- `gl.posting.created` (CA-06)

### `POST /accounts/:id/freeze`
Freeze account (Unit + Q2 Helix pattern)

**Policy Integration:**
- `RZ-03` Targeted account freeze
- `BA-05` OFAC hold procedures
- `IS-09` Incident response

**Request:**
```json
{
  "reason_code": "ofac_hit",
  "reason_description": "Potential OFAC match requires review",
  "allow_inbound_credits": false,
  "initiated_by": "compliance_officer",
  "case_id": "case_01h..."
}
```

**Events Emitted:**
- `account.frozen`
- `cust.freeze.requested` (RZ-03)
- `ofac.hit.reviewed` (BA-05)

### `POST /accounts/:id/entitlements`
Add authorized user (Q2 Helix pattern)

**Policy Integration:**
- `IS-06` Access control
- `CD-09` Ongoing monitoring (ownership change)

**Request:**
```json
{
  "user_id": "mbr_01h2y...",
  "permissions": ["view", "transfer"],
  "limits": {
    "daily_transfer_cents": 50000
  },
  "relationship": "joint_owner"
}
```

**Events Emitted:**
- `account.entitlement.added`
- `bo.change_detected` (if ownership structure changes for CD-09)

### `POST /account-numbers`
Create additional routing/account number set (Increase pattern)

**Policy Integration:**
- `IS-04` Change management
- `CA-06` Reconciliation complexity

**Request:**
```json
{
  "account_id": "acct_01h2x...",
  "purpose": "ach_segregated",
  "routing_number_type": "ach"
}
```

**Response:**
```json
{
  "account_number": "9876543210",
  "routing_number": "321081669",
  "type": "ach",
  "status": "active",
  "created_at": "2024-06-15T10:00:00Z"
}
```

---

## Payments & Transfers

### Pattern: Comprehensive approach from all providers

**From BaaS Analysis:**
- **Column**: Best ACH Positive Pay + check image uploads — we adopt
- **Increase**: Most comprehensive ACH with prenotifications + approval workflows — we adopt
- **Column**: Domestic/international wire separation + tracking — we adopt
- **Increase**: Wire drawdown capability — we adopt
- **Only Increase & Column**: RTP support — we adopt RTP

### Object: Transfer

```json
{
  "id": "xfer_01h2x...",
  "type": "ach_credit",
  "status": "pending",
  "amount_cents": 50000,
  "currency": "USD",
  "from_account": {
    "account_id": "acct_01h2x...",
    "routing_number": "321081669",
    "account_number": "1234567890"
  },
  "to_account": {
    "account_id": null,
    "routing_number": "021000021",
    "account_number": "9876543210",
    "account_holder_name": "External Party"
  },
  "description": "Rent payment",
  "created_at": "2024-01-15T10:00:00Z",
  "effective_date": "2024-01-16",
  "approval_status": "approved",
  "approved_by": "user_01h...",
  "approved_at": "2024-01-15T10:05:00Z"
}
```

### `POST /transfers/ach`
Create ACH transfer

**Policy Integration:**
- `BA-06` Transaction monitoring
- `BA-10` Travel rule (if applicable)
- `LP-03` Maturity mismatch/funding
- `FL-03` Evaluation & pricing rules

**Request:**
```json
{
  "type": "ach_credit",
  "from_account_id": "acct_01h2x...",
  "to_account": {
    "routing_number": "021000021",
    "account_number": "9876543210",
    "account_holder_name": "External Party",
    "account_type": "checking"
  },
  "amount_cents": 50000,
  "description": "Rent payment",
  "effective_date": "2024-01-16",
  "sec_code": "WEB",
  "require_approval": true
}
```

**Events Emitted:**
- `ach.transfer.created`
- `tms.alert.created` (if triggers monitoring rule, BA-06)
- `payment.pre.screen` (OFAC, BA-05)

### `POST /ach-prenotifications`
Send ACH prenotification (Increase pattern)

**Policy Integration:**
- `BA-06` Verify account validity before large transfers
- Risk management best practice

**Request:**
```json
{
  "to_account": {
    "routing_number": "021000021",
    "account_number": "9876543210",
    "account_holder_name": "External Party"
  }
}
```

**Response:**
```json
{
  "id": "prenote_01h...",
  "status": "sent",
  "expected_confirmation_date": "2024-01-17"
}
```

### `POST /transfers/wire`
Create domestic wire (Column pattern with approval)

**Policy Integration:**
- `BA-10` Travel rule (wires ≥ $3,000)
- `FL-03` Pricing evaluation
- `LP-03` Liquidity impact

**Request:**
```json
{
  "from_account_id": "acct_01h2x...",
  "to_beneficiary": {
    "name": "Acme Corp",
    "account_number": "9876543210",
    "routing_number": "021000021",
    "address": {
      "line1": "456 Oak Ave",
      "city": "New York",
      "state": "NY",
      "postal_code": "10001"
    }
  },
  "amount_cents": 10000000,
  "purpose": "Invoice 12345 payment",
  "require_approval": true,
  "approval_method": "dual_control"
}
```

**Events Emitted:**
- `wire.created`
- `wire.release.requested`
- `wire.validation.passed` (travel rule, BA-10)
- `payment.pre.screen` (OFAC, BA-05)

### `POST /transfers/international-wire`
Create international wire (Column pattern)

**Policy Integration:**
- `BA-10` Travel rule
- `CD-07` Enhanced CDD for international activity
- Foreign exchange if needed

**Request:**
```json
{
  "from_account_id": "acct_01h2x...",
  "to_beneficiary": {
    "name": "Global Ltd",
    "iban": "GB82WEST12345698765432",
    "bic_swift": "ABCDGB2LXXX",
    "address": {
      "line1": "10 Downing Street",
      "city": "London",
      "postal_code": "SW1A 2AA",
      "country": "GB"
    }
  },
  "amount": {
    "cents": 5000000,
    "currency": "USD"
  },
  "purpose": "International supplier payment",
  "purpose_code": "SUPP",
  "require_approval": true
}
```

**Events Emitted:**
- `wire.international.created`
- `risk.trigger.geo` (international triggers ECDD review, CD-07)
- `payment.pre.screen`

### `POST /transfers/realtime`
Create Real-Time Payment (Increase + Column)

**Policy Integration:**
- `BA-06` Real-time monitoring
- `BA-05` OFAC screening
- `LP-03` Liquidity (instant settlement)

**Request:**
```json
{
  "from_account_id": "acct_01h2x...",
  "to_account": {
    "routing_number": "021000021",
    "account_number": "9876543210",
    "account_holder_name": "Jane Smith"
  },
  "amount_cents": 25000,
  "description": "Payment for services"
}
```

**Events Emitted:**
- `rtp.transfer.created`
- `payment.pre.screen`
- `settlement.immediate`

### `GET /ach-positive-pay-rules`
List ACH Positive Pay rules (Column pattern)

**Policy Integration:**
- `BA-06` Fraud prevention
- `IS-10` Red flags program

**Response:**
```json
{
  "rules": [
    {
      "id": "rule_01h...",
      "account_id": "acct_01h2x...",
      "rule_type": "whitelist",
      "allowed_originators": [
        {
          "company_id": "1234567890",
          "company_name": "Payroll Co"
        }
      ],
      "action": "allow",
      "created_at": "2024-01-10T00:00:00Z"
    }
  ]
}
```

### `POST /check-deposits`
Mobile/remote check deposit (Increase + Column patterns)

**Policy Integration:**
- `IS-10` Red flags (check fraud)
- `BA-06` Transaction monitoring
- `CA-06` Reconciliation

**Request:**
```json
{
  "account_id": "acct_01h2x...",
  "amount_cents": 150000,
  "images": {
    "front": "base64_encoded_image...",
    "back": "base64_encoded_image..."
  },
  "check_number": "1234",
  "depositor_endorsement": true
}
```

**Events Emitted:**
- `check.deposit.created`
- `check.deposit.review` (if triggers hold, IS-10)
- `redflag.hit` (if fraud indicators, IS-10)

---

## Cards

### Pattern: Q2 Helix comprehensive card features

**From BaaS Analysis:**
- **Q2 Helix**: Best testing with mock endpoints + wallet provisioning — we adopt
- **Increase**: Separate physical/digital + push transfers — we adopt
- **Unit**: PIN management — we adopt
- **Column**: No card capabilities — we need full card suite

### Object: Card

```json
{
  "id": "card_01h2x...",
  "type": "debit_physical",
  "account_id": "acct_01h2x...",
  "cardholder": {
    "member_id": "mbr_01h2x...",
    "name_on_card": "JANE DOE"
  },
  "last_four": "4321",
  "expiration_month": 12,
  "expiration_year": 2027,
  "status": "active",
  "limits": {
    "daily_purchase_cents": 500000,
    "daily_atm_withdrawal_cents": 100000,
    "single_transaction_cents": 500000
  },
  "created_at": "2024-01-15T10:00:00Z",
  "activated_at": "2024-01-20T14:30:00Z",
  "fraud_monitoring": {
    "enabled": true,
    "provider": "enfact"
  }
}
```

### `POST /cards`
Issue new card

**Policy Integration:**
- `IS-10` Red flags / identity verification
- `CD-04` KYC verification required
- `FL-03` Pricing evaluation

**Request:**
```json
{
  "account_id": "acct_01h2x...",
  "cardholder_member_id": "mbr_01h2x...",
  "type": "debit_physical",
  "shipping_address": {
    "line1": "123 Main St",
    "city": "San Jose",
    "state": "CA",
    "postal_code": "95110"
  },
  "limits": {
    "daily_purchase_cents": 500000,
    "daily_atm_withdrawal_cents": 100000
  }
}
```

**Events Emitted:**
- `card.created`
- `card.shipped`
- `kyc.verification.required` (if address differs from profile, IS-10)

### `POST /cards/:id/digital-wallet-tokens`
Provision card to Apple/Google Pay (Q2 Helix + Increase)

**Policy Integration:**
- `IS-06` Authentication required
- `IS-10` Fraud monitoring

**Request:**
```json
{
  "wallet_type": "apple_pay",
  "device_id": "device_abc123",
  "provisioning_data": "encrypted_token_data..."
}
```

**Events Emitted:**
- `card.wallet.provisioned`
- `card.digital_token.created`

### `PATCH /cards/:id/limits`
Update card limits (Unit pattern)

**Policy Integration:**
- `IS-06` Access control (member or admin only)
- `RZ-02` Safe mode can override

**Request:**
```json
{
  "limits": {
    "daily_purchase_cents": 300000,
    "daily_atm_withdrawal_cents": 50000
  }
}
```

**Events Emitted:**
- `card.limits.updated`

### `POST /cards/:id/freeze`
Temporarily freeze card

**Policy Integration:**
- `IS-10` Member-initiated fraud prevention
- `RZ-03` Admin-initiated freeze

**Request:**
```json
{
  "reason": "lost_card",
  "initiated_by": "member"
}
```

**Events Emitted:**
- `card.frozen`

---

## Compliance & Risk

### Pattern: Policy-Driven Endpoints

These endpoints directly implement policy control requirements.

### `POST /compliance/cip-verification`
Perform CIP verification (CD-04, BA-03)

**Policy Integration:**
- `CD-04` CIP & Identity Verification
- `BA-03` BSA/AML CIP program

**Request:**
```json
{
  "member_id": "mbr_01h2x...",
  "verification_method": "document",
  "documents": [
    {
      "type": "drivers_license",
      "issuing_state": "CA",
      "document_number": "D1234567",
      "expiration_date": "2028-03-20",
      "image_front": "base64_image...",
      "image_back": "base64_image..."
    }
  ]
}
```

**Response:**
```json
{
  "verification_id": "cip_01h...",
  "status": "verified",
  "provider": "alloy",
  "timestamp": "2024-01-15T10:00:05Z",
  "match_score": 98,
  "risk_signals": []
}
```

**Events Emitted:**
- `kyc.started`
- `kyc.passed`
- `cip.verified`

### `POST /compliance/ofac-screening`
Screen against OFAC sanctions (BA-05)

**Policy Integration:**
- `BA-05` OFAC Screening & Holds

**Request:**
```json
{
  "subject_type": "member",
  "subject_id": "mbr_01h2x...",
  "screening_context": "onboarding",
  "names": ["Jane Doe", "Jane M Doe"],
  "date_of_birth": "1985-03-20",
  "country": "US"
}
```

**Response:**
```json
{
  "screening_id": "ofac_01h...",
  "status": "clear",
  "matches": [],
  "screened_at": "2024-01-15T10:00:00Z",
  "provider": "dow_jones",
  "retention_required_until": "2035-01-15"
}
```

**Events Emitted:**
- `ofac.screen.at.onboard`
- `ofac.hit.reviewed` (if match)
- `ofac.blocked` (if confirmed match)

### `POST /compliance/sanctions-screening`
Comprehensive sanctions + adverse media (BA-05, CD-06)

**Policy Integration:**
- `BA-05` OFAC
- `CD-06` Sanctions & Adverse Media Screening

**Request:**
```json
{
  "subject_id": "mbr_01h2x...",
  "screening_types": ["sanctions", "pep", "adverse_media"],
  "continuous_monitoring": true
}
```

**Response:**
```json
{
  "screening_id": "screen_01h...",
  "results": {
    "sanctions": "clear",
    "pep": "hit",
    "adverse_media": "clear"
  },
  "pep_details": {
    "is_pep": true,
    "pep_type": "domestic_pep",
    "position": "State Legislator",
    "jurisdiction": "California",
    "status": "current"
  },
  "continuous_monitoring_enabled": true
}
```

**Events Emitted:**
- `screen.new_subject`
- `pep.hit.created` (if PEP, BA-20)
- `risk.trigger.pep` (triggers ECDD, CD-07)

### `POST /compliance/risk-assessment`
Member risk profiling (CD-03, RA-04)

**Policy Integration:**
- `CD-03` Member Risk Profiling
- `RA-04` Risk Assessment & Register

**Request:**
```json
{
  "subject_id": "mbr_01h2x...",
  "assessment_type": "initial",
  "factors": {
    "occupation": "software_engineer",
    "industry_code": "5112",
    "expected_monthly_volume_cents": 500000,
    "international_activity": false,
    "high_risk_jurisdiction": false,
    "cash_intensive": false,
    "pep": false
  }
}
```

**Response:**
```json
{
  "risk_profile_id": "mrp_01h...",
  "inherent_risk": "low",
  "residual_risk": "low",
  "risk_score": 15,
  "factors_applied": [
    {
      "factor": "occupation",
      "weight": 5,
      "rationale": "Standard W2 employment"
    }
  ],
  "next_review_date": "2026-01-15",
  "ecdd_required": false
}
```

**Events Emitted:**
- `mrp.created`
- `risk_assessment.completed`

### `POST /compliance/transaction-monitoring-alert`
Create monitoring alert (BA-06)

**Policy Integration:**
- `BA-06` Transaction Monitoring & Case Management

**Request:**
```json
{
  "alert_type": "structuring",
  "member_id": "mbr_01h2x...",
  "account_id": "acct_01h2x...",
  "transactions": [
    "xfer_01h...",
    "xfer_01h2..."
  ],
  "pattern_description": "Multiple cash deposits just under $10K threshold",
  "risk_score": 75
}
```

**Response:**
```json
{
  "case_id": "case_01h...",
  "status": "open",
  "assigned_to": "analyst_01h...",
  "priority": "high",
  "due_date": "2024-01-17"
}
```

**Events Emitted:**
- `tms.alert.created`
- `case.opened`

### `POST /compliance/sar`
File Suspicious Activity Report (BA-08)

**Policy Integration:**
- `BA-08` SAR Filing & Confidentiality

**Request:**
```json
{
  "case_id": "case_01h...",
  "subject_member_id": "mbr_01h2x...",
  "activity_type": "structuring",
  "suspect_known": true,
  "suspect_details": {
    "name": "Jane Doe",
    "identification": "known_member"
  },
  "narrative": "Detailed description of suspicious activity...",
  "amount_cents": 2500000,
  "time_period": {
    "start_date": "2024-01-01",
    "end_date": "2024-01-14"
  },
  "financial_institution_where_activity_occurred": {
    "name": "Pynthia Federal Credit Union",
    "tin": "12-3456789",
    "address": { ... }
  }
}
```

**Response:**
```json
{
  "sar_id": "sar_01h...",
  "bsa_id": "12345678901234567890",
  "filing_date": "2024-01-15",
  "status": "filed",
  "confidential": true
}
```

**Events Emitted:**
- `sar.decision.made`
- `sar.filed`

### `POST /compliance/ctr`
File Currency Transaction Report (BA-07)

**Policy Integration:**
- `BA-07` CTR Filing

**Request:**
```json
{
  "transaction_date": "2024-01-15",
  "member_id": "mbr_01h2x...",
  "person_on_whose_behalf": {
    "same_as_conductor": true
  },
  "total_amount_cents": 1200000,
  "transactions": [
    {
      "type": "cash_in",
      "amount_cents": 1200000,
      "account_id": "acct_01h2x..."
    }
  ]
}
```

**Response:**
```json
{
  "ctr_id": "ctr_01h...",
  "bsa_id": "98765432109876543210",
  "filing_date": "2024-01-16",
  "status": "filed"
}
```

**Events Emitted:**
- `cash.threshold.exceeded`
- `ctr.generated`
- `ctr.filed`

### `GET /compliance/risk-register`
Access enterprise risk register (RA-04, RA-08)

**Policy Integration:**
- `RA-04` Risk Assessment & Register Maintenance
- `RA-08` Risk Reporting

**Query Parameters:**
- `risk_category` (credit, liquidity, operational, etc.)
- `severity` (low, medium, high, critical)
- `owner_id`
- `status` (identified, assessed, mitigated, closed)

**Response:**
```json
{
  "risks": [
    {
      "id": "risk_01h...",
      "title": "Vendor Concentration Risk - Core Processor",
      "category": "operational",
      "subcategory": "vendor",
      "inherent_risk": "high",
      "residual_risk": "medium",
      "owner_id": "exec_cio",
      "controls": ["VM-02", "VM-07", "VM-09"],
      "kris": ["kri_vendor_uptime", "kri_vendor_incidents"],
      "status": "monitored",
      "last_review_date": "2024-12-01",
      "next_review_date": "2025-03-01"
    }
  ]
}
```

---

## Events & Webhooks

### Pattern: Column + Increase hybrid approach

**From BaaS Analysis:**
- **Column**: 68 webhook events with delivery tracking — we adopt scale
- **Increase**: Real-time decision engine + programmatic subscriptions — we adopt flexibility
- **Unit**: Simple webhook model — too limited

### Object: Event

```json
{
  "id": "evt_01h2x...",
  "type": "account.created",
  "created_at": "2024-01-15T10:00:00Z",
  "data": {
    "account": {
      "id": "acct_01h2x...",
      "type": "share_draft",
      "member_id": "mbr_01h2x...",
      "status": "active"
    }
  },
  "related_resources": {
    "member": "mbr_01h2x...",
    "transaction": null
  }
}
```

### Event Types (Policy-Mapped)

#### Member & Onboarding Events
- `application.created` → FL-05
- `application.completed` → FL-05
- `kyc.started` → CD-04, BA-03
- `kyc.passed` → CD-04
- `kyc.failed` → CD-04
- `kyc.manual_review` → CD-04
- `member.onboarded` → CD-01
- `member.profile.updated` → CD-09

#### Account Events
- `account.created` → CA-06
- `account.frozen` → RZ-03
- `account.unfrozen` → RZ-03
- `account.closed` → CD-12
- `account.entitlement.added` → IS-06

#### Payment Events
- `ach.transfer.created` → BA-06
- `wire.created` → BA-10
- `wire.released` → BA-10
- `rtp.transfer.created` → BA-06
- `check.deposit.created` → IS-10

#### Compliance Events  
- `cip.verified` → BA-03
- `ofac.screen.at.onboard` → BA-05
- `ofac.hit.reviewed` → BA-05
- `ofac.blocked` → BA-05
- `tms.alert.created` → BA-06
- `case.opened` → BA-06
- `sar.filed` → BA-08
- `ctr.filed` → BA-07

#### Risk Events
- `risk.threshold.breach` → RZ-01, RA-06
- `mrp.created` → CD-03
- `risk.trigger.ecdd` → CD-07
- `pep.hit.created` → BA-20

#### Card Events
- `card.created`
- `card.activated`
- `card.frozen`
- `card.authorization.approved`
- `card.authorization.declined`

#### Liquidity & Resolution Events
- `lar.band_changed` → LP-05, CFP-01
- `liquidity.lcr.warn` → RZ-01
- `ops.safe_mode.enable` → RZ-02
- `org.freeze.all` → RZ-04

### `POST /webhooks`
Create webhook endpoint

**Policy Integration:**
- `IS-06` Access control
- `IS-14` Logging & monitoring

**Request:**
```json
{
  "url": "https://partner.example.com/webhooks",
  "events": [
    "account.created",
    "ach.transfer.created",
    "tms.alert.created"
  ],
  "description": "Partner integration webhook",
  "secret": "whsec_...",
  "enabled": true
}
```

**Response:**
```json
{
  "id": "whk_01h...",
  "url": "https://partner.example.com/webhooks",
  "events": ["account.created", "ach.transfer.created"],
  "status": "active",
  "created_at": "2024-01-15T10:00:00Z"
}
```

### `GET /webhooks/:id/deliveries`
View webhook delivery status (Column pattern)

**Policy Integration:**
- `VM-07` Ongoing monitoring
- `IS-14` Logging

**Response:**
```json
{
  "deliveries": [
    {
      "id": "whdel_01h...",
      "event_id": "evt_01h2x...",
      "event_type": "account.created",
      "attempted_at": "2024-01-15T10:00:01Z",
      "status": "success",
      "status_code": 200,
      "response_time_ms": 234
    }
  ]
}
```

---

## Policy Integration Matrix

### Cross-Reference: API Endpoints to Policy Controls

| Endpoint | Primary Policy Controls | Events Emitted | Audit Logs |
|----------|------------------------|----------------|------------|
| `POST /members` | CD-04, CD-03, BA-03 | `application.created`, `kyc.passed`, `cip.verified` | `member.created`, `kyc.verification.completed` |
| `POST /entities` | CD-05, CD-07, BA-04 | `business.application.submitted`, `bo.form_submitted`, `kyb.started` | `entity.created`, `bo.collected` |
| `POST /accounts` | CD-04, LP-06, CA-06 | `account.created`, `account.funded`, `gl.posting.created` | `account.opened`, `gl.posted` |
| `POST /accounts/:id/freeze` | RZ-03, BA-05, IS-09 | `account.frozen`, `cust.freeze.requested`, `ofac.hit.reviewed` | `freeze.applied` |
| `POST /transfers/ach` | BA-06, BA-10, LP-03 | `ach.transfer.created`, `tms.alert.created`, `payment.pre.screen` | `transfer.initiated`, `ofac.screened` |
| `POST /transfers/wire` | BA-10, FL-03, LP-03 | `wire.created`, `wire.validation.passed`, `payment.pre.screen` | `wire.initiated`, `dual_control.approved` |
| `POST /cards` | IS-10, CD-04, FL-03 | `card.created`, `card.shipped`, `kyc.verification.required` | `card.issued` |
| `POST /compliance/ofac-screening` | BA-05 | `ofac.screen.at.onboard`, `ofac.hit.reviewed`, `ofac.blocked` | `ofac.screening.completed`, `ofac.hit.logged` |
| `POST /compliance/sar` | BA-08 | `sar.decision.made`, `sar.filed` | `sar.filed`, `sar.board_reported` |
| `POST /compliance/ctr` | BA-07 | `cash.threshold.exceeded`, `ctr.generated`, `ctr.filed` | `ctr.filed` |

### Event-to-Policy Mapping

| Event Code | Policy Controls | Purpose | Downstream Actions |
|------------|----------------|---------|-------------------|
| `application.created` | FL-05, CD-04 | Trigger CIP and start action notice clock | Begin KYC, start 30-day timer |
| `kyc.passed` | CD-04, BA-03 | CIP verification complete | Allow account opening |
| `decision.recorded` | FL-05 | Credit/account decision made | Generate action notice within 30 days |
| `ofac.hit.reviewed` | BA-05 | OFAC match requires review | Place hold, escalate to compliance |
| `tms.alert.created` | BA-06 | Suspicious activity detected | Assign to analyst, start case |
| `sar.decision.made` | BA-08 | SAR filing decision | File within 30/60 days, notify board monthly |
| `lar.band_changed` | LP-05, CFP-01 | Liquidity ratio crossed threshold | Activate CFP level, notify ALCO |
| `risk.threshold.breach` | RZ-01, RA-06 | Risk appetite breached | Escalate, create remediation plan |
| `pep.hit.created` | BA-20, CD-07 | PEP identified | Trigger ECDD, enhanced monitoring |

### Field Schema Registry

Common fields used across endpoints and policies:

**Member/Entity Fields:**
- `member.id`
- `member.name` → `first_name`, `last_name`
- `member.dob` (date of birth)
- `member.tin` (SSN/EIN)
- `member.addr` (address object)
- `entity.bo_list` (beneficial owners)
- `entity.naics` (industry code)

**Account Fields:**
- `account.id`
- `account.type`
- `account.balance_cents`
- `account.status`

**Transaction Fields:**
- `txn.id`
- `txn.amount_cents`
- `txn.type`
- `txn.from_account_id`
- `txn.to_account_id`

**Risk/Compliance Fields:**
- `risk.score`
- `risk.rating` (low/medium/high)
- `kyc.status`
- `cip.status`
- `ofac.hit`
- `sar.id`
- `ctr.id`

**Liquidity Fields:**
- `lar` (Liquid Assets Ratio)
- `gap.cumulative`
- `survival.days`
- `facility.headroom`

---

## Implementation Notes

### Credit Union vs Bank Distinctions

1. **Membership Required**: Unlike banks, credit unions require membership (share account)
2. **Dividends not Interest**: Credit unions pay dividends on share accounts, not interest
3. **Voting Rights**: Members have voting rights in governance
4. **Field of Membership**: Must verify eligibility basis (community, occupational, associational)
5. **Not-for-Profit**: Affects pricing, fee structures, and capital treatment

### BaaS Provider Pattern Adoption

**From Unit:**
- JWT authentication for internal services
- DACA support for lending
- Unified payment concepts

**From Q2 Helix:**
- Entitlements system for multi-user accounts
- Customer tokens for secure operations
- Card mock endpoints (for testing)

**From Increase:**
- OAuth platform for third-party integrations
- Multiple account numbers per account
- IntraFi FDIC extension
- Wire drawdown capability
- Double-entry bookkeeping endpoints
- ACH prenotifications
- Real-time decision engine pattern

**From Column:**
- ACH Positive Pay rules
- Domestic/international wire separation
- International wire tracking
- Check image uploads
- Transaction simulation endpoints
- Comprehensive webhook delivery tracking

### Next Steps for Implementation

1. **Phase 1: Core Member & Account APIs**
   - Member/entity onboarding
   - Account opening
   - Basic transfers
   - CIP/KYC integration

2. **Phase 2: Compliance & Risk APIs**
   - OFAC/sanctions screening
   - Transaction monitoring
   - SAR/CTR filing
   - Risk assessment

3. **Phase 3: Payments**
   - ACH origination
   - Wire transfers
   - RTP
   - Check deposits

4. **Phase 4: Cards**
   - Card issuance
   - Authorization handling
   - Wallet provisioning
   - Fraud monitoring

5. **Phase 5: Advanced Features**
   - Loan origination
   - IntraFi integration
   - International wires
   - Resolution/safe mode controls

---

## Appendix: Event Schema

### Event Object Structure

```typescript
interface Event {
  id: string;                    // evt_...
  type: string;                  // e.g., "account.created"
  created_at: string;            // ISO 8601
  data: object;                  // Event-specific payload
  related_resources: {           // For correlation
    member?: string;
    account?: string;
    transaction?: string;
    case?: string;
  };
  policy_controls: string[];     // e.g., ["CD-04", "BA-03"]
  idempotency_key?: string;
}
```

### Audit Log Standards

All mutation operations must produce audit logs with:
- `event_type`: What happened
- `actor_id`: Who did it (user, system, service)
- `subject_id`: What was affected (member, account, etc.)
- `timestamp`: When it happened (ISO 8601)
- `changes`: Before/after state (for updates)
- `policy_control`: Which policy control this relates to
- `ip_address`: Source IP (for user actions)
- `user_agent`: Client information (for user actions)

Example audit log entry:
```json
{
  "event_type": "member.created",
  "actor_id": "user_01h...",
  "actor_type": "employee",
  "subject_id": "mbr_01h2x...",
  "subject_type": "member",
  "timestamp": "2024-01-15T10:00:00Z",
  "policy_controls": ["CD-04", "BA-03"],
  "ip_address": "192.168.1.1",
  "user_agent": "Mozilla/5.0...",
  "metadata": {
    "department": "member_services",
    "branch_id": "branch_01"
  }
}
```

---

**END OF SPECIFICATION v1.0.0**

*This specification should be versioned in Git and reviewed quarterly or upon material policy changes.*