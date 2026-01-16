"""
Add Default Sources Script
Adds sample crawl sources to test the system
"""
from database import CrawlerDatabase

def add_default_sources():
    """Add default sources for testing"""
    print("🔧 Adding Default Sources")
    print("=" * 60)
    
    db = CrawlerDatabase()
    
    if db.sources is None:
        print("❌ Database not connected. Please fix MongoDB authentication first.")
        print("\n📝 To disable MongoDB authentication:")
        print("   1. Stop MongoDB")
        print("   2. Find mongod.cfg (usually in C:\\Program Files\\MongoDB\\Server\\<version>\\bin\\)")
        print("   3. Comment out the 'security:' section")
        print("   4. Restart MongoDB")
        return False
    
    # Default sources
    sources = [
        {
            "name": "Example.com",
            "url": "https://example.com",
            "type": "html",
            "frequency": "daily",
            "max_items": 1,
            "schedule_time": "09:00"
        },
        {
            "name": "GitHub Blog RSS",
            "url": "https://github.blog/feed/",
            "type": "rss",
            "frequency": "hourly",
            "max_items": 10,
            "schedule_time": "00:00"
        },
        {
            "name": "Python.org",
            "url": "https://www.python.org",
            "type": "html",
            "frequency": "weekly",
            "max_items": 5,
            "schedule_time": "00:00"
        },
        {
            "name": "W3C Text File",
            "url": "https://www.w3.org/TR/PNG/iso_8859-1.txt",
            "type": "txt",
            "frequency": "monthly",
            "max_items": 1,
            "schedule_time": "00:00"
        }
    ]
    
    added = 0
    for source_data in sources:
        try:
            source_id = db.add_source(source_data)
            print(f"✅ Added: {source_data['name']} (ID: {source_id})")
            added += 1
        except Exception as e:
            print(f"❌ Failed to add {source_data['name']}: {e}")
    
    print("\n" + "=" * 60)
    print(f"✅ Successfully added {added}/{len(sources)} sources")
    print("\n🚀 Next steps:")
    print("   1. Open http://localhost:8501 in your browser")
    print("   2. Go to 🔗 Sources tab to see your sources")
    print("   3. Click ▶️ Crawl Now to test each source")
    
    db.close()
    return True

if __name__ == "__main__":
    add_default_sources()
