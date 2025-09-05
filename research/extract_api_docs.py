#!/usr/bin/env python3
"""
Extract key API information from HTML documentation files
Reduces file size by focusing on documentation content and removing UI elements
"""

import os
import json
from pathlib import Path
from bs4 import BeautifulSoup, NavigableString
import re

class APIDocExtractor:
    def __init__(self, input_dir="column_docs_html", output_dir="column_docs_extracted"):
        self.input_dir = Path(input_dir)
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(exist_ok=True)
    
    def clean_text(self, text):
        """Clean and normalize text content"""
        if not text:
            return ""
        # Remove extra whitespace
        text = re.sub(r'\s+', ' ', text.strip())
        return text
    
    def extract_navigation_structure(self, soup):
        """Extract the sidebar navigation to understand API structure"""
        nav_items = []
        
        # Look for sidebar navigation
        sidebar = soup.find('aside') or soup.find('nav')
        if sidebar:
            # Find all navigation links
            links = sidebar.find_all('a', href=True)
            for link in links:
                href = link.get('href', '')
                text = self.clean_text(link.get_text())
                if '/docs' in href and text:
                    nav_items.append({
                        'url': href,
                        'title': text,
                        'is_api': '/api/' in href
                    })
        
        return nav_items
    
    def extract_api_endpoints(self, soup):
        """Extract API endpoint information"""
        endpoints = []
        
        # Look for HTTP method indicators
        methods = ['GET', 'POST', 'PUT', 'DELETE', 'PATCH']
        for method in methods:
            # Find elements containing HTTP methods
            method_elements = soup.find_all(string=re.compile(f'\\b{method}\\b'))
            for elem in method_elements:
                parent = elem.parent if elem.parent else None
                if parent:
                    # Try to extract endpoint URL
                    code_elem = parent.find_next('code') or parent.find_previous('code')
                    if code_elem:
                        endpoint_text = self.clean_text(code_elem.get_text())
                        if '/' in endpoint_text:
                            endpoints.append({
                                'method': method,
                                'endpoint': endpoint_text,
                                'context': self.clean_text(parent.get_text()[:200])
                            })
        
        return endpoints
    
    def extract_code_examples(self, soup):
        """Extract code examples and API schemas"""
        examples = []
        
        # Find code blocks
        code_blocks = soup.find_all(['pre', 'code'])
        for block in code_blocks:
            code_text = self.clean_text(block.get_text())
            if len(code_text) > 20:  # Skip very short code snippets
                # Determine if it's JSON, curl, or other
                code_type = 'unknown'
                if code_text.strip().startswith('{') or '"' in code_text:
                    code_type = 'json'
                elif 'curl' in code_text.lower():
                    code_type = 'curl'
                elif 'http' in code_text.lower():
                    code_type = 'http'
                
                examples.append({
                    'type': code_type,
                    'content': code_text,
                    'context': self.get_surrounding_context(block)
                })
        
        return examples
    
    def get_surrounding_context(self, element):
        """Get text context around an element"""
        context = ""
        
        # Look for preceding heading
        for tag in ['h1', 'h2', 'h3', 'h4', 'h5', 'h6']:
            heading = element.find_previous(tag)
            if heading:
                context = self.clean_text(heading.get_text())
                break
        
        return context
    
    def extract_data_models(self, soup):
        """Extract object/schema definitions"""
        models = []
        
        # Look for parameter tables or object descriptions
        tables = soup.find_all('table')
        for table in tables:
            headers = table.find_all('th')
            if len(headers) >= 2:  # Likely a parameter table
                header_text = [self.clean_text(th.get_text()) for th in headers]
                if any(keyword in ' '.join(header_text).lower() 
                       for keyword in ['parameter', 'field', 'property', 'type']):
                    
                    rows = []
                    for row in table.find_all('tr')[1:]:  # Skip header row
                        cells = [self.clean_text(td.get_text()) for td in row.find_all(['td', 'th'])]
                        if cells:
                            rows.append(cells)
                    
                    if rows:
                        models.append({
                            'headers': header_text,
                            'rows': rows,
                            'context': self.get_surrounding_context(table)
                        })
        
        return models
    
    def extract_main_content(self, soup):
        """Extract the main documentation content"""
        # Remove navigation, header, footer, scripts
        for element in soup(['nav', 'header', 'footer', 'script', 'style', 'aside']):
            element.decompose()
        
        # Find main content area
        main_content = soup.find('main') or soup.find('article') or soup.find(class_=re.compile(r'content|main|docs'))
        
        if main_content:
            return self.clean_text(main_content.get_text())
        else:
            # Fallback to body content
            return self.clean_text(soup.get_text())
    
    def extract_from_file(self, html_file):
        """Extract structured information from a single HTML file"""
        with open(html_file, 'r', encoding='utf-8') as f:
            content = f.read()
        
        soup = BeautifulSoup(content, 'html.parser')
        
        # Extract page title
        title_elem = soup.find('title') or soup.find('h1')
        page_title = self.clean_text(title_elem.get_text()) if title_elem else str(html_file.name)
        
        # Extract URL from script or meta tags
        page_url = ""
        script_tag = soup.find('script', string=re.compile(r'window\.pagePath'))
        if script_tag:
            match = re.search(r'window\.pagePath="([^"]+)"', script_tag.string)
            if match:
                page_url = match.group(1)
        
        extracted_data = {
            'file': str(html_file.name),
            'url': page_url,
            'title': page_title,
            'navigation': self.extract_navigation_structure(soup),
            'endpoints': self.extract_api_endpoints(soup),
            'code_examples': self.extract_code_examples(soup),
            'data_models': self.extract_data_models(soup),
            'main_content': self.extract_main_content(soup)[:2000],  # Limit content length
            'content_length': len(content),
            'extracted_length': 0  # Will be calculated after JSON serialization
        }
        
        return extracted_data
    
    def process_all_files(self):
        """Process all HTML files in the input directory"""
        html_files = list(self.input_dir.glob("*.html"))
        results = []
        
        print(f"Processing {len(html_files)} HTML files...")
        
        for html_file in html_files:
            print(f"Processing: {html_file.name}")
            try:
                extracted = self.extract_from_file(html_file)
                results.append(extracted)
            except Exception as e:
                print(f"Error processing {html_file.name}: {e}")
                continue
        
        # Save individual extracts
        for result in results:
            filename = result['file'].replace('.html', '_extracted.json')
            output_path = self.output_dir / filename
            
            with open(output_path, 'w', encoding='utf-8') as f:
                json_content = json.dumps(result, indent=2, ensure_ascii=False)
                f.write(json_content)
                result['extracted_length'] = len(json_content)
        
        # Save summary
        summary = {
            'total_files': len(results),
            'total_original_size': sum(r['content_length'] for r in results),
            'total_extracted_size': sum(r['extracted_length'] for r in results),
            'compression_ratio': 0,
            'files': [{'file': r['file'], 'title': r['title'], 'url': r['url']} for r in results]
        }
        
        if summary['total_original_size'] > 0:
            summary['compression_ratio'] = summary['total_extracted_size'] / summary['total_original_size']
        
        with open(self.output_dir / 'extraction_summary.json', 'w', encoding='utf-8') as f:
            json.dump(summary, f, indent=2, ensure_ascii=False)
        
        print(f"\nExtraction complete!")
        print(f"Original size: {summary['total_original_size']:,} bytes")
        print(f"Extracted size: {summary['total_extracted_size']:,} bytes")
        print(f"Compression ratio: {summary['compression_ratio']:.2%}")
        print(f"Results saved to: {self.output_dir}")
        
        return results

def main():
    extractor = APIDocExtractor()
    results = extractor.process_all_files()

if __name__ == "__main__":
    main()