API comparison of specs from Column, Galileo, Increase, Moov, Q2 Helix and Unit using Claude Opus 4.1

# Banking-as-a-Service API Design Comparison

## Authentication/Authorization

**Unit:**
- Authentication: Bearer token authentication
- Headers: Authorization Bearer token required
- Scopes: Not explicitly defined in spec

**Increase:**
- Authentication: API key-based authentication
- Headers: Authorization with API key
- Environment: Sandbox and production environments

**Q2 Helix:**
- Authentication: OAuth 2.0 and API key
- Headers: Authorization token required
- Multi-tenant: Program-level authentication

**Moov:**
- Authentication: OAuth 2.0 flow
- Endpoints: `/oauth2/token`, `/oauth2/authorize`
- Scopes: Granular permission scopes

**Column:**
- Authentication: API key-based
- Headers: X-API-Key header
- Environment: Test and production modes

**Galileo:**
- Authentication: Custom authentication scheme
- Headers: API credentials required
- Session management: Session-based authentication

**Differences:** Moov uses full OAuth 2.0 with explicit authorization flows, while Unit, Increase, and Column use simpler bearer/API key approaches. Q2 Helix supports both OAuth and API keys for flexibility. Galileo uses a more traditional session-based approach typical of older banking systems.

## Core Customer Management

**Unit:**
- Endpoints:
  - GET /customers - List customers
  - GET /customers/{customerId} - Get customer
  - POST /customers - Create customer
  - PATCH /customers/{customerId} - Update customer
  - POST /customers/{customerId}/archive - Archive customer
  - GET /customers/{customerId}/authorized-users - Get authorized users
- Key parameters: Customer type (individual/business), EIN, SSN, address, phone, email
- Special features: Authorized users, customer tags, JWT subject for authentication

**Increase:**
- Endpoints:
  - GET /entities - List entities
  - GET /entities/{entity_id} - Get entity
  - POST /entities - Create entity
  - POST /entities/{entity_id}/archive - Archive entity
  - GET /entities/{entity_id}/beneficial_owners - List beneficial owners
  - POST /entities/{entity_id}/confirm - Confirm entity
  - POST /entities/{entity_id}/update_address - Update address
- Key parameters: Entity type (corporation/individual/trust), EIN, structure, address
- Special features: Beneficial ownership tracking, supplemental documents, entity confirmation workflow

**Q2 Helix:**
- Endpoints:
  - GET /customer/{customerId} - Get customer
  - POST /customer - Create customer  
  - PATCH /customer/{customerId} - Update customer
  - POST /customer/{customerId}/archive - Archive customer
  - GET /customer/{customerId}/relationships - Get relationships
  - POST /customerRelationship - Create relationship
- Key parameters: Customer type, KYC status, risk rating
- Special features: Customer relationships, risk rating, multi-product support

**Moov:**
- Endpoints:
  - GET /accounts - List accounts
  - GET /accounts/{accountID} - Get account
  - POST /accounts - Create account
  - PATCH /accounts/{accountID} - Update account
  - DELETE /accounts/{accountID} - Delete account
  - POST /accounts/{accountID}/business-classification - Set business classification
  - GET /accounts/{accountID}/countries - Get allowed countries
- Key parameters: Account type (individual/business), capabilities, terms of service acceptance
- Special features: Business classification, country restrictions, capability management

**Column:**
- Endpoints:
  - GET /entities - List entities
  - GET /entities/{entity_id} - Get entity
  - POST /entities - Create entity
  - PATCH /entities/{entity_id} - Update entity
  - DELETE /entities/{entity_id} - Delete entity
  - GET /entities/{entity_id}/documents - List documents
  - POST /entities/{entity_id}/documents - Upload document
- Key parameters: Entity type, personal/business details, compliance status
- Special features: Document management integrated, compliance workflow

**Galileo:**
- Complex customer management with numerous specific endpoints for different operations
- Separate endpoints for personal info, addresses, identification, etc.
- Program-based customer creation

**Differences:** Unit and Q2 use "customers" terminology while Increase and Column use "entities" and Moov uses "accounts" for the same concept. Increase has the most sophisticated beneficial ownership tracking. Moov integrates business classification and capabilities directly into the account model. Column tightly integrates document management. Unit provides authorized users as a built-in feature while others handle this through relationships or separate endpoints.

## Account Management

