"""
Web Crawler Engine
Supports multiple content types: HTML, XML, PDF, TXT, RSS feeds
"""
import requests
from bs4 import BeautifulSoup
from seleniumbase import Driver
import PyPDF2
import feedparser
from datetime import datetime
from typing import Dict, List, Any, Optional
import time
import io

class WebCrawler:
    def __init__(self, database):
        """Initialize crawler with database connection"""
        self.db = database
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        })
    
    def crawl_source(self, source: Dict[str, Any]) -> Dict[str, Any]:
        """Crawl a single source based on its type"""
        source_id = source.get("_id")
        url = source.get("url")
        source_type = source.get("type", "html")
        
        log = {
            "source_id": source_id,
            "url": url,
            "status": "started",
            "items_collected": 0,
            "errors": []
        }
        
        try:
            # Validate URL
            if not url or not url.startswith(('http://', 'https://')):
                raise ValueError(f"Invalid URL: {url}")
            
            print(f"🔄 Crawling {url} (type: {source_type})...")
            
            if source_type == "html":
                data = self._crawl_html(source)
            elif source_type == "rss":
                data = self._crawl_rss(source)
            elif source_type == "pdf":
                data = self._crawl_pdf(source)
            elif source_type == "xml":
                data = self._crawl_xml(source)
            elif source_type == "txt":
                data = self._crawl_txt(source)
            elif source_type == "dynamic":
                data = self._crawl_dynamic(source)
            else:
                raise ValueError(f"Unsupported source type: {source_type}")
            
            # Store data
            if data:
                if isinstance(data, list):
                    if self.db.crawled_data is not None:
                        self.db.bulk_store_data(data)
                        log["items_collected"] = len(data)
                        print(f"✅ Collected {len(data)} items")
                    else:
                        log["status"] = "error"
                        log["errors"].append("Database not connected")
                else:
                    if self.db.crawled_data is not None:
                        self.db.store_crawled_data(data)
                        log["items_collected"] = 1
                        print(f"✅ Collected 1 item")
                    else:
                        log["status"] = "error"
                        log["errors"].append("Database not connected")
                
                if log["status"] != "error":
                    log["status"] = "success"
            else:
                log["status"] = "no_data"
                log["errors"].append("No data extracted from source")
                print(f"⚠️ No data found")
        
        except Exception as e:
            log["status"] = "error"
            log["errors"].append(str(e))
            print(f"❌ Error: {e}")
        
        # Log the crawl
        if self.db.crawl_logs is not None:
            self.db.log_crawl(log)
        
        return log
    
    def _crawl_html(self, source: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Crawl HTML pages"""
        url = source.get("url")
        selectors = source.get("selectors", {})
        max_items = source.get("max_items", 50)
        
        response = self.session.get(url, timeout=30)
        response.raise_for_status()
        
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Extract data based on selectors
        items = []
        
        # If container selector is provided
        container_selector = selectors.get("container")
        if container_selector:
            containers = soup.select(container_selector)[:max_items]
            
            if not containers:
                print(f"⚠️ No elements found with selector: {container_selector}")
            
            for container in containers:
                item = {
                    "source_id": source.get("_id"),
                    "source_url": url,
                    "type": "html",
                    "data": {},
                    "title": "",
                    "content": ""
                }
                
                # Extract fields
                for field, selector in selectors.items():
                    if field != "container":
                        elem = container.select_one(selector)
                        if elem:
                            item["data"][field] = elem.get_text(strip=True)
                            # Set title if title field exists
                            if field == "title":
                                item["title"] = elem.get_text(strip=True)
                
                # Extract all text if no specific selectors or as fallback
                if not item["data"]:
                    item["content"] = container.get_text(strip=True)[:500]  # Limit to 500 chars
                else:
                    # Combine all extracted data as content
                    item["content"] = " ".join(item["data"].values())[:500]
                
                # Only add if we got some data
                if item["data"] or item["content"]:
                    items.append(item)
        else:
            # Extract entire page content
            item = {
                "source_id": source.get("_id"),
                "source_url": url,
                "type": "html",
                "title": soup.title.string if soup.title else url,
                "content": soup.get_text(strip=True)[:1000]  # Limit to 1000 chars
            }
            items.append(item)
        
        return items
    
    def _crawl_dynamic(self, source: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Crawl dynamic JavaScript-rendered pages"""
        url = source.get("url")
        selectors = source.get("selectors", {})
        max_items = source.get("max_items", 50)
        wait_time = source.get("wait_time", 5)
        
        driver = Driver(uc=True, headless=True)
        
        try:
            driver.get(url)
            time.sleep(wait_time)
            
            html = driver.page_source
            soup = BeautifulSoup(html, 'html.parser')
            
            items = []
            container_selector = selectors.get("container")
            
            if container_selector:
                containers = soup.select(container_selector)[:max_items]
                
                for container in containers:
                    item = {
                        "source_id": source.get("_id"),
                        "source_url": url,
                        "type": "dynamic",
                        "data": {}
                    }
                    
                    for field, selector in selectors.items():
                        if field != "container":
                            elem = container.select_one(selector)
                            if elem:
                                item["data"][field] = elem.get_text(strip=True)
                    
                    if item["data"]:
                        items.append(item)
            
            return items
        
        finally:
            driver.quit()
    
    def _crawl_rss(self, source: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Crawl RSS feeds"""
        url = source.get("url")
        max_items = source.get("max_items", 50)
        
        feed = feedparser.parse(url)
        
        items = []
        for entry in feed.entries[:max_items]:
            item = {
                "source_id": source.get("_id"),
                "source_url": url,
                "type": "rss",
                "title": entry.get("title", ""),
                "content": entry.get("summary", "") or entry.get("description", ""),
                "link": entry.get("link", ""),
                "published": entry.get("published", "")
            }
            items.append(item)
        
        return items
    
    def _crawl_pdf(self, source: Dict[str, Any]) -> Dict[str, Any]:
        """Crawl PDF documents"""
        url = source.get("url")
        
        response = self.session.get(url, timeout=30)
        response.raise_for_status()
        
        pdf_file = io.BytesIO(response.content)
        pdf_reader = PyPDF2.PdfReader(pdf_file)
        
        text = ""
        for page in pdf_reader.pages:
            text += page.extract_text()
        
        item = {
            "source_id": source.get("_id"),
            "source_url": url,
            "type": "pdf",
            "title": source.get("name", "PDF Document"),
            "content": text,
            "pages": len(pdf_reader.pages)
        }
        
        return item
    
    def _crawl_xml(self, source: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Crawl XML documents"""
        url = source.get("url")
        
        response = self.session.get(url, timeout=30)
        response.raise_for_status()
        
        soup = BeautifulSoup(response.content, 'xml')
        
        items = []
        # Extract all items (customize based on XML structure)
        for item_tag in soup.find_all(['item', 'entry', 'record']):
            item = {
                "source_id": source.get("_id"),
                "source_url": url,
                "type": "xml",
                "content": item_tag.get_text(strip=True)
            }
            items.append(item)
        
        return items if items else [{
            "source_id": source.get("_id"),
            "source_url": url,
            "type": "xml",
            "content": soup.get_text(strip=True)
        }]
    
    def _crawl_txt(self, source: Dict[str, Any]) -> Dict[str, Any]:
        """Crawl plain text files"""
        url = source.get("url")
        
        response = self.session.get(url, timeout=30)
        response.raise_for_status()
        
        item = {
            "source_id": source.get("_id"),
            "source_url": url,
            "type": "txt",
            "title": source.get("name", "Text Document"),
            "content": response.text
        }
        
        return item
