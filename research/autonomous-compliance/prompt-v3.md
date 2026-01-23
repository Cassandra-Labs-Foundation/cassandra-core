# Cassandra Banking Core - Autonomous Compliance System

## Philosophy

Compliance is not a bottleneck—it's a programming problem. We design compliance like an API: well-specified interfaces instead of ad hoc checklists and PDFs.

### Core Principles

1. **Controls are the primitive, not policies.** Each control is an interface with defined inputs, outputs, triggers, events, SLAs, and KPIs. Policies are compositions of controls.

2. **Bidirectional traceability.** When the API changes, legal sees which controls are affected. When policies change, engineering sees which endpoints need updating.

3. **Event-sourced auditability.** Every control execution is an event. Every approval is a log. Every failure is measurable. Audits become real-time dashboards, not archaeological digs.

4. **Design for hostile auditors.** Build assuming we're being examined by a hostile regulator at all times. If we survive that, we outperform competitors who slow to a crawl during exams.

5. **Compliance enables speed.** A clean, observable system lets us say "yes" faster—onboarding more fintechs with more confidence.

6. **Vocabulary as the contract.** Engineering owns the canonical vocabulary (events, fields, SLA patterns, regulations, roles). Compliance can only reference what exists in the vocabulary, ensuring controls stay in sync with what the system actually supports.

7. **Validation at authoring time.** Controls are validated against the vocabulary in real-time. Errors surface immediately during authoring, not during integration or audit.

---

## System Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                     CONTROL BUILDER UI                          │
│  (Compliance authors controls using structured forms)           │
└─────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│                      SHARED VOCABULARY                          │
│  Engineering-owned canonical definitions of:                    │
│  • Events (what can trigger controls)                           │
│  • Fields (what data exists in the system)                      │
│  • SLA Patterns (how deadlines work)                            │
│  • Regulations (citation library)                               │
│  • Roles (who can do what)                                      │
│  • NCUA Account Codes (5300 reporting fields)                   │
└─────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│                    COMPILED YAML + VALIDATION                   │
│  Controls compile to version-controlled YAML that maps          │
│  directly to OpenAPI endpoints and event streams                │
└─────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│                      BANKING CORE                               │
│  Control execution engine consumes YAML, enforces SLAs,         │
│  emits audit events, routes to human review when needed         │
└─────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│                 REAL-TIME 5300 DASHBOARD                        │
│  Live regulatory reporting that turns quarterly exams           │
│  into always-on observability                                   │
└─────────────────────────────────────────────────────────────────┘
```

---

## Vocabulary Schema (Engineering-Owned)

The vocabulary is the contract between compliance and engineering. Engineering maintains it; compliance references it.

```typescript
interface Vocabulary {
  // Events that can trigger controls
  events: Record<string, {
    description: string;
    category: 'member' | 'lending' | 'compliance' | 'bsa' | 'marketing' | 'security' | 'investments' | 'deposits' | 'income' | 'reporting';
    // Link to OpenAPI operation that emits this event
    openapi_source?: string;
    // Which NCUA accounts this event affects (for 5300 calculation)
    affects_accounts?: string[];
  }>;

  // Fields that controls can reference as inputs/outputs
  fields: Record<string, {
    type: 'string' | 'number' | 'boolean' | 'date' | 'object' | 'array' | 'enum';
    description: string;
    category: string;
    // Metadata for compliance awareness
    pii?: boolean;
    fair_lending_risk?: 'low' | 'medium' | 'high' | 'critical';
    confidential?: boolean;
    // Link to OpenAPI schema
    openapi_schema?: string;
  }>;

  // SLA enforcement patterns
  sla_patterns: Record<string, {
    description: string;
    params: string[];
    blocking?: boolean;  // If true, blocks downstream events until satisfied
  }>;

  // Regulation citation library
  regulations: Record<string, {
    name: string;
    citation: string;
    // Optional link to full text or internal policy
    reference_url?: string;
  }>;

  // Roles for access control
  roles: string[];

  // Standard audit event suffixes
  audit_suffixes: string[];

