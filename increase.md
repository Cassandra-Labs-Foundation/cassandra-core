![Increase-DB-Schema](./increase/increase-db-schema.png)

## Textual Diagram

```
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
```

## Schema
erDiagram
    %% ENTITY with extra details (e.g. structure, website, etc.)
    ENTITY {
      string id PK
      string structure
      string name
      string website
      string tax_identifier
      string incorporation_state
      string industry_code
    }
    
    %% ACCOUNT includes informational_entity_id and replacement details
    ACCOUNT {
      string id PK
      string bank
      datetime created_at
      string currency
      string entity_id FK
      string informational_entity_id
      string program_id
      string name
      string status
      string interest_rate
      string interest_accrued
      date interest_accrued_at
      string idempotency_key
      string replacement_replaced_account_id
      string replacement_replaced_by_account_id
    }
    ENTITY ||--o{ ACCOUNT : "owns"

    %% ACCOUNT_NUMBER with nested inbound options and replacement
    ACCOUNT_NUMBER {
      string id PK
      string account_id FK
      string account_number
      datetime created_at
      string name
      string routing_number
      string status
      string type
      string inbound_ach_debit_status
      string inbound_checks_status
      string replacement_replaced_account_number_id
      string replacement_replaced_by_account_number_id
      string idempotency_key
    }
    ACCOUNT ||--o{ ACCOUNT_NUMBER : "has"

    %% ACCOUNT_STATEMENT (unchanged)
    ACCOUNT_STATEMENT {
      string id PK
      string account_id FK
      datetime created_at
      string file_id
      datetime statement_period_start
      datetime statement_period_end
      integer starting_balance
      integer ending_balance
      string type
    }
    ACCOUNT ||--o{ ACCOUNT_STATEMENT : "generates"

    %% TRANSACTION with nested source details (example: inbound_ach_transfer fields)
    TRANSACTION {
      string id PK
      string account_id FK
      integer amount
      string currency
      datetime created_at
      string description
      string route_id
      string route_type
      string source_category
      string source_originator_company_name
      string source_trace_number
      string type
    }
    ACCOUNT ||--o{ TRANSACTION : "records"

    %% PENDING and DECLINED Transactions (keeping high-level)
    PENDING_TRANSACTION {
      string id PK
      string account_id FK
      integer amount
      string currency
      datetime created_at
      datetime completed_at
      string description
      string route_id
      string route_type
      string status
      string type
    }
    DECLINED_TRANSACTION {
      string id PK
      string account_id FK
      integer amount
      string currency
      datetime created_at
      string description
      string route_id
      string route_type
      string type
    }
    TRANSACTION ||--|| PENDING_TRANSACTION : "pending version"
    TRANSACTION ||--|| DECLINED_TRANSACTION : "declined version"

    %% TRANSFERS (generic) with extra nested details for approval/cancellation
    TRANSFER {
      string id PK
      string account_id FK
      integer amount
      string currency
      datetime created_at
      string description
      string status
      string type
      string approval_approved_at
      string cancellation_reason
      string idempotency_key
    }
    ACCOUNT ||--o{ TRANSFER : "initiates"
    
    %% Specific transfer types with extra fields
    ACCOUNT_TRANSFER {
      string id PK
      string account_id FK
      string destination_account_id
      integer amount
      string currency
      datetime created_at
      string description
      string status
      string transaction_id
      string pending_transaction_id
      string type
      string idempotency_key
    }
    ACH_TRANSFER {
      string id PK
      string account_id FK
      string account_number
      integer amount
      string currency
      datetime created_at
      string routing_number
      string status
      string submission_trace_number
      string type
      string idempotency_key
    }
    WIRE_TRANSFER {
      string id PK
      string account_id FK
      integer amount
      string currency
      datetime created_at
      string routing_number
      string status
      string message_to_recipient
      string type
      string idempotency_key
    }
    REAL_TIME_PAYMENTS_TRANSFER {
      string id PK
      string account_id FK
      integer amount
      string currency
      datetime created_at
      string destination_account_number
      string destination_routing_number
      string status
      string remittance_information
      string type
      string idempotency_key
    }
    TRANSFER ||--|| ACCOUNT_TRANSFER : "account transfer"
    TRANSFER ||--|| ACH_TRANSFER : "ACH transfer"
    TRANSFER ||--|| WIRE_TRANSFER : "wire transfer"
    TRANSFER ||--|| REAL_TIME_PAYMENTS_TRANSFER : "RTP transfer"

    %% CARD and related objects with more detail
    CARD {
      string id PK
      string account_id FK
      datetime created_at
      string description
      string last4
      integer expiration_month
      integer expiration_year
      string status
      string billing_address_line1
      string billing_address_line2
      string billing_address_city
      string billing_address_state
      string billing_address_postal_code
      string type
      string idempotency_key
    }
    CARD_PAYMENT {
      string id PK
      string card_id FK
      datetime created_at
      string state_details
      string type
    }
    CARD_DISPUTE {
      string id PK
      string disputed_transaction_id
      datetime created_at
      string explanation
      string status
      string type
      string idempotency_key
    }
    PHYSICAL_CARD {
      string id PK
      string card_id FK
      datetime created_at
      string status
      string shipment_method
      string shipment_status
      string type
      string idempotency_key
    }
    DIGITAL_WALLET_TOKEN {
      string id PK
      string card_id FK
      datetime created_at
      string status
      string token_requestor
      string type
    }
    ACCOUNT ||--o{ CARD : "owns"
    CARD ||--o{ CARD_PAYMENT : "processes"
    CARD ||--o{ CARD_DISPUTE : "has dispute"
    CARD ||--o{ PHYSICAL_CARD : "has physical version"
    CARD ||--o{ DIGITAL_WALLET_TOKEN : "tokenized as"

    %% CHECK DEPOSIT with image file details
    CHECK_DEPOSIT {
      string id PK
      string account_id FK
      integer amount
      datetime created_at
      string currency
      string status
      string front_image_file_id
      string back_image_file_id
      string type
      string idempotency_key
    }
    ACCOUNT ||--o{ CHECK_DEPOSIT : "receives"

    %% FILE and DOCUMENT with additional metadata
    FILE {
      string id PK
      datetime created_at
      string purpose
      string description
      string direction
      string mime_type
      string filename
      string download_url
      string type
      string idempotency_key
    }
    DOCUMENT {
      string id PK
      string category
      datetime created_at
      string entity_id FK
      string file_id FK
      string type
    }
    FILE ||--|| DOCUMENT : "contains"

    %% Supplemental Documents (attached to Entities)
    SUPPLEMENTAL_DOCUMENT {
      string file_id PK
      datetime created_at
      string type
      string idempotency_key
    }
    ENTITY ||--o{ SUPPLEMENTAL_DOCUMENT : "attaches"

    %% EXPORT objects
    EXPORT {
      string id PK
      datetime created_at
      string category
      string status
      string file_id FK
      string file_download_url
      string type
      string idempotency_key
    }
    EXPORT ||--|| FILE : "generated file"

    %% BOOKKEEPING objects with extra keys
    BOOKKEEPING_ACCOUNT {
      string id PK
      string entity_id FK
      string name
      string compliance_category
      string type
      string idempotency_key
    }
    BOOKKEEPING_ENTRY_SET {
      string id PK
      string transaction_id
      datetime date
      datetime created_at
      string type
      string idempotency_key
    }
    BOOKKEEPING_ENTRY {
      string id PK
      string bookkeeping_account_id FK
      integer amount
      string entry_set_id FK
      datetime created_at
      string type
    }
    ACCOUNT ||--o{ BOOKKEEPING_ACCOUNT : "has"
    BOOKKEEPING_ACCOUNT ||--o{ BOOKKEEPING_ENTRY_SET : "contains"
    BOOKKEEPING_ENTRY_SET ||--o{ BOOKKEEPING_ENTRY : "has"

    %% OAUTH and GROUP objects
    GROUP {
      string id PK
      datetime created_at
      string activation_status
      string ach_debit_status
      string type
    }
    OAUTH_CONNECTION {
      string id PK
      string group_id FK
      datetime created_at
      string status
      string type
      string deleted_at
    }
    OAUTH_TOKEN {
      string access_token
      string token_type
      string type
    }
    GROUP ||--o{ OAUTH_CONNECTION : "has"
    OAUTH_CONNECTION ||--|| OAUTH_TOKEN : "issues"

    %% INTRAFI objects with extra details
    INTRAFI_ACCOUNT_ENROLLMENT {
      string id PK
      string account_id FK
      string status
      string intrafi_id
      string type
      string idempotency_key
    }
    INTRAFI_BALANCE {
      string effective_date
      integer total_balance
      string currency
      string type
    }
    INTRAFI_EXCLUSION {
      string id PK
      datetime submitted_at
      datetime excluded_at
      string bank_name
      string fdic_certificate_number
      string entity_id FK
      string status
      string type
      string idempotency_key
    }
    ACCOUNT ||--o{ INTRAFI_ACCOUNT_ENROLLMENT : "enrolls in"
    ENTITY ||--o{ INTRAFI_EXCLUSION : "excludes"

    %% ACH PRENOTIFICATION with extra fields
    ACH_PRENOTIFICATION {
      string id PK
      string account_number
      string routing_number
      datetime created_at
      string status
      string type
      string addendum
      string company_descriptive_date
      string company_discretionary_data
      string company_entry_description
      string company_name
      string credit_debit_indicator
      string effective_date
      string idempotency_key
    }
    ACCOUNT_NUMBER ||--o{ ACH_PRENOTIFICATION : "verifies"


![increase-state-flow](./increase/increase-flowchart.png)
flowchart TD
  %% Main API Node
  API[Increase Banking API]

  %% Authentication
  subgraph Auth [Authentication]
    Auth1[Bearer Authentication<br>API Key: secret_key / sandbox_key]
  end

  %% Accounts
  subgraph Accts [Accounts]
    A_Create[POST /accounts<br>Create account<br>Parameters: entity_id, program_id, name, currency, status, interest_rate, interest_accrued, ...]
    A_List[GET /accounts<br>List accounts]
    A_Get[GET /accounts/#123;id#125;<br>Retrieve account]
    A_Update[PATCH /accounts/#123;id#125;<br>Update account]
    A_Close[POST /accounts/#123;id#125;/close<br>Close account<br>Parameters: none]
    A_Balance[GET /accounts/#123;id#125;/balance<br>Retrieve balance]
  end

  %% Account Numbers
  subgraph AN [Account Numbers]
    AN_Create[POST /account_numbers<br>Create account number<br>Parameters: account_id, name, inbound_ach, inbound_checks, routing_number, status, ...]
    AN_List[GET /account_numbers<br>List account numbers]
    AN_Get[GET /account_numbers/#123;id#125;<br>Retrieve account number]
  end

  %% Transactions
  subgraph Tx [Transactions]
    T_List[GET /transactions<br>List transactions]
    T_Get[GET /transactions/#123;id#125;<br>Retrieve transaction]
    PT_List[GET /pending_transactions<br>List pending transactions]
    PT_Get[GET /pending_transactions/#123;id#125;<br>Retrieve pending transaction]
    DT_List[GET /declined_transactions<br>List declined transactions]
    DT_Get[GET /declined_transactions/#123;id#125;<br>Retrieve declined transaction]
  end

  %% Transfers
  subgraph Xfer [Transfers]
    %% Account Transfers
    AT_Create[POST /account_transfers<br>Create account transfer<br>Parameters: account_id, destination_account_id, amount, currency, description, ...]
    AT_List[GET /account_transfers<br>List account transfers]
    AT_Get[GET /account_transfers/#123;id#125;<br>Retrieve account transfer]
    %% ACH Transfers
    ACH_Create[POST /ach_transfers<br>Initiate ACH transfer<br>Parameters: account_id, account_number, amount, routing_number, statement_descriptor, effective_date, ...]
    ACH_List[GET /ach_transfers<br>List ACH transfers]
    ACH_Get[GET /ach_transfers/#123;id#125;<br>Retrieve ACH transfer]
    ACH_Approve[POST /ach_transfers/#123;id#125;/approve<br>Approve ACH transfer<br>Parameters: none]
    ACH_Cancel[POST /ach_transfers/#123;id#125;/cancel<br>Cancel ACH transfer<br>Parameters: none]
    %% Wire Transfers
    Wire_Create[POST /wire_transfers<br>Initiate wire transfer<br>Parameters: account_id, account_number, amount, routing_number, message_to_recipient, ...]
    Wire_List[GET /wire_transfers<br>List wire transfers]
    Wire_Get[GET /wire_transfers/#123;id#125;<br>Retrieve wire transfer]
    Wire_Cancel[POST /wire_transfers/#123;id#125;/cancel<br>Cancel or reverse wire transfer<br>Parameters: none]
    %% Real-time Payments Transfers
    RTP_Create[POST /real_time_payments_transfers<br>Create realtime transfer<br>Parameters: account_id, destination_account_number, amount, destination_routing_number, remittance_information, ...]
    RTP_List[GET /real_time_payments_transfers<br>List realtime transfers]
    RTP_Get[GET /real_time_payments_transfers/#123;id#125;<br>Retrieve realtime transfer]
  end

  %% Cards
  subgraph Cards [Cards]
    Card_Create[POST /cards<br>Issue card<br>Parameters: account_id, description, card_type, expiration_month, expiration_year, billing_address_line1, billing_address_line2, billing_address_city, billing_address_state, billing_address_postal_code, ...]
    Card_List[GET /cards<br>List cards]
    Card_Get[GET /cards/#123;id#125;<br>Retrieve card]
    Card_Update[PATCH /cards/#123;id#125;<br>Update card]
    Card_Payments[GET /cards/#123;id#125;/payments<br>Card payment history]
    Card_Disputes[POST /cards/#123;id#125;/disputes<br>File card dispute<br>Parameters: disputed_transaction_id, explanation]
  end

  %% Files and Documents
  subgraph FilesDocs [Files & Documents]
    File_Create[POST /files<br>Upload file<br>Parameters: file, purpose, description]
    File_Get[GET /files/#123;id#125;<br>Retrieve file]
    Doc_Get[GET /documents/#123;id#125;<br>Fetch document]
  end

  %% Exports
  subgraph Exp [Exports]
    Export_Create[POST /exports<br>Create export<br>Parameters: category, options: account_id, date_range, ...]
    Export_Get[GET /exports/#123;id#125;<br>Retrieve export details]
  end

  %% Bookkeeping
  subgraph BK [Bookkeeping]
    BK_Account_Create[POST /bookkeeping_accounts<br>Create bookkeeping account<br>Parameters: entity_id, name, compliance_category]
    BK_Account_List[GET /bookkeeping_accounts<br>List bookkeeping accounts]
    BK_EntrySet_Create[POST /bookkeeping_entry_sets<br>Create entry set<br>Parameters: date, transaction_id, entries: account_id, amount]
    BK_EntrySet_Get[GET /bookkeeping_entry_sets/#123;id#125;<br>Retrieve entry set]
    BK_Entry_Get[GET /bookkeeping_entries/#123;id#125;<br>Retrieve bookkeeping entry]
  end

  %% Webhooks
  subgraph WH [Webhooks]
    WH_Create[POST /webhook_endpoints<br>Register webhook<br>Parameters: callback_url, events, secret]
    WH_List[GET /webhook_endpoints<br>List webhooks]
    WH_Update[PATCH /webhook_endpoints/#123;id#125;<br>Update webhook]
    WH_Delete[DELETE /webhook_endpoints/#123;id#125;<br>Remove webhook]
    WH_Deliveries[GET /webhook_deliveries<br>List webhook events]
  end

  %% Simulation (Sandbox Only)
  subgraph Sim [Simulation Sandbox]
    Sim_ACH[POST /simulate/ach_transfers<br>Simulate ACH transfer<br>Parameters: bank_account_id, amount, effective_date]
    Sim_Wire[POST /simulate/wire_transfers<br>Simulate wire transfer<br>Parameters: bank_account_id, amount, beneficiary_details]
    Sim_RTP[POST /simulate/real_time_payments_transfers<br>Simulate realtime transfer<br>Parameters: bank_account_id, amount, destination_details]
    Sim_Card[POST /simulate/card_reversals<br>Simulate card reversal<br>Parameters: none]
  end

  %% Connect API node to each category for overall context
  API --> Auth
  API --> Accts
  API --> AN
  API --> Tx
  API --> Xfer
  API --> Cards
  API --> FilesDocs
  API --> Exp
  API --> BK
  API --> WH
  API --> Sim

