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

## Prototype Architecture

The prototype couples the Control Builder UI directly with OpenAPI documentation to kickstart the feedback loop between legal and engineering teams.

### Core Loop

1. Legal creates/updates a control in the UI
2. Control references events, fields, endpoints from the vocabulary
3. Vocabulary is derived from (or synchronized with) OpenAPI spec
4. When OpenAPI changes, legal sees which controls are affected
5. When legal needs something that doesn't exist, they can see what's available and request what's missing

### Prototype Goals

- Legal can author controls without writing YAML directly
- Controls validate against the actual API surface
- Bidirectional traceability actually works
- The vocabulary abstraction layer is the right boundary between the two teams

### Prototype System Diagram

```
┌─────────────────────────────────────────────────────────────────┐
│                    CONTROL BUILDER UI                           │
│                  (React + TypeScript)                           │
│                                                                 │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────────────────┐ │
│  │ Control     │  │ Vocabulary  │  │ Validation              │ │
│  │ Editor      │  │ Browser     │  │ Panel                   │ │
│  │             │  │             │  │                         │ │
│  │ - Triggers  │  │ - Events    │  │ - Real-time errors     │ │
│  │ - Inputs    │  │ - Fields    │  │ - Warnings (PII, etc)  │ │
│  │ - Outputs   │  │ - Endpoints │  │ - OpenAPI links        │ │
│  │ - SLAs      │  │ - SLA types │  │                         │ │
│  └─────────────┘  └─────────────┘  └─────────────────────────┘ │
└─────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│                    VOCABULARY SERVICE                           │
│                                                                 │
│   Parses OpenAPI spec → Generates vocabulary → Validates        │
│                                                                 │
│   GET /vocabulary/events                                        │
│   GET /vocabulary/fields                                        │
│   GET /vocabulary/endpoints                                     │
│   POST /vocabulary/requests  (for missing items)                │
│   POST /controls/validate                                       │
│   POST /controls/save                                           │
└─────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│                    FILE SYSTEM / GIT                            │
│                                                                 │
│   /specs/openapi.yaml        (source of truth for API)          │
│   /vocabulary/vocabulary.yaml (derived + manual additions)      │
│   /controls/*.yaml           (compiled controls)                │
└─────────────────────────────────────────────────────────────────┘
```

---

## OpenAPI-to-Vocabulary Extraction

The vocabulary service extracts vocabulary items from the OpenAPI specification, ensuring controls reference real API capabilities.

### Extraction Logic

```typescript
interface OpenAPIExtractor {
  // Extract events from webhooks and operation responses
  extractEvents(spec: OpenAPISpec): VocabularyEvent[];
  
  // Extract fields from component schemas
  extractFields(spec: OpenAPISpec): VocabularyField[];
  
  // Extract endpoints for traceability
  extractEndpoints(spec: OpenAPISpec): Endpoint[];
  
  // Map schema properties to field metadata
  inferFieldMetadata(schema: JSONSchema): FieldMetadata;
}

// Event extraction rules
const EVENT_EXTRACTION_RULES = {
  // Webhooks become events directly
  webhooks: (webhook) => ({
    name: webhook.operationId || webhook.summary,
    description: webhook.description,
    category: inferCategoryFromPath(webhook),
    openapi_source: `#/webhooks/${webhook.name}`
  }),
  
  // POST/PUT operations can emit events
  mutations: (operation) => ({
    name: `${resourceName(operation)}.${actionName(operation)}`,
    description: operation.summary,
    category: inferCategoryFromTags(operation),
    openapi_source: `#/paths/${operation.path}/${operation.method}`
  }),
  
  // Async operations emit completion events
  asyncOperations: (operation) => ({
    name: `${resourceName(operation)}.completed`,
    description: `${operation.summary} completed`,
    category: inferCategoryFromTags(operation),
    openapi_source: `#/paths/${operation.path}/${operation.method}`
  })
};

