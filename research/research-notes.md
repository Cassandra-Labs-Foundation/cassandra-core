We are trying to build our own banking-as-a-service API lawyer. We are a credit union that is building its own core and wants to focus on sponsor banking. As part of that process, we want to take all the API docs from the top providers, and runs analysis to identify first what are all of the decision points (as in what kind of design decisions do we need to make) and second do a compare and contrast analysis of each company’s API so that we can better understand how they each decided to address the fundamental endpoints and data structures all BaaS platforms have to expose. Let’s do this step by step, so don’t write any code yet. My first question is what is the best way to take all of the raw API documentation so that it can be ingested by an LLM.

wget --recursive --level=3 --no-parent \
     --wait=2 --random-wait \
     --user-agent="Mozilla/5.0 (compatible; research bot)" \
     --reject-regex=".*\.(css|js|png|jpg|gif|pdf)$" \
     --accept-regex=".*docs.*" \
     https://column.com/docs/

Tried using wget but the documentation info is injected using javascript so it is only able to retrieve a react shell

Used crawler.py script to retrieve pages from column. They are too large to directly give to an llm so we need a way to get only the relevant info.
Used extract_api_docs.py to clean up the files and make them small enough to give to an llm.
Created a validation script to ensure that we are collecting all the documentation data from each page.
https://column.com/docs/api/ contains all the api documentation on a single page
Created api_crawler.py to focus specifically on the api page for column.
Created api_validation.py to validate the output from api_crawler.py

Prompt:

API Documentation Semantic Extraction Task
Objective
Convert raw API documentation crawler output into a structured, semantic intermediate representation suitable for Banking-as-a-Service (BaaS) API analysis and comparison. This will enable systematic analysis of design decisions across multiple BaaS providers.

Why This Conversion Is Necessary
Current Problem: The crawler outputs two separate files:

Sections JSON: Hierarchical structure but minimal semantic content
Clean Text: Rich semantic content but lacks clear boundaries
Goal: Create a unified representation that preserves both structural relationships AND semantic meaning, enabling:

Cross-provider API comparison
Design decision analysis
Systematic evaluation of endpoint patterns, data models, and business logic
Input Files You'll Receive
{provider}_sections.json - Hierarchical section structure
{provider}_clean.txt - Full text content with descriptions, types, validation rules
Required Output Format
Use this exact JSON schema for your semantic map:

{
  "provider": "string (e.g., 'column', 'unit', 'stripe')",
  "source_url": "string",
  "extracted_at": "ISO datetime",
  "api_overview": {
    "description": "string - high-level API purpose",
    "authentication_methods": ["array of auth types"],
    "base_url": "string (if found)",
    "key_concepts": ["array of main concepts/entities"]
  },
  "endpoints": [
    {
      "id": "string - unique identifier (e.g., 'create_person_entity')",
      "name": "string - human readable name",
      "method": "string - HTTP method",
      "path": "string - URL path (extract or infer)",
      "section_hierarchy": ["array", "of", "parent", "sections"],
      "description": "string - what this endpoint does",
      "parameters": {
        "path": {
          "param_name": {
            "type": "string",
            "description": "string",
            "required": true,
            "validation": "string (if any)",
            "example": "any"
          }
        },
        "query": { /* same structure as path */ },
        "body": { /* same structure, can be nested objects */ },
        "headers": { /* same structure */ }
      },
      "responses": {
        "200": {
          "description": "string",
          "schema": "object definition or reference",
          "example": "object (if provided)"
        },
        "error_codes": {
          "400": "description",
          "401": "description"
        }
      },
      "business_rules": ["array of business logic statements"],
      "validation_rules": ["array of validation requirements"],
      "code_examples": {
        "curl": "string (if found)",
        "javascript": "string (if found)",
        "python": "string (if found)"
      },
      "related_objects": ["array of data model references"]
    }
  ],
  "data_models": {
    "ModelName": {
      "description": "string - what this model represents",
      "type": "object",
      "properties": {
        "field_name": {
          "type": "string|number|boolean|object|array",
          "description": "string - field purpose and meaning",
          "required": true,
          "validation": "string (validation rules if any)",
          "business_rules": ["array of business logic"],
          "example": "any (if provided)",
          "nested_properties": {
            /* for object types, include nested structure */
          }
        }
      },
      "relationships": ["array describing relationships to other models"],
      "example": "object (full example if provided in docs)"
    }
  },
  "authentication": {
    "methods": [
      {
        "type": "api_key|oauth|bearer|basic",
        "description": "string",
        "implementation": "string - how to implement",
        "scopes": ["array if applicable"],
        "examples": ["array of example usage"]
      }
    ]
  },
  "webhooks": [
    {
      "event_type": "string",
      "description": "string",
      "payload_schema": "object reference or definition",
      "example_payload": "object (if provided)"
    }
  ],
  "errors": {
    "error_code": {
      "description": "string",
      "typical_causes": ["array"],
      "resolution": "string"
    }
  }
}
Extraction Instructions
Step 1: Structural Analysis (from sections JSON)
Identify endpoint boundaries by looking for:

