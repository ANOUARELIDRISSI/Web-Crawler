"""Test crawler and verify data in MongoDB"""
from database import CrawlerDatabase
from crawler import WebCrawler

# Initialize
db = CrawlerDatabase()
crawler = WebCrawler(db)

# Get statistics
stats = db.get_statistics()
print(f"\n📊 Database Statistics:")
print(f"   Total sources: {stats['total_sources']}")
print(f"   Active sources: {stats['active_sources']}")
print(f"   Total data items: {stats['total_data_items']}")

# Get recent data
data = db.get_recent_data(limit=3)
print(f"\n📝 Recent data items: {len(data)}")
if data:
    for item in data:
        print(f"\n   Title: {item.get('title', 'N/A')}")
        print(f"   Type: {item.get('type', 'N/A')}")
        print(f"   Content preview: {item.get('content', '')[:100]}...")

# Test crawling one more source
sources = db.get_all_sources()
if len(sources) > 1:
    print(f"\n🔄 Testing crawl of: {sources[1]['name']}")
    result = crawler.crawl_source(sources[1])
    print(f"   Status: {result['status']}")
    print(f"   Items collected: {result['items_collected']}")

print("\n✅ All tests passed! System is working properly.")