**Unit:**
- Endpoints:
  - GET /accounts - List accounts
  - GET /accounts/{accountId} - Get account
  - POST /accounts - Create account
  - PATCH /accounts/{accountId} - Update account
  - POST /accounts/{accountId}/close - Close account
  - POST /accounts/{accountId}/reopen - Reopen account
  - POST /accounts/{accountId}/freeze - Freeze account
  - POST /accounts/{accountId}/unfreeze - Unfreeze account
  - GET /accounts/{accountId}/limits - Get limits
  - POST /accounts/{accountId}/enter-daca - Enter DACA
  - POST /accounts/{accountId}/activate-daca - Activate DACA
  - POST /accounts/{accountId}/deactivate-daca - Deactivate DACA
  - GET /account-end-of-day - Get balance history
  - GET /accounts/{accountId}/repayment-information - Get repayment info
- Key parameters: Account type (deposit/credit), currency, deposit products, limits
- Special features: DACA support, balance history, credit account repayment info

**Increase:**
- Endpoints:
  - GET /accounts - List accounts
  - GET /accounts/{account_id} - Get account
  - POST /accounts - Create account
  - PATCH /accounts/{account_id} - Update account
  - POST /accounts/{account_id}/close - Close account
  - GET /accounts/{account_id}/balance - Get balance
  - GET /account_numbers - List account numbers
  - POST /account_numbers - Create account number
  - PATCH /account_numbers/{account_number_id} - Update account number
- Key parameters: Account name, entity_id, program_id, status
- Special features: Separate account numbers management, inbound ACH handling, check deposit instructions

**Q2 Helix:**
- Endpoints:
  - GET /account/{accountId} - Get account
  - POST /account - Create account
  - PATCH /account/{accountId} - Update account
  - POST /account/{accountId}/close - Close account
  - POST /account/{accountId}/freeze - Freeze account
  - POST /account/{accountId}/unfreeze - Unfreeze account
  - GET /account/{accountId}/balance - Get balance
  - GET /account/{accountId}/limits - Get limits
  - POST /account/{accountId}/limits - Set limits
- Key parameters: Product type, interest rates, overdraft settings
- Special features: Product-based accounts, interest configuration, overdraft management

**Moov:**
- Endpoints:
  - GET /accounts/{accountID}/bank-accounts - List bank accounts
  - POST /accounts/{accountID}/bank-accounts - Add bank account
  - GET /accounts/{accountID}/bank-accounts/{bankAccountID} - Get bank account
  - DELETE /accounts/{accountID}/bank-accounts/{bankAccountID} - Remove bank account
  - POST /accounts/{accountID}/bank-accounts/{bankAccountID}/micro-deposits - Initiate micro-deposits
- Key parameters: Routing number, account number, account type
- Special features: Micro-deposit verification, external bank account linking

**Column:**
- Endpoints:
  - GET /bank-accounts - List bank accounts
  - GET /bank-accounts/{bank_account_id} - Get bank account
  - POST /bank-accounts - Create bank account
  - PATCH /bank-accounts/{bank_account_id} - Update bank account
  - POST /bank-accounts/{bank_account_id}/close - Close account
  - GET /account-numbers - List account numbers
  - POST /account-numbers - Create account number
  - PATCH /account-numbers/{account_number_id} - Update account number
- Key parameters: Account type, routing numbers, ACH settings
- Special features: Multiple routing numbers, ACH positive pay rules

**Galileo:**
- Extensive account management with specialized endpoints
- Separate endpoints for different account operations
- Program and product-based account creation

**Differences:** Unit has built-in DACA agreement support which others lack. Increase and Column separate account numbers from accounts as distinct resources, allowing multiple account numbers per account. Q2 focuses on product-based accounts with interest and overdraft features. Moov is primarily focused on external account connections rather than managing internal accounts. Column provides ACH positive pay rules as a security feature unique among these providers.

## Payment Operations

**Unit:**
- Endpoints:
  - GET /payments - List payments
  - GET /payments/{paymentId} - Get payment
  - POST /payments - Create payment
  - PATCH /payments/{paymentId} - Update payment
  - POST /payments/{paymentId}/cancel - Cancel payment
  - GET /recurring-payments - List recurring payments
  - POST /recurring-payments - Create recurring payment
  - POST /recurring-payments/{paymentId}/disable - Disable recurring
  - POST /recurring-payments/{paymentId}/enable - Enable recurring
  - GET /received-payments - List received payments
  - POST /received-payments/{paymentId}/advance - Advance received payment
  - POST /received-payments/{paymentId}/reprocess - Reprocess payment
  - POST /returns/{transactionId} - Return ACH transaction