  // NCUA Account Codes for 5300 reporting
  ncua_accounts: Record<string, NCUAAccountCode>;
}
```

### Initial Vocabulary

```typescript
const VOCABULARY: Vocabulary = {
  events: {
    // ═══════════════════════════════════════════════════════════════
    // MEMBER LIFECYCLE
    // ═══════════════════════════════════════════════════════════════
    'member.created': { 
      description: 'New member record created', 
      category: 'member' 
    },
    'member.updated': { 
      description: 'Member profile changed', 
      category: 'member' 
    },
    
    // ═══════════════════════════════════════════════════════════════
    // LENDING
    // ═══════════════════════════════════════════════════════════════
    'application.created': { 
      description: 'Loan/membership application submitted', 
      category: 'lending' 
    },
    'application.completed': { 
      description: 'Application has all required info', 
      category: 'lending' 
    },
    'decision.recorded': { 
      description: 'Credit decision made', 
      category: 'lending' 
    },
    'counteroffer.issued': { 
      description: 'Counteroffer presented', 
      category: 'lending' 
    },
    'counteroffer.expired': { 
      description: 'Counteroffer deadline passed', 
      category: 'lending' 
    },
    'loan.originated': { 
      description: 'New loan booked', 
      category: 'lending',
      affects_accounts: ['025B', '010', 'schedule_a.*']
    },
    'loan.payment.received': { 
      description: 'Loan payment processed', 
      category: 'lending',
      affects_accounts: ['025B', 'delinquency.*']
    },
    'loan.charged_off': { 
      description: 'Loan charged off', 
      category: 'lending',
      affects_accounts: ['025B', 'CH####', 'schedule_a.charge_offs']
    },
    'loan.recovered': { 
      description: 'Recovery on charged-off loan', 
      category: 'lending',
      affects_accounts: ['CH####', 'schedule_a.recoveries']
    },
    
    // ═══════════════════════════════════════════════════════════════
    // COMPLIANCE / KYC
    // ═══════════════════════════════════════════════════════════════
    'kyc.started': { 
      description: 'Identity verification initiated', 
      category: 'compliance' 
    },
    'kyc.passed': { 
      description: 'Identity verification successful', 
      category: 'compliance' 
    },
    'kyc.failed': { 
      description: 'Identity verification failed', 
      category: 'compliance' 
    },
    'screening.ofac.hit': { 
      description: 'OFAC screening potential match', 
      category: 'compliance' 
    },
    'screening.ofac.cleared': { 
      description: 'OFAC match cleared', 
      category: 'compliance' 
    },
    
    // ═══════════════════════════════════════════════════════════════
    // BSA/AML
    // ═══════════════════════════════════════════════════════════════
    'cash.threshold.exceeded': { 
      description: 'Cash transactions exceed $10k', 
      category: 'bsa' 
    },
    'sar.decision.required': { 
      description: 'Case requires SAR decision', 
      category: 'bsa' 
    },
    'sar.filed': { 
      description: 'SAR submitted to FinCEN', 
      category: 'bsa' 
    },
    
    // ═══════════════════════════════════════════════════════════════
    // MARKETING
    // ═══════════════════════════════════════════════════════════════
    'campaign.created': { 
      description: 'Marketing campaign submitted', 
      category: 'marketing' 
    },
    'campaign.approved': { 
      description: 'Campaign cleared for launch', 
      category: 'marketing' 
    },
    'campaign.launched': { 
      description: 'Campaign went live', 
      category: 'marketing' 
    },
    
    // ═══════════════════════════════════════════════════════════════
    // SECURITY
    // ═══════════════════════════════════════════════════════════════
    'incident.detected': { 
      description: 'Security incident identified', 
      category: 'security' 
    },
    'incident.reportable_determined': { 
      description: 'Incident classified as reportable', 
      category: 'security' 
    },
    
    // ═══════════════════════════════════════════════════════════════
    // INVESTMENTS (Schedule B)
    // ═══════════════════════════════════════════════════════════════
    'investment.purchased': { 
      description: 'Investment security purchased', 
      category: 'investments',
      affects_accounts: ['AS0055', 'AS0061', 'AS0067', 'AS0073', 'AS0013', '010']
    },
    'investment.sold': { 
      description: 'Investment security sold', 
      category: 'investments',
      affects_accounts: ['AS0055', 'AS0061', 'AS0067', 'AS0073', 'IS0029', 'IS0030']
    },
    'investment.matured': { 
      description: 'Investment reached maturity', 
      category: 'investments',
      affects_accounts: ['AS0067', 'AS0073']
    },
    'investment.impaired': { 
      description: 'Investment impairment recognized', 
      category: 'investments',
      affects_accounts: ['AS0041', 'AS0042']
    },
    
    // ═══════════════════════════════════════════════════════════════
    // DEPOSITS / SHARES (Schedule D)
    // ═══════════════════════════════════════════════════════════════
    'share.opened': { 
      description: 'New share account opened', 
      category: 'deposits',
      affects_accounts: ['013', '018', 'schedule_d.*']
    },
    'share.closed': { 
      description: 'Share account closed', 
      category: 'deposits',
      affects_accounts: ['013', '018', 'schedule_d.*']
    },
    'dividend.posted': { 
      description: 'Dividend credited to account', 
      category: 'deposits',
      affects_accounts: ['380', 'IS0010']
    },
    
    // ═══════════════════════════════════════════════════════════════
    // INCOME / EXPENSE
    // ═══════════════════════════════════════════════════════════════
    'interest.accrued': { 
      description: 'Interest income accrued', 
      category: 'income',
      affects_accounts: ['110', '115', 'IS0010']
    },
    'fee.collected': { 
      description: 'Fee income collected', 
      category: 'income',
      affects_accounts: ['131', 'IS0015']
    },
    
    // ═══════════════════════════════════════════════════════════════
    // REGULATORY REPORTING
    // ═══════════════════════════════════════════════════════════════
    'report.5300.generated': { 
      description: '5300 report generation initiated', 
      category: 'reporting'
    },
    'report.5300.validated': { 
      description: '5300 passed all validation rules', 
      category: 'reporting'
    },
    'report.5300.submitted': { 
      description: '5300 submitted to NCUA', 
      category: 'reporting'
    },
    'daily.close': { 
      description: 'End of day processing completed', 
      category: 'reporting'
    }
  },

  fields: {
    // ═══════════════════════════════════════════════════════════════
    // MEMBER FIELDS
    // ═══════════════════════════════════════════════════════════════
    'member_id': { 
      type: 'string', 
      description: 'Unique member identifier', 
      category: 'member', 
      pii: false 
    },
    'member.name': { 
      type: 'string', 
      description: 'Member legal name', 
      category: 'member', 
      pii: true 
    },
    'member.dob': { 
      type: 'date', 
      description: 'Date of birth', 
      category: 'member', 
      pii: true 
    },
    'member.tin': { 
      type: 'string', 
      description: 'SSN/ITIN/EIN', 
      category: 'member', 
      pii: true 
    },
    'member.address': { 
      type: 'object', 
      description: 'Member address', 
      category: 'member', 
      pii: true 
    },
    'member.email': { 
      type: 'string', 
      description: 'Email address', 
      category: 'member', 
      pii: true 
    },
    
    // ═══════════════════════════════════════════════════════════════
    // LENDING FIELDS
    // ═══════════════════════════════════════════════════════════════
    'application_id': { 
      type: 'string', 
      description: 'Application identifier', 
      category: 'lending' 
    },
    'application_type': { 
      type: 'enum', 
      description: 'Type of application', 
      category: 'lending' 
    },
    'decision_type': { 
      type: 'enum', 
      description: 'Credit decision outcome', 
      category: 'lending' 
    },
    'adverse_reasons': { 
      type: 'array', 
      description: 'Reasons for adverse action', 
      category: 'lending' 
    },
    
    // ═══════════════════════════════════════════════════════════════
    // CREDIT FIELDS
    // ═══════════════════════════════════════════════════════════════
    'credit.fico_score': { 
      type: 'integer', 
      description: 'FICO credit score', 
      category: 'credit' 
    },
    'credit.dti_ratio': { 
      type: 'number', 
      description: 'Debt-to-income ratio', 
      category: 'credit' 
    },
    
    // ═══════════════════════════════════════════════════════════════
    // MARKETING FIELDS
    // ═══════════════════════════════════════════════════════════════
    'ad_copy': { 
      type: 'string', 
      description: 'Advertisement text', 
      category: 'marketing' 
    },
    'media_geo': { 
      type: 'array', 
      description: 'Geographic targeting', 
      category: 'marketing', 
      fair_lending_risk: 'high' 
    },
    'target_demographics': { 
      type: 'object', 
      description: 'Demographic targeting', 
      category: 'marketing', 
      fair_lending_risk: 'critical' 
    },
    
    // ═══════════════════════════════════════════════════════════════
    // BSA FIELDS
    // ═══════════════════════════════════════════════════════════════
    'sar.narrative': { 
      type: 'string', 
      description: 'SAR narrative text', 
      category: 'bsa', 
      confidential: true 
    },
    'sar.subjects': { 
      type: 'array', 
      description: 'Subjects of suspicious activity', 
      category: 'bsa' 
    },
    
    // ═══════════════════════════════════════════════════════════════
    // COMPLIANCE FIELDS
    // ═══════════════════════════════════════════════════════════════
    'cip.status': { 
      type: 'enum', 
      description: 'CIP verification status', 
      category: 'compliance' 
    },
    'preflight.approved': { 
      type: 'boolean', 
      description: 'Pre-flight approval status', 
      category: 'compliance' 
    },
    
    // ═══════════════════════════════════════════════════════════════
    // SECURITY FIELDS
    // ═══════════════════════════════════════════════════════════════
    'incident.facts': { 
      type: 'string', 
      description: 'Incident details', 
      category: 'security' 
    },
    
    // ═══════════════════════════════════════════════════════════════
    // 5300 VALIDATION FIELDS
    // ═══════════════════════════════════════════════════════════════
    'validation.balance_sheet_equation': { 
      type: 'object', 
      description: 'Balance sheet validation result', 
      category: 'reporting' 
    },
    'validation.loan_reconciliation': { 
      type: 'object', 
      description: 'Loan portfolio reconciliation result', 
      category: 'reporting' 
    },
    'alert.net_worth_threshold': { 
      type: 'enum', 
      description: 'Net worth threshold alert level', 
      category: 'reporting' 
    }
  },

  sla_patterns: {
    'calendar_days': { 
      description: 'N calendar days from trigger', 
      params: ['days', 'from_event'] 
    },
    'business_days': { 
      description: 'N business days from trigger', 
      params: ['days', 'from_event'] 
    },
    'hours': { 
      description: 'N hours from trigger', 
      params: ['hours', 'from_event'] 
    },
    'before_event': { 
      description: 'Must complete before event', 
      params: ['blocking_event'], 
      blocking: true 
    },
    'immediate': { 
      description: 'Must happen immediately', 
      params: [] 
    },
  },

  regulations: {
    'ecoa_reg_b': { name: 'ECOA / Regulation B', citation: '12 CFR Part 1002' },
    'fcra': { name: 'Fair Credit Reporting Act', citation: '15 U.S.C. §1681' },
    'fha': { name: 'Fair Housing Act', citation: '42 U.S.C. §3605' },
    'reg_z': { name: 'TILA / Regulation Z', citation: '12 CFR Part 1026' },
    'bsa_aml': { name: 'Bank Secrecy Act / AML', citation: '31 CFR Part 1020' },
    'ofac': { name: 'OFAC Sanctions', citation: '31 CFR Part 501' },
    'ncua_748': { name: 'NCUA Security Program', citation: '12 CFR Part 748' },
    'ncua_701': { name: 'NCUA FCU Regulations', citation: '12 CFR Part 701' },
    'ncua_5300': { name: 'NCUA Call Report', citation: 'NCUA Form 5300' },
  },

  roles: [
    'compliance_analyst',
    'compliance_officer', 
    'fair_lending_officer',
    'bsa_officer',
    'underwriter',
    'loan_officer',
    'marketing_manager',
    'ciso',
    'cfo',
    'ceo',
    'board'
  ],

  audit_suffixes: [
    '.created', 
    '.approved', 
    '.rejected', 
    '.filed', 
    '.sent', 
    '.blocked', 
    '.override',
    '.validated',
    '.failed'
  ],

  // NCUA Account Codes - see dedicated section below
  ncua_accounts: { /* ... */ }
};
```

---

## Control Schema

```typescript
interface Control {
  id: string;           // e.g., "FL-07", "BA-05", "5300-VAL-01"
  name: string;
  description: string;
  status: 'draft' | 'active' | 'deprecated';

