Lead Bank API
├── Authentication
│   └── OAuth 2.0 (Bearer Token: sandbox/live) over HTTPS
│
├── Entity
│   ├── Person Entity Object
│   │   ├─ **Parameters:** first_name, last_name, ssn, date_of_birth, email, address (line1, city, state, postal_code, country_code), kyc_status, verification_data
│   │   ├─ **Endpoint:** POST /entities/person  (Create a person entity)
│   │   └─ **Endpoint:** PATCH /entities/person  (Update a person entity)
│   │
│   ├── Business Entity Object
│   │   ├─ **Parameters:** business_name, registration_number, contact_email, address (line1, city, state, postal_code, country_code), kyc_documents, verification_tags
│   │   ├─ **Endpoint:** POST /entities/business  (Create a business entity)
│   │   └─ **Endpoint:** PATCH /entities/business  (Update a business entity)
│   │
│   ├─ **Endpoint:** GET /entities/{id}   (Retrieve an entity by ID)
│   ├─ **Endpoint:** DELETE /entities/{id}   (Delete an entity)
│   └─ **Endpoint:** GET /entities   (List all entities)
│       └─ (Includes document submission endpoints for entity documents)
│
├── Bank Account
│   ├── Bank Account Object
│   │   ├─ **Parameters:** entity_id, account_type, description, currency, default_account_number, routing_number, etc.
│   │   ├─ **Endpoint:** POST /bank-accounts   (Create a bank account)
│   │   ├─ **Endpoint:** GET /bank-accounts   (List all bank accounts)
│   │   ├─ **Endpoint:** GET /bank-accounts/{id}   (Get a bank account by ID)
│   │   ├─ **Endpoint:** PATCH /bank-accounts/{id}   (Update a bank account)
│   │   └─ **Endpoint:** DELETE /bank-accounts/{id}   (Delete a bank account)
│   │
│   └── Account Balance
│       └─ **Endpoint:** GET /bank-accounts/{id}/balance   (Retrieve current balance)
│
├── Account Number
│   ├── Account Number Object
│   │   ├─ **Parameters:** bank_account_id, number, routing_number, status, label
│   │   ├─ **Endpoint:** POST /account-numbers   (Create an account number)
│   │   ├─ **Endpoint:** GET /account-numbers   (List account numbers)
│   │   └─ **Endpoint:** GET /account-numbers/{id}   (Retrieve an account number)
│
├── Loan
│   ├── Loan Object
│   │   ├─ **Parameters:** bank_account_id, principal, term, interest_rate, start_date, collateral, etc.
│   │   ├─ **Endpoint:** POST /loans   (Create a loan)
│   │   ├─ **Endpoint:** GET /loans   (List loans)
│   │   ├─ **Endpoint:** GET /loans/{id}   (Retrieve a loan)
│   │   └─ **Endpoint:** PATCH /loans/{id}   (Update a loan)
│   │
│   ├── Loan Disbursement
│   │   ├─ **Endpoint:** POST /loans/{id}/disbursements   (Initiate a disbursement)
│   │   ├─ **Endpoint:** GET /loans/{id}/disbursements   (List disbursements)
│   │   └─ **Endpoint:** PATCH /loans/{id}/disbursements   (Update a disbursement)
│   │
│   └── Loan Payment
│       ├─ **Endpoint:** POST /loans/{id}/payments   (Submit a payment)
│       ├─ **Endpoint:** GET /loans/{id}/payments   (List payments)
│       └─ **Endpoint:** GET /loans/{id}/all-payments   (All payment history)
│
├── Counterparty
│   ├── Counterparty Object
│   │   ├─ **Endpoint:** POST /counterparties   (Create a counterparty)
│   │   ├─ **Endpoint:** GET /counterparties   (List counterparties)
│   │   ├─ **Endpoint:** GET /counterparties/{id}   (Retrieve a counterparty)
│   │   └─ **Endpoint:** DELETE /counterparties/{id}   (Delete a counterparty)
│   │
│   ├── Financial Institution Object
│   │   └─ **Endpoint:** GET /financial-institutions   (Get institution details)
│   │
│   └── IBAN Validation
│       └─ **Endpoint:** POST /validate-iban   (Validate an IBAN)
│
├── Transfers
│   ├── ACH Transfer
│   │   ├─ **Parameters:** bank_account_id, amount, account_number, routing_number, effective_date, etc.
│   │   ├─ **Endpoint:** POST /transfers/ach   (Initiate an ACH transfer)
│   │   ├─ **Endpoint:** GET /transfers/ach   (List ACH transfers)
│   │   ├─ **Endpoint:** GET /transfers/ach/{id}   (Retrieve an ACH transfer)
│   │   ├─ **Endpoint:** POST /transfers/ach/{id}/cancel   (Cancel an ACH transfer)
│   │   └─ **Endpoint:** POST /transfers/ach/{id}/reverse   (Reverse an ACH transfer)
│   │
│   ├── Wire Transfer
│   │   ├─ **Parameters:** bank_account_id, amount, beneficiary_account, beneficiary_routing, message, etc.
│   │   ├─ **Endpoint:** POST /transfers/wire   (Initiate a wire transfer)
│   │   ├─ **Endpoint:** GET /transfers/wire   (List wire transfers)
│   │   ├─ **Endpoint:** GET /transfers/wire/{id}   (Retrieve a wire transfer)
│   │   └─ **Endpoint:** POST /transfers/wire/{id}/reverse   (Reverse a wire transfer)
│   │
│   ├── Realtime Transfer
│   │   ├─ **Endpoint:** POST /transfers/realtime   (Create a realtime transfer)
│   │   ├─ **Endpoint:** GET /transfers/realtime   (List realtime transfers)
│   │   └─ **Endpoint:** GET /transfers/realtime/{id}   (Retrieve a realtime transfer)
│   │
│   └── Transfer Summary
│       └─ **Endpoint:** GET /transfers/summary   (Get transfer history)
│
├── Cards
│   ├── Card Object
│   │   ├─ **Parameters:** bank_account_id, description, card_type, expiration_month, expiration_year, billing_address, etc.
│   │   ├─ **Endpoint:** POST /cards   (Issue a new card)
│   │   ├─ **Endpoint:** GET /cards   (List all cards)
│   │   ├─ **Endpoint:** GET /cards/{id}   (Retrieve card details)
│   │   └─ **Endpoint:** PATCH /cards/{id}   (Update card information)
│   │
│   ├── Card Payment
│   │   └─ **Endpoint:** GET /cards/{id}/payments   (View card payment history)
│   │
│   └── Card Dispute
│       └─ **Endpoint:** POST /cards/{id}/disputes   (File a card dispute)
│
├── Documents
│   ├── Document Upload
│   │   └─ **Endpoint:** POST /documents   (Upload a document)
│   └── Document Retrieve
│       └─ **Endpoint:** GET /documents/{id}   (Fetch a document)
│
├── Reporting
│   ├── Report Generation
│   │   ├─ **Endpoint:** POST /reports   (Generate a report)
│   │   └─ **Endpoint:** GET /reports/{id}   (Retrieve report details)
│   └── Report Listing
│       └─ **Endpoint:** GET /reports   (List available reports)
│
├── Webhooks
│   ├── Webhook Endpoint
│   │   ├─ **Endpoint:** POST /webhooks   (Register a webhook)
│   │   ├─ **Endpoint:** GET /webhooks   (List webhook endpoints)
│   │   ├─ **Endpoint:** PATCH /webhooks/{id}   (Update a webhook)
│   │   └─ **Endpoint:** DELETE /webhooks/{id}   (Remove a webhook)
│   └── Webhook Events
│       └─ **Endpoint:** GET /webhook-events   (List webhook events)
│
└── Simulation (Sandbox Only)
    ├─ **Endpoint:** POST /simulate/ach-credit      (Simulate an ACH credit)
    ├─ **Endpoint:** POST /simulate/wire           (Simulate a wire transfer)
    ├─ **Endpoint:** POST /simulate/realtime       (Simulate a realtime transfer)
    └─ **Endpoint:** POST /simulate/card-reversal  (Simulate a card authorization reversal)