- Key parameters: Payment type (ACH/book/wire), amount, description, counterparty
- Special features: Recurring payments, payment advancing, ACH returns

**Increase:**
- Endpoints:
  - GET /ach_transfers - List ACH transfers
  - POST /ach_transfers - Create ACH transfer
  - GET /ach_transfers/{ach_transfer_id} - Get ACH transfer
  - POST /ach_transfers/{ach_transfer_id}/approve - Approve ACH
  - POST /ach_transfers/{ach_transfer_id}/cancel - Cancel ACH
  - GET /wire_transfers - List wire transfers
  - POST /wire_transfers - Create wire transfer
  - GET /wire_transfers/{wire_transfer_id} - Get wire transfer
  - POST /wire_transfers/{wire_transfer_id}/approve - Approve wire
  - POST /wire_transfers/{wire_transfer_id}/cancel - Cancel wire
  - POST /ach_prenotifications - Create ACH prenotification
  - GET /real_time_payments_transfers - List RTP transfers
  - POST /real_time_payments_transfers - Create RTP transfer
- Key parameters: Transfer type, account_id, amount, statement_descriptor, approval required
- Special features: ACH prenotifications, Real-Time Payments support, approval workflows

**Q2 Helix:**
- Endpoints:
  - GET /transfer - List transfers
  - GET /transfer/{transferId} - Get transfer
  - POST /transfer - Create transfer
  - POST /transfer/{transferId}/cancel - Cancel transfer
  - GET /transaction - List transactions
  - GET /transaction/{transactionId} - Get transaction
  - POST /externalAccount - Create external account
  - GET /externalAccount/{externalAccountId} - Get external account
  - POST /externalAccount/{externalAccountId}/verify - Verify external account
- Key parameters: Transfer type, from/to accounts, amount, scheduled date
- Special features: External account verification, scheduled transfers

**Moov:**
- Endpoints:
  - GET /transfers - List transfers
  - POST /transfers - Create transfer
  - GET /transfers/{transferID} - Get transfer
  - PATCH /transfers/{transferID} - Update transfer
  - POST /transfers/{transferID}/refunds - Create refund
  - GET /transfer-options - Get transfer options
  - POST /payment-methods - Create payment method
  - GET /payment-methods/{paymentMethodID} - Get payment method
- Key parameters: Source, destination, amount, payment method type
- Special features: Transfer options analysis, refund management, payment method abstraction

**Column:**
- Endpoints:
  - GET /transfers - List transfers
  - GET /transfers/{transfer_id} - Get transfer
  - POST /transfers/ach - Create ACH transfer
  - POST /transfers/wire - Create wire transfer
  - POST /transfers/book - Create book transfer
  - POST /transfers/check - Create check
  - POST /transfers/{transfer_id}/cancel - Cancel transfer
  - POST /transfers/{transfer_id}/reverse - Reverse transfer
  - GET /ach-positive-pay-rules - List ACH rules
  - POST /ach-positive-pay-rules - Create ACH rule
- Key parameters: Transfer type, direction, amount, counterparty details
- Special features: Check creation, ACH positive pay rules, transfer reversal

**Galileo:**
- Various payment and transfer endpoints
- Separate endpoints for different payment types
- Complex fee and settlement management

**Differences:** Increase offers the most payment rails including Real-Time Payments. Unit has built-in recurring payment support while others would require external scheduling. Column uniquely offers check creation alongside electronic payments. Increase and Column have approval workflows for payments. Moov abstracts payment methods and provides transfer options analysis. Column and Increase support ACH prenotifications for account verification.

## Card Management

**Unit:**
- Endpoints:
  - GET /cards - List cards
  - GET /cards/{cardId} - Get card
  - POST /cards - Create card
  - PATCH /cards/{cardId} - Update card
  - POST /cards/{cardId}/close - Close card
  - POST /cards/{cardId}/freeze - Freeze card
  - POST /cards/{cardId}/unfreeze - Unfreeze card
  - POST /cards/{cardId}/report-stolen - Report stolen
  - POST /cards/{cardId}/report-lost - Report lost
  - POST /cards/{cardId}/replace - Replace card
  - GET /cards/{cardId}/limits - Get limits
  - PATCH /cards/{cardId}/limits - Update limits
  - GET /cards/{cardId}/secure-data/pin/status - Get PIN status