  // Regulatory basis
  regulations: Array<{
    id: string;         // Must exist in vocabulary.regulations
    section: string;    // Specific section citation
  }>;

  // What activates this control
  triggers: Array<{
    event: string;      // Must exist in vocabulary.events
    human_action: string;  // Plain-language description for documentation
  }>;

  // What the system must do
  system_behavior: string;  // Prose description of automated behavior

  // Data requirements
  inputs: Array<{
    field: string;      // Must exist in vocabulary.fields
    required: boolean;
    notes: string;
  }>;

  // Data produced
  outputs: Array<{
    field: string;      // Must exist in vocabulary.fields
    notes: string;
  }>;

  // Time constraints
  slas: Array<{
    description: string;
    pattern: string;    // Must exist in vocabulary.sla_patterns
    params: Record<string, any>;
  }>;

  // Audit trail
  audit_events: string[];  // Suffixes from vocabulary.audit_suffixes

  // Permissions
  access: {
    edit: string[];     // Roles that can modify
    view: string[];     // Roles that can view
    approve: string[];  // Roles that can approve
  };

  // Optional: Alert thresholds
  alerts_metrics?: Array<{
    metric: string;
    thresholds: Array<{
      level: 'warning' | 'critical' | 'emergency';
      condition: string;
      escalate_to: string[];
    }>;
  }>;
}
```

---

## Example Controls

### FL-07: Advertising & Fair Housing

```yaml
id: "FL-07"
name: "Advertising & Fair Housing"
description: "Enforce trigger-term disclosures, Fair Housing legend, prohibit exclusionary targeting"
status: active