// Field extraction from schemas
function extractFieldsFromSchema(
  schemaName: string, 
  schema: JSONSchema, 
  path: string = ''
): VocabularyField[] {
  const fields: VocabularyField[] = [];
  
  for (const [propName, propSchema] of Object.entries(schema.properties || {})) {
    const fieldPath = path ? `${path}.${propName}` : `${schemaName}.${propName}`;
    
    fields.push({
      name: fieldPath,
      type: mapOpenAPITypeToVocabulary(propSchema),
      description: propSchema.description || '',
      category: inferCategoryFromSchemaName(schemaName),
      openapi_schema: `#/components/schemas/${schemaName}/properties/${propName}`,
      // Infer compliance metadata from schema
      pii: inferPII(propName, propSchema),
      fair_lending_risk: inferFairLendingRisk(propName, propSchema),
      confidential: inferConfidentiality(propName, propSchema)
    });
    
    // Recursively extract nested objects
    if (propSchema.type === 'object' && propSchema.properties) {
      fields.push(...extractFieldsFromSchema(schemaName, propSchema, fieldPath));
    }
  }
  
  return fields;
}

// PII inference heuristics
function inferPII(fieldName: string, schema: JSONSchema): boolean {
  const piiPatterns = [
    /ssn|social.?security/i,
    /tin|tax.?id/i,
    /dob|birth.?date|date.?of.?birth/i,
    /address|street|city|zip|postal/i,
    /phone|mobile|cell/i,
    /email/i,
    /name|first.?name|last.?name|full.?name/i,
    /passport|license|id.?number/i
  ];
  
  return piiPatterns.some(pattern => 
    pattern.test(fieldName) || pattern.test(schema.description || '')
  );
}

// Fair lending risk inference
function inferFairLendingRisk(
  fieldName: string, 
  schema: JSONSchema
): 'low' | 'medium' | 'high' | 'critical' | undefined {
  const criticalPatterns = [/race|ethnicity|national.?origin|sex|gender|religion/i];
  const highPatterns = [/age|marital|familial|disability|geographic|zip|census/i];
  const mediumPatterns = [/income|employment|occupation/i];
  
  const text = `${fieldName} ${schema.description || ''}`;
  
  if (criticalPatterns.some(p => p.test(text))) return 'critical';
  if (highPatterns.some(p => p.test(text))) return 'high';
  if (mediumPatterns.some(p => p.test(text))) return 'medium';
  return undefined;
}
```

### Vocabulary Synchronization

```typescript
interface VocabularySyncResult {
  added: { events: string[]; fields: string[]; endpoints: string[] };
  removed: { events: string[]; fields: string[]; endpoints: string[] };
  modified: { events: string[]; fields: string[]; endpoints: string[] };
  affectedControls: ControlImpact[];
}

interface ControlImpact {
  controlId: string;
  controlName: string;
  impactType: 'broken' | 'warning' | 'info';
  details: string[];
}

// Sync vocabulary when OpenAPI spec changes
async function syncVocabulary(
  previousSpec: OpenAPISpec,
  currentSpec: OpenAPISpec,
  existingControls: Control[]
): Promise<VocabularySyncResult> {
  const previousVocab = extractVocabulary(previousSpec);
  const currentVocab = extractVocabulary(currentSpec);
  
  const diff = computeVocabularyDiff(previousVocab, currentVocab);
  
  // Find affected controls
  const affectedControls = existingControls
    .map(control => computeControlImpact(control, diff))
    .filter(impact => impact.details.length > 0);
  
  return {
    ...diff,
    affectedControls
  };
}

function computeControlImpact(
  control: Control, 
  diff: VocabularyDiff
): ControlImpact {
  const details: string[] = [];
  let impactType: 'broken' | 'warning' | 'info' = 'info';
  
  // Check triggers
  control.triggers?.forEach(trigger => {
    if (diff.removed.events.includes(trigger.event)) {
      details.push(`Trigger event "${trigger.event}" was removed from API`);
      impactType = 'broken';
    } else if (diff.modified.events.includes(trigger.event)) {
      details.push(`Trigger event "${trigger.event}" was modified`);
      if (impactType !== 'broken') impactType = 'warning';
    }
  });
  
  // Check inputs
  control.inputs?.forEach(input => {
    if (diff.removed.fields.includes(input.field)) {
      details.push(`Input field "${input.field}" was removed from API`);
      impactType = 'broken';
    } else if (diff.modified.fields.includes(input.field)) {
      details.push(`Input field "${input.field}" was modified`);
      if (impactType !== 'broken') impactType = 'warning';
    }
  });
  
  // Check outputs
  control.outputs?.forEach(output => {
    if (diff.removed.fields.includes(output.field)) {
      details.push(`Output field "${output.field}" was removed from API`);
      impactType = 'broken';
    }
  });
  
  return {
    controlId: control.id,
    controlName: control.name,
    impactType,
    details
  };
}
```

---

## Control Builder UI Specification

### Component Architecture

```typescript
// Main application state
interface ControlBuilderState {
  // Current control being edited
  currentControl: Control | null;
  isDirty: boolean;
  