HTTP methods (GET, POST, PUT, DELETE, PATCH) at level 3
Section names containing "Create", "Update", "Get", "List", "Delete"
Sections marked with hasEndpoints: true
Identify data model definitions by looking for:

Sections ending with "object" (e.g., "Person Entity object")
Sections with "Object Parameters" subsections
Map parameter hierarchies by following level relationships:

Level 2: Major sections (endpoints, objects)
Level 3: Sub-components (parameters, methods)
Level 4+: Nested properties
Step 2: Content Extraction (from clean text)
For each endpoint identified in Step 1:

Extract the full description from the text
Find parameter definitions with types and descriptions
Look for validation rules, business logic, and examples
Capture any code examples (curl, JavaScript, etc.)
For each data model:

Extract the model description and purpose
Map all properties with their types and descriptions
Capture nested object structures
Find example JSON objects
Extract cross-cutting concerns:

Authentication patterns and implementation details
Error handling and status codes
Webhook events and payloads
Step 3: Semantic Enhancement
Identify business rules (statements about when/how/why)
Extract validation patterns (format requirements, constraints)
Map relationships between models and endpoints
Preserve compliance and regulatory notes
Capture design decisions and trade-offs mentioned
Quality Checks
Every endpoint must have: method, path (or clear indication if missing), description
Every parameter must have: type, description, required status
Preserve ALL business logic and validation rules found in text
Include complete examples when provided
Maintain traceability to source sections via section_hierarchy
Critical Requirements
Lossless extraction: Don't summarize or paraphrase descriptions
Preserve structure: Maintain object hierarchies and nesting
Business context: Include all compliance, validation, and business rules
Cross-references: Link related endpoints and data models
Examples: Include all code examples and sample responses exactly as provided
Your output will be used for systematic comparison across BaaS providers to identify design patterns, architectural decisions, and implementation approaches.

Used the prompt to create semantic_extractor.py which takes the txt and json files from our crawler output and converts to semantic representation.
Added semantic_verifier.py to check the semantic_extractor.py output for missing endpoints or other content.
Updated semantic_extractor.py based on the output of semantic verifier.

api_crawler.py is validated by api_validation.py
semantic_extractor.py is validated by semantic_verifier.py

Need to finish updating semantic extractor.
Move api/semantic crawler and validation to correct directory.

Updated semantic extractor to be more accurate.
To run semantic extractor python semantic_extractor.py column_com_api_docs
To run semantic verifier python semantic_verifier.py column_com_api_docs column_com_api_docs/column_semantic_map_improved.json

Updated semantic extractor to use less aggressive pattern matching to reduce the amount of extra endpoints
Updated version was missing all the endpoints, updating again to find endpoints
Updated semantic extractor again to improve accuracy of endpoint detection

Created python script (/endpoint_comparisons/api_comparison.py) to compare endpoints from openAPI documentation and generate a CSV file for comparisons
Convert api docs to openapi.json format and run comparison tool
How to run comparison tool: python api_comparisons.py combined_unit_openapi.json increase_openapi.json q2_openapi.json