- Key parameters: Card type (physical/virtual), shipping address, limits, design
- Special features: Card replacement workflow, PIN status management, custom designs

**Increase:**
- Endpoints:
  - GET /cards - List cards
  - POST /cards - Create card
  - GET /cards/{card_id} - Get card
  - PATCH /cards/{card_id} - Update card
  - GET /card_details - Get card details (PAN, CVV)
  - GET /digital_card_profiles - List digital profiles
  - POST /digital_card_profiles - Create digital profile
  - POST /digital_card_profiles/{id}/clone - Clone profile
  - POST /digital_card_profiles/{id}/archive - Archive profile
  - GET /digital_wallet_tokens - List wallet tokens
  - GET /card_push_transfers - List card push transfers
  - POST /simulations/card_authorizations - Simulate authorization
- Key parameters: Card status, spending limits, digital wallet enablement
- Special features: Digital card profiles, wallet tokenization, card push transfers, authorization simulation

**Q2 Helix:**
- Endpoints:
  - GET /card - List cards
  - GET /card/{cardId} - Get card
  - POST /card - Create card
  - POST /card/{cardId}/activate - Activate card
  - POST /card/{cardId}/freeze - Freeze card
  - POST /card/{cardId}/unfreeze - Unfreeze card
  - POST /card/{cardId}/close - Close card
  - POST /card/{cardId}/reissue - Reissue card
  - GET /cardControl - List card controls
  - POST /cardControl - Create card control
  - PATCH /cardControl/{controlId} - Update card control
- Key parameters: Card product, PIN, activation status, controls
- Special features: Granular card controls, PIN management, card products

**Moov:**
- Endpoints:
  - GET /issuing/cards - List cards
  - POST /issuing/cards - Create card
  - GET /issuing/cards/{cardID} - Get card
  - PATCH /issuing/cards/{cardID} - Update card
  - POST /issuing/cards/{cardID}/controls - Set controls
  - GET /issuing/cards/{cardID}/controls - Get controls
- Key parameters: Card type, controls, spending limits
- Special features: Issuing controls, commercial card features

**Column:**
- No card management endpoints (focused on ACH/wire/check operations)

**Galileo:**
- Extensive card management functionality
- Virtual and physical card support
- Card controls and limits

**Differences:** Increase has the most sophisticated digital wallet integration with profiles and tokenization. Q2 offers granular card controls as a separate resource. Unit provides card design customization. Increase includes card push transfers for disbursements. Column doesn't offer card services, focusing on traditional banking operations. Moov's card features are under an "issuing" namespace suggesting white-label card programs.

## Transaction & Authorization Management

**Unit:**
- Endpoints:
  - GET /transactions - List transactions
  - GET /transactions/{transactionId} - Get transaction
  - GET /authorizations - List authorizations
  - GET /authorizations/{authorizationId} - Get authorization
  - GET /authorization-requests - List authorization requests
  - GET /authorization-requests/{authorizationId} - Get request
  - POST /authorization-requests/{authorizationId}/approve - Approve
  - POST /authorization-requests/{authorizationId}/decline - Decline
- Key parameters: Transaction type, amount, status, tags
- Special features: Real-time authorization decisions, authorization request handling

**Increase:**
- Endpoints:
  - GET /transactions - List transactions
  - GET /transactions/{transaction_id} - Get transaction
  - GET /pending_transactions - List pending
  - GET /declined_transactions - List declined
  - GET /card_payments - List card payments
  - GET /card_payments/{card_payment_id} - Get card payment
  - POST /simulations/card_authorizations - Simulate authorization
  - POST /simulations/card_settlements - Simulate settlement
  - POST /simulations/card_refunds - Simulate refund
- Key parameters: Transaction status, route type, source
- Special features: Separate declined transaction tracking, extensive simulation capabilities

**Q2 Helix:**
- Endpoints:
  - GET /transaction - List transactions
  - GET /transaction/{transactionId} - Get transaction
  - POST /transaction - Create transaction
  - POST /transaction/{transactionId}/reverse - Reverse transaction
  - GET /transaction/pending - List pending
  - POST /transaction/{transactionId}/settle - Settle transaction
- Key parameters: Transaction type, status, amount, merchant info
- Special features: Manual transaction creation, reversal capability, settlement control

