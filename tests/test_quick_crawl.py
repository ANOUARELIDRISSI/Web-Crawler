"""Test the Quick Crawl functionality"""
from database import CrawlerDatabase
from crawler import WebCrawler
from default_sources import DEFAULT_SOURCES

print("=" * 70)
print("🧪 TESTING QUICK CRAWL FEATURE")
print("=" * 70)

# Initialize
db = CrawlerDatabase()
crawler = WebCrawler(db)

# Simulate user selecting a source
print("\n📋 Available Default Sources:")
for i, source in enumerate(DEFAULT_SOURCES[:5], 1):
    print(f"   {i}. {source['name']} ({source['type']}) - {source['category']}")

# Select first RSS source (GitHub Blog)
selected = DEFAULT_SOURCES[1]  # GitHub Blog RSS
print(f"\n✅ Selected: {selected['name']}")
print(f"   URL: {selected['url']}")
print(f"   Type: {selected['type']}")

# User configures settings
max_items = 15
frequency = "daily"

print(f"\n⚙️  Configuration:")
print(f"   Max Items: {max_items}")
print(f"   Frequency: {frequency}")

# Create temporary source for immediate crawl
temp_source = {
    "_id": "temp_quick_crawl",
    "name": selected["name"],
    "url": selected["url"],
    "type": selected["type"],
    "max_items": max_items,
    "frequency": frequency
}

# Crawl now
print(f"\n🚀 Starting crawl...")
result = crawler.crawl_source(temp_source)

print(f"\n📊 Crawl Results:")
print(f"   Status: {result['status']}")
print(f"   Items Collected: {result['items_collected']}")
if result.get('errors'):
    print(f"   Errors: {result['errors']}")

# Show preview of collected data
if result['status'] == 'success' and result['items_collected'] > 0:
    print(f"\n📄 Preview of Collected Data:")
    recent = db.get_recent_data(limit=3)
    for i, item in enumerate(recent[:3], 1):
        print(f"\n   Item {i}:")
        print(f"      Title: {item.get('title', 'N/A')}")
        print(f"      Type: {item.get('type', 'N/A')}")
        content = item.get('content', '')
        if content:
            preview = content[:100] + "..." if len(content) > 100 else content
            print(f"      Content: {preview}")

# Check total data
stats = db.get_statistics()
print(f"\n📊 Database Statistics:")
print(f"   Total Data Items: {stats['total_data_items']}")
print(f"   Total Sources: {stats['total_sources']}")

print("\n" + "=" * 70)
print("✅ QUICK CRAWL TEST COMPLETE")
print("=" * 70)
print("\n💡 The dashboard now allows users to:")
print("   1. Select any default source from a dropdown")
print("   2. Configure max items and frequency")
print("   3. Click 'Crawl Now' to immediately scrape data")
print("   4. See preview of collected data")
print("   5. Optionally add to sources for scheduling")
print("\n🌐 Open http://localhost:8502 and go to Sources → Quick Crawl tab")
print("=" * 70)

db.close()
