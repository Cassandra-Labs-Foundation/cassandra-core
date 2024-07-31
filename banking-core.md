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
        - [] what is a "goal"? 
        - [] [Actual reference API](https://docs.helix.q2.com/reference/programget)
    - _Q2’s cloud-based core allows it to extend favorable economics to its clients. Q2 BaaS tech isn’t middleware that sits on a legacy core._ [cite](https://tearsheet.co/wp-content/uploads/2021/05/BaaS-Guide-2021-Ad-1.pdf)
        - They power Credit Karma, Betterment, Gusto
    - API analysis 
        - They don't do webhooks, but instead use Azure Service Bus 
        - Overview 
            - Each object has a customerId and tag and common actions (create, initiate, verify, archive, get, getByTag, list)
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
            2. [] Account
                - DDA, FBO, Savings
                - Available, Pending, and Actual balances
                - "Supports concept of a goal via account properties"
            3. [] External Account
                - Real-time routing number verification via the Federal Reserve
                - Account number verification via Trial Deposits
            4. [] Transaction
                - Rules that can limit transfers 
                - Detailed auditing of how transaction states change
                - Funds availability tracking which accounts for settling, hold days and banking holidays 
                - End-to-end tracking of ACH returns
            5. [] Card
                - "Integrated with debit rails via ISO-8583 interface" 
                - Real-time locking and unlocking 
                - Real-time notifications about success/failure of the transaction
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
            7. [] Transfer
            8. [] Statement
            9. [] Costumer Due Diligence
            10. [] Customer Relationship
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