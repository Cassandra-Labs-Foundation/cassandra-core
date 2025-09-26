import json
import csv
import sys
from pathlib import Path
from typing import Dict, List, Set, Any
from collections import defaultdict
import codecs

class APIEndpointComparator:
    def __init__(self):
        self.apis = []
        self.all_endpoints = set()
        self.endpoint_methods = defaultdict(set)
        self.warnings = []
    
    def load_json_file(self, file_path: str) -> dict:
        """Load JSON file handling UTF-8 BOM and other encoding issues"""
        try:
            # Try UTF-8 with BOM first
            with open(file_path, 'r', encoding='utf-8-sig') as f:
                return json.load(f)
        except UnicodeDecodeError:
            # Fallback to regular UTF-8
            with open(file_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        except json.JSONDecodeError as e:
            # If JSON parsing fails, try to read and clean the content
            with open(file_path, 'rb') as f:
                content = f.read()
                # Remove BOM if present
                if content.startswith(codecs.BOM_UTF8):
                    content = content[len(codecs.BOM_UTF8):]
                return json.loads(content.decode('utf-8'))
        
    def parse_openapi(self, file_path: str) -> Dict[str, Any]:
        """Parse OpenAPI specification file"""
        data = self.load_json_file(file_path)
        
        api_name = Path(file_path).stem
        endpoints = []
        has_refs = False
        
        for path, path_item in data.get('paths', {}).items():
            # Check if this path uses $ref
            if isinstance(path_item, dict) and '$ref' in path_item:
                has_refs = True
                endpoint = {
                    'path': path,
                    'method': 'UNKNOWN',
                    'full_signature': f"UNKNOWN {path}",
                    'note': f"References external file: {path_item['$ref']}"
                }
                endpoints.append(endpoint)
                self.all_endpoints.add(f"UNKNOWN {path}")
            else:
                # Normal OpenAPI path definition
                for method in path_item.keys():
                    if method not in ['$ref', 'summary', 'description', 'servers', 'parameters']:
                        endpoint = {
                            'path': path,
                            'method': method.upper(),
                            'full_signature': f"{method.upper()} {path}"
                        }
                        endpoints.append(endpoint)
                        self.all_endpoints.add(endpoint['full_signature'])
                        self.endpoint_methods[path].add(method.upper())
        
        if has_refs:
            warning = f"Warning: {api_name} uses $ref to external files. Methods are marked as UNKNOWN."
            self.warnings.append(warning)
            print(f"  ⚠️  {warning}")
        
        return {
            'name': api_name,
            'type': 'openapi',
            'base_url': data.get('servers', [{}])[0].get('url', ''),
            'endpoints': endpoints,
            'auth_methods': list(data.get('components', {}).get('securitySchemes', {}).keys()),
            'total_endpoints': len(endpoints),
            'has_external_refs': has_refs
        }
    
    def parse_semantic_model(self, file_path: str) -> Dict[str, Any]:
        """Parse semantic model JSON file"""
        data = self.load_json_file(file_path)
        
        api_name = data.get('provider', Path(file_path).stem)
        endpoints = []
        
        for endpoint in data.get('endpoints', []):
            path = endpoint.get('path', '')
            method = endpoint.get('method', 'GET').upper()
            full_sig = f"{method} {path}"
            
            endpoints.append({
                'path': path,
                'method': method,
                'full_signature': full_sig,
                'name': endpoint.get('name', ''),
                'description': endpoint.get('description', ''),
                'confidence': endpoint.get('confidence', 0)
            })
            self.all_endpoints.add(full_sig)
            self.endpoint_methods[path].add(method)
        
        auth_methods = [m.get('type') for m in data.get('authentication', {}).get('methods', [])]
        
        return {
            'name': api_name,
            'type': 'semantic',
            'base_url': data.get('api_overview', {}).get('base_url', ''),
            'endpoints': endpoints,
            'auth_methods': auth_methods,
            'data_models': list(data.get('data_models', {}).keys()),
            'webhooks': len(data.get('webhooks', [])),
            'total_endpoints': len(endpoints)
        }
    
    def load_api_file(self, file_path: str):
        """Auto-detect and load API file"""
        try:
            data = self.load_json_file(file_path)
            
            if 'openapi' in data or 'swagger' in data:
                api_data = self.parse_openapi(file_path)
            elif 'provider' in data or 'endpoints' in data:
                api_data = self.parse_semantic_model(file_path)
            else:
                print(f"Warning: Could not determine type for {file_path}")
                return
            
            self.apis.append(api_data)
            print(f"✓ Loaded: {api_data['name']} ({api_data['total_endpoints']} endpoints)")
            
        except Exception as e:
            print(f"✗ Error loading {file_path}: {e}")
    
    def generate_path_comparison_csv(self, output_file: str = 'path_comparison.csv'):
        """Generate CSV comparing paths across APIs (regardless of method)"""
        if not self.apis:
            print("No APIs loaded.")
            return
        
        # Collect all unique paths
        all_paths = set()
        for api in self.apis:
            for endpoint in api['endpoints']:
                all_paths.add(endpoint['path'])
        
        sorted_paths = sorted(all_paths)
        
        with open(output_file, 'w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            
            # Header row
            header = ['Path'] + [api['name'] for api in self.apis]
            writer.writerow(header)
            
            # Path rows
            for path in sorted_paths:
                row = [path]
                for api in self.apis:
                    api_paths = {ep['path'] for ep in api['endpoints']}
                    methods = [ep['method'] for ep in api['endpoints'] if ep['path'] == path]
                    if path in api_paths:
                        row.append(', '.join(methods) if methods else '✓')
                    else:
                        row.append('✗')
                writer.writerow(row)
        
        print(f"✓ Path comparison saved to: {output_file}")
    
    def generate_endpoint_matrix_csv(self, output_file: str = 'endpoint_comparison.csv'):
        """Generate CSV with endpoint coverage matrix"""
        if not self.apis:
            print("No APIs loaded.")
            return
        
        sorted_endpoints = sorted(self.all_endpoints)
        
        with open(output_file, 'w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            
            # Header row
            header = ['Method', 'Path'] + [api['name'] for api in self.apis]
            writer.writerow(header)
            
            # Endpoint rows
            for endpoint in sorted_endpoints:
                parts = endpoint.split(' ', 1)
                method = parts[0] if len(parts) > 1 else 'UNKNOWN'
                path = parts[1] if len(parts) > 1 else parts[0]
                
                row = [method, path]
                for api in self.apis:
                    api_endpoints = {ep['full_signature'] for ep in api['endpoints']}
                    row.append('✓' if endpoint in api_endpoints else '✗')
                writer.writerow(row)
        
        print(f"✓ Endpoint matrix saved to: {output_file}")
    
    def generate_summary_csv(self, output_file: str = 'api_summary.csv'):
        """Generate summary comparison CSV"""
        if not self.apis:
            print("No APIs loaded.")
            return
        
        with open(output_file, 'w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            
            # Headers
            writer.writerow(['Metric'] + [api['name'] for api in self.apis])
            
            # Total Endpoints
            writer.writerow(['Total Endpoints'] + [api['total_endpoints'] for api in self.apis])
            
            # Base URL
            writer.writerow(['Base URL'] + [api.get('base_url', 'N/A') for api in self.apis])
            
            # Authentication Methods
            writer.writerow(['Authentication'] + [
                ', '.join(api.get('auth_methods', [])) or 'Not specified' 
                for api in self.apis
            ])
            
            # Has External Refs
            writer.writerow(['Uses External Refs'] + [
                'Yes' if api.get('has_external_refs') else 'No'
                for api in self.apis
            ])
            
            # Data Models (for semantic models)
            writer.writerow(['Data Models'] + [
                len(api.get('data_models', [])) if 'data_models' in api else 'N/A'
                for api in self.apis
            ])
            
            # Webhooks (for semantic models)
            writer.writerow(['Webhooks'] + [
                api.get('webhooks', 'N/A') if 'webhooks' in api else 'N/A'
                for api in self.apis
            ])
        
        print(f"✓ Summary saved to: {output_file}")
    
    def generate_detailed_csv(self, output_file: str = 'endpoint_details.csv'):
        """Generate detailed endpoint information CSV"""
        with open(output_file, 'w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            
            # Header
            writer.writerow(['API', 'Method', 'Path', 'Name', 'Description', 'Note'])
            
            # Write all endpoints
            for api in self.apis:
                for endpoint in api['endpoints']:
                    writer.writerow([
                        api['name'],
                        endpoint['method'],
                        endpoint['path'],
                        endpoint.get('name', ''),
                        endpoint.get('description', ''),
                        endpoint.get('note', '')
                    ])
        
        print(f"✓ Detailed endpoints saved to: {output_file}")

def main():
    if len(sys.argv) < 2:
        print("Usage: python api_comparison.py <file1.json> <file2.json> ...")
        print("\nExample:")
        print("  python api_comparison.py q2helix_openapi.json column_semantic_map.json")
        sys.exit(1)
    
    comparator = APIEndpointComparator()
    
    print("\n" + "="*60)
    print("LOADING API FILES")
    print("="*60 + "\n")
    
    # Load all files
    for file_path in sys.argv[1:]:
        comparator.load_api_file(file_path)
    
    if not comparator.apis:
        print("\n✗ No APIs loaded successfully. Exiting.")
        sys.exit(1)
    
    print("\n" + "="*60)
    print("GENERATING COMPARISON REPORTS")
    print("="*60 + "\n")
    
    # Generate all reports
    comparator.generate_path_comparison_csv('path_comparison.csv')
    comparator.generate_endpoint_matrix_csv('endpoint_comparison.csv')
    comparator.generate_summary_csv('api_summary.csv')
    comparator.generate_detailed_csv('endpoint_details.csv')
    
    print("\n" + "="*60)
    print("COMPARISON COMPLETE")
    print("="*60)
    print(f"\n📊 Total APIs compared: {len(comparator.apis)}")
    print(f"📍 Total unique endpoints found: {len(comparator.all_endpoints)}")
    
    if comparator.warnings:
        print(f"\n⚠️  {len(comparator.warnings)} warning(s):")
        for warning in comparator.warnings:
            print(f"   - {warning}")
    
    print("\n📁 Generated files:")
    print("   - path_comparison.csv (path-level comparison with methods)")
    print("   - endpoint_comparison.csv (full endpoint coverage matrix)")
    print("   - api_summary.csv (high-level comparison)")
    print("   - endpoint_details.csv (detailed endpoint list)")

if __name__ == "__main__":
    main()