#!/usr/bin/env python3
"""
Validate that extraction captured all relevant documentation
"""

import json
import os
from pathlib import Path
from collections import Counter

def load_all_extracts(extract_dir="column_docs_extracted"):
    """Load all extracted JSON files"""
    extracts = []
    extract_path = Path(extract_dir)
    
    for json_file in extract_path.glob("*_extracted.json"):
        with open(json_file, 'r') as f:
            extracts.append(json.load(f))
    
    return extracts

def analyze_navigation_coverage(extracts):
    """Check if we have files for all documented URLs"""
    # Collect all unique URLs from navigation
    all_nav_urls = set()
    for extract in extracts:
        for nav_item in extract.get('navigation', []):
            url = nav_item.get('url', '').strip('/')
            if url and '/docs' in url:
                all_nav_urls.add(url)
    
    # Collect URLs we actually extracted
    extracted_urls = set()
    for extract in extracts:
        url = extract.get('url', '').strip('/')
        if url:
            extracted_urls.add(url)
    
    print(f"URLs found in navigation: {len(all_nav_urls)}")
    print(f"URLs we extracted: {len(extracted_urls)}")
    
    missing_urls = all_nav_urls - extracted_urls
    if missing_urls:
        print(f"\nMissing URLs ({len(missing_urls)}):")
        for url in sorted(missing_urls):
            print(f"  {url}")
    
    extra_urls = extracted_urls - all_nav_urls
    if extra_urls:
        print(f"\nExtra URLs not in navigation ({len(extra_urls)}):")
        for url in sorted(extra_urls):
            print(f"  {url}")
    
    return all_nav_urls, extracted_urls, missing_urls

def analyze_content_quality(extracts):
    """Check if extracts have meaningful content"""
    issues = []
    
    for extract in extracts:
        file_name = extract.get('file', 'unknown')
        url = extract.get('url', 'unknown')
        
        # Check for empty or minimal content
        main_content = extract.get('main_content', '')
        if len(main_content) < 100:
            issues.append(f"{file_name}: Very short content ({len(main_content)} chars)")
        
        # Check for API-related pages that have no endpoints/examples
        if '/api' in url or 'api' in extract.get('title', '').lower():
            if not extract.get('endpoints') and not extract.get('code_examples'):
                issues.append(f"{file_name}: API page with no endpoints or examples")
        
        # Check for pages that might have failed to render
        if 'error' in main_content.lower() or 'not found' in main_content.lower():
            issues.append(f"{file_name}: May contain error content")
    
    if issues:
        print(f"\nContent Quality Issues ({len(issues)}):")
        for issue in issues:
            print(f"  {issue}")
    
    return issues

def analyze_api_coverage(extracts):
    """Analyze API endpoint and example coverage"""
    total_endpoints = 0
    total_examples = 0
    api_pages = 0
    
    for extract in extracts:
        endpoints = extract.get('endpoints', [])
        examples = extract.get('code_examples', [])
        
        if endpoints or examples or extract.get('url', '').startswith('/docs/api'):
            api_pages += 1
            total_endpoints += len(endpoints)
            total_examples += len(examples)
    
    print(f"\nAPI Coverage:")
    print(f"  API-related pages: {api_pages}")
    print(f"  Total endpoints found: {total_endpoints}")
    print(f"  Total code examples: {total_examples}")
    
    # Show example distribution
    example_types = Counter()
    for extract in extracts:
        for example in extract.get('code_examples', []):
            example_types[example.get('type', 'unknown')] += 1
    
    if example_types:
        print(f"  Example types: {dict(example_types)}")

def compare_with_sitemap(sitemap_file=None):
    """Compare against original sitemap if available"""
    if not sitemap_file or not os.path.exists(sitemap_file):
        print("No sitemap file provided for comparison")
        return
    
    # This would need sitemap parsing logic
    print("Sitemap comparison not implemented yet")

def validate_specific_content(extracts):
    """Look for specific important API concepts"""
    key_concepts = [
        'authentication', 'webhook', 'endpoint', 'parameter', 
        'response', 'error', 'rate limit', 'pagination',
        'transfer', 'account', 'entity', 'compliance'
    ]
    
    concept_coverage = {concept: 0 for concept in key_concepts}
    
    for extract in extracts:
        content = (extract.get('main_content', '') + ' ' + 
                  extract.get('title', '')).lower()
        
        for concept in key_concepts:
            if concept in content:
                concept_coverage[concept] += 1
    
    print(f"\nKey Concept Coverage:")
    for concept, count in concept_coverage.items():
        print(f"  {concept}: {count} pages")
    
    # Flag if important concepts are missing
    missing_concepts = [k for k, v in concept_coverage.items() if v == 0]
    if missing_concepts:
        print(f"  WARNING: No pages found for: {missing_concepts}")

def main():
    print("=== Documentation Extraction Validation ===\n")
    
    extracts = load_all_extracts()
    print(f"Loaded {len(extracts)} extracted files")
    
    # Navigation coverage analysis
    all_urls, extracted_urls, missing_urls = analyze_navigation_coverage(extracts)
    
    # Content quality check
    content_issues = analyze_content_quality(extracts)
    
    # API coverage analysis
    analyze_api_coverage(extracts)
    
    # Key concept validation
    validate_specific_content(extracts)
    
    # Summary
    print(f"\n=== SUMMARY ===")
    print(f"✓ Extracted {len(extracts)} files")
    print(f"✓ Found {len(all_urls)} unique URLs in navigation")
    print(f"{'✗' if missing_urls else '✓'} {len(missing_urls)} missing URLs")
    print(f"{'✗' if content_issues else '✓'} {len(content_issues)} content issues")
    
    if not missing_urls and not content_issues:
        print("\n🎉 Extraction appears complete and high-quality!")
    else:
        print("\n⚠️  Some issues found - review above for details")

if __name__ == "__main__":
    main()