![Database-Schema](./database-schema.png)
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