**Moov:**
- Endpoints:
  - GET /accounts/{accountID}/transactions - List transactions
  - GET /transfers/{transferID}/events - Get transfer events
  - GET /receipts/{receiptID} - Get receipt
  - POST /receipts - Create receipt
- Key parameters: Transaction status, transfer events
- Special features: Receipt generation, event tracking for transfers

**Column:**
- Endpoints:
  - GET /transfers - List transfers (includes all transaction types)
  - GET /transfers/{transfer_id} - Get transfer
  - GET /history/bank-accounts/{id} - Get account history
  - POST /transfers/{transfer_id}/reverse - Reverse transfer
- Key parameters: Transfer status, type, amount
- Special features: Unified transfer model for all transactions, reversal support

**Galileo:**
- Complex transaction management
- Various transaction types and statuses
- Authorization and settlement processes

**Differences:** Unit separates authorization requests that need approval from regular authorizations. Increase provides the most comprehensive simulation capabilities and tracks declined transactions separately. Q2 allows manual transaction creation and settlement control. Column uses a unified "transfer" model for all transaction types. Moov focuses on receipts and event tracking rather than traditional transaction records.

## Compliance & KYC

**Unit:**
- Endpoints:
  - GET /applications - List applications
  - GET /applications/{applicationId} - Get application
  - POST /applications - Create application
  - POST /applications/{applicationId}/cancel - Cancel application
  - GET /applications/{applicationId}/documents - List documents
  - POST /applications/{applicationId}/documents/{documentId}/multipart - Upload document
  - POST /applications/{applicationId}/documents/{documentId}/verify - Verify document
  - GET /application-forms - List application forms
  - POST /application-forms - Create application form
- Key parameters: Application type, status, documents, verification
- Special features: Application forms, document verification workflow, multi-part uploads

**Increase:**
- Endpoints:
  - GET /entities/{entity_id}/beneficial_owners - List beneficial owners
  - POST /entities/{entity_id}/beneficial_owners - Create beneficial owner
  - POST /entities/{entity_id}/confirm - Confirm entity
  - GET /entities/{entity_id}/supplemental_documents - List documents
  - POST /supplemental_documents - Create document
  - GET /proofs_of_authorization_requests - List POA requests
  - POST /proofs_of_authorization_requests/{id}/submit - Submit POA
- Key parameters: Beneficial ownership percentage, document type, verification status
- Special features: Beneficial ownership tracking, proof of authorization workflow, supplemental documents

**Q2 Helix:**
- Endpoints:
  - GET /customerDocument - List documents
  - GET /customerDocument/{documentId} - Get document
  - POST /customerDocument - Upload document
  - POST /customer/{customerId}/verify - Verify customer
  - GET /customer/{customerId}/kyc - Get KYC status
  - POST /customer/{customerId}/kyc - Update KYC
- Key parameters: Document type, KYC status, verification level
- Special features: KYC status management, customer verification workflow

**Moov:**
- Endpoints:
  - POST /accounts/{accountID}/identity-verification - Start verification
  - GET /accounts/{accountID}/documents - List documents
  - POST /accounts/{accountID}/documents - Upload document
  - GET /onboarding-invites - List invites
  - POST /onboarding-invites - Create invite
- Key parameters: Verification status, document type, capabilities
- Special features: Onboarding invites, capability-based verification

**Column:**
- Endpoints:
  - GET /entities/{entity_id}/documents - List documents
  - POST /entities/{entity_id}/documents - Upload document
  - GET /documents/{document_id} - Get document
  - POST /entities/{entity_id}/verify - Verify entity
- Key parameters: Document type, verification status
- Special features: Integrated document management with entities

**Galileo:**
- Customer identification and verification endpoints
- Document management
- Compliance reporting

**Differences:** Unit uses an application model separate from customers. Increase has the most sophisticated beneficial ownership tracking and proof of authorization workflows. Moov uses capability-based verification tied to account features. Q2 provides explicit KYC status management. Column integrates document management directly with entities.

## Webhook & Event Management

**Unit:**
- Endpoints:
  - GET /events - List events
  - GET /events/{eventId} - Get event
  - GET /webhooks - List webhook subscriptions
  - POST /webhooks - Create webhook subscription
  - POST /webhooks/{webhookId}/verify - Verify webhook
- Key parameters: Event type, webhook URL, secret
- Special features: Webhook verification, event replay

