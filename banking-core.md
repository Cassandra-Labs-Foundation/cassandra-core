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