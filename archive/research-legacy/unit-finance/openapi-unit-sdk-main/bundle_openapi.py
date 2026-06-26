import json
from pathlib import Path

def create_llm_bundle(openapi_file, schemas_file, output_file):
    """Create a single file by inlining the schemas.json content"""
    
    with open(openapi_file, 'r') as f:
        openapi = json.load(f)
    
    with open(schemas_file, 'r') as f:
        schemas = json.load(f)
    
    # Merge schemas into openapi components
    if 'components' not in openapi:
        openapi['components'] = {}
    if 'schemas' not in openapi['components']:
        openapi['components']['schemas'] = {}
    
    openapi['components']['schemas'].update(schemas['components']['schemas'])
    
    # Update all references from ./schemas.json#/... to #/...
    def localize_refs(obj):
        if isinstance(obj, dict):
            if '$ref' in obj and obj['$ref'].startswith('./schemas.json#/'):
                obj['$ref'] = obj['$ref'].replace('./schemas.json#/', '#/')
            return {k: localize_refs(v) for k, v in obj.items()}
        elif isinstance(obj, list):
            return [localize_refs(item) for item in obj]
        return obj
    
    openapi = localize_refs(openapi)
    
    # Save bundled version
    with open(output_file, 'w') as f:
        json.dump(openapi, f, indent=2)
    
    file_size = Path(output_file).stat().st_size
    print(f"Created LLM-ready bundle: {output_file}")
    print(f"File size: {file_size:,} bytes ({file_size / 1024 / 1024:.2f} MB)")

if __name__ == "__main__":
    create_llm_bundle('openapi.json', 'schemas.json', 'openapi-bundled.json')