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
```

---

## Vocabulary Schema (Engineering-Owned)

The vocabulary is the contract between compliance and engineering. Engineering maintains it; compliance references it.
```typescript
interface Vocabulary {
  // Events that can trigger controls
  events: Record<string, {
    description: string;
    category: 'member' | 'lending' | 'compliance' | 'bsa' | 'marketing' | 'security';
    // Link to OpenAPI operation that emits this event
    openapi_source?: string;
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
}
```

### Initial Vocabulary
```typescript
const VOCABULARY: Vocabulary = {
  events: {
    // Member lifecycle
    'member.created': { description: 'New member record created', category: 'member' },
    'member.updated': { description: 'Member profile changed', category: 'member' },
    
    // Lending
    'application.created': { description: 'Loan/membership application submitted', category: 'lending' },
    'application.completed': { description: 'Application has all required info', category: 'lending' },
    'decision.recorded': { description: 'Credit decision made', category: 'lending' },
    'counteroffer.issued': { description: 'Counteroffer presented', category: 'lending' },
    'counteroffer.expired': { description: 'Counteroffer deadline passed', category: 'lending' },
    
    // Compliance / KYC
    'kyc.started': { description: 'Identity verification initiated', category: 'compliance' },
    'kyc.passed': { description: 'Identity verification successful', category: 'compliance' },
    'kyc.failed': { description: 'Identity verification failed', category: 'compliance' },
    'screening.ofac.hit': { description: 'OFAC screening potential match', category: 'compliance' },
    'screening.ofac.cleared': { description: 'OFAC match cleared', category: 'compliance' },
    
    // BSA/AML
    'cash.threshold.exceeded': { description: 'Cash transactions exceed $10k', category: 'bsa' },
    'sar.decision.required': { description: 'Case requires SAR decision', category: 'bsa' },
    'sar.filed': { description: 'SAR submitted to FinCEN', category: 'bsa' },
    
    // Marketing
    'campaign.created': { description: 'Marketing campaign submitted', category: 'marketing' },
    'campaign.approved': { description: 'Campaign cleared for launch', category: 'marketing' },
    'campaign.launched': { description: 'Campaign went live', category: 'marketing' },
    
    // Security
    'incident.detected': { description: 'Security incident identified', category: 'security' },
    'incident.reportable_determined': { description: 'Incident classified as reportable', category: 'security' },
  },

  fields: {
    // Member fields
    'member_id': { type: 'string', description: 'Unique member identifier', category: 'member', pii: false },
    'member.name': { type: 'string', description: 'Member legal name', category: 'member', pii: true },
    'member.dob': { type: 'date', description: 'Date of birth', category: 'member', pii: true },
    'member.tin': { type: 'string', description: 'SSN/ITIN/EIN', category: 'member', pii: true },
    'member.address': { type: 'object', description: 'Member address', category: 'member', pii: true },
    'member.email': { type: 'string', description: 'Email address', category: 'member', pii: true },
    
    // Lending fields
    'application_id': { type: 'string', description: 'Application identifier', category: 'lending' },
    'application_type': { type: 'enum', description: 'Type of application', category: 'lending' },
    'decision_type': { type: 'enum', description: 'Credit decision outcome', category: 'lending' },
    'adverse_reasons': { type: 'array', description: 'Reasons for adverse action', category: 'lending' },
    
    // Credit fields
    'credit.fico_score': { type: 'integer', description: 'FICO credit score', category: 'credit' },
    'credit.dti_ratio': { type: 'number', description: 'Debt-to-income ratio', category: 'credit' },
    
    // Marketing fields
    'ad_copy': { type: 'string', description: 'Advertisement text', category: 'marketing' },
    'media_geo': { type: 'array', description: 'Geographic targeting', category: 'marketing', fair_lending_risk: 'high' },
    'target_demographics': { type: 'object', description: 'Demographic targeting', category: 'marketing', fair_lending_risk: 'critical' },
    
    // BSA fields
    'sar.narrative': { type: 'string', description: 'SAR narrative text', category: 'bsa', confidential: true },
    'sar.subjects': { type: 'array', description: 'Subjects of suspicious activity', category: 'bsa' },
    
    // Compliance fields
    'cip.status': { type: 'enum', description: 'CIP verification status', category: 'compliance' },
    'preflight.approved': { type: 'boolean', description: 'Pre-flight approval status', category: 'compliance' },
    
    // Security fields
    'incident.facts': { type: 'string', description: 'Incident details', category: 'security' },
  },

  sla_patterns: {
    'calendar_days': { description: 'N calendar days from trigger', params: ['days', 'from_event'] },
    'business_days': { description: 'N business days from trigger', params: ['days', 'from_event'] },
    'hours': { description: 'N hours from trigger', params: ['hours', 'from_event'] },
    'before_event': { description: 'Must complete before event', params: ['blocking_event'], blocking: true },
    'immediate': { description: 'Must happen immediately', params: [] },
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
  },

  roles: [
    'compliance_analyst',
    'compliance_officer', 
    'fair_lending_officer',
    'bsa_officer',
    'underwriter',
    'loan_officer',
    'marketing_manager',
    'ciso'
  ],

  audit_suffixes: ['.created', '.approved', '.rejected', '.filed', '.sent', '.blocked', '.override']
};
```

---

## Control Schema
```typescript
interface Control {
  id: string;           // e.g., "FL-07", "BA-05"
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

## Northstar Metrics

- **Exam cycle time**: Months → Weeks
- **Control automation rate**: % of controls fully automated vs. requiring manual review
- **SLA compliance**: % of control executions completing within defined timers
- **Traceability coverage**: % of API endpoints mapped to controls
- **Vocabulary coverage**: % of system events/fields referenced by at least one control

---

## Benchmark

Interactive Brokers model: 10x net income per employee through automation of account opening, funding, risk management, clearing, settlement, and real-time financial position reporting. Every morning, leadership gets a comprehensive report of the entire company's financial position marked in real-time. That's the operational posture we want for compliance and exams.