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
            1. [] Customer 
                - Tracks sensitive info like SSN 
                - On-boarding with verification 
                - Security functions (Ex. locking, archiving, date tracking)
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
            6. [] Transfer
            7. [] Statement
            8. [] Costumer Due Diligence
            9. [] Customer Relationship
            10. [] Customer Document
            11. [] Customer Beneficiary 
            12. [] Address
            13. [] Bin
            14. [] Customer Note
            15. [] Deposit Availability 
            16. [] Check 
            17. [] Digital Wallet Token 
            18. [] File Content 
            19. [] Industry Classification Code 
            20. [] Interest Rate 
            21. [] Limit
            22. [] Phone
            23. [] Product
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