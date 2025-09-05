import os
import sys
import xml.etree.ElementTree as ET
from playwright.sync_api import sync_playwright
import re

OUT_DIR = "column_docs_html"
os.makedirs(OUT_DIR, exist_ok=True)

def get_urls_from_sitemap_file(sitemap_file):
    with open(sitemap_file, "r", encoding="utf-8") as f:
        content = f.read()
    
    # Debug: Show first few lines
    print("First 200 chars of file:")
    print(repr(content[:200]))
    
    # Try to extract XML from HTML wrapper
    if "<html" in content.lower() or "<!doctype" in content.lower():
        # Look for XML content within HTML
        xml_match = re.search(r'(<\?xml.*?</urlset>)', content, re.DOTALL)
        if xml_match:
            content = xml_match.group(1)
        else:
            # Try to find just the urlset content
            urlset_match = re.search(r'(<urlset.*?</urlset>)', content, re.DOTALL)
            if urlset_match:
                content = '<?xml version="1.0" encoding="UTF-8"?>\n' + urlset_match.group(1)
            else:
                raise ValueError("Could not find XML content in HTML file")
    
    # Clean up any remaining HTML entities
    content = content.replace('&lt;', '<').replace('&gt;', '>').replace('&amp;', '&')
    
    try:
        root = ET.fromstring(content)
    except ET.ParseError as e:
        print(f"XML Parse Error: {e}")
        print("Content that failed to parse:")
        print(content[:500])
        raise
    
    # Handle both sitemap index and regular sitemap
    ns = {"sm": "http://www.sitemaps.org/schemas/sitemap/0.9"}
    
    # Check if this is a sitemap index (contains <sitemap> elements)
    sitemaps = root.findall(".//sm:sitemap/sm:loc", ns)
    if sitemaps:
        print(f"Found sitemap index with {len(sitemaps)} sitemaps")
        return [loc.text for loc in sitemaps]
    
    # Otherwise look for URLs
    urls = [loc.text for loc in root.findall(".//sm:loc", ns)]
    return urls

def sanitize_filename(url):
    return url.replace("https://", "").replace("http://", "").replace("/", "_").replace("?", "_").replace("#", "_").strip("_") + ".html"

def crawl_and_save(urls):
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        
        for i, url in enumerate(urls, 1):
            # Skip non-docs URLs to focus on documentation
            if "/docs" not in url:
                print(f"Skipping non-docs URL: {url}")
                continue
                
            print(f"[{i}/{len(urls)}] Fetching {url}")
            try:
                page.goto(url, timeout=60000)
                page.wait_for_load_state("networkidle")
                html = page.content()
                filename = sanitize_filename(url)
                outpath = os.path.join(OUT_DIR, filename)
                with open(outpath, "w", encoding="utf-8") as f:
                    f.write(html)
                print(f"  Saved to {filename}")
            except Exception as e:
                print(f"  Failed to fetch {url}: {e}")
        
        browser.close()

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python crawler.py <sitemap_file>")
        print("Note: If the sitemap file is HTML-wrapped, the script will try to extract XML")
        sys.exit(1)

    sitemap_file = sys.argv[1]
    
    if not os.path.exists(sitemap_file):
        print(f"File not found: {sitemap_file}")
        sys.exit(1)
    
    try:
        urls = get_urls_from_sitemap_file(sitemap_file)
        print(f"Found {len(urls)} URLs in sitemap")
        
        # Filter to docs URLs
        docs_urls = [url for url in urls if "/docs" in url]
        print(f"Found {len(docs_urls)} documentation URLs")
        
        if docs_urls:
            crawl_and_save(docs_urls)
        else:
            print("No documentation URLs found. Showing all URLs:")
            for url in urls[:10]:  # Show first 10
                print(f"  {url}")
    except Exception as e:
        print(f"Error processing sitemap: {e}")
        sys.exit(1)