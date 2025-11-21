from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup
import json
import re
import time
from urllib.parse import urljoin

# --- CONFIGURATION ---
START_URL = "https://docs.galileo-ft.com/pro/reference/program-api-intro"
BASE_DOMAIN = "https://docs.galileo-ft.com"
OUTPUT_FILE = "galileo_api_reference_only.json"

def setup_driver():
    """Sets up a headless Chrome browser."""
    chrome_options = Options()
    chrome_options.add_argument("--headless") 
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--window-size=1920,1080")
    chrome_options.add_argument("--log-level=3") # Suppress logs
    
    service = Service(ChromeDriverManager().install())
    return webdriver.Chrome(service=service, options=chrome_options)

def clean_text(text):
    if not text: return ""
    return " ".join(text.split())

def scrape_page_with_selenium(driver, url):
    print(f"⏳ Processing: {url}...")
    driver.get(url)
    
    # Smart Wait:
    # If it's an API Endpoint, parameters usually load within 2-3 seconds.
    # If it's a Concept page (e.g., "About Program API"), this will timeout safely.
    try:
        WebDriverWait(driver, 4).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "label[class*='Param-name']"))
        )
        is_endpoint = True
    except Exception:
        is_endpoint = False

    # Parse content
    soup = BeautifulSoup(driver.page_source, 'html.parser')
    
    # 1. Basic Info
    title = soup.find('h1')
    title_text = clean_text(title.get_text()) if title else "Unknown"
    
    # Breadcrumbs/Category
    breadcrumb = soup.find('div', class_='hub-breadcrumb')
    category = clean_text(breadcrumb.get_text()) if breadcrumb else "General"

    # Method & Endpoint (Only present on actual API pages)
    method_tag = soup.find(class_=re.compile(r'APIMethod_lg'))
    method = clean_text(method_tag.get_text()) if method_tag else None
    
    url_tag = soup.find(attrs={"data-testid": "serverurl"})
    endpoint_path = clean_text(url_tag.get_text()) if url_tag else None

    # 2. Description
    description_div = soup.find('div', class_='rm-Markdown')
    description = clean_text(description_div.get_text()) if description_div else ""

    # 3. Parameters (Dynamic Content)
    parameters = []
    if is_endpoint:
        param_labels = soup.find_all('label', class_=re.compile(r'Param-name'))
        for label in param_labels:
            try:
                parent = label.find_parent(class_=re.compile(r'Param-contentWrapper'))
                if not parent: continue

                param_name = clean_text(label.get_text())
                type_tag = parent.find(class_=re.compile(r'Param-type'))
                param_type = clean_text(type_tag.get_text()) if type_tag else "unknown"
                
                req_tag = parent.find(class_=re.compile(r'Param-required'))
                is_required = True if req_tag else False
                
                desc_tag = parent.find(class_='field-description')
                param_desc = clean_text(desc_tag.get_text()) if desc_tag else ""

                # Deduplicate parameters
                if not any(p['name'] == param_name for p in parameters):
                    parameters.append({
                        "name": param_name,
                        "type": param_type,
                        "required": is_required,
                        "description": param_desc
                    })
            except: continue

    # 4. Response Data Fields
    response_fields = []
    # Galileo response schemas usually live in a specific div structure
    response_div = soup.find('div', id=re.compile(r'object-.*response_data'))
    if response_div:
        resp_labels = response_div.find_all('label', class_=re.compile(r'Param-name'))
        for label in resp_labels:
            response_fields.append(clean_text(label.get_text()))

    # 5. Tables (Status Codes / Error Codes)
    status_codes = []
    tables = soup.find_all('table')
    for table in tables:
        headers = [clean_text(th.get_text()) for th in table.find_all('th')]
        # Check if it's a Status Code table
        if any(x in headers for x in ["Status code", "Code"]):
            rows = table.find_all('tr')
            for tr in rows[1:]:
                cols = [clean_text(td.get_text()) for td in tr.find_all('td')]
                if len(cols) >= 2:
                    status_codes.append({"code": cols[0], "description": cols[1]})

    return {
        "url": url,
        "type": "api_endpoint" if method else "concept",
        "category": category,
        "title": title_text,
        "method": method,
        "endpoint": endpoint_path,
        "description": description,
        "parameters": parameters,
        "response_fields": response_fields,
        "status_codes": status_codes
    }

def get_reference_links(driver, start_url):
    """Crawls the sidebar but ONLY keeps links containing /pro/reference/"""
    print(f"🔍 Scanning sidebar at {start_url}...")
    driver.get(start_url)
    time.sleep(3) # Allow sidebar to render
    
    soup = BeautifulSoup(driver.page_source, 'html.parser')
    links = set()
    
    # ReadMe sidebar container
    sidebar = soup.find('div', class_='hub-sidebar-content') or soup.find('nav')
    
    if sidebar:
        for a in sidebar.find_all('a', href=True):
            href = a['href']
            full_url = urljoin(BASE_DOMAIN, href)
            
            # --- THE CRITICAL FILTER ---
            # Only keep links that are strictly in the API Reference section
            if "/pro/reference/" in full_url and "#" not in href:
                links.add(full_url)
    
    sorted_links = sorted(list(links))
    print(f"✅ Found {len(sorted_links)} Reference pages.")
    return sorted_links

def main():
    driver = setup_driver()
    try:
        # 1. Get Filtered Links
        all_links = get_reference_links(driver, START_URL)
        
        results = []
        
        # 2. Scrape Pages
        for i, link in enumerate(all_links):
            print(f"[{i+1}/{len(all_links)}]")
            data = scrape_page_with_selenium(driver, link)
            if data:
                results.append(data)
                if data['type'] == 'api_endpoint':
                    print(f"   👉 API Endpoint: {data['title']} ({len(data['parameters'])} params)")
                else:
                    print(f"   📄 Reference Concept: {data['title']}")
            
        # 3. Save
        with open(OUTPUT_FILE, 'w', encoding='utf-8') as f:
            json.dump({"api_reference": results}, f, indent=2, ensure_ascii=False)
            
        print(f"\n✅ SUCCESS! Saved {len(results)} reference items to {OUTPUT_FILE}")
        
    finally:
        driver.quit()

if __name__ == "__main__":
    main()