  // Vocabulary (loaded from service)
  vocabulary: Vocabulary;
  vocabularyLoading: boolean;
  
  // Validation state
  validationResult: ValidationResult | null;
  
  // UI state
  activePanel: 'editor' | 'vocabulary' | 'preview';
  vocabularyFilter: {
    category: string | null;
    search: string;
    type: 'events' | 'fields' | 'all';
  };
}

// Control Editor component props
interface ControlEditorProps {
  control: Control;
  vocabulary: Vocabulary;
  onChange: (control: Control) => void;
  onValidate: () => void;
  validationResult: ValidationResult | null;
}

// Vocabulary Browser component props
interface VocabularyBrowserProps {
  vocabulary: Vocabulary;
  filter: VocabularyFilter;
  onFilterChange: (filter: VocabularyFilter) => void;
  onSelectItem: (type: 'event' | 'field', name: string) => void;
  onRequestItem: (request: VocabularyRequest) => void;
}

// Validation Panel component props
interface ValidationPanelProps {
  result: ValidationResult | null;
  onNavigateToError: (error: ValidationError) => void;
  onOpenAPILink: (ref: string) => void;
}
```

### UI Layout

```
┌──────────────────────────────────────────────────────────────────────────┐
│  CONTROL BUILDER                                           [Save] [Export]│
├────────────────────────┬─────────────────────────┬───────────────────────┤
│                        │                         │                       │
│  CONTROL EDITOR        │  VOCABULARY BROWSER     │  VALIDATION PANEL     │
│                        │                         │                       │
│  ┌──────────────────┐  │  [Events] [Fields] [All]│  ✓ Valid              │
│  │ ID: FL-07        │  │  Search: [___________]  │                       │
│  │ Name: [________] │  │  Category: [All     ▼]  │  Errors (0)           │
│  │ Status: [draft▼] │  │                         │  ──────────           │
│  └──────────────────┘  │  ┌───────────────────┐  │                       │
│                        │  │ member.created    │  │  Warnings (2)         │
│  Regulations           │  │ member.updated    │  │  ──────────           │
│  ┌──────────────────┐  │  │ application.crea… │  │  ⚠ Input "member.tin" │
│  │ + Add regulation │  │  │ application.comp… │  │    contains PII       │
│  │ ┌──────────────┐ │  │  │ decision.recorded │  │  ⚠ Input "member.dob" │
│  │ │ reg_z §1026… │ │  │  │ ...               │  │    contains PII       │
│  │ └──────────────┘ │  │  └───────────────────┘  │                       │
│  └──────────────────┘  │                         │  OpenAPI References   │
│                        │  ┌───────────────────┐  │  ──────────────────   │
│  Triggers              │  │ DETAILS           │  │  → POST /members      │
│  ┌──────────────────┐  │  │                   │  │  → MemberSchema       │
│  │ + Add trigger    │  │  │ member.created    │  │                       │
│  │ ┌──────────────┐ │  │  │ Category: member  │  │                       │
│  │ │ Event:       │ │  │  │                   │  │  [Request Missing     │
│  │ │ [member.cre…]│ │  │  │ New member record │  │   Vocabulary Item]    │
│  │ │ Human action:│ │  │  │ created           │  │                       │
│  │ │ [__________] │ │  │  │                   │  │                       │
│  │ └──────────────┘ │  │  │ OpenAPI:          │  │                       │
│  └──────────────────┘  │  │ POST /v1/members  │  │                       │
│                        │  │ [View in Spec →]  │  │                       │
│  Inputs                │  └───────────────────┘  │                       │
│  ┌──────────────────┐  │                         │                       │
│  │ + Add input      │  │  ┌───────────────────┐  │                       │
│  │ ┌──────────────┐ │  │  │ Can't find what   │  │                       │
│  │ │ Field:       │ │  │  │ you need?         │  │                       │
│  │ │ [member.name]│ │  │  │                   │  │                       │
│  │ │ Required: [✓]│ │  │  │ [Request New      │  │                       │
│  │ │ Notes:       │ │  │  │  Vocabulary Item] │  │                       │
│  │ │ [__________] │ │  │  └───────────────────┘  │                       │
│  │ └──────────────┘ │  │                         │                       │
│  └──────────────────┘  │                         │                       │
│                        │                         │                       │
│  [+ Outputs]           │                         │                       │
│  [+ SLAs]              │                         │                       │
│  [+ Access Control]    │                         │                       │
│                        │                         │                       │
└────────────────────────┴─────────────────────────┴───────────────────────┘
```

### Autocomplete Behavior

```typescript
interface AutocompleteConfig {
  triggerCharacters: string[];
  minChars: number;
  maxSuggestions: number;
  showCategories: boolean;
  showWarnings: boolean;
}

