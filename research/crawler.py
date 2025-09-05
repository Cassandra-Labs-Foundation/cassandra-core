#!/usr/bin/env python3
"""
Enhanced crawler for banking API documentation
Fixes issues with JavaScript-heavy sites and improves data collection
"""

import os
import sys
import json
import xml.etree.ElementTree as ET
from playwright.sync_api import sync_playwright
from urllib.parse import urljoin, urlparse
import re
import time
from pathlib import Path

class EnhancedDocCrawler:
    def __init__(self, base_url, output_dir="docs_html"):
        self.base_url = base_url.rstrip('/')
        self.domain = urlparse(base_url).netloc
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(exist_ok=True)
        
        # Track what we've crawled to avoid duplicates
        self.crawled_urls = set()
        self.failed_urls = set()
        
    def sanitize_filename(self, url):
        """Create safe filename from URL"""
        return url.replace("https://", "").replace("http://", "").replace("/", "_").replace("?", "_").replace("#", "_").strip("_") + ".html"
    
    def get_urls_from_sitemap(self, sitemap_content):
        """Extract URLs from sitemap XML"""
        urls = []
        
        # Try to extract XML from HTML wrapper if needed
        if "<html" in sitemap_content.lower() or "<!doctype" in sitemap_content.lower():
            xml_match = re.search(r'(<\?xml.*?</urlset>)', sitemap_content, re.DOTALL)
            if xml_match:
                sitemap_content = xml_match.group(1)
            else:
                urlset_match = re.search(r'(<urlset.*?</urlset>)', sitemap_content, re.DOTALL)
                if urlset_match:
                    sitemap_content = '<?xml version="1.0" encoding="UTF-8"?>\n' + urlset_match.group(1)
        
        # Clean up HTML entities
        sitemap_content = sitemap_content.replace('&lt;', '<').replace('&gt;', '>').replace('&amp;', '&')
        
        try:
            root = ET.fromstring(sitemap_content)
            ns = {"sm": "http://www.sitemaps.org/schemas/sitemap/0.9"}
            
            # Check for sitemap index first
            sitemaps = root.findall(".//sm:sitemap/sm:loc", ns)
            if sitemaps:
                return [loc.text for loc in sitemaps]
            
            # Extract regular URLs
            urls = [loc.text for loc in root.findall(".//sm:loc", ns)]
            
        except ET.ParseError as e:
            print(f"XML Parse Error: {e}")
            # Fallback: try to extract URLs with regex
            url_pattern = r'https?://[^\s<>"{}|\\^`\[\]]+/docs[^\s<>"{}|\\^`\[\]]*'
            urls = re.findall(url_pattern, sitemap_content)
        
        return urls
    
    def discover_docs_urls(self, page):
        """Discover documentation URLs from the main docs page"""
        print("🔍 Discovering documentation URLs...")
        
        docs_urls = set()
        
        # Start with the main docs page
        try:
            print(f"Loading main docs page: {self.base_url}/docs")
            page.goto(f"{self.base_url}/docs", timeout=60000, wait_until="networkidle")
            
            # Wait for dynamic content to load
            page.wait_for_timeout(3000)
            
            # Extract all docs links from the page
            links = page.eval_on_selector_all('a[href*="/docs"]', '''
                (elements) => elements.map(el => ({
                    href: el.href,
                    text: el.textContent.trim(),
                    visible: el.offsetParent !== null
                }))
            ''')
            
            for link in links:
                href = link['href']
                if href and '/docs' in href and self.domain in href:
                    docs_urls.add(href)
                    print(f"  Found: {link['text'][:50]}... -> {href}")
            
        except Exception as e:
            print(f"Error discovering docs URLs: {e}")
        
        return list(docs_urls)
    
    def extract_page_links(self, page):
        """Extract additional documentation links from current page"""
        try:
            # Look for navigation links, sidebar links, etc.
            nav_links = page.eval_on_selector_all('nav a, aside a, [class*="nav"] a, [class*="sidebar"] a', '''
                (elements) => elements.map(el => el.href).filter(href => href && href.includes('/docs'))
            ''')
            return [link for link in nav_links if self.domain in link]
        except:
            return []
    
    def crawl_page_enhanced(self, page, url):
        """Enhanced page crawling with better error handling"""
        print(f"📄 Crawling: {url}")
        
        try:
            # Navigate with retries
            for attempt in range(3):
                try:
                    page.goto(url, timeout=60000, wait_until="networkidle")
                    break
                except Exception as e:
                    if attempt == 2:
                        raise e
                    print(f"  Retry {attempt + 1}/3 for {url}")
                    time.sleep(2)
            
            # Wait for dynamic content - critical for JS-heavy sites
            page.wait_for_timeout(5000)
            
            # Wait for specific indicators that content has loaded
            try:
                # Wait for common doc page elements
                page.wait_for_selector('main, article, [class*="content"], [class*="docs"]', timeout=10000)
            except:
                print(f"  ⚠️  Main content selector not found, proceeding anyway")
            
            # Additional wait for any lazy-loaded content
            page.wait_for_timeout(2000)
            
            # Get the final rendered HTML
            html_content = page.content()
            
            # Basic content validation
            if len(html_content) < 1000:
                print(f"  ⚠️  Short content ({len(html_content)} chars) - possible load failure")
            
            # Check for error indicators
            page_text = page.evaluate('document.body ? document.body.innerText.toLowerCase() : ""')
            error_indicators = ['404', 'not found', 'error', 'unauthorized', 'forbidden']
            
            if any(indicator in page_text for indicator in error_indicators):
                print(f"  ⚠️  Possible error content detected")
                # Still save it for manual review
            
            # Save the page
            filename = self.sanitize_filename(url)
            filepath = self.output_dir / filename
            
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(html_content)
            
            print(f"  ✅ Saved: {filename} ({len(html_content):,} chars)")
            
            # NO LONGER EXTRACTING ADDITIONAL LINKS - this was causing duplicates
            
            return {
                'url': url,
                'filename': filename,
                'size': len(html_content),
                'status': 'success'
            }
            
        except Exception as e:
            print(f"  ❌ Failed: {e}")
            self.failed_urls.add(url)
            return {
                'url': url,
                'status': 'failed',
                'error': str(e)
            }
    
    def crawl_from_sitemap(self, sitemap_file):
        """Crawl from sitemap file"""
        print(f"📋 Reading sitemap: {sitemap_file}")
        
        with open(sitemap_file, 'r', encoding='utf-8') as f:
            sitemap_content = f.read()
        
        urls = self.get_urls_from_sitemap(sitemap_content)
        docs_urls = [url for url in urls if '/docs' in url]
        
        print(f"Found {len(urls)} total URLs, {len(docs_urls)} docs URLs")
        return docs_urls
    
    def crawl_comprehensive(self, sitemap_file=None, max_pages=None):
        """Comprehensive crawling strategy"""
        results = {
            'crawled': [],
            'failed': [],
            'discovered_urls': set()
        }
        
        with sync_playwright() as p:
            # Use persistent context for better compatibility
            browser = p.chromium.launch(
                headless=True,
                args=['--no-sandbox', '--disable-setuid-sandbox']
            )
            
            # Create context with realistic settings
            context = browser.new_context(
                viewport={'width': 1280, 'height': 720},
                user_agent='Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
            )
            
            page = context.new_page()
            
            # Enable request interception to handle failures gracefully
            page.route("**/*", lambda route: route.continue_())
            
            try:
                # Step 1: Get URLs from sitemap if provided
                initial_urls = set()
                if sitemap_file and os.path.exists(sitemap_file):
                    initial_urls.update(self.crawl_from_sitemap(sitemap_file))
                
                # Step 2: Discover URLs by crawling the main docs page
                discovered_urls = self.discover_docs_urls(page)
                initial_urls.update(discovered_urls)
                results['discovered_urls'].update(discovered_urls)
                
                print(f"\n🎯 Total URLs to crawl: {len(initial_urls)}")
                
                # Step 3: Crawl each page
                all_urls = list(initial_urls)
                crawled_count = 0
                
                for i, url in enumerate(all_urls, 1):
                    if max_pages and crawled_count >= max_pages:
                        print(f"\n⏹️  Stopping at {max_pages} pages limit")
                        break
                    
                    if url in self.crawled_urls:
                        print(f"[{i}/{len(all_urls)}] ⏭️  Skipping already crawled: {url}")
                        continue
                    
                    print(f"\n[{i}/{len(all_urls)}] 🔄 Processing: {url}")
                    
                    result = self.crawl_page_enhanced(page, url)
                    
                    if result['status'] == 'success':
                        results['crawled'].append(result)
                        self.crawled_urls.add(url)
                        crawled_count += 1
                        
                        # Add any newly discovered links to our queue
                        for new_url in result.get('additional_links', []):
                            if new_url not in self.crawled_urls and new_url not in all_urls:
                                all_urls.append(new_url)
                                results['discovered_urls'].add(new_url)
                                print(f"  🆕 Discovered new URL: {new_url}")
                    else:
                        results['failed'].append(result)
                    
                    # Rate limiting
                    time.sleep(1)
                
            finally:
                browser.close()
        
        # Save crawl report
        report = {
            'base_url': self.base_url,
            'total_attempted': len(results['crawled']) + len(results['failed']),
            'successful': len(results['crawled']),
            'failed': len(results['failed']),
            'discovered_urls_count': len(results['discovered_urls']),
            'crawled_pages': results['crawled'],
            'failed_pages': results['failed'],
            'all_discovered_urls': list(results['discovered_urls'])
        }
        
        with open(self.output_dir / 'crawl_report.json', 'w') as f:
            json.dump(report, f, indent=2)
        
        print(f"\n📊 CRAWL SUMMARY:")
        print(f"✅ Successfully crawled: {len(results['crawled'])} pages")
        print(f"❌ Failed: {len(results['failed'])} pages")
        print(f"🔍 Total URLs discovered: {len(results['discovered_urls'])}")
        print(f"📁 Output directory: {self.output_dir}")
        
        if results['failed']:
            print(f"\n❌ Failed URLs:")
            for failure in results['failed']:
                print(f"  {failure['url']}: {failure.get('error', 'Unknown error')}")
        
        return results