regulations:
  - id: reg_z
    section: "§1026.24"
  - id: fha
    section: "§3605"
  - id: ncua_701
    section: "§701.31"

triggers:
  - event: campaign.created
    human_action: "Marketing creates campaign"

system_behavior: |
  Check ad copy for trigger terms. Verify Fair Housing legend for 
  real-estate ads. Analyze geo-targeting for exclusionary patterns.
  Route to compliance review. Block launch until approved.

inputs:
  - field: ad_copy
    required: true
    notes: "Scan for trigger terms"
  - field: media_geo
    required: true
    notes: "Check for exclusionary patterns"

outputs:
  - field: preflight.approved
    notes: "Set true when compliance approves"

slas:
  - description: "Approval before launch"
    pattern: before_event
    params:
      blocking_event: campaign.launched

audit_events:
  - .approved
  - .rejected

access:
  edit: [marketing_manager]
  view: [compliance_analyst]
  approve: [compliance_officer]
```

### BA-05: OFAC Screening & Holds

```yaml
id: "BA-05"
name: "OFAC Screening & Holds"
description: "Screen against OFAC lists, hold/block on match, file required reports"
status: active

regulations:
  - id: ofac
    section: "Part 501"
  - id: bsa_aml
    section: "§1020.210"

triggers:
  - event: member.created
    human_action: "New member onboarding"

system_behavior: |
  Screen all parties against SDN lists. Hold on potential match.
  Route to analyst for review. Block or reject confirmed matches.
  File required reports.

inputs:
  - field: member.name
    required: true
    notes: "Include all name variations"
  - field: member.dob
    required: true
    notes: "For identity confirmation"

outputs:
  - field: cip.status
    notes: "Screening result status"

slas:
  - description: "Hold on potential match"
    pattern: immediate
    params: {}

audit_events:
  - .approved
  - .blocked
  - .filed

access:
  edit: [compliance_analyst]
  view: [compliance_officer]
  approve: [compliance_officer]
```

### 5300-VAL-01: Balance Sheet Equation

```yaml
id: "5300-VAL-01"
name: "Balance Sheet Equation"
description: "Total Assets must equal Total Liabilities plus Equity"
status: active

regulations:
  - id: ncua_5300
    section: "Balance Sheet"

triggers:
  - event: report.5300.generated
    human_action: "5300 report generation requested"

system_behavior: |
  Validate that account 010 (Total Assets) equals account 014 
  (Total Liabilities + Equity). If not equal, block submission
  and surface the variance.

inputs:
  - field: ncua.010
    required: true
    notes: "Total Assets"
  - field: ncua.014
    required: true
    notes: "Total Liabilities + Equity"

outputs:
  - field: validation.balance_sheet_equation
    notes: "PASS/FAIL with variance amount"

slas:
  - description: "Validate before submission"
    pattern: before_event
    params:
      blocking_event: report.5300.submitted

audit_events:
  - .validated
  - .failed

access:
  view: [compliance_analyst, compliance_officer]
  approve: [compliance_officer]
```

### 5300-VAL-02: Loan Portfolio Reconciliation

```yaml
id: "5300-VAL-02"
name: "Loan Portfolio Reconciliation"
description: "Total Loans on Schedule A must equal Total Loans on Balance Sheet"
status: active

regulations:
  - id: ncua_5300
    section: "Schedule A / Balance Sheet"

triggers:
  - event: report.5300.generated
    human_action: "5300 report generation requested"

system_behavior: |
  Sum all loan categories in Schedule A and compare to account 025B.
  Surface any variance for investigation.

inputs:
  - field: ncua.025B
    required: true
    notes: "Total Loans from Balance Sheet"
  - field: schedule_a.total_loans
    required: true
    notes: "Sum of all Schedule A loan categories"

outputs:
  - field: validation.loan_reconciliation
    notes: "PASS/FAIL with variance"

slas:
  - description: "Validate before submission"
    pattern: before_event
    params:
      blocking_event: report.5300.submitted

