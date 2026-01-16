"""
Test All Reference Sources
Tests the crawler with different website types
"""
from database import CrawlerDatabase
from crawler import WebCrawler
import time

def test_all_sources():
    """Test crawler with all reference sources"""
    print("🧪 Testing Crawler with All Reference Sources")
    print("=" * 60)
    
    db = CrawlerDatabase()
    crawler = WebCrawler(db)
    
    # Test sources covering all types
    test_sources = [
        {
            "_id": "test_html_1",
            "name": "Example.com (HTML)",
            "url": "https://example.com",
            "type": "html",
            "max_items": 1
        },
        {
            "_id": "test_html_2",
            "name": "Python.org (HTML)",
            "url": "https://www.python.org",
            "type": "html",
            "max_items": 5
        },
        {
            "_id": "test_rss_1",
            "name": "GitHub Blog (RSS)",
            "url": "https://github.blog/feed/",
            "type": "rss",
            "max_items": 5
        },
        {
            "_id": "test_txt_1",
            "name": "Simple Text File (TXT)",
            "url": "https://www.gutenberg.org/files/74/74-0.txt",
            "type": "txt",
            "max_items": 1
        },
        {
            "_id": "test_html_3",
            "name": "Wikipedia (HTML)",
            "url": "https://en.wikipedia.org/wiki/Web_scraping",
            "type": "html",
            "max_items": 1
        },
        {
            "_id": "test_dynamic_1",
            "name": "Sarouty.ma (Dynamic)",
            "url": "https://www.sarouty.ma/louer",
            "type": "dynamic",
            "max_items": 3,
            "selectors": {
                "container": ".MuiCard-root",
                "title": "h5.MuiTypography-h5",
                "price": "h5.css-1xwnyu4"
            }
        }
    ]
    
    results = []
    
    for i, source in enumerate(test_sources, 1):
        print(f"\n[{i}/{len(test_sources)}] Testing: {source['name']}")
        print("-" * 60)
        
        try:
            result = crawler.crawl_source(source)
            
            results.append({
                "name": source["name"],
                "url": source["url"],
                "type": source["type"],
                "status": result["status"],
                "items": result["items_collected"],
                "errors": result.get("errors", [])
            })
            
            if result["status"] == "success":
                print(f"✅ SUCCESS: Collected {result['items_collected']} items")
            elif result["status"] == "no_data":
                print(f"⚠️  NO DATA: {result.get('errors', ['No data found'])}")
            else:
                print(f"❌ FAILED: {result.get('errors', ['Unknown error'])}")
            
            # Be polite - wait between requests
            if i < len(test_sources):
                time.sleep(2)
                
        except Exception as e:
            print(f"❌ EXCEPTION: {e}")
            results.append({
                "name": source["name"],
                "url": source["url"],
                "type": source["type"],
                "status": "error",
                "items": 0,
                "errors": [str(e)]
            })
    
    # Summary
    print("\n" + "=" * 60)
    print("📊 TEST SUMMARY")
    print("=" * 60)
    
    success_count = sum(1 for r in results if r["status"] == "success")
    total_items = sum(r["items"] for r in results)
    
    print(f"\nTotal Tests: {len(results)}")
    print(f"Successful: {success_count}")
    print(f"Failed: {len(results) - success_count}")
    print(f"Total Items Collected: {total_items}")
    
    print("\n📋 Detailed Results:")
    print("-" * 60)
    
    for result in results:
        status_icon = "✅" if result["status"] == "success" else "❌"
        print(f"{status_icon} {result['name']}")
        print(f"   URL: {result['url']}")
        print(f"   Type: {result['type']}")
        print(f"   Status: {result['status']}")
        print(f"   Items: {result['items']}")
        if result["errors"]:
            print(f"   Errors: {', '.join(result['errors'][:2])}")
        print()
    
    # Final verdict
    print("=" * 60)
    if success_count == len(results):
        print("🎉 ALL TESTS PASSED!")
        print("✅ Crawler is working perfectly with all source types")
    elif success_count > 0:
        print(f"⚠️  PARTIAL SUCCESS: {success_count}/{len(results)} tests passed")
        print("   Some sources may need adjustment")
    else:
        print("❌ ALL TESTS FAILED")
        print("   Check MongoDB authentication and network connection")
    
    print("=" * 60)
    
    db.close()
    return results

if __name__ == "__main__":
    test_all_sources()
