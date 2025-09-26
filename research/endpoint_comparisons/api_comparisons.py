import json
import csv
import sys
from pathlib import Path
from typing import Dict, List, Set, Any
from collections import defaultdict

class APIEndpointComparator:
    def __init__(self):
        self.apis = []
        self.all_endpoints = set()
        self.endpoint_methods = defaultdict(set)
        
    def parse_openapi(self, file_path: str) -> Dict[str, Any]:
        """Parse OpenAPI specification file"""
        with open(file_path, 'r') as f:
            data = json.load(f)
        
        api_name = Path(file_path).stem
        endpoints = []
        
        for path, methods in data.get('paths', {}).items():
            for method in methods.keys():
                if method != '$ref':
                    endpoint = {
                        'path': path,
                        'method': method.upper(),
                        'full_signature': f"{method.upper()} {path}"
                    }
                    endpoints.append(endpoint)
                    self.all_endpoints.add(endpoint['full_signature'])
                    self.endpoint_methods[path].add(method.upper())
        
        return {
            'name': api_name,
            'type': 'openapi',
            'base_url': data.get('servers', [{}])[0].get('url', ''),
            'endpoints': endpoints,
            'auth_methods': list(data.get('components', {}).get('securitySchemes', {}).keys()),
            'total_endpoints': len(endpoints)
        }
    
    def parse_semantic_model(self, file_path: str) -> Dict[str, Any]:
        """Parse semantic model JSON file"""
        with open(file_path, 'r') as f:
            data = json.load(f)
        
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
            with open(file_path, 'r') as f:
                content = f.read()
                data = json.loads(content)
            
            if 'openapi' in data or 'swagger' in data:
                api_data = self.parse_openapi(file_path)
            elif 'provider' in data or 'endpoints' in data:
                api_data = self.parse_semantic_model(file_path)
            else:
                print(f"Warning: Could not determine type for {file_path}")
                return
            
            self.apis.append(api_data)
            print(f"Loaded: {api_data['name']} ({api_data['total_endpoints']} endpoints)")
            
        except Exception as e:
            print(f"Error loading {file_path}: {e}")
    
    def generate_endpoint_matrix_csv(self, output_file: str = 'endpoint_comparison.csv'):
        """Generate CSV with endpoint coverage matrix"""
        if not self.apis:
            print("No APIs loaded. Please load API files first.")
            return
        
        # Sort endpoints for consistent output
        sorted_endpoints = sorted(self.all_endpoints)
        
        with open(output_file, 'w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            
            # Header row
            header = ['Endpoint'] + [api['name'] for api in self.apis]
            writer.writerow(header)
            
            # Endpoint rows
            for endpoint in sorted_endpoints:
                row = [endpoint]
                for api in self.apis:
                    api_endpoints = {ep['full_signature'] for ep in api['endpoints']}
                    row.append('✓' if endpoint in api_endpoints else '✗')
                writer.writerow(row)
        
        print(f"Endpoint matrix saved to: {output_file}")
    
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
        
        print(f"Summary saved to: {output_file}")
    
    def generate_detailed_csv(self, output_file: str = 'endpoint_details.csv'):
        """Generate detailed endpoint information CSV"""
        with open(output_file, 'w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            
            # Header
            writer.writerow(['API', 'Method', 'Path', 'Name', 'Description', 'Confidence'])
            
            # Write all endpoints
            for api in self.apis:
                for endpoint in api['endpoints']:
                    writer.writerow([
                        api['name'],
                        endpoint['method'],
                        endpoint['path'],
                        endpoint.get('name', ''),
                        endpoint.get('description', ''),
                        endpoint.get('confidence', '')
                    ])
        
        print(f"Detailed endpoints saved to: {output_file}")
    
    def generate_coverage_report_csv(self, output_file: str = 'coverage_report.csv'):
        """Generate coverage statistics CSV"""
        with open(output_file, 'w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            
            writer.writerow(['API Name', 'Unique Endpoints', 'Shared Endpoints', 
                           'Coverage %', 'Unique Paths'])
            
            total_endpoints = len(self.all_endpoints)
            
            for api in self.apis:
                api_sigs = {ep['full_signature'] for ep in api['endpoints']}
                unique = len(api_sigs - (self.all_endpoints - api_sigs))
                shared = len(api_sigs & self.all_endpoints) - unique
                coverage = (len(api_sigs) / total_endpoints * 100) if total_endpoints > 0 else 0
                unique_paths = len({ep['path'] for ep in api['endpoints']})
                
                writer.writerow([
                    api['name'],
                    unique,
                    shared,
                    f"{coverage:.1f}%",
                    unique_paths
                ])
        
        print(f"Coverage report saved to: {output_file}")

def main():
    if len(sys.argv) < 2:
        print("Usage: python api_comparison.py <file1.json> <file2.json> ...")
        print("\nExample:")
        print("  python api_comparison.py openapi.json column_semantic_map.json")
        sys.exit(1)
    
    comparator = APIEndpointComparator()
    
    # Load all files
    for file_path in sys.argv[1:]:
        comparator.load_api_file(file_path)
    
    if not comparator.apis:
        print("No APIs loaded successfully. Exiting.")
        sys.exit(1)
    
    print("\n" + "="*60)
    print("GENERATING COMPARISON REPORTS")
    print("="*60 + "\n")
    
    # Generate all reports
    comparator.generate_endpoint_matrix_csv('endpoint_comparison.csv')
    comparator.generate_summary_csv('api_summary.csv')
    comparator.generate_detailed_csv('endpoint_details.csv')
    comparator.generate_coverage_report_csv('coverage_report.csv')
    
    print("\n" + "="*60)
    print("COMPARISON COMPLETE")
    print("="*60)
    print(f"\nTotal APIs compared: {len(comparator.apis)}")
    print(f"Total unique endpoints found: {len(comparator.all_endpoints)}")
    print("\nGenerated files:")
    print("  - endpoint_comparison.csv (coverage matrix)")
    print("  - api_summary.csv (high-level comparison)")
    print("  - endpoint_details.csv (detailed endpoint list)")
    print("  - coverage_report.csv (coverage statistics)")

if __name__ == "__main__":
    main()