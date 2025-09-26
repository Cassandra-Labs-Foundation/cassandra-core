import json
import os
import sys
from pathlib import Path
from typing import Dict, Any, Set
from urllib.parse import urlparse, urljoin

class OpenAPIResolver:
    def __init__(self, base_dir: str):
        self.base_dir = Path(base_dir)
        self.resolved_refs = {}
        self.processed_files = set()
        
    def resolve_ref(self, ref_path: str, current_file_path: Path) -> Any:
        """Resolve a $ref reference to its actual content"""
        # Parse the reference
        if '#' in ref_path:
            file_path, json_path = ref_path.split('#', 1)
        else:
            file_path = ref_path
            json_path = ''
        
        # Resolve relative file path
        if file_path:
            if file_path.startswith('./') or file_path.startswith('../'):
                full_path = (current_file_path.parent / file_path).resolve()
            else:
                full_path = (self.base_dir / file_path).resolve()
        else:
            full_path = current_file_path
        
        # Check if we've already loaded this file
        cache_key = f"{full_path}#{json_path}"
        if cache_key in self.resolved_refs:
            return self.resolved_refs[cache_key]
        
        # Load the referenced file
        try:
            with open(full_path, 'r') as f:
                ref_data = json.load(f)
            
            # Navigate to the specific path if provided
            if json_path:
                parts = json_path.strip('/').split('/')
                for part in parts:
                    ref_data = ref_data[part]
            
            # Recursively resolve any nested $refs
            resolved_data = self.resolve_refs_in_object(ref_data, full_path)
            
            # Cache the result
            self.resolved_refs[cache_key] = resolved_data
            return resolved_data
            
        except FileNotFoundError:
            print(f"Warning: Referenced file not found: {full_path}")
            return {"error": f"Reference not found: {ref_path}"}
        except KeyError as e:
            print(f"Warning: Path not found in file {full_path}: {json_path}")
            return {"error": f"Path not found: {json_path}"}
        except Exception as e:
            print(f"Error resolving reference {ref_path}: {e}")
            return {"error": str(e)}
    
    def resolve_refs_in_object(self, obj: Any, current_file: Path) -> Any:
        """Recursively resolve all $ref in an object"""
        if isinstance(obj, dict):
            if '$ref' in obj and len(obj) == 1:
                # This is a pure reference, replace it entirely
                return self.resolve_ref(obj['$ref'], current_file)
            else:
                # Process each key-value pair
                resolved = {}
                for key, value in obj.items():
                    if key == '$ref':
                        # Inline the reference
                        ref_content = self.resolve_ref(value, current_file)
                        if isinstance(ref_content, dict):
                            resolved.update(ref_content)
                        else:
                            resolved['$ref_resolved'] = ref_content
                    else:
                        resolved[key] = self.resolve_refs_in_object(value, current_file)
                return resolved
        elif isinstance(obj, list):
            return [self.resolve_refs_in_object(item, current_file) for item in obj]
        else:
            return obj
    
    def combine_openapi(self, main_file: str, output_file: str = 'combined_openapi.json'):
        """Combine OpenAPI spec with all referenced files"""
        main_path = Path(main_file)
        
        print(f"Loading main OpenAPI file: {main_file}")
        
        try:
            with open(main_path, 'r') as f:
                openapi_spec = json.load(f)
        except Exception as e:
            print(f"Error loading main file: {e}")
            return
        
        print("Resolving all $ref references...")
        
        # Resolve all references
        resolved_spec = self.resolve_refs_in_object(openapi_spec, main_path)
        
        # Add metadata about the combination
        if 'info' not in resolved_spec:
            resolved_spec['info'] = {}
        
        resolved_spec['info']['x-combined'] = True
        resolved_spec['info']['x-original-file'] = str(main_path)
        resolved_spec['info']['x-total-refs-resolved'] = len(self.resolved_refs)
        
        # Save the combined spec
        with open(output_file, 'w') as f:
            json.dump(resolved_spec, f, indent=2)
        
        print(f"\nCombined OpenAPI spec saved to: {output_file}")
        print(f"Total references resolved: {len(self.resolved_refs)}")
        
        # Show statistics
        paths_count = len(resolved_spec.get('paths', {}))
        schemas_count = len(resolved_spec.get('components', {}).get('schemas', {}))
        print(f"Total paths: {paths_count}")
        print(f"Total schemas: {schemas_count}")
        
        return resolved_spec

def main():
    if len(sys.argv) < 2:
        print("Usage: python combine_openapi.py <main_openapi_file.json> [output_file.json]")
        print("\nExample:")
        print("  python combine_openapi.py unit_openapi.json combined_unit_api.json")
        print("\nThis script will:")
        print("  1. Load the main OpenAPI file")
        print("  2. Resolve all $ref references to external files")
        print("  3. Combine everything into a single JSON file")
        print("\nNote: The script will look for referenced files relative to the main file's location")
        sys.exit(1)
    
    main_file = sys.argv[1]
    output_file = sys.argv[2] if len(sys.argv) > 2 else 'combined_openapi.json'
    
    # Get the base directory from the main file
    base_dir = Path(main_file).parent
    
    print("="*60)
    print("OpenAPI Reference Resolver & Combiner")
    print("="*60)
    print(f"Base directory: {base_dir}\n")
    
    resolver = OpenAPIResolver(base_dir)
    resolver.combine_openapi(main_file, output_file)
    
    print("\n" + "="*60)
    print("DONE")
    print("="*60)

if __name__ == "__main__":
    main()