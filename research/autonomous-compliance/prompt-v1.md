# Autonomous Compliance

## Core Thesis

Compliance is traditionally treated as defensive overhead—a bottleneck that slows launches and adds headcount without generating revenue. We reject this framing.

**Our view: Compliance is a programming problem.** If we treat it like governance for a codebase, the solution becomes clear: design compliance like an API with well-specified interfaces instead of ad hoc checklists and PDFs.

## The Control Primitive

Compliance can be reduced to:
1. **Identifying risks**
2. **Designing well-documented controls**

The hierarchy:
- **Policies** = internal documents detailing how you comply with regulations (the *what*)
- **Procedures** = written processes that operationalize policies (the *how*)
- **Controls** = concrete things you have to do (KYC onboarding, transaction monitoring, etc.)

**Key insight:** Compliance policies are composed of smaller, reusable **controls**. Each control can be expressed as an interface with well-defined inputs, outputs, events, and KPIs. Policies are just compositions of these controls.

**The real primitive we need to integrate into our banking core is the control, not the policy document.**

## Control Interface Specification

Every control follows this structure:

```
CONTROL: [ID] — [Name]

WHY:            Regulatory citation (e.g., Reg Z §1026.24; FHA; NCUA 701.31)
SYSTEM BEHAVIOR: What the system must do
TRIGGERS:       Events that activate this control (e.g., campaign.created)
INPUTS:         Required data (e.g., ad_copy, media_geo)
OUTPUTS:        Events/artifacts produced (e.g., ad.preflight_approved)
TIMERS/SLAs:    Timing requirements (e.g., approval before launch)
EDGE CASES:     Known exceptions and handling
AUDIT LOGS:     Events to capture for audit trail
ACCESS CONTROL: Who can do what (e.g., Marketing drafts; Compliance approves)
ALERTS/METRICS: KPIs and alerting rules (e.g., % ads with checklist, target 100%)
```

### Example: FL-07 — Advertising & Fair Housing

```yaml
id: FL-07
name: Advertising & Fair Housing

why: Reg Z §1026.24; FHA; NCUA 701.31

system_behavior: |
  Enforce trigger-term disclosures; apply Fair Housing legend for 
  real-estate ads; prohibit exclusionary geo-targeting; require 
  pre-flight checklist.

triggers:
  - campaign.created

inputs:
  - ad_copy
  - media_geo (media plan/geo targeting)

outputs:
  - ad.preflight_approved

timers_slas: Approval before launch

edge_cases:
  - Social/dynamic ads
  - Co-marketing partners

audit_logs:
  - ad.preflight_approved
  - ad.launched

access_control:
  draft: Marketing
  approve: Compliance

alerts_metrics:
  - metric: "% ads with checklist"
    target: 100%
```

## Integration Model

This structure enables tight coupling between legal and engineering:

| When this happens... | This team is notified... | About this... |
|---------------------|-------------------------|---------------|
| API changes | Legal/Compliance | Which controls are affected, which policies need review |
| Policy updates | Engineering | Which endpoints and services need to be updated |

**This is the leverage most banks never get:** Instead of manually re-reviewing everything after each small change, we propagate changes through clearly mapped controls.

## The Problem with Traditional Compliance

Today, most banks won't sign a non-binding term sheet with a fintech without a Chief Compliance Officer. The CCO is expected to:

1. Draft 10–20 policies (200–400 pages total)
2. Get them approved over 4–6 months
3. Back each policy with written procedures
4. Maintain internal policies
5. Train employees
6. Coordinate independent third-party reviews
7. Operate risk-based customer due diligence
8. Run transaction monitoring

**This is slow, people-heavy, and fragile.**

## Our Advantage

Because we're building our own core, we treat **technical execution and compliance as the same problem**: knowing where the money is, how it's moving, and being able to reconstruct that story in real time with an auditable trail.

### Design Principles

1. **Hostile examiner assumption**: Design as if we're being audited by a hostile regulator at all times. If we can survive that environment, we outperform competitors who slow to a crawl when examiners show up.

2. **Compliance = observability**: Our capacity to onboard and scale fintech programs is a direct function of how observable our system is. Clean, fast systems let us say "yes" faster and with more confidence.

3. **Exams become dashboards**: The northstar is cutting down the audit/exam process from months to weeks by turning every exam into a real-time dashboard.

## The Economics

**Most of the operating cost of a bank is compliance, and most banks solve it by throwing people at the problem.**

Why big banks can't use AI for compliance:
- Policies and data are fragmented across emails, PowerPoints, and scattered SharePoint sites
- No structured systems for machine learning to operate on

**Our approach:**
- Automate controls and embed them into the core
- Dramatically reduce manual reviews, remediation projects, and one-off exceptions
- Create the structured event stream that ML systems actually need

## The Interactive Brokers Model

Interactive Brokers shows what operational excellence looks like when taken seriously:

| Capability | Their Approach | Result |
|-----------|----------------|--------|
| Account opening | Automated | Faster onboarding |
| Funding | Automated | Reduced friction |
| Risk management | Real-time margin evaluation | Constant oversight |
| Tax statements | Automated | No manual prep |
| Performance reports | Automated | Always available |
| Trade clearing/settlement | Self-clearing | No third-party dependency |
| Accounting | **Every morning the founder gets a comprehensive report about the entire company's financial position marked in real-time** | Complete visibility |

**Result: ~10x the net income per employee of Charles Schwab**

**This is the operational posture we want for compliance and exams.**

## Summary

Autonomous Compliance is not just a way to avoid fines—it's how Cassandra turns compliance into infrastructure:

- **Composable controls** wired directly into the core
- **Faster, cheaper, and more resilient** than a traditional bank
- **Real-time dashboards** instead of months-long exam prep

The northstar: cut audit/exam process from months to weeks. Our system needs to be so good that we basically turn every exam into a real-time dashboard.