**Increase:**
- Endpoints:
  - GET /events - List events
  - GET /events/{event_id} - Get event
  - GET /event_subscriptions - List subscriptions
  - POST /event_subscriptions - Create subscription
  - PATCH /event_subscriptions/{id} - Update subscription
  - DELETE /event_subscriptions/{id} - Delete subscription
- Key parameters: Event category, subscription URL, status
- Special features: Event categories, subscription management

**Q2 Helix:**
- Endpoints:
  - GET /events - List events
  - GET /events/{eventId} - Get event
  - POST /webhook - Register webhook
  - DELETE /webhook/{webhookId} - Delete webhook
- Key parameters: Event type, webhook URL
- Special features: Simple webhook registration

**Moov:**
- Endpoints:
  - GET /webhooks - List webhooks
  - POST /webhooks - Create webhook
  - GET /webhooks/{webhookID} - Get webhook
  - PUT /webhooks/{webhookID} - Update webhook
  - DELETE /webhooks/{webhookID} - Delete webhook
  - GET /webhooks/{webhookID}/test - Test webhook
- Key parameters: Webhook URL, events to subscribe
- Special features: Webhook testing endpoint

**Column:**
- Endpoints:
  - GET /events - List events
  - GET /webhook-endpoints - List endpoints
  - POST /webhook-endpoints - Create endpoint
  - PATCH /webhook-endpoints/{id} - Update endpoint
  - DELETE /webhook-endpoints/{id} - Delete endpoint
  - GET /webhook-deliveries - List deliveries
  - POST /webhook-deliveries/{id}/retry - Retry delivery
- Key parameters: Endpoint URL, event types, delivery status
- Special features: Delivery tracking and retry mechanism

**Galileo:**
- Event notification system
- Webhook configuration
- Event types and filters

**Differences:** Column provides the most sophisticated webhook delivery tracking with retry capabilities. Moov includes a webhook testing endpoint. Unit offers webhook verification. Increase uses event categories for organization. Column tracks individual webhook deliveries as separate resources.

## Reporting & Statements

**Unit:**
- Endpoints:
  - GET /statements - List statements
  - GET /statements/{statementId}/html - Get HTML statement
  - GET /statements/{statementId}/pdf - Get PDF statement
  - GET /statements/{accountId}/bank/pdf - Get bank statement
  - GET /account-end-of-day - Get end-of-day balances
- Key parameters: Account ID, period, format
- Special features: Multiple format support (HTML/PDF), bank statements

**Increase:**
- Endpoints:
  - GET /account_statements - List statements
  - GET /account_statements/{id} - Get statement
  - GET /files - List files
  - GET /files/{file_id} - Get file
  - POST /exports - Create export
  - GET /exports/{export_id} - Get export
- Key parameters: Account ID, created_at date range
- Special features: Generic file management, data export functionality

**Q2 Helix:**
- Endpoints:
  - GET /statement - List statements
  - GET /statement/{statementId} - Get statement
  - POST /statement - Generate statement
  - GET /bankDocument - List bank documents
  - GET /bankDocument/{documentId} - Get document
- Key parameters: Account ID, statement period, document type
- Special features: On-demand statement generation, bank document management

**Moov:**
- Endpoints:
  - GET /accounts/{accountID}/statement.pdf - Get PDF statement
  - GET /accounts/{accountID}/transactions.csv - Export transactions
- Key parameters: Date range, format
- Special features: Direct PDF and CSV endpoints

**Column:**
- Endpoints:
  - GET /reporting/statements - List statements
  - GET /reporting/statements/{id} - Get statement
  - POST /reporting/statements - Generate statement
  - GET /history/bank-accounts/{id} - Get account history
  - POST /preview-pdf - Preview PDF document
- Key parameters: Account, date range, format
- Special features: PDF preview capability, account history separate from statements

**Galileo:**
- Statement generation and retrieval
- Various report types
- Transaction exports

**Differences:** Unit provides multiple statement formats including HTML. Increase has generic file management and export capabilities beyond just statements. Q2 and Column allow on-demand statement generation. Moov uses direct file format endpoints. Column includes PDF preview functionality.

## Fee Management

**Unit:**
- Endpoints:
  - POST /fees - Create fee
  - POST /fees/reverse - Reverse fee
- Key parameters: Account, amount, description
- Special features: Fee reversal capability

**Increase:**
- Endpoints:
  - No dedicated fee endpoints (fees handled as transactions)
