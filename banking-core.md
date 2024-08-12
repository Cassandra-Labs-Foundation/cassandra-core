# Banking Core FAQs

|  | Bank License |  |  |
| --- | --- | --- | --- |
| Green Dot | Yes |  |  |
| Q2 |  |  |  |
| Synapse |  |  |  |
| Cross River |  |  |  |
| Galileo |  |  |  |
| Unit |  |  |  |
| Agora |  |  |  |
| Marqeta |  |  |  |
| Bond |  |  |  |
| Treasury Prime |  |  |  |
| Column |  |  |  |
1. [ ]  https://www.greendot.com/business-solutions/developer
    - TODO:
        - [] have to [contact the biz dev department](https://www.greendot.com/business-solutions/contact) in order to see the actual documentation 
        - [] what are "purses"? 
    - _Green Dot handles everything needed to run end-to-end embedded ﬁnancial BaaS programs, including account origination, payments, compliance and fraud, and card issuance. Green Dot offers Restful APIs for customers and can provide white label apps. The company offers a suite of ﬁnancial products to consumers and busi- nesses, including debit, prepaid, checking, credit and payroll cards, as well as mon- ey processing services, tax refunds, cash deposits and disbursements._ [cite](https://tearsheet.co/wp-content/uploads/2021/05/BaaS-Guide-2021-Ad-1.pdf)
        - Uber partnered with them to issue debit cards for earn-waged access 
        - Stash partnered with them to do a Stock-based Card that enables spenders to earn rewards in stocks 
    - They appear to have 6 core APIs
        1. Enrollments
            - enrollment + account creation + payment instrument all appear to happen withing a single API call 
            - the arguments are: 
                - user data (name + address + social security + date of birth + email address + phone number) 
                - account information (direct deposit info, account or purse information, account holder information)
        2. Users & Accounts
            - retrieves and update the following
                - personal information 
                - transaction history
                - account details 
                - account balances
                - available statements
                - identity verification
        3. Payment Instruments
            - enables the creation, replacement and activation of both physical and virtual cards
            - includes re-setting a PIN
        4. Transfers
            - enables moving money to and from internal accounts, external accounts, purses 
        5. ATM Locator
            - enables users to find nearby ATMs
        6. Webhooks
            - enables notifications of certain events that happen within a user's account
            - Examples include
                - transactions
                - account updates
                - statement availability 
                - ACH transfers
                - user updates 
                - batch closures 
    - They offer UX testing in a "partner integration environment" (PIE)
2. [ ]  https://helix.q2.com/developers
    - TODO
        - [] [Actual reference API](https://docs.helix.q2.com/reference/programget)
    - _Q2’s cloud-based core allows it to extend favorable economics to its clients. Q2 BaaS tech isn’t middleware that sits on a legacy core._ [cite](https://tearsheet.co/wp-content/uploads/2021/05/BaaS-Guide-2021-Ad-1.pdf)
        - They power Credit Karma, Betterment, Gusto
        - Lorenzo really likes the practical scenarios used to discuss Common Mistakes and suggests we use our own fintech partners as case studies 
            - ![Example of Practical Scenarios](assets/sub-accounts-and-goals-mistake.png)
    - API analysis 
        - They don't do webhooks, but instead use Azure Service Bus 
        - Overview 
            - Each object has a customerId and tag and common actions (create, initiate, verify, archive, get, getByTag, list)
            - _"A common mistake we see developers make is attempting to cache-in account and transactional data from Customers as a kind of pseudo-system of record. The critical mistake here is that an account, the balances of that account, the beneficiaries, and other transactional information can all be updated out of band from the application calling the API."_
        - Key Objects
            1. Customer 
                - tracks sensitive info
                    - for humans
                        1. attestation
                        2. driver's license
                        3. foreign documents
                            - DriversLicense
                            - ConsularIdCard
                            - Passport
                            - PermanentResidentCard
                            - EmploymentAuthorizationCard
                            - VoterRegistrationCard
                            - IdentificationCard
                        4. taxId
                            - Social Security Number (SSN)
                            - Individual Taxpayer Identification Number (ITIN)
                    - for businesses 
                        1. attestation 
                        2. business legal name (includes DBA)
                        3. industryClassificationCode
                        4. taxId
                            - Employer Identification Number (EIN)
                    - tracks the legal entity type
                        - Individual
                        - SingleMemberLLC
                        - SCorporation
                        - CCorporation
                        - SoleProprietorship
                        - NonProfit
                        - Association
                        - Partnership
                        - LimitedLiabilityCompany
                        - LimitedLiabilityPartnership
                        - RevocableTrust
                        - IrrevocableTrust
                        - FinancialInstitutionOther
                        - Estate
                        - Trust
                        - Church
                        - Conservator
                        - Guardianship
                        - Government
                        - Cooperative
                        - BCorporation
                        - TottenTrustPOD
                        - LimitedPartnership
                        - GeneralPartnership
                        - GovernmentDepartment
                        - GovernmentAgency
                        - GovernmentAuthority
                        - GovernmentNonCommercialNonUSDepartmentOrAgency
                        - GovernmentOther
                        - RegulatedFinancialInstitution
                        - RegulatedBankLoanHoldingsCompany
                        - RegulatedSavingsAndLoanHoldingCompany
                        - ForeignFinancialInstitutionRegulatorKeepsUBOInfo
                    - the reason the business is exempt from Beneficial Ownership is classified with the followign types 
                        1. UsStockExchangeTradedEntity
                        2. CharityOrNonProfitEntity
                        3. PublicAccountingFirmRegisteredUnderSection102
                        4. UsStateRegulatedBank
                        5. UsRegulatedInsuranceCompany
                        6. UsRegulatedFinancialInstitution
                        7. UsFederalGovernmentAgency
                        8. UsStateGovernmentAgency
                        9. UsLocalGovernmentAgency
                        10. NonUsGovernmentAgency
                        11. BankHoldingCompany
                        12. SavingsAndLoanHoldingCompany
                        13. FinancialMarketUtility
                        14. NonUsEntityOpeningAPrivateBankingAccount
                        15. ForeignFinancialInstitution
                        16. ClassOfSecuritiesIssuer
                        17. SecCurrentRegisteredFirm
                        18. CommodityFuturesTradingCommissionRegisteredEntity
                        19. ExcludedPooledInvestmentVehicle
                        20. NonExludedPooledInvestmentVehicle
                        21. UsStockExchangeMajorityEquityEntity
                - can be accessed through either /`customer/getByTag` (by using an id that is generated by the front-end and passed as a `tag` during customer creation) or through /`customer/Get` (by using the id generated by Helix)
                    - `customerId` is a unique ID assigned by Helix during `/customer/create`
                    - `tag` is the unique identifier assigned by the front-end  
                - tracks the on-boarding status 
                    - if legacy onboarding API endpoints were used  
                        - Initiated
                        - Manual Review
                        - Verified (as opposed to Active)
                    - otherwise
                        - Active    
                    - Denied
                    - Expired
                    - Archived
                    - Deceased

                
                - security functions
                    1. Fraud status 
                        - Verified
                        - Denied
                        - Automated Review
                        - Manual Review
                        - Null/Blank
                    2. tracks the status of a locked customer, including date and the reason the customer was locked
                    3. Last activity and last contact 
                - compliance functions
                    1. KYB date and status 
                        - Initiated
                        - Manual Review
                        - Verified
                        - Denied
                        - Expired
                        - Deceased
                        - Archived
                        - Automated Review
                    2. KYC date and status
                        - Verified
                        - Denied
                        - Automated Review
                        - Manual Review
                        - Null/Blank
                - tracks whether a user is subject to [backup witholding](https://www.irs.gov/taxtopics/tc307.html)
                                    - _"Helix will withhold the appropriate
                percentage of earned interest and submit these funds
                directly to the IRS. The amount withheld will be reported on the annual 1099-INT generated by Helix."_
                                - supports custom fields to save information otherwise not already included 
            2. Account
                - "Supports concept of a goal via account properties"
                    - it does so through `target` properties which track a user's contribution journey until `availableAmount` reachers a certain point
                - not the same as an External Account (I.E. a bank account with another financial institution)
                - `availableBalance` is the amount that can be immediately withdrawn
                    - for DDA accounts, the credit is immediate
                    - for savings or FBO accounts there maybe be a hold time between when the trasnaction gets settled and when the funds are available
                - `pendingBalance` 
                    - When a deposit transaction is initiated, it doesn’t immediately reflect in the account’s `availableBalance`. Instead, it is marked as "pending" and adds to the pendingBalance. Once the transaction settles (i.e., the funds are fully transferred and verified), `pendingBalance` is decreased by the amount that was pending. 
                    - Immediate deposits, which settle instantly, do not affect this balance.
                - `productId` is the unique ID of the product (from the Program) to which the account is associated
                    - the types of product are
                        1. Checking
                        2. Savings (RegD restrictions apply)
                        3. Prepaid
                        4. ForBenefitOf (A more restrictive dda account)
                - `regDWithdrawalCount` tracks withdrawal on a savings product which will lead to a fee at the end of the month
                - recurring contributions can be setup according to parameters (amount, start date, end date...)
                    - the contributions can come from an External Account
                - primary owners have higher priority over join owners 
                - limits can be put on the account (although it seems limited to ACH)
                    - `stopPay` enables users to set mins and maxes can be applied to payment amounts as well as blacklisting other entities from charging the account
                - locks can be put on an account (by the customer or admin system) for the following reasons 
                    1. UNK: Unknown
                    2. FRD: Fraud investigation
                    3. ADM: Administrative
                    4. TMP: Temporary
                    5. FRZ: Freeze
                    6. SUS: Suspected fraud
                    7. CO: Credits only
                    8. RTN: Return Risk
                    9. REC: Recovery
                    10. DED: Deceased
                    11. DOR: Dorman
            3. External Account
                - Real-time routing number verification via the Federal Reserve
                - Account number verification via Trial Deposits
                - Funds can be transferred between Helix accounts and accounts at other financial institutinos
                    - a customer is limited in the number of external accounts they can have by the `perUserExternalAccountCountMax` set in the Program
                - it saves the account number and routing number from the external bank, and once verified a unique Id is assigned by Helix
                    - verification customer ownership of an external account prior to initiative transfers can be done in 2 ways
                        1. Instant Verification
                            - _"Most programs opt to use an Instant Account Verification (IAV) service such as Plaid"_
                            - customer enters online banking credentials into the IAV service, who then validates and returns account number and routing number that are used to create a new account on Helix
                        2. Micro-deposits
                            - customer enters account and routing info which Helix uses to create an account with "unverified" status 
                        - Helix then sends (through ACH) 2 small deposits (<$0.49) which the customer then enters at a later date (~3 days bc of ACH) to update the account status to "verified" 
                - status options
                    1. Unverified
                    2. VerifyLocked
                    3. Verified
                    4. Denied
                    5. Expired
                    6. Archived
                - types of accounts
                    1. Savings
                    2. Checking
                    3. Business Checking
                    4. Business Savings
                    5. Prepaid
                    6. Loan
            4. Transaction  
                - /transfer/create is the endpoint used to create a transaction
                that includes any movement of funds
                    1. interest paid
                    2. manual adjustments
                    3. debit card transactions
                    4. incoming ACH requests
                - IDs 
                    1. `accountId` links to the Account and `customerId` links to the Customer that owns the bank account
                    2. `cardId` is generated by Helix for the Card that created the transaction 
                        - Will be left empty or 0 if the transaction is not associated with a Card 
                    3. `cardMerchantInfo` contains the meta-data from the merchant  
                        - it includes city, country, location, state, zip code 
                        - `merchantGroupcode` is a super-set of several Merchant Category Codes
                        - `merchantId` identifies the merchant that accepted the card
                    4. Whenever possible `institutionName` records the name of the financial institution that originated the transaction
                    5. `masterId` is a unique identifier created by Helix used to group related transactions together, such as
                        - an ACH withdrawal and a subsequent return. 
                        - A debit card authorization and its corresponding completion(s). 
                        - A mobile check deposit return and its corresponding original mobile check deposit.
                    6. `requestingCustomerId` identifies who requested the transaction if they are not the business costumer who owns the Account 
                    7. `transactionTag` tags a transfer between funds with a tag setup in the Program
                    8. `transactionId` is a unique ID generated by Helix 
                - they record how the transaction state changes through status and dates
                    1. Initiated: Transaction has been created but not yet put into a NACHA file
                        - `createdDate` records the exact date and time in the time zone local to the bank
                    2. Pending: Transaction has been created and put into a NACHA file
                    3. Settled: Transaction has been posted to the account
                        - `settledDate` and `statementDate` record the exact date and time in the time zone local to the bank
                        - `availableDate` records exactly when the funds associated with the transaction became available
                        - `runningAccountBalance` is the `accountBalance` of the Account AFTER settlement occurs
                    4. Voided: Transaction has been voided
                        - `voidedDate` records the exact date the transaction was voided in the bank's local time zone
                            - _"Transactions that are initiated via the /transfer/create route with external bank accounts (or via a recurring contribution) can be voided as long as the ACH request has not yet been delivered to NACHA."_
                        - `returnCode` is a NACHA return code that explains why the transaction was returned
                - they categorize the transaction by the nature of the transaction (`isCredit`, `isEarlyDirectDeposit`, `isSameDaySettle`) and its descriptions and codes
                    1. `description` is the description that must be displayed to the end user by law
                        - _"If transaction was received from a Nacha file (typeCode is UNKWTH, UNKDEP, UNKPRG) this property contains the description verbatim from the Nacha file. "_
                            - `nachaInfo` holds the info from externally-originated ACH deposits 
                        - _"If transaction was received from an ISO-8583 interface (i.e. debit card transaction), this property contains description verbatim from DataElement 43 (Card Acceptor Name/Location) of ISO-8583 interface plus details of any fees or surcharges that may have been incurred."_
                        - _"Otherwise, the transaction was received from a call to Helix API or it was line item in the Bulk Transfer File."_
                    2. `feeCode` and `feeDescription` are formal 
                        - ACH: Same Day ACH Fee
                        - DAF: Dormancy Fee
                        - IAF: Inactivity Fee
                        - ICF: International Card Fee
                        - NSF: Insufficient Funds Fee
                        - RGD: Regulation D Fee
                        - RTN: Return Item Fee
                    3. `friendlyDescription` are generated by Helix through `typeCode`
                        - `subTypeCode` is the Merchant Category Code (which groups merchants of similar kinds of businesses) that generates the `subType` description
                        - `typeCode` is the [Transaction Type](https://docs.helix.q2.com/docs/transaction-types) that then generates `type` which is a human-readable description  
                    4. `purposeCode` is alphanumeric identifier describing the purpose of the transaction that is provided to the third-party fraud and risk vendor 
                        - _"These values are agreed upon by the bank of record and client during onboarding"_
            5. Card
                - "Integrated with debit rails via ISO-8583 interface" 
                - Real-time locking and unlocking 
                - Real-time notifications about success/failure of the transaction
                - Each card is a debit card issuedby Helix that is connected to either a savings or checking Account
                    - "To correlate a specific card in Helix to a specific card record in your system, store your system's unique key in the tag property, or store Helix's cardId in your system."
                - Steps to creating a physical card
                    1. /card/initiate
                    2. Physical card gets printed and shipped to the customer
                    3. Customer is prompted to activate their card, which triggers /card/verify
                    4. Card is activated 
                - Properties 
                    - A single customer can have multiple cards.. A single account can be tied to multiple cards.
                        - `accounts` is an array of Accounts because a single card can be tied to multiple accounts (4 checking, and 4 savings)
                            - beyond the regular Account properties (`accountBalance`, `availableBalance`, `pendingBalance`, `status`, `type`) it also has `cardPriority`(whose values will be between 1 and 4 inclusive) which is not explained in the documentation but I think refers to the scenario where a transaction is attempted and insufficient funds are present in the primary account thus the system attempts to draw funds from the next account in the priority order
                        - `binId`
                            - BIN (Bank Identification Number) is a unique identifier that represents a specific range of card numbers assigned by a card network provider (like Visa or Mastercard). It is used to identify the issuer of the card and the card's type so that the transactions can be routed to the correct network
                            - in Helix, `binId` links to a specific BIN configuration (which includes details like the card's PAN prefix and network provider type) from the Program
                        - `customerId` is the unique id of the customer who called /card/initiate	
                            - the initator must be "verified" and `accessTypeCode` "FULL"
                        - `cardHolderCustomerId` identifies the customer who is in possession of the card (which is why it defaults to `customerId` if the value is null)
                            - the holder must be a "verified" Customer who has `accessTypeCode` of "FULL", "ACCT", or "CARD"
                        - `cardId` is the uniqueId assigned by Helix
                            - `tag` is where the user id from the front-end can be stored to associate the card
                        - `primaryAccountId` is the `acccountId` of the default Account (which must have `type` of "Checking") for the card 
                    - dates track the status of a card
                        - `requestedDate` --> `createdDate` --> `verifiedDate` (or `deniedDate`) --> `archivedDate` 
                        - they can be set to expire through `expireMonth` and `expireYear` --> `expiredDate`
                    - card classification 
                        - `typeCode` defaults to "DBT" (Debit) but can be GPR ("General Purpose Pre-paid")
                        - `vendorTypeCode` is either "VS" (Visa) or "MC" (Mastercard)
                        - `isDigitalOnly` is "true" if the card was created thrugh /card/createDigital or card/initiate with `isCreateDualIssuanceSinglePAN` set to "true" and `IsPhysicalCardOrdered` set to "false"
                        - `isDualIssuanceSinglePAN` tells if the card is functional as a digital card for use with mobile wallets
                            - `digitalWalletTokens` is an array of `digitalWalletToken` which is created when a customer provisions a card into a digital walleter
                    - card locking
                        - `lockTypeCode` tells the type of lock applied to the card
                            - "UNL" is unlocked
                            - "CST" is Customer Locked via /card/unlock
                            - "SYS" is System Locked by the admin console or automated process 
                            - Admin user specifies whether the Customer can unlock the card 
                                - customers can unlock most CST locks but none
of the SYS locks
                        - `lockReasonTypeCode` tells the reason the card was locked
                            - some can be set and removed easily
                                - UNK: Unknown
                                - FRD: Suspected Fraud
                                - DMG: Physical Damage
                                - TMP: Temporary
                            - some are set via /card/hotlist API route only and cannot be subsequently unlocked.
                                - STL: Stolen
                                - LST: Lost
                            - some can be set via Admin Console or background processing only.
                                - ADM: Administrative
                                - PIN: PIN Retries Exceeded
                    - status
                        - Initiated
                        - Pending
                        - PendingVerification
                        - Verified
                        - Denied
                        - Expired
                        - Archived
                        - Reissued
                        - HotListed
                        - ReissuedPendingVerification
                        - AutoReissuedPendingVerification
                        - DigitalActivePhysicalInitiated
                        - DigitalActivePhysicalPending
                        - AutoReissueInitiated
                        - ReissueStaged
                    - limits of purchases and withdrawals
                        - `bankCeiling` is the bank-level `purchaseLimit` and `withdrawalLimit`
                        - `effectiveDailyLimits` is the program-level purchase and withdrawal limit
                        - `programDefault` is the standard limits set for the program, applicable to all users by default.
                        - `limitGroupOverride` is the custom limits applied to a specific card, overriding the default program limits.
                        - `temporaryOverride` is temporary limits which expire after a set period
                    - `cardControl` has `rules` which is an array of `cardControlRule` objects that each contain the rules applied to the debit cards set by a `source` (either "Customer" or "Program")
                        - _"Each cardControlRule object is a rule you’re applying to the targeted Helix debit card, which is how we can support multi-tenancy with any combination of program applied or customer applied rules within the same card control object."_
                        - supports both `domestic` and `international`
                        - `limit` which is the max amount after which the transaction is automatically declined
                        - `entryMethod` is array of allowed PAN entry method(s). 
                            - CP: Card Present
                            - DP: Device Present
                            - CNP: Card Not Present
                            - IAP: In App Purchase
                        - `mccs` are the Merchant Category Codes and `merchantGroups` are teh Merchant Group Codes
            6. Program 
                - it represents each business on Helix, and contains the settings to be applied to all customers, accounts, transactions, and products 
                - an array of accounts is connected to a specific sponsor bank's object
                    - a single customer can have multiple accounts (including external accounts), subject to limits defined in the program
                - an array of products offered by the program
                - daily and monthly and per-transaction limits for deposits and withdrawals 
                    - a fee can be charged when a customer goes over the limit
                - recurring contributions and debit rewards 
                - a list of algorithms approved for use by the program needed by any public key encryption required by the API.
            6. Bank Document
                - it represents a document issued by a bank that a customer must indicate they have read and accepted during customer/account creation
                - supports a variety of document types 
                    1. TermsAndConditions
                    2. PrivacyPolicy
                    3. TruthInSavings
                    4. eStatement
                    5. ConsumerDepositAgreement
                    6. FeeSchedule
                    7. ReferAFriend
                    8. EftInfo
                    9. ProductInfo
                    10. CardInfo
                    11. FeeDisclosure
                - each document has an id and is attached to a program and a bank's unique id  
                - the url for the pdf is saved alongside an html version 
            7. Transfer
                - A `customerId` (the Helix-assigend unique ID for the Customer) initiates the transfer from `fromId` (an `accountId` or `externalAccountId` indicating where the funds are being withdrawn from) to `toId` (also an `accountId` or `externalAccountId` where the funds are deposited)
                - the transaction is classied through `amount`, `tag`, `description` and `purposeCode` (identifier created by the bank that is sent to the 3rd party risk manager)
                - peer-to-peer transfers need be approved by both Q2 and the bank partner
                    - if the receiver of the funds is different from the sender, then `toCustomerId`, `toCustomerTag`, `toTransactionTag` is used to log the transfer
                - TransferResponse
                    - `customerId` for the customer initiating the transfer
                    - `masterId` groups related transactions
                    - `tag` is the frontend label
                    - `transactionId` is a NACHA-compliant unique idnetifier for the single transfer
                - transfers take different times based on the type of transfer
                    - Transfers between accounts owned by the same Customer settle immediately 
                        - the ACH network is not used therefore they have no [Originating Depository Financial Institution](https://en.wikipedia.org/wiki/Originating_Depository_Financial_Institution) 
                        - this is true even for "reserve accounts" (I.E. special-purpose accounts used for activities relating to the Program that need to be kept separate from standard checking and savings, such as managing reserves and operational funds)
                    - an Account "pushing" to an External Account or an Account "pulling" from an External Account settle in a matter of business days
                        - Day 1 is when Helix initiates the transaction (which can be any time), and Day 2 is when Helix submits the ACH via NACHA (which has to be a business day), so everything gets moved in case of a weekend or bank holiday
                        - the ODFI is Helix in this case
                    - Receiving an ACH via NACHA to "pull" funds out of an Account and "push" funds into an Account settles immediately
            8. Statement
                - Helix creates monthly bank statements and yearly tax (1099) of different types
                    1. Monthly
                    2. Quarterly
                    3. Tax1099INT
                    4. Tax1099MISC
                - they each have their own `statementId` and they are connected to a `customerId`
            9. Costumer Due Diligence
                - "/program/questionsList" gets questions from Program
                - "/customer/answerPost" records a Customer's answers that can be retrieved " /customer/answerList" retrivers a Customer's answers
                - DueDiligenceCategory
                    - `categoryDescription`
                    - `categoryId`
                    - `questions` is an array of DueDiligenceQuestion
                        - `questionName` and `questionId`
                        - `answerDate`
                        - `answerType`
                            1. `Single-Select`
                            2. `Multi-Select`
                            3. `Text`
                        - `choices` is an array DueDiligenceChoice 
                            - `choiceId`
                            - `answeredDate`
                            - `choiceDescription` and `choiceName`
                            - `followUpQuestionIds` array of `questionId` to be asked if the customer selects this choice
                    - `followupQuestions` is an array of DueDiliegenceQuestions triggered by answers to `question`
                - DueDiligenceAnswer 
                    - `questionAnswer` if `DueDiligenceQuestion` has `answerType` of "text"
                    - `questionId`
                    - `selectedChoices` is an array of DueDiligenceSelectedChoices
                        - `choiceId` Helix-assigned unique ID for the DueDiligenceChoice
                        - `choiceName` 
            10. Customer Relationship
                - an object that formalizes the relationship between `primaryCustomerId` and `relatedCustomerId`
                    - the `relationshipType` is classified through the following:
                        1. Signer
                        2. Owner
                        3. NonTransactional
                        4. BeneficialOwner
                        5. Trustee
                        6. SuccessorTrustee
                        7. Guardian
                        8. Conservator
                        9. Executor
                        10. Agent
                        11. PowerOfAttorney
                        12. Custodian
                        13. Administrator
                        14. Fiduciary
                    - `isBeneficialOwner` and `beneficialOwnerPercentage` track whether the related Customer owns a company account that is technically under the company's name
                - permission system is based on `isPrimaryContact`, `isControlPerson`, `canOpenAccounts` 
                    - `externalAccountAccessType` clarifies the access `relatedCustomerId` has over the External Accounts of `primaryCustomerId`
                        - FULL
                        - RDLY (Ready-only)
                        - ACH
                        - NONE
            11. [] Customer Document
            12. [] Customer Beneficiary 
            13. [] Address
            14. [] Bin
            15. [] Customer Note
            16. [] Deposit Availability 
            17. [] Check 
            18. [] Digital Wallet Token 
            19. [] File Content 
            20. [] Industry Classification Code 
            21. [] Interest Rate 
            22. [] Limit
            23. [] Phone
            24. [] Product
        - Backend processes
            1. ACH Processing Including Same-day ACH
            2. Monthly or Quarterly interest payment (daily accrual)
            3. Daily file generation: Customer Registrations, Customers, Account Balances, and Posted Transactions
            4. Event Notification File - keep your data in sync with Helix's 
            5. Goal target met processing
            6. Bulk Transfers
            7. Monthly statement generation
            8. Quarterly OFAC re-verification
            9. Annual 1099-INT statement generation
            10. Daily Recon and Trial Balance calculation
            11. Monthly RegD fee calculation
    - Takeaways
        - Here's a list of security measures they adhere to 
            1. Annual PCI Compliance Level 1 Audit
            2. Annual SOC 2 Audit
            3. HTTPS TLS 1.1+ for API
            4. SFTP for file transfer
            5. IP whitelisting for API and SFTP server access
            6. Fully encrypted TLS 1.2 internal network communications
            7. AES-256 encryption for sensitive data at rest
            8. PCI compliant key management (annual key rotations, multiple active keys, key custodians, etc) for PAN and other PCI-sensitive data
            9. Optional PGP encryption for files sitting on SFTP server
        - "A common mistake we see developers make is attempting to cache-in account and transactional data from Customers as a kind of pseudo-system of record. The critical mistake here is that an account, the balances of that account, the beneficiaries, and other transactional information can all be updated out of band from the application calling the API."

3. [ ]  https://docs.synapsefi.com/
4. [ ]  https://www.crossriver.com/developers
5. [ ]  https://docs.galileo-ft.com/pro/reference/program-api-intro
6. [ ]  https://www.unit.co/docs/api/
7. [ ]  https://api.agoracoretech.com/docs/v2/
8. [ ]  https://www.marqeta.com/docs/developer-guides/
9. [ ]  https://docs.bond.tech/docs/welcome-introduction
10. [ ]  https://docs.treasuryprime.com/docs/getting-started
11. [ ]  https://column.com/docs/guides/getting-started-with-the-column-api
12. [ ]  https://www.lead.bank/baas-partner-platform
13. [ ]  https://www.alkami.com/

---

# what are the relevant regulation/compliance/audit requirements/standards?

we have identified the following requirements and standards:

- requirements
- standards
    - payment card industry data security standard (PCI DSS)
    - statement on standards for attestation engagements (SSAE)
        - system and organization controls (SOC)
    - [open banking](https://www.openbanking.org.uk)
    - [FFIEC IT examination handbook](https://ithandbook.ffiec.gov)
    - [ISO/IEC 27001](https://www.iso.org/standard/27001) (infosec)

we do not mention AML/KYC above, because we consider those requirements to apply broadly beyond the banking core.

---