def main():
    import time
    
    if len(sys.argv) < 2:
        print("Usage: python enhanced_crawler.py <mode> [options]")
        print("\nModes:")
        print("  api <url>                    - Crawl comprehensive API page (recommended)")
        print("  sitemap <base_url> [file]    - Crawl from sitemap")
        print("  discover <base_url>          - Discover and crawl all docs")
        print("\nExamples:")
        print("  python enhanced_crawler.py api https://column.com/docs/api/")
        print("  python enhanced_crawler.py sitemap https://column.com sitemap.xml")
        print("  python enhanced_crawler.py discover https://column.com")
        sys.exit(1)
    
    mode = sys.argv[1].lower()
    
    if mode == 'api':
        # Crawl comprehensive API page
        api_url = sys.argv[2] if len(sys.argv) > 2 else "https://column.com/docs/api/"
        
        # Create output directory based on domain
        domain = urlparse(api_url).netloc
        output_dir = f"{domain.replace('.', '_')}_api_docs"
        
        crawler = EnhancedDocCrawler(api_url, output_dir)
        results = crawler.crawl_comprehensive_api_page(api_url)
        
    elif mode == 'sitemap':
        if len(sys.argv) < 3:
            print("Error: sitemap mode requires base_url")
            print("Usage: python enhanced_crawler.py sitemap <base_url> [sitemap_file]")
            sys.exit(1)
            
        base_url = sys.argv[2]
        sitemap_file = sys.argv[3] if len(sys.argv) > 3 else None
        
        domain = urlparse(base_url).netloc
        output_dir = f"{domain.replace('.', '_')}_docs_html"
        
        crawler = EnhancedDocCrawler(base_url, output_dir)
        results = crawler.crawl_comprehensive(sitemap_file)
        
    elif mode == 'discover':
        if len(sys.argv) < 3:
            print("Error: discover mode requires base_url")
            print("Usage: python enhanced_crawler.py discover <base_url> [max_pages]")
            sys.exit(1)
            
        base_url = sys.argv[2]
        max_pages = int(sys.argv[3]) if len(sys.argv) > 3 else None
        
        domain = urlparse(base_url).netloc
        output_dir = f"{domain.replace('.', '_')}_docs_html"
        
        crawler = EnhancedDocCrawler(base_url, output_dir)
        results = crawler.crawl_comprehensive(max_pages=max_pages)
        
    else:
        print(f"Unknown mode: {mode}")
        print("Valid modes: api, sitemap, discover")
        sys.exit(1)

if __name__ == "__main__":
    main()