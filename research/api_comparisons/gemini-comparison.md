API comparison of specs from Column, Galileo, Increase, Moov, Q2 Helix and Unit using Gemini 3 thinking.

1. Authentication & Security
Column:

Method: Basic Auth (API Key as username, empty password).

Key Parameters: Authorization: Basic <base64_key>

Capabilities: IP allowlisting, granular API keys.

Galileo:

Method: Custom Header / Basic Auth mix.

Key Parameters: apiLogin, apiTransKey, providerId often required in the request body or headers.

Capabilities: providerId identifies the program.

Increase:

Method: Bearer Token (OAuth or API Key).

Key Parameters: Authorization: Bearer <token>

Capabilities: Scoped API keys, Development/Production environment switching via base URL.

Moov:

Method: OAuth2 (Access Tokens).

Key Parameters: Authorization: Bearer <access_token>, X-Account-ID (for acting on behalf of connected accounts).

Capabilities: Scopes (e.g., /accounts.write), ping endpoint for health checks.

Helix (Q2):

Method: Basic Auth.

Key Parameters: Authorization: Basic <token> (base64 encoded).

Capabilities: Sandbox and Production servers separated.

Unit:

Method: Bearer Token (JWT).

Key Parameters: Authorization: Bearer <token>.

Capabilities: User vs Org level tokens, specific "Customer Tokens" for mobile SDKs.

Differences:

Architecture: Moov and Unit lean heavily into OAuth/JWT patterns suitable for marketplaces and platforms where the platform acts on behalf of a user. Galileo and Helix use legacy "service user" credentials (apiLogin/TransKey) often passed in the body or custom headers, reflecting an older architectural style compared to the standard HTTP Authorization headers used by Column and Increase.

Scoping: Moov offers granular OAuth scopes (e.g., profile.read), whereas Column and Increase rely more on API key permissions managed in a dashboard.

2. Identity & Onboarding (Entities/Customers)
Column:

Object: Entity

Endpoints: POST /entities/person, POST /entities/business, GET /entities/{id}

Key Parameters: first_name, last_name, ssn, dob, address (street, city, state, zip).

Features: Direct "Person" and "Business" distinct structures.

Galileo:

Object: Customer

Endpoints: POST /customer/create, POST /customer/update

Key Parameters: firstName, lastName, address1, city, state, postalCode, id (SSN), idType.

Features: Flat parameter structure.

Increase:

Object: Entity

Endpoints: POST /entities, GET /entities

Key Parameters: structure (corporation, natural_person), corporation object, natural_person object.

Features: Supplemental documents endpoint POST /entities/{id}/supplemental_documents.

Moov:

Object: Account (with Profile)

Endpoints: POST /accounts, PATCH /accounts/{id}

Key Parameters: accountType (individual/business), profile (individual/business details).

Features: "Capabilities" request model where you ask for specific features (e.g., transfers, card-issuing) and Moov triggers requirements.

Helix (Q2):

Object: Customer

Endpoints: POST /customer/create, GET /customer/get/{customerId}

Key Parameters: firstName, lastName, taxId.

Features: "Tag" based retrieval.

Unit:

Object: Application & Customer

Endpoints: POST /applications, POST /applications/{id}/documents, GET /customers

Key Parameters: type (individual/business), fullName, ssn, dateOfBirth, address.

Features: Application-first workflow. You create an "Application", upload documents, and Unit asynchronously approves it to create a "Customer".

Differences:

Workflow: Unit is unique in enforcing an "Application" lifecycle (Draft -> Pending -> Approved/Denied) for KYC, whereas others like Column and Increase allow direct Entity creation which may enter a pending state.