audit_events:
  - .validated
  - .failed

access:
  view: [compliance_analyst, compliance_officer]
  approve: [compliance_officer]
```

### 5300-ALERT-01: Net Worth Ratio Threshold Alert

```yaml
id: "5300-ALERT-01"
name: "Net Worth Ratio Threshold Alert"
description: "Alert when net worth ratio approaches regulatory thresholds"
status: active

regulations:
  - id: ncua_701
    section: "§701.34"

triggers:
  - event: report.5300.generated
    human_action: "5300 calculated"
  - event: daily.close
    human_action: "End of day processing"

system_behavior: |
  Calculate net worth ratio. If below 7.5% (approaching well-capitalized 
  threshold), alert compliance. If below 7%, escalate to management.
  If below 6%, escalate to board.

inputs:
  - field: ncua.998
    required: true
    notes: "Net Worth Ratio"

outputs:
  - field: alert.net_worth_threshold
    notes: "Alert level: none | warning | critical | emergency"

slas:
  - description: "Alert within 1 hour of threshold breach"
    pattern: hours
    params:
      hours: 1

alerts_metrics:
  - metric: net_worth_ratio
    thresholds:
      - level: warning
        condition: "< 7.5%"
        escalate_to: [compliance_officer]
      - level: critical
        condition: "< 7%"
        escalate_to: [cfo, ceo]
      - level: emergency
        condition: "< 6%"
        escalate_to: [board]

audit_events:
  - .created

access:
  view: [compliance_analyst, compliance_officer, cfo, ceo]
  approve: [compliance_officer]
```

---

## Validation Rules

Controls are validated against the vocabulary at authoring time:

```typescript
interface ValidationResult {
  valid: boolean;
  errors: string[];
  warnings: string[];
}

function validateControl(control: Control, vocabulary: Vocabulary): ValidationResult {
  const errors: string[] = [];
  const warnings: string[] = [];

  // Required fields
  if (!control.id) errors.push('Control ID is required');
  if (!control.name) errors.push('Control name is required');
  if (!control.triggers?.length) errors.push('At least one trigger is required');

  // Vocabulary references - events
  control.triggers?.forEach((t, i) => {
    if (t.event && !vocabulary.events[t.event]) {
      errors.push(`Trigger ${i + 1}: Unknown event "${t.event}"`);
    }
  });

  // Vocabulary references - fields
  control.inputs?.forEach((inp, i) => {
    if (inp.field && !vocabulary.fields[inp.field]) {
      errors.push(`Input ${i + 1}: Unknown field "${inp.field}"`);
    }
  });

  control.outputs?.forEach((out, i) => {
    if (out.field && !vocabulary.fields[out.field]) {
      errors.push(`Output ${i + 1}: Unknown field "${out.field}"`);
    }
  });

  // Vocabulary references - SLA patterns
  control.slas?.forEach((sla, i) => {
    if (sla.pattern && !vocabulary.sla_patterns[sla.pattern]) {
      errors.push(`SLA ${i + 1}: Unknown pattern "${sla.pattern}"`);
    }
  });

  // Vocabulary references - regulations
  control.regulations?.forEach((reg, i) => {
    if (reg.id && !vocabulary.regulations[reg.id]) {
      errors.push(`Regulation ${i + 1}: Unknown regulation "${reg.id}"`);
    }
  });

  // Warnings for risk metadata
  control.inputs?.forEach((inp) => {
    const field = vocabulary.fields[inp.field];
    if (field?.pii) {
      warnings.push(`Input "${inp.field}" contains PII`);
    }
    if (field?.fair_lending_risk === 'critical') {
      warnings.push(`Input "${inp.field}" has critical fair lending risk`);
    }
    if (field?.confidential) {
      warnings.push(`Input "${inp.field}" is confidential`);
    }
  });

  return { valid: errors.length === 0, errors, warnings };
}
```

---

## Vocabulary Request Workflow

When compliance needs an event or field that doesn't exist in the vocabulary, they submit a request rather than inventing ad-hoc terms. This maintains vocabulary integrity while giving compliance a clear path forward.

```typescript
interface VocabularyRequest {
  request_id: string;        // e.g., "VR-2026-001"
  type: 'event' | 'field';
  control_context: string;   // Which control needs this
  
  // What they're requesting
  name: string;              // Proposed event/field name
  description: string;
  
  // Justification
  requirement: string;       // Regulatory citation or business need
  priority: 'critical' | 'high' | 'medium' | 'low';
  
  // Workflow state
  status: 'submitted' | 'under_review' | 'approved' | 'rejected' | 'implemented';
  submitted_at: string;
  submitted_by: string;
  
  // Engineering response
  engineering_notes?: string;
  estimated_delivery?: string;
  implemented_as?: string;   // Final name if different from requested
}
```

### Priority Definitions

- **Critical**: Regulatory deadline—we must have this by a specific date or face penalties
- **High**: Exam finding—regulator has identified a gap we need to close
- **Medium**: Process improvement—would make compliance more efficient
- **Low**: Nice to have—would be helpful but not urgent

---

## YAML Compilation Target

Controls compile to YAML for version control and engineering consumption:

```yaml
# Generated from Control Builder - DO NOT EDIT MANUALLY
# Control: FL-07
# Last modified: 2026-01-15T14:32:00Z
# Modified by: compliance_officer@cassandra.bank

id: "FL-07"
name: "Advertising & Fair Housing"
description: "Enforce trigger-term disclosures, Fair Housing legend, prohibit exclusionary targeting"
status: active

regulations:
  - id: reg_z
    section: "§1026.24"
  - id: fha
    section: "§3605"

