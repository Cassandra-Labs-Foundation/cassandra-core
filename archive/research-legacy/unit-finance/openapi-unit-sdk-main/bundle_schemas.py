import json
from pathlib import Path

def collect_schemas_from_directory(schemas_dir):
    """Collect all schemas from files in the schemas directory"""
    schemas_path = Path(schemas_dir)
    all_schemas = {}
    
    print(f"Scanning directory: {schemas_path}")
    
    # Find all JSON files in schemas directory
    json_files = list(schemas_path.glob('**/*.json'))
    print(f"Found {len(json_files)} JSON files")
    
    for json_file in json_files:
        print(f"  Processing: {json_file.name}")
        
        with open(json_file, 'r') as f:
            try:
                data = json.load(f)
                
                # Extract schemas from components/schemas
                if 'components' in data and 'schemas' in data['components']:
                    for schema_name, schema_def in data['components']['schemas'].items():
                        if schema_name in all_schemas:
                            print(f"    Warning: Duplicate schema '{schema_name}' (keeping first occurrence)")
                        else:
                            all_schemas[schema_name] = schema_def
                            print(f"    Added: {schema_name}")
                
                # Also check for top-level schemas (some files might be structured differently)
                elif isinstance(data, dict) and 'type' in data:
                    # This looks like a schema itself
                    schema_name = json_file.stem
                    all_schemas[schema_name] = data
                    print(f"    Added: {schema_name} (top-level schema)")
                    
            except json.JSONDecodeError as e:
                print(f"    Error reading {json_file}: {e}")
    
    return all_schemas

def extract_schemas_from_openapi(openapi_file):
    """Extract schemas already defined in openapi.json"""
    with open(openapi_file, 'r') as f:
        openapi = json.load(f)
    
    schemas = {}
    if 'components' in openapi and 'schemas' in openapi['components']:
        schemas = openapi['components']['schemas']
        print(f"Found {len(schemas)} schemas in openapi.json")
    
    return schemas

def create_bundled_schemas(openapi_file, schemas_dir, output_file):
    """Create a single schemas.json file from all sources"""
    
    print("Step 1: Collecting schemas from /schemas directory...")
    dir_schemas = collect_schemas_from_directory(schemas_dir)
    
    print("\nStep 2: Extracting schemas from openapi.json...")
    openapi_schemas = extract_schemas_from_openapi(openapi_file)
    
    print("\nStep 3: Merging schemas...")
    # Merge both sources (directory schemas take precedence)
    all_schemas = {**openapi_schemas, **dir_schemas}
    
    print(f"Total unique schemas: {len(all_schemas)}")
    
    # Create the bundled structure
    bundled = {
        "components": {
            "schemas": all_schemas
        }
    }
    
    # Save to file
    output_path = Path(output_file)
    with open(output_path, 'w') as f:
        json.dump(bundled, f, indent=2)
    
    file_size = output_path.stat().st_size
    print(f"\nCreated: {output_file}")
    print(f"File size: {file_size:,} bytes ({file_size / 1024:.2f} KB)")
    print(f"Schemas included: {len(all_schemas)}")

if __name__ == "__main__":
    # Adjust these paths if needed
    create_bundled_schemas(
        openapi_file='openapi.json',
        schemas_dir='schemas',
        output_file='schemas.json'
    )