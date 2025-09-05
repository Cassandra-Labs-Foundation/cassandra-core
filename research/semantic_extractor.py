#!/usr/bin/env python3
"""
API Documentation Semantic Extractor
Converts raw API crawler output into structured semantic representation for BaaS analysis
"""

import json
import re
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Any, Optional
from urllib.parse import urlparse
from dataclasses import dataclass

@dataclass
class ContentSection:
    """Represents a section of content with its hierarchy"""
    level: int
    title: str
    text: str
    has_endpoints: bool
    has_code: bool
    section_id: str = ""

class APISemanticExtractor:
    def __init__(self, api_docs_dir: str):
        self.api_docs_dir = Path(api_docs_dir)
        self.sections_data = None
        self.clean_text = ""
        self.crawl_report = None
        
        # Patterns for extraction
        self.http_methods = ['GET', 'POST', 'PUT', 'DELETE', 'PATCH', 'HEAD', 'OPTIONS']
        self.endpoint_patterns = [
            r'(GET|POST|PUT|DELETE|PATCH)\s+([/\w\-{}.:]+)',
            r'(GET|POST|PUT|DELETE|PATCH)\s*\n\s*([/\w\-{}.:]+)',
            r'([/\w\-{}.:]+)\s+(GET|POST|PUT|DELETE|PATCH)',
        ]
        
    def load_data(self) -> bool:
        """Load all data files from the crawler output"""
        print("📊 Loading crawler output data...")
        
        # Load sections JSON
        sections_files = list(self.api_docs_dir.glob("*_sections.json"))
        if sections_files:
            with open(sections_files[0], 'r') as f:
                self.sections_data = json.load(f)
            print(f"✅ Loaded sections data from {sections_files[0].name}")
        else:
            print("❌ No sections file found")
            return False
        
        # Load clean text
        text_files = list(self.api_docs_dir.glob("*_clean.txt"))
        if text_files:
            with open(text_files[0], 'r', encoding='utf-8') as f:
                self.clean_text = f.read()
            print(f"✅ Loaded clean text from {text_files[0].name}")
        else:
            print("❌ No clean text file found")
            return False
        
        # Load crawl report
        crawl_report_path = self.api_docs_dir / 'crawl_report.json'
        if crawl_report_path.exists():
            with open(crawl_report_path, 'r') as f:
                self.crawl_report = json.load(f)
            print(f"✅ Loaded crawl report")
        
        return True
    
    def extract_provider_info(self) -> Dict[str, Any]:
        """Extract basic provider information"""
        provider_name = "unknown"
        source_url = ""
        
        if self.crawl_report:
            source_url = self.crawl_report.get('url', '')
            # Extract provider name from URL
            if source_url:
                domain = urlparse(source_url).netloc
                provider_name = domain.split('.')[0] if domain else "unknown"
        
        # Try to extract from directory name as fallback
        if provider_name == "unknown":
            dir_name = self.api_docs_dir.name
            if '_' in dir_name:
                provider_name = dir_name.split('_')[0]
        
        return {
            "provider": provider_name,
            "source_url": source_url,
            "extracted_at": datetime.now().isoformat()
        }
    
    def build_section_hierarchy(self) -> List[ContentSection]:
        """Build hierarchical content sections from sections data and text"""
        print("🏗️  Building section hierarchy...")
        
        sections = []
        text_lines = self.clean_text.split('\n')
        current_line = 0
        
        for i, section_data in enumerate(self.sections_data):
            title = section_data.get('text', '').strip()
            level = section_data.get('level', 1)
            has_endpoints = section_data.get('hasEndpoints', False)
            has_code = section_data.get('hasCodeExamples', False)
            
            # Extract text content for this section
            section_text = self.extract_section_text(title, text_lines, current_line)
            
            sections.append(ContentSection(
                level=level,
                title=title,
                text=section_text,
                has_endpoints=has_endpoints,
                has_code=has_code,
                section_id=f"section_{i}"
            ))
        
        print(f"📋 Built {len(sections)} content sections")
        return sections
    
    def extract_section_text(self, title: str, text_lines: List[str], start_line: int) -> str:
        """Extract text content for a specific section"""
        section_text_lines = []
        found_section = False
        
        # Find the section in the text
        for i in range(start_line, len(text_lines)):
            line = text_lines[i].strip()
            
            # Check if this line matches our section title
            if title.lower() in line.lower() and len(line) < len(title) + 20:
                found_section = True
                continue
            
            if found_section:
                # Stop at next major heading (all caps, or very short line that looks like heading)
                if (line.isupper() and len(line) > 3 and len(line) < 50) or \
                   (len(line) < 50 and line.endswith(':') and line.count(' ') < 3):
                    break
                
                section_text_lines.append(line)
                
                # Limit section size to avoid too much content
                if len(section_text_lines) > 100:
                    break
        
        return '\n'.join(section_text_lines)
    
    def extract_api_overview(self, sections: List[ContentSection]) -> Dict[str, Any]:
        """Extract high-level API overview information"""
        print("🔍 Extracting API overview...")
        
        # Look for overview/introduction section
        overview_text = ""
        for section in sections[:5]:  # Check first few sections
            if any(keyword in section.title.lower() for keyword in ['introduction', 'overview', 'getting started', 'api']):
                overview_text = section.text
                break
        
        if not overview_text:
            overview_text = sections[0].text if sections else ""
        
        # Extract authentication methods
        auth_methods = []
        auth_keywords = {
            'api_key': ['api key', 'api-key', 'apikey'],
            'bearer': ['bearer token', 'bearer', 'authorization header'],
            'oauth': ['oauth', 'oauth2', 'oauth 2.0'],
            'basic': ['basic auth', 'basic authentication'],
        }
        
        overview_lower = overview_text.lower()
        for auth_type, keywords in auth_keywords.items():
            if any(keyword in overview_lower for keyword in keywords):
                auth_methods.append(auth_type)
        
        # Extract base URL
        base_url = ""
        url_pattern = r'https?://[a-zA-Z0-9\.-]+/[a-zA-Z0-9\./]*'
        urls = re.findall(url_pattern, overview_text)
        if urls:
            # Find the shortest URL (likely base URL)
            base_url = min(urls, key=len)
        
        # Extract key concepts
        key_concepts = []
        concept_patterns = [
            r'(?:create|manage|handle)\s+([a-zA-Z\s]+?)(?:\s|$|\.)',
            r'([A-Z][a-z]+(?:\s+[A-Z][a-z]+)*)\s+(?:object|entity|model)',
            r'(?:API\s+for|manage)\s+([a-zA-Z\s]+?)(?:\s|$|\.)'
        ]
        
        for pattern in concept_patterns:
            matches = re.findall(pattern, overview_text, re.IGNORECASE)
            for match in matches:
                clean_match = match.strip().lower()
                if len(clean_match) > 2 and clean_match not in key_concepts:
                    key_concepts.append(clean_match)
        
        return {
            "description": overview_text[:500] + "..." if len(overview_text) > 500 else overview_text,
            "authentication_methods": auth_methods,
            "base_url": base_url,
            "key_concepts": key_concepts[:10]  # Limit to top 10
        }
    
    def extract_endpoints(self, sections: List[ContentSection]) -> List[Dict[str, Any]]:
        """Extract API endpoints with full semantic information"""
        print("🔗 Extracting API endpoints...")
        
        endpoints = []
        endpoint_counter = 0
        
        for section in sections:
            # Skip if this section doesn't have endpoints
            if not section.has_endpoints and section.level > 3:
                continue
            
            # Look for endpoint patterns in the section
            section_endpoints = self.find_endpoints_in_section(section, sections)
            endpoints.extend(section_endpoints)
            endpoint_counter += len(section_endpoints)
        
        # Also scan the full text for any missed endpoints
        additional_endpoints = self.find_endpoints_in_text()
        
        # Merge and deduplicate
        all_endpoints = endpoints + additional_endpoints
        unique_endpoints = self.deduplicate_endpoints(all_endpoints)
        
        print(f"🎯 Found {len(unique_endpoints)} unique endpoints")
        return unique_endpoints
    
    def find_endpoints_in_section(self, section: ContentSection, all_sections: List[ContentSection]) -> List[Dict[str, Any]]:
        """Find endpoints within a specific section"""
        endpoints = []
        section_text = section.text
        
        # Build section hierarchy for context
        hierarchy = self.build_section_hierarchy_path(section, all_sections)
        
        # Look for HTTP methods followed by paths
        for pattern in self.endpoint_patterns:
            matches = re.finditer(pattern, section_text, re.MULTILINE | re.IGNORECASE)
            
            for match in matches:
                method = match.group(1).upper()
                path = match.group(2) if len(match.groups()) > 1 else ""
                
                if method in self.http_methods and path.startswith('/'):
                    endpoint = self.extract_endpoint_details(
                        method=method,
                        path=path,
                        section=section,
                        hierarchy=hierarchy,
                        context_text=section_text
                    )
                    endpoints.append(endpoint)
        
        return endpoints
    
    def build_section_hierarchy_path(self, target_section: ContentSection, all_sections: List[ContentSection]) -> List[str]:
        """Build the hierarchy path for a section"""
        hierarchy = []
        current_level = target_section.level
        
        # Work backwards to find parent sections
        target_index = None
        for i, section in enumerate(all_sections):
            if section.section_id == target_section.section_id:
                target_index = i
                break
        
        if target_index is None:
            return [target_section.title]
        
        # Build hierarchy by looking at previous sections with lower levels
        for i in range(target_index, -1, -1):
            section = all_sections[i]
            if section.level < current_level:
                hierarchy.insert(0, section.title)
                current_level = section.level
        
        # Add the target section itself
        hierarchy.append(target_section.title)
        return hierarchy
    
    def extract_endpoint_details(self, method: str, path: str, section: ContentSection, 
                                hierarchy: List[str], context_text: str) -> Dict[str, Any]:
        """Extract detailed information for a single endpoint"""
        
        # Generate unique ID
        endpoint_id = self.generate_endpoint_id(method, path, section.title)
        
        # Extract name from section title or path
        name = self.extract_endpoint_name(section.title, method, path)
        
        # Extract description
        description = self.extract_endpoint_description(context_text, method, path)
        
        # Extract parameters
        parameters = self.extract_parameters(context_text, method)
        
        # Extract responses
        responses = self.extract_responses(context_text)
        
        # Extract business rules
        business_rules = self.extract_business_rules(context_text)
        
        # Extract validation rules
        validation_rules = self.extract_validation_rules(context_text)
        
        # Extract code examples
        code_examples = self.extract_code_examples(context_text)
        
        # Extract related objects
        related_objects = self.extract_related_objects(context_text, hierarchy)
        
        return {
            "id": endpoint_id,
            "name": name,
            "method": method,
            "path": path,
            "section_hierarchy": hierarchy,
            "description": description,
            "parameters": parameters,
            "responses": responses,
            "business_rules": business_rules,
            "validation_rules": validation_rules,
            "code_examples": code_examples,
            "related_objects": related_objects
        }
    
    def generate_endpoint_id(self, method: str, path: str, section_title: str) -> str:
        """Generate a unique identifier for an endpoint"""
        # Clean path to create ID
        clean_path = re.sub(r'[^a-zA-Z0-9_]', '_', path.lower())
        clean_path = re.sub(r'_+', '_', clean_path).strip('_')
        
        # Use section title for additional context
        clean_title = re.sub(r'[^a-zA-Z0-9_]', '_', section_title.lower())
        clean_title = re.sub(r'_+', '_', clean_title).strip('_')
        
        return f"{method.lower()}_{clean_path}_{clean_title}"[:50]
    
    def extract_endpoint_name(self, section_title: str, method: str, path: str) -> str:
        """Extract human-readable name for endpoint"""
        # Try to use section title
        if section_title and not any(word in section_title.lower() for word in ['parameter', 'response', 'example']):
            return section_title
        
        # Generate from method and path
        path_parts = [part for part in path.split('/') if part and not part.startswith('{')]
        if path_parts:
            resource = path_parts[-1].replace('_', ' ').replace('-', ' ').title()
            return f"{method.title()} {resource}"
        
        return f"{method.title()} Endpoint"
    
    def extract_endpoint_description(self, text: str, method: str, path: str) -> str:
        """Extract description for an endpoint"""
        lines = text.split('\n')
        description_lines = []
        
        # Look for descriptive text near the method/path
        for i, line in enumerate(lines):
            line = line.strip()
            
            # Skip empty lines and obvious non-description content
            if not line or line.isupper() or line.startswith('#'):
                continue
            
            # Look for descriptive sentences
            if (len(line) > 20 and 
                ('.' in line or ',' in line) and 
                not line.startswith('{') and
                not any(keyword in line.lower() for keyword in ['curl', 'http', 'request', 'response'])):
                description_lines.append(line)
            
            # Stop after we have enough description
            if len(description_lines) >= 3:
                break
        
        return ' '.join(description_lines) if description_lines else f"API endpoint for {method} {path}"
    
    def extract_parameters(self, text: str, method: str) -> Dict[str, Dict[str, Any]]:
        """Extract parameter information"""
        parameters = {
            "path": {},
            "query": {},
            "body": {},
            "headers": {}
        }
        
        # Look for parameter sections
        param_patterns = [
            r'(?:Path\s+)?Parameters?:?\s*\n(.*?)(?:\n\n|\n[A-Z]|$)',
            r'Request\s+Body:?\s*\n(.*?)(?:\n\n|\n[A-Z]|$)',
            r'Query\s+Parameters?:?\s*\n(.*?)(?:\n\n|\n[A-Z]|$)',
            r'Headers?:?\s*\n(.*?)(?:\n\n|\n[A-Z]|$)'
        ]
        
        for i, pattern in enumerate(param_patterns):
            matches = re.finditer(pattern, text, re.MULTILINE | re.IGNORECASE | re.DOTALL)
            
            for match in matches:
                param_text = match.group(1)
                param_type = ["path", "body", "query", "headers"][i]
                
                # Extract individual parameters
                extracted_params = self.parse_parameter_text(param_text)
                parameters[param_type].update(extracted_params)
        
        return parameters
    
    def parse_parameter_text(self, param_text: str) -> Dict[str, Any]:
        """Parse parameter text to extract individual parameters"""
        params = {}
        
        # Look for parameter definitions
        # Pattern: parameter_name (type) - description
        param_pattern = r'(\w+)\s*\(([^)]+)\)\s*[-:]?\s*(.+?)(?=\n\w+\s*\(|\n\n|$)'
        matches = re.finditer(param_pattern, param_text, re.MULTILINE | re.DOTALL)
        
        for match in matches:
            param_name = match.group(1).strip()
            param_type = match.group(2).strip()
            description = match.group(3).strip()
            
            # Determine if required
            required = any(keyword in description.lower() for keyword in ['required', 'mandatory', 'must'])
            
            # Extract validation info
            validation = ""
            if 'format' in description.lower() or 'pattern' in description.lower():
                validation = description
            
            params[param_name] = {
                "type": param_type,
                "description": description,
                "required": required,
                "validation": validation,
                "example": ""  # Could be enhanced to extract examples
            }
        
        return params
    
    def extract_responses(self, text: str) -> Dict[str, Any]:
        """Extract response information"""
        responses = {}
        
        # Look for response sections
        response_pattern = r'(?:Response|Returns?):?\s*\n(.*?)(?:\n\n|\n[A-Z]|$)'
        matches = re.finditer(response_pattern, text, re.MULTILINE | re.IGNORECASE | re.DOTALL)
        
        for match in matches:
            response_text = match.group(1)
            
            # Look for status codes
            status_pattern = r'(\d{3})\s*[-:]?\s*(.+?)(?=\n\d{3}|\n\n|$)'
            status_matches = re.finditer(status_pattern, response_text, re.MULTILINE)
            
            for status_match in status_matches:
                status_code = status_match.group(1)
                description = status_match.group(2).strip()
                
                if status_code.startswith('2'):
                    responses[status_code] = {
                        "description": description,
                        "schema": "object",  # Could be enhanced
                        "example": ""
                    }
                else:
                    if "error_codes" not in responses:
                        responses["error_codes"] = {}
                    responses["error_codes"][status_code] = description
        
        # Default success response if none found
        if not any(k.startswith('2') for k in responses.keys() if k != "error_codes"):
            responses["200"] = {
                "description": "Successful response",
                "schema": "object",
                "example": ""
            }
        
        return responses
    
    def extract_business_rules(self, text: str) -> List[str]:
        """Extract business rules and logic statements"""
        rules = []
        
        # Look for business rule indicators
        rule_patterns = [
            r'(?:must|should|will|cannot|may not|required to)\s+(.+?)(?:\.|$)',
            r'(?:when|if)\s+(.+?)(?:then|,)',
            r'(?:only|unless)\s+(.+?)(?:\.|$)'
        ]
        
        for pattern in rule_patterns:
            matches = re.finditer(pattern, text, re.IGNORECASE)
            for match in matches:
                rule = match.group(0).strip()
                if len(rule) > 10 and rule not in rules:
                    rules.append(rule)
        
        return rules[:5]  # Limit to 5 most relevant rules
    
    def extract_validation_rules(self, text: str) -> List[str]:
        """Extract validation requirements"""
        validations = []
        
        # Look for validation patterns
        validation_patterns = [
            r'(?:format|pattern|must be|should be)\s+(.+?)(?:\.|$)',
            r'(?:minimum|maximum|length|size)\s+(.+?)(?:\.|$)',
            r'(?:valid|invalid|allowed|forbidden)\s+(.+?)(?:\.|$)'
        ]
        
        for pattern in validation_patterns:
            matches = re.finditer(pattern, text, re.IGNORECASE)
            for match in matches:
                validation = match.group(0).strip()
                if len(validation) > 5 and validation not in validations:
                    validations.append(validation)
        
        return validations[:5]
    
    def extract_code_examples(self, text: str) -> Dict[str, str]:
        """Extract code examples by language"""
        examples = {}
        
        # Look for curl examples
        curl_pattern = r'curl\s+[^\n]*(?:\n\s*[^curl\n]*)*'
        curl_matches = re.findall(curl_pattern, text, re.IGNORECASE | re.MULTILINE)
        if curl_matches:
            examples["curl"] = curl_matches[0].strip()
        
        # Look for JSON examples
        json_pattern = r'\{[^{}]*\}'
        json_matches = re.findall(json_pattern, text)
        if json_matches:
            # Find the largest JSON block
            largest_json = max(json_matches, key=len)
            if len(largest_json) > 20:
                examples["json"] = largest_json
        
        return examples
    
    def extract_related_objects(self, text: str, hierarchy: List[str]) -> List[str]:
        """Extract references to related data models"""
        objects = []
        
        # Look for object references
        object_patterns = [
            r'([A-Z][a-z]+(?:\s+[A-Z][a-z]+)*)\s+object',
            r'returns?\s+(?:a|an)\s+([A-Z][a-z]+(?:\s+[A-Z][a-z]+)*)',
            r'(?:see|refer to)\s+([A-Z][a-z]+(?:\s+[A-Z][a-z]+)*)'
        ]
        
        for pattern in object_patterns:
            matches = re.findall(pattern, text)
            for match in matches:
                if isinstance(match, tuple):
                    match = match[0]
                clean_match = match.strip()
                if clean_match and clean_match not in objects:
                    objects.append(clean_match)
        
        return objects[:5]
    
    def find_endpoints_in_text(self) -> List[Dict[str, Any]]:
        """Find any additional endpoints in the full text that might have been missed"""
        endpoints = []
        
        # This is a backup method - implementation can be added if needed
        # For now, we rely primarily on section-based extraction
        
        return endpoints
    
    def deduplicate_endpoints(self, endpoints: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Remove duplicate endpoints"""
        seen = set()
        unique_endpoints = []
        
        for endpoint in endpoints:
            # Create a key based on method and path
            key = f"{endpoint['method']}_{endpoint['path']}"
            if key not in seen:
                seen.add(key)
                unique_endpoints.append(endpoint)
        
        return unique_endpoints
    
    def extract_data_models(self, sections: List[ContentSection]) -> Dict[str, Any]:
        """Extract data model definitions"""
        print("📋 Extracting data models...")
        
        models = {}
        
        for section in sections:
            # Look for sections that define objects/models
            if (section.title.endswith('object') or 
                section.title.endswith('Object') or
                'Object Parameters' in section.title or
                section.level <= 2 and any(keyword in section.title.lower() 
                                         for keyword in ['entity', 'model', 'schema'])):
                
                model_name = self.extract_model_name(section.title)
                model_data = self.extract_model_details(section.text, model_name)
                
                if model_data:
                    models[model_name] = model_data
        
        print(f"📊 Found {len(models)} data models")
        return models
    
    def extract_model_name(self, title: str) -> str:
        """Extract model name from section title"""
        # Remove common suffixes
        name = title.replace(' object', '').replace(' Object', '').replace(' Parameters', '')
        name = name.replace('Object Parameters', '').strip()
        
        # Convert to PascalCase
        words = name.split()
        return ''.join(word.capitalize() for word in words) if words else "UnknownModel"
    
    def extract_model_details(self, text: str, model_name: str) -> Dict[str, Any]:
        """Extract detailed model information"""
        
        # Extract description (first paragraph)
        lines = [line.strip() for line in text.split('\n') if line.strip()]
        description = lines[0] if lines else f"Data model for {model_name}"
        
        # Extract properties
        properties = self.extract_model_properties(text)
        
        # Extract relationships
        relationships = self.extract_model_relationships(text)
        
        # Extract example
        example = self.extract_model_example(text)
        
        return {
            "description": description,
            "type": "object",
            "properties": properties,
            "relationships": relationships,
            "example": example
        }
    
    def extract_model_properties(self, text: str) -> Dict[str, Any]:
        """Extract model properties with types and descriptions"""
        properties = {}
        
        # Look for property definitions
        # Pattern: property_name (type) - description
        prop_pattern = r'(\w+)\s*\(([^)]+)\)\s*[-:]?\s*(.+?)(?=\n\w+\s*\(|\n\n|$)'
        matches = re.finditer(prop_pattern, text, re.MULTILINE | re.DOTALL)
        
        for match in matches:
            prop_name = match.group(1).strip()
            prop_type = match.group(2).strip().lower()
            description = match.group(3).strip()
            
            # Determine if required
            required = any(keyword in description.lower() for keyword in ['required', 'mandatory'])
            
            # Extract validation
            validation = ""
            if any(keyword in description.lower() for keyword in ['format', 'pattern', 'must be']):
                validation = description
            
            # Extract business rules
            business_rules = []
            if any(keyword in description.lower() for keyword in ['when', 'if', 'only', 'cannot']):
                business_rules.append(description)
            
            properties[prop_name] = {
                "type": prop_type,
                "description": description,
                "required": required,
                "validation": validation,
                "business_rules": business_rules,
                "example": ""
            }
        
        return properties
    
    def extract_model_relationships(self, text: str) -> List[str]:
        """Extract relationships to other models"""
        relationships = []
        
        # Look for relationship indicators
        rel_patterns = [
            r'(?:belongs to|has many|has one|contains|references)\s+([A-Z][a-z]+(?:\s+[A-Z][a-z]+)*)',
            r'(?:related to|linked to|associated with)\s+([A-Z][a-z]+(?:\s+[A-Z][a-z]+)*)'
        ]
        
        for pattern in rel_patterns:
            matches = re.findall(pattern, text, re.IGNORECASE)
            for match in matches:
                if isinstance(match, tuple):
                    match = match[0]
                relationships.append(match.strip())
        
        return relationships[:3]
    
    def extract_model_example(self, text: str) -> str:
        """Extract example JSON for the model"""
        # Look for JSON objects
        json_pattern = r'\{[^{}]*(?:\{[^{}]*\}[^{}]*)*\}'
        matches = re.findall(json_pattern, text)
        
        if matches:
            # Return the largest JSON object
            return max(matches, key=len)
        
        return ""
    
    def extract_authentication(self, sections: List[ContentSection]) -> Dict[str, Any]:
        """Extract authentication information"""
        print("🔐 Extracting authentication information...")
        
        auth_section = None
        for section in sections:
            if any(keyword in section.title.lower() for keyword in ['auth', 'security', 'token']):
                auth_section = section
                break
        
        if not auth_section:
            # Look in the overview section
            auth_section = sections[0] if sections else None
        
        methods = []
        if auth_section:
            text = auth_section.text.lower()
            
            if 'api key' in text:
                methods.append({
                    "type": "api_key",
                    "description": "API key authentication",
                    "implementation": self.extract_auth_implementation(auth_section.text, "api key"),
                    "scopes": [],
                    "examples": []
                })
            
            if 'bearer' in text or 'token' in text:
                methods.append({
                    "type": "bearer",
                    "description": "Bearer token authentication",
                    "implementation": self.extract_auth_implementation(auth_section.text, "bearer"),
                    "scopes": [],
                    "examples": []
                })
            
            if 'oauth' in text:
                methods.append({
                    "type": "oauth",
                    "description": "OAuth authentication",
                    "implementation": self.extract_auth_implementation(auth_section.text, "oauth"),
                    "scopes": self.extract_oauth_scopes(auth_section.text),
                    "examples": []
                })
        
        return {"methods": methods}
    
    def extract_auth_implementation(self, text: str, auth_type: str) -> str:
        """Extract implementation details for authentication"""
        lines = text.split('\n')
        implementation_lines = []
        
        found_auth_section = False
        for line in lines:
            if auth_type.lower() in line.lower():
                found_auth_section = True
                continue
            
            if found_auth_section:
                line = line.strip()
                if line and not line.isupper():
                    implementation_lines.append(line)
                    if len(implementation_lines) >= 3:
                        break
        
        return ' '.join(implementation_lines) if implementation_lines else f"Use {auth_type} for authentication"
    
    def extract_oauth_scopes(self, text: str) -> List[str]:
        """Extract OAuth scopes from text"""
        scopes = []
        scope_pattern = r'scope[s]?:?\s*([^\n]+)'
        matches = re.findall(scope_pattern, text, re.IGNORECASE)
        
        for match in matches:
            # Split on common delimiters
            scope_list = re.split(r'[,;|\s]+', match)
            scopes.extend([scope.strip() for scope in scope_list if scope.strip()])
        
        return scopes[:5]
    
    def extract_webhooks(self, sections: List[ContentSection]) -> List[Dict[str, Any]]:
        """Extract webhook information"""
        print("🪝 Extracting webhook information...")
        
        webhooks = []
        
        for section in sections:
            if any(keyword in section.title.lower() for keyword in ['webhook', 'event', 'notification']):
                webhook_events = self.extract_webhook_events(section.text)
                webhooks.extend(webhook_events)
        
        return webhooks
    
    def extract_webhook_events(self, text: str) -> List[Dict[str, Any]]:
        """Extract individual webhook events"""
        events = []
        
        # Look for event type patterns
        event_patterns = [
            r'([a-z_\.]+)\s*[-:]?\s*(.+?)(?=\n[a-z_\.]+\s*[-:]|\n\n|$)',
            r'Event:\s*([^\n]+)\n?(.+?)(?=Event:|\n\n|$)'
        ]
        
        for pattern in event_patterns:
            matches = re.finditer(pattern, text, re.MULTILINE | re.IGNORECASE | re.DOTALL)
            
            for match in matches:
                event_type = match.group(1).strip()
                description = match.group(2).strip() if len(match.groups()) > 1 else ""
                
                # Extract payload schema
                payload_schema = self.extract_webhook_payload(description)
                
                # Extract example payload
                example_payload = self.extract_model_example(description)
                
                events.append({
                    "event_type": event_type,
                    "description": description,
                    "payload_schema": payload_schema,
                    "example_payload": example_payload
                })
        
        return events
    
    def extract_webhook_payload(self, text: str) -> str:
        """Extract webhook payload schema"""
        # Look for payload description
        if 'payload' in text.lower():
            return "object"  # Could be enhanced to extract actual schema
        return "object"
    
    def extract_errors(self, sections: List[ContentSection]) -> Dict[str, Any]:
        """Extract error information"""
        print("⚠️ Extracting error information...")
        
        errors = {}
        
        for section in sections:
            if any(keyword in section.title.lower() for keyword in ['error', 'status', 'code']):
                section_errors = self.extract_error_codes(section.text)
                errors.update(section_errors)
        
        return errors
    
    def extract_error_codes(self, text: str) -> Dict[str, Any]:
        """Extract error codes and their descriptions"""
        errors = {}
        
        # Look for HTTP status codes with descriptions
        error_pattern = r'(\d{3})\s*[-:]?\s*(.+?)(?=\n\d{3}|\n\n|$)'
        matches = re.finditer(error_pattern, text, re.MULTILINE)
        
        for match in matches:
            code = match.group(1)
            description = match.group(2).strip()
            
            # Extract typical causes and resolution
            causes = self.extract_error_causes(description)
            resolution = self.extract_error_resolution(description)
            
            errors[code] = {
                "description": description,
                "typical_causes": causes,
                "resolution": resolution
            }
        
        return errors
    
    def extract_error_causes(self, description: str) -> List[str]:
        """Extract typical causes of an error"""
        causes = []
        
        # Look for cause indicators
        cause_patterns = [
            r'(?:caused by|due to|when)\s+(.+?)(?:\.|$)',
            r'(?:if|occurs when)\s+(.+?)(?:\.|$)'
        ]
        
        for pattern in cause_patterns:
            matches = re.findall(pattern, description, re.IGNORECASE)
            causes.extend([match.strip() for match in matches])
        
        return causes[:3]
    
    def extract_error_resolution(self, description: str) -> str:
        """Extract error resolution information"""
        # Look for resolution indicators
        resolution_patterns = [
            r'(?:to fix|resolve|solution)\s*:?\s*(.+?)(?:\.|$)',
            r'(?:should|try|ensure)\s+(.+?)(?:\.|$)'
        ]
        
        for pattern in resolution_patterns:
            match = re.search(pattern, description, re.IGNORECASE)
            if match:
                return match.group(1).strip()
        
        return ""
    
    def generate_semantic_map(self) -> Dict[str, Any]:
        """Generate the complete semantic map"""
        print("🎯 Generating semantic map...")
        
        if not self.load_data():
            raise Exception("Failed to load crawler data")
        
        # Build section hierarchy
        sections = self.build_section_hierarchy()
        
        # Extract all components
        provider_info = self.extract_provider_info()
        api_overview = self.extract_api_overview(sections)
        endpoints = self.extract_endpoints(sections)
        data_models = self.extract_data_models(sections)
        authentication = self.extract_authentication(sections)
        webhooks = self.extract_webhooks(sections)
        errors = self.extract_errors(sections)
        
        # Build the semantic map
        semantic_map = {
            **provider_info,
            "api_overview": api_overview,
            "endpoints": endpoints,
            "data_models": data_models,
            "authentication": authentication,
            "webhooks": webhooks,
            "errors": errors
        }
        
        return semantic_map
    
    def save_semantic_map(self, output_path: Optional[str] = None) -> str:
        """Generate and save the semantic map"""
        semantic_map = self.generate_semantic_map()
        
        if output_path is None:
            output_path = self.api_docs_dir / f"{semantic_map['provider']}_semantic_map.json"
        
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(semantic_map, f, indent=2, ensure_ascii=False)
        
        print(f"✅ Semantic map saved to: {output_path}")
        
        # Print summary
        print(f"\n📊 SEMANTIC EXTRACTION SUMMARY:")
        print(f"  Provider: {semantic_map['provider']}")
        print(f"  Endpoints: {len(semantic_map['endpoints'])}")
        print(f"  Data Models: {len(semantic_map['data_models'])}")
        print(f"  Auth Methods: {len(semantic_map['authentication']['methods'])}")
        print(f"  Webhooks: {len(semantic_map['webhooks'])}")
        print(f"  Error Codes: {len(semantic_map['errors'])}")
        
        return str(output_path)

def main():
    import sys
    
    if len(sys.argv) < 2:
        print("Usage: python semantic_extractor.py <api_docs_directory> [output_file]")
        print("\nExamples:")
        print("  python semantic_extractor.py column_com_api_docs")
        print("  python semantic_extractor.py stripe_com_api_docs stripe_semantic_map.json")
        sys.exit(1)
    
    api_docs_dir = sys.argv[1]
    output_file = sys.argv[2] if len(sys.argv) > 2 else None
    
    try:
        extractor = APISemanticExtractor(api_docs_dir)
        output_path = extractor.save_semantic_map(output_file)
        
        print(f"\n🎉 Semantic extraction completed successfully!")
        print(f"📄 Output file: {output_path}")
        print(f"\nYou can now use this semantic map for:")
        print(f"  • Cross-provider API comparison")
        print(f"  • Design decision analysis")
        print(f"  • Systematic evaluation of patterns")
        
    except Exception as e:
        print(f"❌ Error during semantic extraction: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()