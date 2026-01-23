# Cassandra Banking Core - Autonomous Compliance System

## Philosophy

Compliance is not a bottleneck—it's a programming problem. We design compliance like an API: well-specified interfaces instead of ad hoc checklists and PDFs.

### Core Principles

1. **Controls are the primitive, not policies.** Each control is an interface with defined inputs, outputs, triggers, events, SLAs, and KPIs. Policies are compositions of controls.

2. **Bidirectional traceability.** When the API changes, legal sees which controls are affected. When policies change, engineering sees which endpoints need updating.

3. **Event-sourced auditability.** Every control execution is an event. Every approval is a log. Every failure is measurable. Audits become real-time dashboards, not archaeological digs.

4. **Design for hostile auditors.** Build assuming we're being examined by a hostile regulator at all times. If we survive that, we outperform competitors who slow to a crawl during exams.

5. **Compliance enables speed.** A clean, observable system lets us say "yes" faster—onboarding more fintechs with more confidence.

## Control Schema

Every control follows this structure:
```yaml
control:
  id: string           # e.g., "FL-07", "AML-03"
  name: string         # Human-readable name
  why: string[]        # Regulatory citations (Reg Z §1026.24, BSA, etc.)
  
  # Execution model
  triggers: string[]   # Events that invoke this control (e.g., campaign.created)
  inputs: object       # Required data schema
  outputs: string[]    # Events/artifacts produced on completion
  
  # Constraints
  timers_slas: object  # Time requirements (e.g., "approval before launch")
  edge_cases: string[] # Known exceptions requiring human review
  
  # Observability
  audit_logs: string[] # Specific events logged
  alerts_metrics:      # KPIs and thresholds
    metric: string
    target: number
    unit: string
  
  # Access
  access_control:
    drafters: string[]   # Roles that can initiate
    approvers: string[]  # Roles that can approve
```

## Example Control
```yaml
control:
  id: "FL-07"
  name: "Advertising & Fair Housing"
  why:
    - "Reg Z §1026.24"
    - "Fair Housing Act"
    - "NCUA 701.31"
  
  triggers:
    - "campaign.created"
  
  inputs:
    ad_copy: string
    media_geo: object  # Media plan and geo-targeting config
  
  outputs:
    - "ad.preflight_approved"
  
  timers_slas:
    approval_timing: "before launch"
  
  edge_cases:
    - "Social/dynamic ads"
    - "Co-marketing partners"
  
  audit_logs:
    - "ad.preflight_approved"
    - "ad.launched"
  
  alerts_metrics:
    - metric: "ads_with_checklist_pct"
      target: 100
      unit: "percent"
  
  access_control:
    drafters: ["marketing"]
    approvers: ["compliance"]
```

## Policy Composition

Policies are compositions of controls:
```yaml
policy:
  id: string
  name: string
  regulations: string[]      # Regulatory requirements covered
  controls: string[]         # List of control IDs
  version: string            # Semantic version
  effective_date: date
  review_schedule: string    # e.g., "annual", "quarterly"
```

## Northstar Metrics

- **Exam cycle time:** Months → Weeks
- **Control automation rate:** % of controls fully automated vs. requiring manual review
- **SLA compliance:** % of control executions completing within defined timers
- **Traceability coverage:** % of API endpoints mapped to controls

## Benchmark

Interactive Brokers model: 10x net income per employee through automation of account opening, funding, risk management, clearing, settlement, and real-time financial position reporting. Every morning, leadership gets a comprehensive report of the entire company's financial position marked in real-time. That's the operational posture we want for compliance.