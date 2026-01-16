"""
Enhanced Web Crawler with Image Support
Adds image URL extraction to the base crawler
"""
from crawler import WebCrawler
from bs4 import BeautifulSoup
from typing import Dict, List, Any
from urllib.parse import urljoin

class EnhancedWebCrawler(WebCrawler):
    """Enhanced crawler with better image handling"""
    
    def _crawl_html(self, source: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Crawl HTML pages with image extraction"""
        url = source.get("url")
        selectors = source.get("selectors", {})
        max_items = source.get("max_items", 50)
        
        response = self.session.get(url, timeout=30)
        response.raise_for_status()
        
        soup = BeautifulSoup(response.text, 'html.parser')
        
        items = []
        container_selector = selectors.get("container")
        
        if container_selector:
            all_containers = soup.select(container_selector)
            containers = all_containers[:max_items]
            
            print(f"   Found {len(all_containers)} containers, processing {len(containers)} (max_items={max_items})")
            
            if not containers:
                print(f"⚠️ No elements found with selector: {container_selector}")
            
            for container in containers:
                item = {
                    "source_id": source.get("_id"),
                    "source_url": url,
                    "type": "html",
                    "data": {},
                    "title": "",
                    "content": "",
                    "images": []
                }
                
                # Extract fields
                for field, selector in selectors.items():
                    if field != "container":
                        elem = container.select_one(selector)
                        if elem:
                            # Check if it's an image
                            if elem.name == 'img':
                                img_src = elem.get('src', '')
                                img_alt = elem.get('alt', '')
                                if img_src:
                                    img_src = self._make_absolute_url(img_src, url)
                                    item["images"].append({
                                        "url": img_src,
                                        "alt": img_alt
                                    })
                                item["data"][field] = img_alt or img_src
                                if field == "title":
                                    item["title"] = img_alt or "Image"
                            else:
                                text = elem.get_text(strip=True)
                                item["data"][field] = text
                                if field == "title":
                                    item["title"] = text
                
                # Extract all images in container
                for img in container.find_all('img'):
                    img_src = img.get('src', '')
                    if img_src:
                        img_src = self._make_absolute_url(img_src, url)
                        # Avoid duplicates
                        if not any(i['url'] == img_src for i in item["images"]):
                            item["images"].append({
                                "url": img_src,
                                "alt": img.get('alt', '')
                            })
                
                # Extract text content
                if not item["data"]:
                    item["content"] = container.get_text(strip=True)[:500]
                else:
                    item["content"] = " ".join(str(v) for v in item["data"].values())[:500]
                
                # Only add if we got some data
                if item["data"] or item["content"] or item["images"]:
                    items.append(item)
        else:
            # Extract entire page
            item = {
                "source_id": source.get("_id"),
                "source_url": url,
                "type": "html",
                "title": soup.title.string if soup.title else url,
                "content": soup.get_text(strip=True)[:1000],
                "images": []
            }
            
            # Extract all images from page
            for img in soup.find_all('img')[:20]:
                img_src = img.get('src', '')
                if img_src:
                    img_src = self._make_absolute_url(img_src, url)
                    item["images"].append({
                        "url": img_src,
                        "alt": img.get('alt', '')
                    })
            
            items.append(item)
        
        return items
    
    def _crawl_rss(self, source: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Crawl RSS feeds with image extraction"""
        import feedparser
        
        url = source.get("url")
        max_items = source.get("max_items", 50)
        
        feed = feedparser.parse(url)
        
        # Check if feed has entries
        total_available = len(feed.entries)
        print(f"   RSS feed has {total_available} entries, requesting {max_items}")
        
        items = []
        for entry in feed.entries[:max_items]:
            item = {
                "source_id": source.get("_id"),
                "source_url": url,
                "type": "rss",
                "title": entry.get("title", ""),
                "content": entry.get("summary", "") or entry.get("description", ""),
                "link": entry.get("link", ""),
                "published": entry.get("published", ""),
                "images": []
            }
            
            # Extract images from media content
            if hasattr(entry, 'media_content'):
                for media in entry.media_content:
                    if media.get('type', '').startswith('image'):
                        item["images"].append({
                            "url": media.get('url', ''),
                            "alt": entry.get("title", "")
                        })
            
            # Extract images from enclosures
            if hasattr(entry, 'enclosures'):
                for enclosure in entry.enclosures:
                    if enclosure.get('type', '').startswith('image'):
                        item["images"].append({
                            "url": enclosure.get('href', ''),
                            "alt": entry.get("title", "")
                        })
            
            # Parse content for images
            content_html = entry.get("content", [{}])[0].get("value", "") if entry.get("content") else entry.get("summary", "")
            if content_html:
                soup = BeautifulSoup(content_html, 'html.parser')
                for img in soup.find_all('img'):
                    img_src = img.get('src', '')
                    if img_src:
                        item["images"].append({
                            "url": img_src,
                            "alt": img.get('alt', entry.get("title", ""))
                        })
            
            items.append(item)
        
        print(f"   Collected {len(items)} items (requested {max_items}, available {total_available})")
        return items
    
    def _make_absolute_url(self, url: str, base_url: str) -> str:
        """Convert relative URLs to absolute"""
        if url.startswith('//'):
            return 'https:' + url
        elif url.startswith('/'):
            return urljoin(base_url, url)
        elif not url.startswith('http'):
            return urljoin(base_url, url)
        return url