const eventAutocomplete: AutocompleteConfig = {
  triggerCharacters: ['.'],
  minChars: 2,
  maxSuggestions: 10,
  showCategories: true,
  showWarnings: false
};

const fieldAutocomplete: AutocompleteConfig = {
  triggerCharacters: ['.'],
  minChars: 2,
  maxSuggestions: 10,
  showCategories: true,
  showWarnings: true  // Show PII, fair lending risk badges
};

interface AutocompleteSuggestion {
  value: string;
  label: string;
  description: string;
  category: string;
  badges: Array<{
    type: 'pii' | 'fair_lending' | 'confidential';
    level?: string;
  }>;
  openApiRef?: string;
}
```

### Drag-and-Drop from Vocabulary Browser

```typescript
interface DragData {
  type: 'event' | 'field' | 'regulation' | 'role';
  value: string;
  metadata: Record<string, any>;
}

type DropZone = 
  | 'triggers'      // Accept events
  | 'inputs'        // Accept fields
  | 'outputs'       // Accept fields
  | 'regulations'   // Accept regulations
  | 'access.edit'   // Accept roles
  | 'access.view'   // Accept roles
  | 'access.approve'; // Accept roles

function handleDrop(zone: DropZone, data: DragData): void {
  switch (zone) {
    case 'triggers':
      if (data.type === 'event') {
        addTrigger({ event: data.value, human_action: '' });
      }
      break;
    case 'inputs':
      if (data.type === 'field') {
        addInput({ field: data.value, required: true, notes: '' });
      }
      break;
  }
}
```

---

## Bidirectional Traceability Implementation

### Control → OpenAPI Linking

```typescript
function openAPILinkForField(fieldName: string): OpenAPILink {
  const field = vocabulary.fields[fieldName];
  if (!field.openapi_schema) {
    return { available: false, reason: 'Manual vocabulary item' };
  }
  
  return {
    available: true,
    ref: field.openapi_schema,
    specUrl: config.openApiSpecUrl,
    lineNumber: getLineNumber(parsedSpec, field.openapi_schema)
  };
}
```

### OpenAPI → Control Impact Analysis

```typescript
async function analyzeOpenAPIChange(
  previousCommit: string,
  currentCommit: string
): Promise<ImpactReport> {
  const previousSpec = await loadSpec(previousCommit);
  const currentSpec = await loadSpec(currentCommit);
  
  const syncResult = await syncVocabulary(previousSpec, currentSpec, controls);
  
  return {
    vocabularyChanges: syncResult,
    brokenControls: syncResult.affectedControls.filter(c => c.impactType === 'broken'),
    warningControls: syncResult.affectedControls.filter(c => c.impactType === 'warning'),
    report: generateImpactReport(syncResult)
  };
}

function generateImpactReport(syncResult: VocabularySyncResult): string {
  let report = '# OpenAPI Change Impact Report\n\n';
  
  if (syncResult.affectedControls.some(c => c.impactType === 'broken')) {
    report += '## 🚨 BREAKING CHANGES\n\n';
    report += 'The following controls reference vocabulary items that were removed:\n\n';
    
    syncResult.affectedControls
      .filter(c => c.impactType === 'broken')
      .forEach(control => {
        report += `### ${control.controlId}: ${control.controlName}\n`;
        control.details.forEach(detail => {
          report += `- ${detail}\n`;
        });
        report += '\n';
      });
  }
  
  return report;
}
```

### Traceability Matrix

```typescript
interface TraceabilityMatrix {
  endpointToControls: Map<string, Control[]>;
  controlToEndpoints: Map<string, string[]>;
  regulationToControls: Map<string, Control[]>;
  controlToRegulations: Map<string, string[]>;
}