- Special features: Fees appear as transaction records

**Q2 Helix:**
- Endpoints:
  - GET /fee - List fees
  - GET /fee/{feeId} - Get fee
  - POST /fee - Create fee
  - POST /fee/{feeId}/waive - Waive fee
- Key parameters: Fee type, amount, account
- Special features: Fee waiving capability

**Moov:**
- Endpoints:
  - No explicit fee management (handled in transfer pricing)
- Special features: Fees included in transfer costs

**Column:**
- Endpoints:
  - Fees handled as transfer types
- Special features: Fees are transfers with specific types

**Galileo:**
- Comprehensive fee management
- Fee schedules and configurations
- Automated fee assessment

**Differences:** Unit and Q2 have explicit fee management endpoints with Q2 adding fee waiving. Increase, Moov, and Column handle fees as part of their transaction/transfer models. Unit uniquely offers fee reversal as a dedicated endpoint.

## Simulation & Testing

**Unit:**
- Endpoints:
  - POST /sandbox/... - Various sandbox simulation endpoints
- Special features: Sandbox-specific endpoints for testing

**Increase:**
- Endpoints:
  - POST /simulations/card_authorizations - Simulate card auth
  - POST /simulations/card_settlements - Simulate settlement
  - POST /simulations/card_refunds - Simulate refund
  - POST /simulations/ach_transfers - Simulate ACH
  - POST /simulations/wire_transfers - Simulate wire
  - POST /simulations/check_deposits - Simulate check deposit
  - POST /simulations/inbound_ach_transfers - Simulate inbound ACH
  - POST /simulations/inbound_wire_transfers - Simulate inbound wire
- Key parameters: Amount, account, status to simulate
- Special features: Comprehensive simulation suite for all payment types

**Q2 Helix:**
- No explicit simulation endpoints in spec

**Moov:**
- No explicit simulation endpoints in spec

**Column:**
- Endpoints:
  - POST /simulate/ach - Simulate ACH transfer
  - POST /simulate/wire - Simulate wire transfer
  - POST /simulate/check - Simulate check
- Key parameters: Transfer details, desired outcome
- Special features: Simulation for major transfer types

**Galileo:**
- Test environment capabilities
- Transaction simulation features

**Differences:** Increase has the most comprehensive simulation capabilities covering all payment types and card operations. Column provides simulation for core transfer types. Unit uses sandbox-specific endpoints. Q2 and Moov don't expose simulation in their main API specs.

## Lending & Credit Features

**Unit:**
- Endpoints:
  - GET /accounts/{accountId}/repayment-information - Get repayment info
  - Credit accounts supported through account types
- Special features: Credit account support with repayment information

**Increase:**
- No explicit lending endpoints (focus on deposit accounts)

**Q2 Helix:**
- Endpoints:
  - Lending features through account products
  - Interest rate configuration on accounts
- Special features: Product-based lending configuration

**Moov:**
- No lending-specific endpoints

**Column:**
- Endpoints:
  - GET /loans - List loans
  - GET /loans/{loan_id} - Get loan
  - POST /loans - Create loan
  - PATCH /loans/{loan_id} - Update loan
  - POST /loans/{loan_id}/payments - Make payment
  - GET /loans/{loan_id}/schedule - Get payment schedule
- Key parameters: Principal, interest rate, term, payment schedule
- Special features: Full loan lifecycle management, payment scheduling

**Galileo:**
- Credit and loan management features
- Payment scheduling
- Interest calculation

**Differences:** Column has the most complete lending platform with dedicated loan objects and payment scheduling. Unit supports credit accounts but treats them as a type of account. Q2 handles lending through product configuration. Increase and Moov don't have lending features in their core APIs.

## Check & Cash Operations

**Unit:**
- Endpoints:
  - GET /check-deposits - List check deposits
  - GET /check-deposits/{checkDepositId} - Get check deposit
  - POST /check-deposits - Create check deposit
  - POST /check-deposits/{checkDepositId}/confirm - Confirm deposit
  - GET /check-payments - List check payments
  - POST /check-payments - Create check payment
  - POST /check-payments/{paymentId}/cancel - Cancel check
  - GET /cash-deposits/barcodes - Generate barcode
  - GET /store-locations - Find cash deposit locations
- Key parameters: Check images, amount, barcode generation
- Special features: Cash deposit via barcode at retail locations, mobile check deposit

