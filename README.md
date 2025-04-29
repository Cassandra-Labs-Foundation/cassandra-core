# Banking Core UI

> **Status:** MVP in active development – internal demo scheduled **May 20 2025**

---

## 1 ▪ Purpose
Provide a modern, web‑based teller & back‑office console for the Pynthia banking core.  
The UI enables credit‑union staff—tellers, member‑services reps, loan officers, accountants, and admins—to perform daily work without terminal commands.

---

## 2 ▪ Roadmap & Task List (MVP‑0.1)

- **Foundation**
  - Project scaffold
    - Initialize **Next.js 14** (Pages Router) with TypeScript
    - Configure **Materialize CSS** via CDN import in `_app.tsx`
    - Add React Context for global session state
  - Developer tooling
    - ESLint + Prettier configuration
    - `tsconfig.json` strict mode enabled
    - GitHub Actions workflow: `lint`, `type‑check`
  - Mock data layer
    - `src/lib/mock.ts` returns Promise‑based JSON stubs
    - Introduce `MOCK_LATENCY_MS` constant for realistic delays
  - Performance & accessibility
    - First contentful paint < 1 s (local dev)
    - Lighthouse accessibility score ≥ 90 on Home page

- **Core UI Components**
  - Sidebar navigation (collapsible on mobile)
  - Top breadcrumb header
  - Global search bar (client‑side fuzzy search)
  - `DataTable` wrapper around Materialize tables
  - Modal form pattern (`ModalForm.tsx`)

- **Feature Modules**
  - [ ] Home
    - [ ] Shortcut cards linking to each module
  - [ ] Teller
    - [ ] Drawer balance card (mock values)
    - [ ] Member quick‑edit modal
    - [ ] Transaction journal (read‑only table)
  - [ ] Member Services
    - [ ] Member account CRUD modal shells
    - [ ] Multi‑member transaction stub
    - [ ] Shared‑branch network placeholder
  - [ ] Lending
    - [ ] New‑loan form stub
    - [ ] Adjust‑loan details modal
    - [ ] Charge‑off modal
    - [ ] NCUA / credit‑reporting field set (read‑only)
  - [ ] Accounting
    - [ ] General‑ledger table (mock rows)
    - [ ] Adjustment‑ledger entries
    - [ ] Project‑specific GL selector dropdown
  - [ ] Reports
    - [ ] 5300 report placeholder card
    - [ ] BSA report placeholder card
  - [ ] Administrator
    - [ ] User table (mock dataset)
    - [ ] Role selector dropdown
    - [ ] IAM matrix grid

> _Out of scope for MVP‑0.1: real ledger posting, authentication hardening, multi‑tenancy._

---

## 3 ▪ Repo Layout
```text
banking-core-ui/
├─ README.md
├─ package.json
├─ next.config.js
├─ public/
├─ src/
│   ├─ pages/
│   │   ├─ _app.tsx
│   │   ├─ index.tsx          # Home
│   │   ├─ teller/
│   │   ├─ member-services/
│   │   ├─ lending/
│   │   ├─ accounting/
│   │   ├─ reports/
│   │   └─ administrator/
│   ├─ components/
│   ├─ lib/
│   └─ types/
└─ .github/workflows/ci.yml
```



## 4 ▪ Core‑Provider Benchmark
The UI we’re building must eventually sit on top of a production core. Below is a condensed comparison of the three vendors we’ve evaluated so far. This context helps outside contributors understand future integration constraints and naming conventions in the codebase.

| Dimension | CU*Answers | Sharetec | Fiserv (Portico) |
|-----------|------------|----------|------------------|
| **Ownership / model** | CUSO owned by member CUs; free licence for start‑up CUs (first 2 yrs). | Private‑equity backed (Evergreen Services). Commercial licence. | Public mega‑vendor; enterprise pricing, long‑term contracts; heavy upsells to add‑on modules. |
| **Tech stack** | Legacy engine + **OpenAPI**; modular “tools” UI. | Angular front‑end, .NET REST API; MS SQL + Progress OpenEdge. | Proprietary stack; Portico thick‑client UI in browser shell; core accessible only from whitelisted IPs. |
| **UI / UX** | Search‑centric home, widgets visible only when relevant, multi‑tab modal drill‑downs. | Global fuzzy search, drag‑drop KPI dashboards, granular change logs. | Search lacks autocomplete; teller balancing & cash‑drawer flows central; reversal UI day‑limited; in‑app message feed. |
| **Customisation** | Unified object model for loans & deposits; highly configurable DB. | “Metrics” builder for products; relationship‑based pricing; CRUD‑level permissions. | Relies on add‑ons (Loanscierge, GenX Accounting) for deeper functions; creating/managing tellers & ACH originations viewed as cumbersome. |
| **Cards & payments** | No native card module; integrate with any processor; digital‑card push to wallets. | Leverage Payment Solutions + NeuralPayments; RTP/FedNow support. | ACH interface flags rejects; shared‑branch network supported; card issuing via third‑party processors. |
| **Lending flow** | Pre‑set loan flows, recent‑activity checks, built‑in e‑sign & imaging. | Visual decision engine, dynamic pricing via bureau polling, MeridianLink/SyncOne. | Loanscierge queue‑based origination; loan reversals common; collection often outsourced via Portico sub‑access. |
| **Reporting & analytics** | Table‑based “Where Members Borrow/Shop” reports. | Split operational vs analytics; async dashboards (LogiAnalytics). | Auto‑generated PDF reports (used for 5300); manual data‑cache refresh; GenX Accounting for call‑report. |
| **Reg‑tech / audit** | Strong e‑docs, CU‑Folks form pre‑fill, co‑op managed knowledge base. | Adverse‑action forms, full audit trail per item, automated call‑report. | Docusign integration for user updates; charge‑off loans reported to bureaus; audit searches require teller‑by‑teller lookup. |
| **Community & cadence** | 53‑yr co‑op, roadmap steered by owners. | Quarterly releases, vendor due‑diligence handled in‑house. | Slow release cadence; feature requests routed through account manager; heavy reliance on third‑party ecosystem. |
| **BaaS fit (subjective)** | ✅ Co‑op licensing & OpenAPI ease integration; must bolt on cards. | ✅ Modern REST + richer analytics; licensing cost & PE control are trade‑offs. | ⚠️ Mature but closed stack; add‑ons & manual workflows increase integration friction and cost. |

> **Take‑away for contributors:** keep adapter layers thin and generic (`CoreAdapter`, `Account`, `Loan`, `GLTransaction`) so we can pivot between cores—or operate multi‑core—without rewriting UI logic.