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