triggers:
  - event: campaign.created
    human_action: "Marketing creates campaign"

system_behavior: |
  Check ad copy for trigger terms, verify Fair Housing legend,
  analyze geo-targeting for exclusionary patterns, route to
  compliance review, block launch until approved.

inputs:
  - field: ad_copy
    required: true
    notes: "Scan for trigger terms"
  - field: media_geo
    required: true
    notes: "Check for exclusionary patterns"

outputs:
  - field: preflight.approved
    notes: "Set true when compliance approves"

slas:
  - description: "Approval before launch"
    pattern: before_event
    params:
      blocking_event: campaign.launched

audit_events:
  - campaign.preflight.approved
  - campaign.preflight.rejected

access:
  edit: [marketing_manager]
  view: [compliance_analyst]
  approve: [compliance_officer]

# OpenAPI mappings (auto-generated from vocabulary)
openapi_refs:
  trigger_endpoint: "/v1/campaigns"
  trigger_operation: "createCampaign"
  input_schemas:
    - "$ref: '#/components/schemas/AdCopy'"
    - "$ref: '#/components/schemas/MediaGeography'"
```

---

## NCUA 5300 Call Report Integration

The 5300 Call Report is the primary regulatory report for credit unions. Our system should be able to generate a **real-time 5300 dashboard** that turns quarterly exam prep into a live view.

### 5300 as Proof of Concept

If we can produce an accurate, real-time 5300, we've proven:
- Our data model captures all regulatory-required fields
- Our event stream is complete enough to compute any balance
- Our calculation engine handles complex dependencies
- Our audit trail is sufficient for examiner review

### Account Code Hierarchy

The 5300 uses a hierarchical account numbering system:

| Prefix | Category |
|--------|----------|
| AS#### | Asset accounts |
| LI#### | Liability accounts |
| EQ#### | Equity accounts |
| IS#### | Income Statement accounts |
| DL#### | Delinquent loan accounts |
| CH#### | Charge-off/Recovery accounts |
| RB#### | Risk-based capital accounts |
| NW#### | Net worth related accounts |

### NCUA Account Code Schema

```typescript
interface NCUAAccountCode {
  code: string;           // e.g., "AS0009", "025B", "010"
  name: string;
  category: 'asset' | 'liability' | 'equity' | 'income' | 'expense' | 'memo';
  schedule: string;       // Which 5300 schedule uses this
  
  // Calculation dependency
  formula?: string;       // e.g., "730A + 730B + AS0007 + AS0008"
  components?: string[];  // Account codes this depends on
  
  // Mapping to core
  core_aggregation?: {
    entity: string;       // e.g., "loans", "shares", "transactions"
    filter?: object;      // How to filter the entity
    aggregation: 'sum' | 'count' | 'average';
    field: string;        // Which field to aggregate
  };
}
```

### Key Account Dependencies (Calculation DAG)

```
AS0009 (Total Cash) = 730A + 730B + AS0007 + AS0008
  ├── 730A (Cash on Hand) = AS0004 + AS0005
  ├── 730B (Cash on Deposit) = 730B1 + AS0003 + 730B2
  ├── AS0007 (Time deposits)
  └── AS0008 (All other deposits)

AS0013 (Total Investment Securities) = AS0055 + AS0061 + AS0067 + AS0073 - AS0041
  ├── AS0055 (Equity Securities)
  ├── AS0061 (Trading Debt Securities)
  ├── AS0067 (Available-for-Sale Debt Securities)
  ├── AS0073 (Held-to-Maturity Debt Securities)
  └── AS0041 (Allowance for Credit Losses on HTM)

025B (Total Loans & Leases) = Sum of all loan categories
  ├── 396 (Unsecured Credit Card Loans)
  ├── 397A (Payday Alternative Loans)
  ├── 385 (New Vehicle Loans)
  ├── 370 (Used Vehicle Loans)
  ├── 703A (1-4 Family Residential 1st Lien)
  ├── 386A (1-4 Family Residential Jr Lien)
  ├── 718A5 (Commercial RE Secured)
  └── 400P (Commercial Non-RE Secured)

010 (Total Assets) = AS0009 + AS0013 + AS0017 + 003 + 025B - 719 - AS0048 + 798A + 007 + 008 + 794 + AS0036

998 (Net Worth Ratio) = (940 + 668 + 658 + 602 + NW0004 + 925A + 1004) / 010
```

### Schedule Conditional Logic

```typescript
interface ScheduleRequirement {
  schedule: string;
  name: string;
  condition: (data: ReportData) => boolean;
  sections: string[];
}