**Increase:**
- Endpoints:
  - GET /check_deposits - List check deposits
  - POST /check_deposits - Create check deposit
  - GET /check_deposits/{id} - Get check deposit
  - GET /check_transfers - List check transfers
  - POST /check_transfers - Create check transfer
  - POST /check_transfers/{id}/approve - Approve check
  - POST /check_transfers/{id}/cancel - Cancel check
  - POST /check_transfers/{id}/stop_payment - Stop payment
  - POST /simulations/check_deposits - Simulate deposit
- Key parameters: Check images, MICR, amount, mail delivery
- Special features: Physical check mailing, stop payment, approval workflow

**Q2 Helix:**
- No check-specific endpoints in spec

**Moov:**
- No check operations

**Column:**
- Endpoints:
  - POST /transfers/check - Create check
  - Check operations handled as transfer type
- Key parameters: Payee, amount, memo
- Special features: Check creation as transfer type

**Galileo:**
- Check processing capabilities
- Check image capture
- Check verification

**Differences:** Unit supports both check deposits and payments plus unique cash deposit barcodes for retail locations. Increase offers physical check mailing and stop payment. Column treats checks as a transfer type. Q2 and Moov don't support check operations in their APIs.

## International & FX

**Unit:**
- Limited international support (domestic focus)

**Increase:**
- Endpoints:
  - Support for international wires
  - GET /routing_numbers - Validate routing numbers
- Special features: International wire support

**Q2 Helix:**
- No explicit international endpoints

**Moov:**
- Endpoints:
  - GET /accounts/{accountID}/countries - Get allowed countries
  - Support for international transfers
- Special features: Country restrictions per account

**Column:**
- Endpoints:
  - GET /iban/validate - Validate IBAN
  - GET /institutions - Institution lookup including international
- Special features: IBAN validation for international transfers

**Galileo:**
- Multi-currency support
- International transfer capabilities

**Differences:** Moov has country-level restrictions on accounts. Column provides IBAN validation. Increase supports international wires. Most providers are primarily domestic-focused with limited international capabilities.

## Rate & Market Data

**Unit:**
- No market data endpoints

**Increase:**
- No market data endpoints

**Q2 Helix:**
- Interest rate configuration on products

**Moov:**
- No market data endpoints

**Column:**
- Endpoints:
  - GET /market-rates - Get market rates
  - GET /market-rates/{rate_type} - Get specific rate
- Key parameters: Rate type (SOFR, Fed Funds, etc.)
- Special features: Real-time market rate data

**Galileo:**
- No explicit market data endpoints

**Differences:** Column uniquely provides market rate data access, useful for variable rate products. Q2 has interest configuration but not market data. Others don't expose rate information through their APIs.

## Summary of Key Design Decisions

### Architectural Patterns

1. **Resource Naming**: "Customers" (Unit, Q2) vs "Entities" (Increase, Column) vs "Accounts" (Moov)
2. **Transaction Model**: Unified "transfers" (Column) vs separate payment types (Unit, Increase)
3. **Approval Workflows**: Built-in (Increase) vs external (Unit, Moov)
4. **Document Management**: Integrated (Column) vs separate (Unit, Increase)

### Unique Capabilities by Provider

**Unit:**
- DACA agreement management
- Cash deposits at retail locations
- Recurring payment native support
- Authorized users built-in

**Increase:**
- Most comprehensive simulation suite
- Beneficial ownership tracking
- Real-Time Payments support
- Physical check mailing

**Q2 Helix:**
- Product-based account model
- Granular card controls
- Interest and overdraft management
- Multi-tenant program support

**Moov:**
- OAuth 2.0 authentication
- Transfer options analysis
- Capability-based permissions
- Focus on account connectivity

**Column:**
- Full loan lifecycle management
- ACH positive pay rules
- Market rate data access
- Webhook delivery tracking

**Galileo:**
- Most extensive API surface
- Legacy banking integration
- Complex fee management
- Program-based architecture

### Missing Capabilities

- **Column**: No card management
- **Moov**: No check operations, limited statement generation
- **Increase**: No lending features
- **Q2**: No simulation endpoints
- **Unit**: No market data, limited international

This analysis reveals that each provider has made distinct architectural choices reflecting their target markets and use cases, from Column's focus on traditional banking operations to Increase's developer-friendly simulation capabilities to Moov's emphasis on connectivity and money movement.