Data Model: Moov treats every participant as an "Account" (whether it's the platform or the end-user), whereas others distinguish between "Customers" (the end-users) and the Program/Platform.

KYC: Moov uses a "Capabilities" model where requirements are dynamic based on what the user wants to do (e.g., just collecting funds vs. issuing cards).

3. Accounts (Core Banking)
Column:

Object: BankAccount

Endpoints: POST /bank-accounts, GET /bank-accounts/{id}

Key Parameters: entity_id, description.

Features: Overdraft reserve accounts.

Galileo:

Object: Account

Endpoints: POST /account/create, POST /account/update

Key Parameters: productId, customerId.

Features: Accounts are heavily tied to "Products" defined in the backend configuration.

Increase:

Object: Account

Endpoints: POST /accounts, GET /accounts

Key Parameters: entity_id, program_id, currency.

Features: informational_entity_id for associating activity without ownership.

Moov:

Object: Wallet (Stored Value) & BankAccount (External)

Endpoints: POST /wallets (Create stored value), POST /accounts/{id}/bank-accounts (Link external).

Features: Distinction between "Wallets" (Moov-held funds) and "Bank Accounts" (External funding sources).

Helix (Q2):

Object: Account

Endpoints: POST /account/create

Key Parameters: productId, customerId.

Features: "Entitlements" endpoints to manage access.

Unit:

Object: Account (Deposit Account)

Endpoints: POST /accounts, POST /accounts/{id}/limits

Key Parameters: depositProduct, customer (relationship).

Features: Explicit "Deposit Product" selection (Checking, Savings).

Differences:

Model: Moov uses a "Wallet" concept for the stored balance, while linking external "Bank Accounts" as funding sources. The others (Column, Increase, Unit, Helix) act as the core ledger where the "Account" is the primary store of value.

Hierarchy: Helix and Galileo have strong concepts of "Product IDs" that dictate account behavior (fees, limits) at creation time. Increase and Column tend to be more flexible/API-driven with fewer pre-configured "Products".

4. Money Movement (Transfers & Payments)
Column:

Types: ACH, Wire, Book (Internal).

Endpoints: POST /transfers/ach, POST /transfers/wire, POST /transfers/book.

Key Params: amount, receiver_account_number_id, currency.

Galileo:

Types: Internal Transfer, ACH (via separate integration or specific endpoints).

Endpoints: POST /transfer/create, POST /createAccountTransfer.

Key Params: amount, sourceAccount, destinationAccount.

Increase:

Types: ACH, Wire, Check, Real-Time Payments (RTP), Account Transfer.

Endpoints: POST /ach_transfers, POST /wire_transfers, POST /check_transfers, POST /real_time_payments_transfers.

Key Params: source_account_number_id, destination_account_number, routing_number.

Features: "Interactive" transfers (approvals).

Moov:

Types: Generic "Transfer" (abstracts rail).

Endpoints: POST /transfers.

Key Params: source (payment-method-id), destination (payment-method-id), amount.

Features: Rail Agnostic. You specify source/destination, and Moov handles the rail (ACH/Card/RTP) logic or allows selection.

Helix (Q2):

Types: Transfer (Internal), Wire.

Endpoints: POST /transfer/create, POST /transfer/wire/create.

Key Params: receiverRoutingNumber, amount.

Unit:

Types: Payments (ACH/Book), Wires.

Endpoints: POST /payments, POST /payments/{id}/cancel.

Key Params: counterparty (inline or ID), direction (Credit/Debit).

Features: "Counterparty" object management is central to payments.

Differences:

Abstraction vs. Specificity: Moov abstracts the payment rail (you Create a Transfer between paymentMethod A and paymentMethod B). Increase and Column provide specific endpoints for each rail (/ach_transfers, /wire_transfers), giving the developer explicit control over the network used.

Counterparties: Unit and Moov heavily utilize "Counterparty" or "PaymentMethod" objects that must be created/tokenized before transacting. Column and Increase allow "inline" definitions (passing routing/account number directly in the transfer request).

5. Card Issuing
Column:

Endpoints: Not explicitly detailed in the extracted snippet (likely separate module or implicit in account).

Galileo:

Capabilities: Deep physical card issuing features (embossing, shipping).

Endpoints: POST /card/create, POST /card/reissue, POST /card/provision/applePay.

Features: "Digital First" issuance, specialized endpoints for Apple/Google Pay provisioning.

Increase:

Endpoints: POST /cards, GET /cards/{id}/details.

Features: digital_wallet object for provisioning, virtual cards.

Moov:

Endpoints: /accounts/{id}/cards (Link external), /issuing/... (Issue virtual).

Features: Linking external cards for acquiring vs. issuing new cards.

Helix (Q2):

Endpoints: POST /card/createDigital, POST /card/orderPhysical.

Features: Distinct endpoints for Digital vs Physical creation.

Unit:

Endpoints: POST /cards.

Features: Physical card printing/shipping built into the POST via shippingAddress and design attributes. Limits management via /cards/{id}/limits.

Differences:

Depth: Galileo offers the most granular control over physical card lifecycle (embossing, reissuing types, damage reasons).

Simplicity: Increase and Unit treat cards more like API resources with properties, handling the complex provisioning logic internally.

Provisioning: Galileo and Increase expose specific endpoints/data structures for push-provisioning to Apple/Google Pay wallets directly from the API response.

6. Simulation & Testing
Column:

Endpoints: /simulate/receive-ach-debit, /simulate/receive-wire.

Philosophy: Trigger inbound events to test webhook handlers.

Galileo:

Endpoints: POST /card/mock/... (e.g., falconFraud, withdrawal/cardCash).

Philosophy: Extensive mocking of card network messages (ISO 8583 simulations) to test processor logic.

Increase:

Endpoints: /simulations/... (e.g., inbound_ach_transfer, card_authorization).

Philosophy: First-class simulation API to force state changes and trigger inbound events in Sandbox.

Moov:

Features: Test mode toggles, specific test headers or magic values (often used in amount or description) to trigger specific outcomes.

Helix (Q2):

Endpoints: /card/mock/...

Philosophy: Similar to Galileo, focuses on mocking card transaction flows.

Unit:

Endpoints: /sandbox/atm-deposits, /sandbox/received-payments.

Philosophy: Dedicated sandbox endpoints to mimic external world actions (receiving money).

Differences:

Granularity: Increase and Unit provide the most modern "Simulation API" experience, allowing developers to programmatically trigger "incoming" money events. Galileo and Helix focus heavily on simulating the complex card network messages (Auth/Settlement/Reversal) which is critical for card processors.

7. Events & Webhooks
Column:

Endpoints: /events, /webhook-endpoints.

Features: List events, retry logic, signature verification.

Galileo:

Features: "Events API" (formerly Alerts). Webhook retry logic with exponential backoff parameters.

Increase:

Endpoints: /events, /event_subscriptions.

Features: First-class API to manage subscriptions. Events are immutable logs of state changes.

Moov:

Endpoints: Standard webhook management via Dashboard/API.

Unit:

Endpoints: /webhooks, /events.

Features: API tokens for webhook authentication.

Differences:

Management: Increase and Unit expose the Webhook configuration itself as an API resource (EventSubscription or Webhook), allowing programmatic setup of listeners. Galileo tends to rely on static configuration or "Product Parameters" for enabling specific event streams.

Summary of Architectural Distinctions
Legacy vs. Modern: Galileo and Helix represent "Processor-first" architectures (heavy configuration, specific endpoint-per-action, distinct physical/digital flows). Increase, Unit, and Column represent "API-first" architectures (RESTful resources, standardized auth, simulation APIs).

Money Movement: Moov is unique as a "Payment Orchestrator" (rail agnostic transfers), whereas the others act more as the "Bank" (holding the ledger and exposing specific rails like ACH/Wire).

Onboarding: Unit's "Application" model is distinctively asynchronous and compliance-heavy upfront. Column and Increase allow for more immediate Entity creation, shifting compliance checks to a background process or specific "Verification" status checks.