const SCHEDULE_REQUIREMENTS: ScheduleRequirement[] = [
  {
    schedule: 'A',
    name: 'Loans',
    condition: (data) => data.accounts['025B'] > 0,
    sections: ['loans_portfolio', 'delinquent', 'charge_offs', 'other_loan_info', 
               'indirect', 'purchased_sold', 'residential', 'commercial']
  },
  {
    schedule: 'B',
    name: 'Investments',
    condition: (data) => data.accounts['AS0067'] > 0 || data.accounts['AS0073'] > 0,
    sections: ['htm_afs', 'trading', 'maturity_distribution', 'memoranda']
  },
  {
    schedule: 'C',
    name: 'Liquidity',
    condition: () => true,
    sections: ['unfunded_commitments', 'off_balance_sheet', 'contingent_liabilities', 
               'borrowing_arrangements', 'borrowing_maturity']
  },
  {
    schedule: 'D',
    name: 'Shares and Deposits',
    condition: () => true,  // Always required
    sections: ['maturity_distribution', 'insurance_computation']
  },
  {
    schedule: 'E',
    name: 'Supplemental Information',
    condition: () => true,
    sections: ['grants', 'employees', 'branches', 'remittances', 'cusos', 'msb']
  },
  {
    schedule: 'F',
    name: 'Derivatives',
    condition: (data) => data.has_derivatives,
    sections: ['derivative_positions']
  },
  {
    schedule: 'G',
    name: 'Capital Adequacy',
    condition: () => true,
    sections: ['net_worth_calculation']
  },
  {
    schedule: 'H',
    name: 'CCULR',
    condition: (data) => {
      const assets = data.accounts['010'];
      const nwRatio = data.accounts['998'];
      const offBalanceSheet = data.accounts['off_balance_total'];
      const tradingAssets = data.accounts['trading_total'];
      return assets > 500_000_000 && 
             nwRatio >= 0.09 &&
             offBalanceSheet <= assets * 0.25 &&
             tradingAssets <= assets * 0.05;
    },
    sections: ['cculr_calculation']
  },
  {
    schedule: 'I',
    name: 'Risk-Based Capital',
    condition: (data) => data.accounts['010'] > 500_000_000,
    sections: ['rbc_calculation']
  }
];
```

### Regulatory Thresholds

```yaml
thresholds:
  net_worth_classifications:
    well_capitalized:
      net_worth_ratio: ">= 7%"
      conditions: ["not_new_cu"]
      
    adequately_capitalized:
      net_worth_ratio: ">= 6%"
      
    undercapitalized:
      net_worth_ratio: "< 6%"
      
  complex_cu_threshold:
    assets: "> $500 million"
    
  commercial_loan_limits:
    member_business_loans:
      limit: "< 1.75 × net_worth"
      
  cculr_eligibility:
    assets: "> $500 million"
    net_worth_ratio: ">= 9%"
    off_balance_sheet: "<= 25% of assets"
    trading_assets: "<= 5% of assets"
```

### Cross-Schedule Validation Rules

```yaml
cross_validations:
  - rule: "Loans in Schedule A must equal loans on balance sheet"
    left: "schedule_a.total_loans"
    right: "ncua.025B"
    
  - rule: "Investments in Schedule B must equal investments on balance sheet"
    left: "schedule_b.total_investments"
    right: "ncua.AS0013"
    
  - rule: "Shares in Schedule D must equal shares on balance sheet"
    left: "schedule_d.total_shares"
    right: "ncua.018"
    
  - rule: "Off-balance sheet in Schedule C must not appear on balance sheet"
    constraint: "schedule_c items excluded from ncua.010"
```

### Real-Time 5300 Dashboard

```typescript
interface RealtimeDashboard {
  // Current state
  as_of: Date;
  reporting_period: { start: Date; end: Date };
  
  // Key metrics (always visible)
  key_metrics: {
    total_assets: { 
      code: '010', 
      value: number, 
      change_24h: number 
    };
    total_loans: { 
      code: '025B', 
      value: number, 
      change_24h: number 
    };
    total_shares: { 
      code: '018', 
      value: number, 
      change_24h: number 
    };
    net_worth_ratio: { 
      code: '998', 
      value: number, 
      threshold: 0.07, 
      status: 'well_capitalized' | 'adequately_capitalized' | 'undercapitalized' 
    };
    delinquency_rate: { 
      value: number, 
      trend: 'improving' | 'stable' | 'deteriorating' 
    };
  };
  
  // Schedule status
  schedules: Array<{
    schedule: string;
    name: string;
    required: boolean;
    status: 'complete' | 'incomplete' | 'has_errors';
    last_updated: Date;
    validation_errors: string[];
  }>;
  
  // Validation summary
  validations: {
    total_rules: number;
    passing: number;
    failing: number;
    blocked_submission: boolean;
    failing_rules: Array<{
      control_id: string;
      description: string;
      expected: number;
      actual: number;
      variance: number;
    }>;
  };
  
  // Audit readiness
  audit_readiness: {
    data_completeness: number;  // % of required fields populated
    documentation_coverage: number;  // % of balances with supporting docs
    days_since_last_reconciliation: number;
    open_exceptions: number;
  };
}
```

### API Endpoints for 5300

```yaml
/api/v1/reporting/5300:
  
  /dashboard:
    GET: Real-time 5300 dashboard
    response:
      - key_metrics
      - schedule_status
      - validation_summary
      - audit_readiness
  
  /accounts/{code}:
    GET: Single account balance with drill-down
    response:
      - current_value
      - formula (if calculated)
      - components (if calculated)
      - source_transactions (if leaf)
      - history (last 12 quarters)
  
  /schedules/{schedule}:
    GET: Complete schedule data
    parameters:
      - as_of_date
      - format: json | xml | xbrl
    response:
      - all_sections
      - validation_status
  
  /generate:
    POST: Generate complete 5300 report
    parameters:
      - reporting_period
      - asset_election: quarter_end | daily_avg | monthly_avg | quarterly_avg
    response:
      - report_id
      - status
      - validation_results
      - download_url
  
  /validate:
    POST: Run all validation rules
    response:
      - total_rules
      - results_by_rule
      - blocking_errors
      - warnings
  
  /submit:
    POST: Submit to NCUA
    preconditions:
      - all_validations_pass
      - compliance_officer_approval
    response:
      - submission_id
      - confirmation_number
      - submitted_at
  
  /history:
    GET: Historical submissions
    response:
      - past_submissions[]
      - amendments[]
      - examiner_queries[]
```

### Delinquency Aging Calculation

```typescript
// For Schedule A delinquency reporting
type DelinquencyBucket = 
  | 'current' 
  | '30-59' 
  | '60-89' 
  | '90-179' 
  | '180-359' 
  | '360+';