function buildTraceabilityMatrix(
  controls: Control[],
  vocabulary: Vocabulary
): TraceabilityMatrix {
  const matrix: TraceabilityMatrix = {
    endpointToControls: new Map(),
    controlToEndpoints: new Map(),
    regulationToControls: new Map(),
    controlToRegulations: new Map()
  };
  
  for (const control of controls) {
    const endpoints: string[] = [];
    
    control.triggers?.forEach(trigger => {
      const event = vocabulary.events[trigger.event];
      if (event?.openapi_source) {
        endpoints.push(event.openapi_source);
        
        if (!matrix.endpointToControls.has(event.openapi_source)) {
          matrix.endpointToControls.set(event.openapi_source, []);
        }
        matrix.endpointToControls.get(event.openapi_source)!.push(control);
      }
    });
    
    matrix.controlToEndpoints.set(control.id, [...new Set(endpoints)]);
    
    const regulations = control.regulations?.map(r => r.id) || [];
    matrix.controlToRegulations.set(control.id, regulations);
    
    regulations.forEach(regId => {
      if (!matrix.regulationToControls.has(regId)) {
        matrix.regulationToControls.set(regId, []);
      }
      matrix.regulationToControls.get(regId)!.push(control);
    });
  }
  
  return matrix;
}
```

---

## Vocabulary Service API

```yaml
openapi: 3.0.3
info:
  title: Vocabulary Service API
  version: 1.0.0

paths:
  /vocabulary:
    get:
      summary: Get complete vocabulary
      responses:
        '200':
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/Vocabulary'

  /vocabulary/events:
    get:
      summary: List all events
      parameters:
        - name: category
          in: query
          schema:
            type: string
        - name: search
          in: query
          schema:
            type: string

  /vocabulary/fields:
    get:
      summary: List all fields
      parameters:
        - name: category
          in: query
          schema:
            type: string
        - name: pii
          in: query
          schema:
            type: boolean
        - name: fair_lending_risk
          in: query
          schema:
            type: string
            enum: [low, medium, high, critical]

  /vocabulary/sync:
    post:
      summary: Sync vocabulary from OpenAPI spec
      requestBody:
        content:
          application/json:
            schema:
              type: object
              properties:
                openapi_spec_url:
                  type: string
                  format: uri

  /vocabulary/requests:
    get:
      summary: List vocabulary requests
    post:
      summary: Submit vocabulary request

  /controls:
    get:
      summary: List all controls
    post:
      summary: Create new control

  /controls/{id}:
    get:
      summary: Get control by ID
    put:
      summary: Update control

  /controls/validate:
    post:
      summary: Validate control against vocabulary

  /controls/impact:
    post:
      summary: Check impact of vocabulary changes on controls

  /controls/{id}/yaml:
    get:
      summary: Export control as YAML

  /openapi/link:
    get:
      summary: Get OpenAPI spec location for a vocabulary item
```

---

## Vocabulary Schema (Engineering-Owned)

The vocabulary is the contract between compliance and engineering. Engineering maintains it; compliance references it.

```typescript
interface Vocabulary {
  events: Record<string, {
    description: string;
    category: 'member' | 'lending' | 'compliance' | 'bsa' | 'marketing' | 'security' | 'investments' | 'deposits' | 'income' | 'reporting';
    openapi_source?: string;
    affects_accounts?: string[];
  }>;

  fields: Record<string, {
    type: 'string' | 'number' | 'boolean' | 'date' | 'object' | 'array' | 'enum';
    description: string;
    category: string;
    pii?: boolean;
    fair_lending_risk?: 'low' | 'medium' | 'high' | 'critical';
    confidential?: boolean;
    openapi_schema?: string;
  }>;

  sla_patterns: Record<string, {
    description: string;
    params: string[];
    blocking?: boolean;
  }>;

  regulations: Record<string, {
    name: string;
    citation: string;
    reference_url?: string;
  }>;

