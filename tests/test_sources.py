"""Test which default sources are working"""
from database import CrawlerDatabase
from crawler_enhanced import EnhancedWebCrawler
from default_sources import DEFAULT_SOURCES

print("=" * 70)
print("TESTING DEFAULT SOURCES")
print("=" * 70)

db = CrawlerDatabase()
crawler = EnhancedWebCrawler(db)

working = []
not_working = []

for source in DEFAULT_SOURCES:
    print(f"\n🔄 Testing: {source['name']} ({source['type']})")
    print(f"   URL: {source['url']}")
    
    temp_source = {
        "_id": "test_" + source['name'].replace(" ", "_"),
        "name": source["name"],
        "url": source["url"],
        "type": source["type"],
        "max_items": 5
    }
    
    if "selectors" in source:
        temp_source["selectors"] = source["selectors"]
    
    try:
        result = crawler.crawl_source(temp_source)
        
        if result['status'] == 'success':
            print(f"   ✅ SUCCESS - Collected {result['items_collected']} items")
            working.append(source['name'])
        elif result['status'] == 'no_data':
            print(f"   ⚠️  NO DATA - {result.get('errors', ['No items found'])}")
            not_working.append((source['name'], 'No data'))
        else:
            print(f"   ❌ ERROR - {result.get('errors', ['Unknown error'])}")
            not_working.append((source['name'], str(result.get('errors', ['Unknown error']))))
    except Exception as e:
        print(f"   ❌ EXCEPTION - {str(e)}")
        not_working.append((source['name'], str(e)))

print("\n" + "=" * 70)
print("SUMMARY")
print("=" * 70)
print(f"\n✅ Working sources ({len(working)}):")
for name in working:
    print(f"   • {name}")

print(f"\n❌ Not working sources ({len(not_working)}):")
for name, error in not_working:
    print(f"   • {name}: {error}")

print(f"\n📊 Success rate: {len(working)}/{len(DEFAULT_SOURCES)} ({len(working)/len(DEFAULT_SOURCES)*100:.1f}%)")
print("=" * 70)

db.close()
