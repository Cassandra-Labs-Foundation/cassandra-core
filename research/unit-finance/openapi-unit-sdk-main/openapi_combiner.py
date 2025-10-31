#!/usr/bin/env python3
"""
OpenAPI Schema Combiner
Resolves $ref references and combines OpenAPI specification files into a single document.
"""

import json
import os
from pathlib import Path
from typing import Any, Dict, Set
from urllib.parse import urljoin, urlparse


class OpenAPICombiner:
    def __init__(self, base_path: str):
        """
        Initialize the combiner with a base path for resolving relative references.
        
        Args:
            base_path: Directory containing the main OpenAPI file
        """
        self.base_path = Path(base_path).resolve()
        self.loaded_files: Dict[str, Any] = {}
        self.processed_refs: Set[str] = set()
        
    def load_json_file(self, file_path: Path) -> Any:
        """Load a JSON file and cache it."""
        file_path = file_path.resolve()
        file_key = str(file_path)
        
        if file_key not in self.loaded_files:
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    self.loaded_files[file_key] = json.load(f)
            except FileNotFoundError:
                print(f"Warning: File not found: {file_path}")
                return None
            except json.JSONDecodeError as e:
                print(f"Warning: Invalid JSON in {file_path}: {e}")
                return None
                
        return self.loaded_files[file_key]
    
    def resolve_json_pointer(self, data: Any, pointer: str) -> Any:
        """
        Resolve a JSON pointer (e.g., '#/paths/users' or '#/application').
        
        Args:
            data: The data structure to navigate
            pointer: JSON pointer string (starting with #)
            
        Returns:
            The referenced data
        """
        if not pointer or pointer == '#':
            return data
            
        # Remove leading '#/' or '#'
        pointer = pointer.lstrip('#').lstrip('/')
        
        if not pointer:
            return data
            
        # Split by '/' and navigate the structure
        parts = pointer.split('/')
        current = data
        
        for part in parts:
            # Unescape JSON pointer tokens
            part = part.replace('~1', '/').replace('~0', '~')
            
            if isinstance(current, dict):
                if part not in current:
                    print(f"Warning: Pointer part '{part}' not found in data")
                    return None
                current = current[part]
            elif isinstance(current, list):
                try:
                    index = int(part)
                    current = current[index]
                except (ValueError, IndexError):
                    print(f"Warning: Invalid array index '{part}'")
                    return None
            else:
                print(f"Warning: Cannot navigate further at '{part}'")
                return None
                
        return current
    
    def resolve_ref(self, ref: str, current_file_path: Path) -> Any:
        """
        Resolve a $ref reference.
        
        Args:
            ref: The reference string (e.g., './schemas/application/applicationPaths.json#/application')
            current_file_path: Path of the file containing this reference
            
        Returns:
            The resolved content
        """
        # Skip already processed refs to avoid infinite loops
        ref_key = f"{current_file_path}::{ref}"
        if ref_key in self.processed_refs:
            return {"$ref": ref}  # Return original ref if already processed
        
        self.processed_refs.add(ref_key)
        
        # Split reference into file path and JSON pointer
        if '#' in ref:
            file_ref, pointer = ref.split('#', 1)
            pointer = '#' + pointer
        else:
            file_ref = ref
            pointer = '#'
        
        # Resolve file path
        if file_ref:
            # Relative to current file
            ref_file_path = (current_file_path.parent / file_ref).resolve()
        else:
            # Same file reference
            ref_file_path = current_file_path
        
        # Load the referenced file
        ref_data = self.load_json_file(ref_file_path)
        if ref_data is None:
            return {"$ref": ref}  # Keep original if file not found
        
        # Resolve the JSON pointer
        resolved = self.resolve_json_pointer(ref_data, pointer)
        if resolved is None:
            return {"$ref": ref}  # Keep original if pointer invalid
        
        # Recursively resolve any nested $refs
        return self.resolve_refs_recursive(resolved, ref_file_path)
    
    def resolve_refs_recursive(self, data: Any, current_file_path: Path) -> Any:
        """
        Recursively resolve all $ref references in a data structure.
        
        Args:
            data: The data to process
            current_file_path: Path of the file containing this data
            
        Returns:
            Data with all references resolved
        """
        if isinstance(data, dict):
            if '$ref' in data:
                # This is a reference - resolve it
                ref = data['$ref']
                resolved = self.resolve_ref(ref, current_file_path)
                
                # If the ref resolved to something other than itself, use it
                if resolved != {"$ref": ref}:
                    return resolved
                return data
            else:
                # Process all values in the dictionary
                return {key: self.resolve_refs_recursive(value, current_file_path) 
                       for key, value in data.items()}
        
        elif isinstance(data, list):
            # Process all items in the list
            return [self.resolve_refs_recursive(item, current_file_path) 
                   for item in data]
        
        else:
            # Primitive value - return as is
            return data
    
    def combine(self, openapi_file: str, output_file: str = None) -> Dict[str, Any]:
        """
        Combine an OpenAPI specification with all its references.
        
        Args:
            openapi_file: Path to the main OpenAPI JSON file
            output_file: Optional path to save the combined spec
            
        Returns:
            The combined OpenAPI specification
        """
        openapi_path = Path(openapi_file).resolve()
        
        # Load the main OpenAPI file
        spec = self.load_json_file(openapi_path)
        if spec is None:
            raise ValueError(f"Could not load OpenAPI file: {openapi_file}")
        
        # Resolve all references
        print("Resolving references...")
        combined = self.resolve_refs_recursive(spec, openapi_path)
        
        # Save to file if requested
        if output_file:
            print(f"Writing combined specification to {output_file}...")
            with open(output_file, 'w', encoding='utf-8') as f:
                json.dump(combined, f, indent=2)
            print("Done!")
        
        return combined


def main():
    """Main entry point for the script."""
    import argparse
    
    parser = argparse.ArgumentParser(
        description='Combine OpenAPI specification files by resolving $ref references'
    )
    parser.add_argument(
        'input_file',
        help='Path to the main OpenAPI JSON file'
    )
    parser.add_argument(
        '-o', '--output',
        default='openapi-combined.json',
        help='Output file path (default: openapi-combined.json)'
    )
    parser.add_argument(
        '--base-path',
        help='Base path for resolving relative references (default: directory of input file)'
    )
    
    args = parser.parse_args()
    
    # Determine base path
    if args.base_path:
        base_path = args.base_path
    else:
        base_path = os.path.dirname(os.path.abspath(args.input_file))
    
    # Create combiner and process
    combiner = OpenAPICombiner(base_path)
    
    try:
        combined = combiner.combine(args.input_file, args.output)
        print(f"\nSuccessfully combined OpenAPI specification!")
        print(f"Total files loaded: {len(combiner.loaded_files)}")
        print(f"Output saved to: {args.output}")
    except Exception as e:
        print(f"Error: {e}")
        return 1
    
    return 0


if __name__ == '__main__':
    exit(main())