  roles: string[];
  audit_suffixes: string[];
  ncua_accounts: Record<string, NCUAAccountCode>;
}
```

### Initial Vocabulary

```typescript
const VOCABULARY: Vocabulary = {
  events: {
    // MEMBER LIFECYCLE
    'member.created': { description: 'New member record created', category: 'member' },
    'member.updated': { description: 'Member profile changed', category: 'member' },
    
    // LENDING
    'application.created': { description: 'Loan/membership application submitted', category: 'lending' },
    'application.completed': { description: 'Application has all required info', category: 'lending' },
    'decision.recorded': { description: 'Credit decision made', category: 'lending' },
    'counteroffer.issued': { description: 'Counteroffer presented', category: 'lending' },
    'counteroffer.expired': { description: 'Counteroffer deadline passed', category: 'lending' },
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
    
    // COMPLIANCE / KYC
    'kyc.started': { description: 'Identity verification initiated', category: 'compliance' },
    'kyc.passed': { description: 'Identity verification successful', category: 'compliance' },
    'kyc.failed': { description: 'Identity verification failed', category: 'compliance' },
    'screening.ofac.hit': { description: 'OFAC screening potential match', category: 'compliance' },
    'screening.ofac.cleared': { description: 'OFAC match cleared', category: 'compliance' },
    
    // BSA/AML
    'cash.threshold.exceeded': { description: 'Cash transactions exceed $10k', category: 'bsa' },
    'sar.decision.required': { description: 'Case requires SAR decision', category: 'bsa' },
    'sar.filed': { description: 'SAR submitted to FinCEN', category: 'bsa' },
    
    // MARKETING
    'campaign.created': { description: 'Marketing campaign submitted', category: 'marketing' },
    'campaign.approved': { description: 'Campaign cleared for launch', category: 'marketing' },
    'campaign.launched': { description: 'Campaign went live', category: 'marketing' },
    
    // SECURITY
    'incident.detected': { description: 'Security incident identified', category: 'security' },
    'incident.reportable_determined': { description: 'Incident classified as reportable', category: 'security' },
    
    // INVESTMENTS
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
    
    // DEPOSITS / SHARES
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
    
    // REGULATORY REPORTING
    'report.5300.generated': { description: '5300 report generation initiated', category: 'reporting' },
    'report.5300.validated': { description: '5300 passed all validation rules', category: 'reporting' },
    'report.5300.submitted': { description: '5300 submitted to NCUA', category: 'reporting' },
    'daily.close': { description: 'End of day processing completed', category: 'reporting' }
  },

  fields: {
    // MEMBER FIELDS
    'member_id': { type: 'string', description: 'Unique member identifier', category: 'member', pii: false },
    'member.name': { type: 'string', description: 'Member legal name', category: 'member', pii: true },
    'member.dob': { type: 'date', description: 'Date of birth', category: 'member', pii: true },
    'member.tin': { type: 'string', description: 'SSN/ITIN/EIN', category: 'member', pii: true },
    'member.address': { type: 'object', description: 'Member address', category: 'member', pii: true },
    'member.email': { type: 'string', description: 'Email address', category: 'member', pii: true },
    
    // LENDING FIELDS
    'application_id': { type: 'string', description: 'Application identifier', category: 'lending' },
    'application_type': { type: 'enum', description: 'Type of application', category: 'lending' },
    'decision_type': { type: 'enum', description: 'Credit decision outcome', category: 'lending' },
    'adverse_reasons': { type: 'array', description: 'Reasons for adverse action', category: 'lending' },
    
    // CREDIT FIELDS
    'credit.fico_score': { type: 'number', description: 'FICO credit score', category: 'credit' },
    'credit.dti_ratio': { type: 'number', description: 'Debt-to-income ratio', category: 'credit' },
    
    // MARKETING FIELDS
    'ad_copy': { type: 'string', description: 'Advertisement text', category: 'marketing' },
    'media_geo': { type: 'array', description: 'Geographic targeting', category: 'marketing', fair_lending_risk: 'high' },
    'target_demographics': { type: 'object', description: 'Demographic targeting', category: 'marketing', fair_lending_risk: 'critical' },
    
    // BSA FIELDS
    'sar.narrative': { type: 'string', description: 'SAR narrative text', category: 'bsa', confidential: true },
    'sar.subjects': { type: 'array', description: 'Subjects of suspicious activity', category: 'bsa' },
    
    // COMPLIANCE FIELDS
    'cip.status': { type: 'enum', description: 'CIP verification status', category: 'compliance' },
    'preflight.approved': { type: 'boolean', description: 'Pre-flight approval status', category: 'compliance' },
    
    // SECURITY FIELDS
    'incident.facts': { type: 'string', description: 'Incident details', category: 'security' },
    
    // 5300 VALIDATION FIELDS
    'validation.balance_sheet_equation': { type: 'object', description: 'Balance sheet validation result', category: 'reporting' },
    'validation.loan_reconciliation': { type: 'object', description: 'Loan portfolio reconciliation result', category: 'reporting' },
    'alert.net_worth_threshold': { type: 'enum', description: 'Net worth threshold alert level', category: 'reporting' }
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
    'ncua_5300': { name: 'NCUA Call Report', citation: 'NCUA Form 5300' },
  },

  roles: [
    'compliance_analyst', 'compliance_officer', 'fair_lending_officer',
    'bsa_officer', 'underwriter', 'loan_officer', 'marketing_manager',
    'ciso', 'cfo', 'ceo', 'board'
  ],

  audit_suffixes: ['.created', '.approved', '.rejected', '.filed', '.sent', '.blocked', '.override', '.validated', '.failed'],

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

  regulations: Array<{
    id: string;         // Must exist in vocabulary.regulations
    section: string;    // Specific section citation
  }>;

  triggers: Array<{
    event: string;      // Must exist in vocabulary.events
    human_action: string;
  }>;

  system_behavior: string;

  inputs: Array<{
    field: string;      // Must exist in vocabulary.fields
    required: boolean;
    notes: string;
  }>;

  outputs: Array<{
    field: string;      // Must exist in vocabulary.fields
    notes: string;
  }>;

  slas: Array<{
    description: string;
    pattern: string;    // Must exist in vocabulary.sla_patterns
    params: Record<string, any>;
  }>;

  audit_events: string[];

  access: {
    edit: string[];
    view: string[];
    approve: string[];
  };

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

---

## Validation Rules

```typescript
interface ValidationResult {
  valid: boolean;
  errors: ValidationError[];
  warnings: ValidationWarning[];
}

interface ValidationError {
  path: string;
  message: string;
  suggestion?: string;
}

interface ValidationWarning {
  path: string;
  message: string;
  type: 'pii' | 'fair_lending' | 'confidential';
}

function validateControl(control: Control, vocabulary: Vocabulary): ValidationResult {
  const errors: ValidationError[] = [];
  const warnings: ValidationWarning[] = [];

  // Required fields
  if (!control.id) errors.push({ path: 'id', message: 'Control ID is required' });
  if (!control.name) errors.push({ path: 'name', message: 'Control name is required' });
  if (!control.triggers?.length) errors.push({ path: 'triggers', message: 'At least one trigger is required' });

  // Vocabulary references - events
  control.triggers?.forEach((t, i) => {
    if (t.event && !vocabulary.events[t.event]) {
      const suggestion = findClosestMatch(t.event, Object.keys(vocabulary.events));
      errors.push({
        path: `triggers[${i}].event`,
        message: `Unknown event "${t.event}"`,
        suggestion: suggestion ? `Did you mean "${suggestion}"?` : undefined
      });
    }
  });

  // Vocabulary references - fields
  control.inputs?.forEach((inp, i) => {
    if (inp.field && !vocabulary.fields[inp.field]) {
      const suggestion = findClosestMatch(inp.field, Object.keys(vocabulary.fields));
      errors.push({
        path: `inputs[${i}].field`,
        message: `Unknown field "${inp.field}"`,
        suggestion: suggestion ? `Did you mean "${suggestion}"?` : undefined
      });
    }
  });

  // Warnings for risk metadata
  control.inputs?.forEach((inp, i) => {
    const field = vocabulary.fields[inp.field];
    if (field?.pii) {
      warnings.push({
        path: `inputs[${i}].field`,
        message: `Input "${inp.field}" contains PII - ensure appropriate handling`,
        type: 'pii'
      });
    }
    if (field?.fair_lending_risk === 'critical') {
      warnings.push({
        path: `inputs[${i}].field`,
        message: `Input "${inp.field}" has critical fair lending risk - review required`,
        type: 'fair_lending'
      });
    }
  });

  return { valid: errors.length === 0, errors, warnings };
}
```

---

## Vocabulary Request Workflow

```typescript
interface VocabularyRequest {
  request_id: string;
  type: 'event' | 'field';
  control_context: string;
  name: string;
  description: string;
  requirement: string;
  priority: 'critical' | 'high' | 'medium' | 'low';
  status: 'submitted' | 'under_review' | 'approved' | 'rejected' | 'implemented';
  submitted_at: string;
  submitted_by: string;
  engineering_notes?: string;
  estimated_delivery?: string;
  implemented_as?: string;
}
```

### Priority Definitions

| Priority | Definition | SLA |
|----------|------------|-----|
| **Critical** | Regulatory deadline—we must have this by a specific date or face penalties | 48 hours |
| **High** | Exam finding—regulator has identified a gap we need to close | 1 week |
| **Medium** | Process improvement—would make compliance more efficient | 2 weeks |
| **Low** | Nice to have—would be helpful but not urgent | Backlog |

---

## YAML Compilation Target

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

### NCUA Account Code Schema

```typescript
interface NCUAAccountCode {
  code: string;
  name: string;
  category: 'asset' | 'liability' | 'equity' | 'income' | 'expense' | 'memo';
  schedule: string;
  formula?: string;
  components?: string[];
  core_aggregation?: {
    entity: string;
    filter?: object;
    aggregation: 'sum' | 'count' | 'average';
    field: string;
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

010 (Total Assets) = AS0009 + AS0013 + AS0017 + 003 + 025B - 719 - AS0048 + 798A + 007 + 008 + 794 + AS0036

998 (Net Worth Ratio) = (940 + 668 + 658 + 602 + NW0004 + 925A + 1004) / 010
```

### Real-Time 5300 Dashboard

```typescript
interface RealtimeDashboard {
  as_of: Date;
  reporting_period: { start: Date; end: Date };
  
  key_metrics: {
    total_assets: { code: '010', value: number, change_24h: number };
    total_loans: { code: '025B', value: number, change_24h: number };
    total_shares: { code: '018', value: number, change_24h: number };
    net_worth_ratio: { 
      code: '998', 
      value: number, 
      threshold: 0.07, 
      status: 'well_capitalized' | 'adequately_capitalized' | 'undercapitalized' 
    };
    delinquency_rate: { value: number, trend: 'improving' | 'stable' | 'deteriorating' };
  };
  
  schedules: Array<{
    schedule: string;
    name: string;
    required: boolean;
    status: 'complete' | 'incomplete' | 'has_errors';
    last_updated: Date;
    validation_errors: string[];
  }>;
  
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
  
  audit_readiness: {
    data_completeness: number;
    documentation_coverage: number;
    days_since_last_reconciliation: number;
    open_exceptions: number;
  };
}
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
```

---

## Performance Targets

```yaml
performance:
  dashboard_refresh: "< 2 seconds"
  single_account_drill_down: "< 500ms"
  full_report_generation: "< 30 seconds"
  validation_suite: "< 10 seconds"
  balance_update_propagation: "< 100ms"
  transactions_per_hour: "> 1,000,000"
  
  caching_strategy:
    real_time: [current_balance, transaction_status]
    near_real_time: [portfolio_summaries, delinquency_reports]
    periodic: [ytd_totals, average_balances, risk_calculations]
    static: [loan_terms, account_configurations, regulatory_thresholds]
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

---

## Implementation Roadmap

### Phase 1: Prototype (Weeks 1-4)

**Goal**: Get the feedback loop spinning between legal and engineering.

| Week | Deliverable |
|------|-------------|
| 1 | Vocabulary Service: Parse OpenAPI spec, expose vocabulary endpoints |
| 2 | Control Builder UI: Basic editor with autocomplete against vocabulary |
| 3 | Validation: Real-time validation, did-you-mean suggestions, PII warnings |
| 4 | Bidirectional links: Click-through to OpenAPI spec, impact analysis on spec changes |

**Success criteria**:
- Legal can create a control referencing real API events/fields
- Validation errors surface immediately
- When engineering changes the OpenAPI spec, legal sees which controls are affected

### Phase 2: Integration (Weeks 5-8)

| Week | Deliverable |
|------|-------------|
| 5-6 | YAML compilation and Git integration |
| 7-8 | Vocabulary request workflow with priority SLAs |

### Phase 3: 5300 Engine (Weeks 9-12)

| Week | Deliverable |
|------|-------------|
| 9-10 | Calculation DAG and account dependencies |
| 11-12 | Real-time dashboard and validation suite |

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

---

## Appendix: Technology Stack (Prototype)

```yaml
frontend:
  framework: React 18 + TypeScript
  state: Zustand or Redux Toolkit
  ui_components: Radix UI + Tailwind CSS
  editor: Monaco Editor (for YAML preview)
  
backend:
  runtime: Node.js 20 or Bun
  framework: Hono or Express
  validation: Zod
  openapi_parser: "@readme/openapi-parser"
  
storage:
  controls: Git repository (YAML files)
  vocabulary: PostgreSQL or SQLite
  cache: Redis (for vocabulary lookups)
  
infrastructure:
  local_dev: Docker Compose
  ci_cd: GitHub Actions
  hosting: Fly.io or Railway (prototype)
```