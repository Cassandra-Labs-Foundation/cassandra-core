flowchart TD
    A[API Client: Start]
    B[Authenticate via OAuth 2.0 – Bearer Token over HTTPS]
    A --> B
    B --> C[Select Operation]

    %% Entity Operations
    C --> D[Entity Operations]
    D --> D1[Create Entity: POST /entities/person  
Params: first_name, last_name, ssn, dob, email, address: line1, city, state, postal_code, country_code, person_details, verification_tags]
    D1 --> D2{Entity Type?}
    D2 -- Person --> D3[POST /entities/person – Create a person entity  
Params: first_name, last_name, ssn, dob, email, address: line1, city, state, postal_code, country_code, person_details, verification_tags]
    D2 -- Business --> D4[POST /entities/business – Create a business entity  
Params: business_name, registration_number, contact_email, address: line1, city, state, postal_code, country_code, kyc_documents, verification_tags]
    D3 & D4 --> D5[GET /entities/#123;id#125; – Retrieve entity by ID]
    D5 --> D6[PATCH or DELETE /entities/#123;id#125; – Update or delete entity]

    %% Bank Account Operations
    C --> E[Bank Account Operations]
    E --> E1[POST /bank-accounts – Create bank account  
Params: entity_id, account_type, description, currency, default_account_number, routing_number]
    E1 --> E2[GET /bank-accounts/#123;id#125; – Retrieve bank account]
    E2 --> E3[GET /bank-accounts/#123;id#125;/balance – Get account balance]
    E --> E4[Manage Account Numbers]
    E4 --> E41[POST /account-numbers – Create account number  
Params: bank_account_id, number, routing_number, status, label]
    E41 --> E42[GET /account-numbers/#123;id#125; – Retrieve account number]

    %% Loan Operations
    C --> F[Loan Operations]
    F --> F1[POST /loans – Create loan  
Params: bank_account_id, principal, term, interest_rate, start_date, collateral]
    F1 --> F2[POST /loans/#123;id#125;/disbursements – Disburse loan  
Params: amount, method, disbursement_date]
    F --> F3[POST /loans/#123;id#125;/payments – Create loan payment  
Params: amount, payment_date, payment_method]
    F3 --> F4[GET /loans/#123;id#125;/all-payments – Payment history]

    %% Counterparty and IBAN
    C --> G[Counterparty and IBAN]
    G --> G1[POST /counterparties – Create counterparty  
Params: name, type, contact_info, account_details]
    G --> G2[POST /validate-iban – Validate IBAN  
Params: iban]
    G --> G3[GET /financial-institutions – Retrieve institution details]

    %% Transfer Operations
    C --> H[Transfer Operations]
    H --> H1[POST /transfers/ach – Initiate ACH transfer  
Params: bank_account_id, amount, account_number, routing_number, effective_date]
    H --> H2[POST /transfers/wire – Initiate wire transfer  
Params: bank_account_id, amount, beneficiary_account, beneficiary_routing, message]
    H --> H3[POST /transfers/realtime – Create realtime transfer  
Params: bank_account_id, amount, destination_account_number, destination_routing_number]
    H --> H4[GET /transfers/summary – Get transfer history]

    %% Card Operations
    C --> I[Card Operations]
    I --> I1[POST /cards – Issue new card  
Params: bank_account_id, description, card_type, expiration_month, expiration_year, billing_address: line1, line2, city, state, postal_code]
    I1 --> I2[GET /cards/#123;id#125; – Retrieve card details]
    I --> I3[GET /cards/#123;id#125;/payments – View card payment history]
    I --> I4[POST /cards/#123;id#125;/disputes – File card dispute  
Params: disputed_transaction_id, explanation]

    %% Documents and Reporting
    C --> J[Documents and Reporting]
    J --> J1[POST /documents – Upload document  
Params: file, document_type, description]
    J --> J2[GET /documents/#123;id#125; – Retrieve document]
    J --> J3[POST /reports – Generate report  
Params: report_type, date_range, bank_account_id]
    J3 --> J4[GET /reports/#123;id#125; – Retrieve report details]

    %% Webhooks
    C --> K[Webhooks]
    K --> K1[POST /webhooks – Register webhook endpoint  
Params: callback_url, events, secret]
    K --> K2[GET /webhook-events – List webhook events]

    %% Simulation (Sandbox Only)
    C --> L[Simulation Sandbox]
    L --> L1[POST /simulate/ach-credit – Simulate ACH credit  
Params: bank_account_id, amount, effective_date]
    L --> L2[POST /simulate/wire – Simulate wire transfer  
Params: bank_account_id, amount, beneficiary_details]
    L --> L3[POST /simulate/realtime – Simulate realtime transfer  
Params: bank_account_id, amount, destination_details]
    L --> L4[POST /simulate/card-reversal – Simulate card reversal  
Params: card_payment_id]

    %% End Flow
    J4 --> M[Reconciliation and Reporting]
    K2 --> M
    L4 --> M
