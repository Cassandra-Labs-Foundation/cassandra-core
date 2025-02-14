Increase API
├── Authentication
│   └── Bearer Authentication (API Key: secret_key / sandbox_key) over HTTPS
│
├── Accounts
│   ├── Account Object
│   │   ├─ **Parameters**: entity_id, program_id, name, currency, status, interest_rate, interest_accrued, etc.
│   │   ├─ **Endpoint**: POST /accounts
│   │   │   (Create an account)
│   │   ├─ **Endpoint**: GET /accounts
│   │   │   (List accounts; filterable by entity_id, status, etc.)
│   │   ├─ **Endpoint**: GET /accounts/#123;id#125;
│   │   │   (Retrieve an account by ID)
│   │   ├─ **Endpoint**: PATCH /accounts/#123;id#125;
│   │   │   (Update an account)
│   │   └─ **Endpoint**: POST /accounts/#123;id#125;/close
│   │       (Close an account)
│   │
│   └── Account Balance
│   └─ **Endpoint**: GET /accounts/#123;id#125;/balance
│   (Retrieve current balance)
│
├── Account Numbers
│   ├── Account Number Object
│   │   ├─ **Parameters**: account_id, name, inbound_ach, inbound_checks, routing_number, status, etc.
│   │   ├─ **Endpoint**: POST /account_numbers
│   │   │   (Create an account number)
│   │   ├─ **Endpoint**: GET /account_numbers
│   │   │   (List account numbers)
│   │   └─ **Endpoint**: GET /account_numbers/#123;id#125;
│   │       (Retrieve an account number)
│
├── Transactions
│   ├── Transaction Object
│   │   ├─ **Parameters**: account_id, amount, currency, description, created_at, route_id, route_type, source, etc.
│   │   ├─ **Endpoint**: GET /transactions
│   │   │   (List transactions)
│   │   └─ **Endpoint**: GET /transactions/#123;id#125;
│   │       (Retrieve a transaction)
│   │
│   ├── Pending Transaction Object
│   │   ├─ **Endpoint**: GET /pending_transactions
│   │   │   (List pending transactions)
│   │   └─ **Endpoint**: GET /pending_transactions/#123;id#125;
│   │       (Retrieve a pending transaction)
│   │
│   └── Declined Transaction Object
│       ├─ **Endpoint**: GET /declined_transactions
│       │   (List declined transactions)
│       └─ **Endpoint**: GET /declined_transactions/#123;id#125;
│           (Retrieve a declined transaction)
│
├── Transfers
│   ├── Account Transfers
│   │   ├─ **Parameters**: account_id, destination_account_id, amount, currency, description, etc.
│   │   ├─ **Endpoint**: POST /account_transfers
│   │   │   (Create an account transfer)
│   │   ├─ **Endpoint**: GET /account_transfers
│   │   │   (List account transfers)
│   │   └─ **Endpoint**: GET /account_transfers/#123;id#125;
│   │       (Retrieve an account transfer)
│   │
│   ├── ACH Transfers
│   │   ├─ **Parameters**: account_id, account_number, amount, routing_number, statement_descriptor, effective_date, etc.
│   │   ├─ **Endpoint**: POST /ach_transfers
│   │   │   (Initiate an ACH transfer)
│   │   ├─ **Endpoint**: GET /ach_transfers
│   │   │   (List ACH transfers)
│   │   ├─ **Endpoint**: GET /ach_transfers/#123;id#125;
│   │   │   (Retrieve an ACH transfer)
│   │   ├─ **Endpoint**: POST /ach_transfers/#123;id#125;/approve
│   │   │   (Approve an ACH transfer)
│   │   └─ **Endpoint**: POST /ach_transfers/#123;id#125;/cancel
│   │       (Cancel an ACH transfer)
│   │
│   ├── Wire Transfers
│   │   ├─ **Parameters**: account_id, account_number, amount, routing_number, message_to_recipient, etc.
│   │   ├─ **Endpoint**: POST /wire_transfers
│   │   │   (Initiate a wire transfer)
│   │   ├─ **Endpoint**: GET /wire_transfers
│   │   │   (List wire transfers)
│   │   ├─ **Endpoint**: GET /wire_transfers/#123;id#125;
│   │   │   (Retrieve a wire transfer)
│   │   └─ **Endpoint**: POST /wire_transfers/#123;id#125;/cancel
│   │       (Cancel or reverse a wire transfer)
│   │
│   └── Realtime Transfers
│       ├─ **Parameters**: account_id, destination_account_number, amount, destination_routing_number, remittance_information, etc.
│       ├─ **Endpoint**: POST /real_time_payments_transfers
│       │   (Create a realtime transfer)
│       ├─ **Endpoint**: GET /real_time_payments_transfers
│       │   (List realtime transfers)
│       └─ **Endpoint**: GET /real_time_payments_transfers/#123;id#125;
│           (Retrieve a realtime transfer)
│
├── Cards
│   ├── Card Object
│   │   ├─ **Parameters**: account_id, description, card_type, expiration_month, expiration_year, billing_address (line1, line2, city, state, postal_code), etc.
│   │   ├─ **Endpoint**: POST /cards
│   │   │   (Issue a new card)
│   │   ├─ **Endpoint**: GET /cards
│   │   │   (List all cards)
│   │   ├─ **Endpoint**: GET /cards/#123;id#125;
│   │   │   (Retrieve card details)
│   │   └─ **Endpoint**: PATCH /cards/#123;id#125;
│   │       (Update card information)
│   │
│   ├── Card Payment
│   │   └─ **Endpoint**: GET /cards/#123;id#125;/payments
│   │       (View card payment history)
│   │
│   └── Card Dispute
│       └─ **Endpoint**: POST /cards/#123;id#125;/disputes
│           (File a card dispute; Params: disputed_transaction_id, explanation)
│
├── Files & Documents
│   ├── File Object
│   │   ├─ **Parameters**: file (multipart), purpose, description
│   │   ├─ **Endpoint**: POST /files
│   │   │   (Upload a file)
│   │   └─ **Endpoint**: GET /files/#123;id#125;
│   │       (Retrieve a file)
│   │
│   └── Document Object
│       ├─ **Parameters**: associated_entity_id, file_id, category, description
│       └─ **Endpoint**: GET /documents/#123;id#125;
│           (Fetch a document)
│
├── Exports
│   ├─ **Parameters**: category, options (e.g. account_id, date_range)
│   ├─ **Endpoint**: POST /exports
│   │   (Create an export)
│   └─ **Endpoint**: GET /exports/#123;id#125;
│       (Retrieve export details)
│
├── Bookkeeping
│   ├── Bookkeeping Account Object
│   │   ├─ **Parameters**: entity_id, name, compliance_category
│   │   ├─ **Endpoint**: POST /bookkeeping_accounts
│   │   │   (Create a bookkeeping account)
│   │   └─ **Endpoint**: GET /bookkeeping_accounts
│   │       (List bookkeeping accounts)
│   │
│   ├── Bookkeeping Entry Set Object
│   │   ├─ **Parameters**: date, transaction_id, entries (each: account_id, amount)
│   │   ├─ **Endpoint**: POST /bookkeeping_entry_sets
│   │   │   (Create an entry set)
│   │   └─ **Endpoint**: GET /bookkeeping_entry_sets/#123;id#125;
│   │       (Retrieve an entry set)
│   │
│   └── Bookkeeping Entry Object
│       └─ **Endpoint**: GET /bookkeeping_entries/#123;id#125;
│           (Retrieve a bookkeeping entry)
│
├── Webhooks
│   ├── Webhook **Endpoint** Object
│   │   ├─ **Parameters**: callback_url, events, secret
│   │   ├─ **Endpoint**: POST /webhook_**Endpoint**s
│   │   │   (Register a webhook)
│   │   ├─ **Endpoint**: GET /webhook_**Endpoint**s
│   │   │   (List webhook **Endpoint**s)
│   │   ├─ **Endpoint**: PATCH /webhook_**Endpoint**s/#123;id#125;
│   │   │   (Update a webhook)
│   │   └─ **Endpoint**: DELETE /webhook_**Endpoint**s/#123;id#125;
│   │       (Remove a webhook)
│   │
│   └── Webhook Deliveries
│       └─ **Endpoint**: GET /webhook_deliveries
│           (List webhook events)
│
└── Simulation (Sandbox Only)
├─ **Endpoint**: POST /simulate/ach_transfers
│   (Simulate ACH transfer events; Params: bank_account_id, amount, effective_date)
├─ **Endpoint**: POST /simulate/wire_transfers
│   (Simulate wire transfer events; Params: bank_account_id, amount, beneficiary_details)
├─ **Endpoint**: POST /simulate/real_time_payments_transfers
│   (Simulate realtime transfers; Params: bank_account_id, amount, destination_details)
└─ **Endpoint**: POST /simulate/card_reversals