function calculateDelinquencyBucket(loan: Loan): DelinquencyBucket {
  const daysPastDue = differenceInDays(new Date(), loan.lastPaymentDate);
  
  if (daysPastDue < 30) return 'current';
  if (daysPastDue < 60) return '30-59';
  if (daysPastDue < 90) return '60-89';
  if (daysPastDue < 180) return '90-179';
  if (daysPastDue < 360) return '180-359';
  return '360+';
}

// Aggregate by loan type and delinquency bucket
interface DelinquencyReport {
  loan_type: string;
  ncua_code: string;
  buckets: Record<DelinquencyBucket, {
    count: number;
    balance: number;
  }>;
}
```

### Calculation Engine

```typescript
interface CalculationEngine {
  // Build dependency graph from account definitions
  buildDependencyGraph(accounts: NCUAAccountCode[]): DependencyGraph;
  
  // Calculate a single account (recursively resolving dependencies)
  calculateAccount(code: string, asOf: Date): number;
  
  // Calculate all accounts for a report
  calculateAllAccounts(asOf: Date): Record<string, number>;
  
  // Determine which accounts are affected by an event
  getAffectedAccounts(event: string): string[];
  
  // Invalidate cache for affected accounts
  invalidateCache(accounts: string[]): void;
}

// Example flow:
// 1. loan.payment.received event fires
// 2. getAffectedAccounts('loan.payment.received') → ['025B', 'delinquency.*', '010']
// 3. invalidateCache(['025B', 'delinquency.*', '010'])
// 4. Next dashboard request triggers recalculation
// 5. Only recalculate invalidated nodes, reuse cached upstream values
```

### Data Models

```typescript
interface Loan {
  id: string;
  account_code: string;      // Maps to NCUA codes (396, 385, 703A, etc.)
  type: 'consumer' | 'commercial' | 'real_estate';
  subtype: string;
  principal_balance: number;
  interest_rate: number;
  delinquency_days: number;
  delinquency_bucket: DelinquencyBucket;
  risk_weight: number;
  collateral_type?: string;
  lien_position?: 'first' | 'junior';
  origination_date: Date;
  maturity_date: Date;
}

interface Investment {
  id: string;
  account_code: string;      // AS0055, AS0061, AS0067, AS0073
  type: 'equity' | 'debt';
  classification: 'trading' | 'afs' | 'htm';
  amortized_cost: number;
  fair_value: number;
  risk_weight: number;
  purchase_date: Date;
  maturity_date?: Date;
}

interface Share {
  id: string;
  account_code: string;
  type: 'draft' | 'regular' | 'money_market' | 'certificate' | 'ira_keogh';
  balance: number;
  rate: number;
  open_date: Date;
  maturity_date?: Date;
  insured_amount: number;
  uninsured_amount: number;
}
```

---

## Performance Targets

```yaml
performance:
  # Dashboard
  dashboard_refresh: "< 2 seconds"
  single_account_drill_down: "< 500ms"
  
  # Report generation
  full_report_generation: "< 30 seconds"
  validation_suite: "< 10 seconds"
  
  # Real-time updates
  balance_update_propagation: "< 100ms"
  
  # Batch processing
  transactions_per_hour: "> 1,000,000"
  
  # Achieved through:
  caching_strategy:
    real_time:        # No caching
      - current_balance
      - transaction_status
    near_real_time:   # 1-5 minute cache
      - portfolio_summaries
      - delinquency_reports
    periodic:         # Daily cache
      - ytd_totals
      - average_balances
      - risk_calculations
    static:           # Until data changes
      - loan_terms
      - account_configurations
      - regulatory_thresholds
```

---

## Northstar Metrics

| Metric | Current (Industry) | Target |
|--------|-------------------|--------|
| Exam cycle time | 3-6 months | 2-4 weeks |
| Control automation rate | ~20% | >80% |
| SLA compliance | Unknown | >99% |
| Traceability coverage | ~30% | 100% |
| 5300 generation time | Days | <30 seconds |
| Time to answer examiner query | Hours/Days | Minutes |

---

## Benchmark

**Interactive Brokers model**: 10x net income per employee through automation of account opening, funding, risk management, clearing, settlement, and real-time financial position reporting. 

Every morning, leadership gets a comprehensive report of the entire company's financial position marked in real-time. 

**That's the operational posture we want for compliance and exams.**

Our system needs to be so good that we basically turn every exam into a real-time dashboard. If we can survive a hostile regulator examining us at any moment, we will inevitably outperform competitors who slow to a crawl whenever the examiners show up.

---

## Implementation Notes

### Data Quality Requirements
- **Precision**: All monetary values must support at least 2 decimal places
- **Rounding**: Follow NCUA rounding rules (generally round to nearest dollar)
- **Sign Convention**: Use positive for assets/income, negative for contra-accounts
- **Date/Time**: Store all timestamps in UTC, display in institution's timezone

### Audit Trail Requirements
- Every change to reportable data must be logged
- Maintain before/after values for all updates
- Track user, timestamp, and reason for changes
- Support report regeneration for any historical date

### Security Requirements
- Encrypt sensitive data at rest (AES-256)
- Encrypt data in transit (TLS 1.3)
- Implement field-level encryption for PII
- Support MFA for all user access
- Maintain detailed access logs

### Disaster Recovery
- RPO (Recovery Point Objective): < 1 hour
- RTO (Recovery Time Objective): < 4 hours
- Daily backups with 90-day retention
- Geographically distributed replicas
- Automated failover capabilities