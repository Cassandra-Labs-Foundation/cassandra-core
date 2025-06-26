# Blnk Finance Core

This is a test using [Blnk Finance](https://docs.blnkfinance.com/home/install) to build our banking core

## Roadmap

- [ ] Setup
    - [ ] New Supabase instance
    - [ ] Tiny Redis 
    - [ ] Build Blnk from source
    - [ ] Write `blnk.json`
    - [ ] Run initial migration 
        - [ ] Create `Ledgers`
        - [ ] Create `Balances`
        - [ ] Create `Transactions`
- [ ] Seed Ledgers
    - [ ] Deposits
    - [ ] NostroUSD
    - [ ] Fees
- [ ] Edge Functions
    - [ ] OpenAccounts
    - [ ] Deposit
    - [ ] Transfer
- [ ] Test & Observation
    - [ ] Row-Level Security Policies
    - [ ] Watch Redis at 'localhost:5001/monitoring'
    - [ ] Test a full transaction life-cycle
        `curl POST /functions/v1/open-account
curl POST /functions/v1/deposit
curl POST /functions/v1/transfer
./blnk trial-balance --as-of now`