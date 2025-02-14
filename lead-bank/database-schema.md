erDiagram
    ENTITY {
      string id PK
      string type "person or business"
      string name
      string website
      string tax_identifier
      string registration_number
      string incorporation_state
      string industry_code
    }

    BANK_ACCOUNT {
      string id PK
      string entity_id FK
      string account_type
      datetime created_at
      string currency
      string default_account_number
      string routing_number
      string description
      string status
      string idempotency_key
    }

    ACCOUNT_NUMBER {
      string id PK
      string bank_account_id FK
      string number
      string routing_number
      string status
      string label
      datetime created_at
      string idempotency_key
    }

    LOAN {
      string id PK
      string bank_account_id FK
      decimal principal
      int term
      decimal interest_rate
      datetime start_date
      string collateral
      string status
      datetime created_at
      string idempotency_key
    }

    LOAN_DISBURSEMENT {
      string id PK
      string loan_id FK
      decimal amount
      datetime disbursement_date
      string method
      string status
      datetime created_at
    }

    LOAN_PAYMENT {
      string id PK
      string loan_id FK
      decimal amount
      datetime payment_date
      string payment_method
      string status
      datetime created_at
    }

    COUNTERPARTY {
      string id PK
      string name
      string type
      string contact_info
      string account_details
      datetime created_at
    }

    FINANCIAL_INSTITUTION {
      string id PK
      string name
      string identifier
      datetime created_at
    }

    ACH_TRANSFER {
      string id PK
      string bank_account_id FK
      decimal amount
      string account_number
      string routing_number
      datetime effective_date
      string status
      string submission_trace_number
      datetime created_at
      string idempotency_key
    }

    WIRE_TRANSFER {
      string id PK
      string bank_account_id FK
      decimal amount
      string beneficiary_account
      string beneficiary_routing
      string message_to_recipient
      datetime created_at
      string status
      string idempotency_key
    }

    REALTIME_TRANSFER {
      string id PK
      string bank_account_id FK
      decimal amount
      string destination_account_number
      string destination_routing_number
      string remittance_information
      datetime created_at
      string status
      string idempotency_key
    }

    CARD {
      string id PK
      string bank_account_id FK
      string description
      string card_type
      string last4
      int expiration_month
      int expiration_year
      string billing_address_line1
      string billing_address_line2
      string billing_city
      string billing_state
      string billing_postal_code
      datetime created_at
      string status
      string idempotency_key
    }

    CARD_PAYMENT {
      string id PK
      string card_id FK
      decimal amount
      datetime created_at
      string state
      string idempotency_key
    }

    CARD_DISPUTE {
      string id PK
      string card_id FK
      string disputed_transaction_id
      string explanation
      datetime created_at
      string status
      string idempotency_key
    }

    DOCUMENT {
      string id PK
      string associated_entity_id "Could refer to an entity, bank account, loan, etc."
      datetime created_at
      string file_id
      string category
      string description
      string type
      string idempotency_key
    }

    WEBHOOK {
      string id PK
      string callback_url
      string events
      datetime created_at
      string status
      string idempotency_key
    }

    EXPORT {
      string id PK
      datetime created_at
      string category
      string status
      string file_id
      string file_download_url
      string idempotency_key
      string type
    }

    BOOKKEEPING_ACCOUNT {
      string id PK
      string entity_id FK
      string name
      string compliance_category
      datetime created_at
      string idempotency_key
      string type
    }

    BOOKKEEPING_ENTRY_SET {
      string id PK
      string transaction_id
      datetime date
      datetime created_at
      string idempotency_key
      string type
    }

    BOOKKEEPING_ENTRY {
      string id PK
      string bookkeeping_account_id FK
      decimal amount
      string entry_set_id FK
      datetime created_at
      string type
    }

    OAUTH_CONNECTION {
      string id PK
      string group_id FK
      datetime created_at
      string status
      string deleted_at
      string type
    }

    GROUP {
      string id PK
      datetime created_at
      string activation_status
      string ach_debit_status
      string type
    }

    OAUTH_TOKEN {
      string access_token
      string token_type
      string type
    }

    INTRAFI_ACCOUNT_ENROLLMENT {
      string id PK
      string bank_account_id FK
      string status
      string intrafi_id
      datetime created_at
      string idempotency_key
      string type
    }

    INTRAFI_BALANCE {
      datetime effective_date
      decimal total_balance
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
      string idempotency_key
      string type
    }

    ACH_PRENOTIFICATION {
      string id PK
      string account_number
      string routing_number
      datetime created_at
      string status
      string addendum
      string company_descriptive_date
      string company_discretionary_data
      string company_entry_description
      string company_name
      string credit_debit_indicator
      string effective_date
      string idempotency_key
      string type
    }

    %% Relationships
    ENTITY ||--o{ BANK_ACCOUNT : "owns"
    BANK_ACCOUNT ||--o{ ACCOUNT_NUMBER : "has"
    BANK_ACCOUNT ||--o{ LOAN : "originates"
    LOAN ||--o{ LOAN_DISBURSEMENT : "disburses"
    LOAN ||--o{ LOAN_PAYMENT : "receives"
    BANK_ACCOUNT ||--o{ ACH_TRANSFER : "initiates"
    BANK_ACCOUNT ||--o{ WIRE_TRANSFER : "initiates"
    BANK_ACCOUNT ||--o{ REALTIME_TRANSFER : "initiates"
    BANK_ACCOUNT ||--o{ CARD : "issues"
    CARD ||--o{ CARD_PAYMENT : "processes"
    CARD ||--o{ CARD_DISPUTE : "has"
    ENTITY ||--o{ BOOKKEEPING_ACCOUNT : "has"
    BOOKKEEPING_ACCOUNT ||--o{ BOOKKEEPING_ENTRY_SET : "groups"
    BOOKKEEPING_ENTRY_SET ||--o{ BOOKKEEPING_ENTRY : "contains"
    GROUP ||--o{ OAUTH_CONNECTION : "has"
