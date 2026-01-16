"""Test crawling PDFs, Books, and Images"""
from database import CrawlerDatabase
from crawler_enhanced import EnhancedWebCrawler
from default_sources import DEFAULT_SOURCES

print("=" * 70)
print("🧪 TESTING SPECIAL CONTENT SOURCES")
print("=" * 70)

# Initialize
db = CrawlerDatabase()
crawler = EnhancedWebCrawler(db)

# Get sources by category
pdf_sources = [s for s in DEFAULT_SOURCES if s['category'] == 'PDF Documents']
book_sources = [s for s in DEFAULT_SOURCES if s['category'] == 'Books']
image_sources = [s for s in DEFAULT_SOURCES if s['category'] == 'Images']

print(f"\n📄 PDF Sources: {len(pdf_sources)}")
for s in pdf_sources:
    print(f"   • {s['name']}")

print(f"\n📚 Book Sources: {len(book_sources)}")
for s in book_sources:
    print(f"   • {s['name']}")

print(f"\n🖼️  Image Sources: {len(image_sources)}")
for s in image_sources:
    print(f"   • {s['name']}")

# Test Image Source
print("\n" + "=" * 70)
print("🖼️  TESTING IMAGE SOURCE")
print("=" * 70)

if image_sources:
    test_source = image_sources[0]  # NASA Image of the Day
    print(f"\n🔄 Crawling: {test_source['name']}")
    print(f"   URL: {test_source['url']}")
    
    temp_source = {
        "_id": "temp_image_test",
        "name": test_source["name"],
        "url": test_source["url"],
        "type": test_source["type"],
        "max_items": 5
    }
    
    result = crawler.crawl_source(temp_source)
    print(f"\n📊 Results:")
    print(f"   Status: {result['status']}")
    print(f"   Items: {result['items_collected']}")
    
    if result['status'] == 'success':
        # Get the data
        recent = db.get_recent_data(limit=3)
        for i, item in enumerate(recent[:3], 1):
            print(f"\n   Item {i}:")
            print(f"      Title: {item.get('title', 'N/A')}")
            if 'images' in item and item['images']:
                print(f"      Images found: {len(item['images'])}")
                for img in item['images'][:2]:
                    print(f"         • {img.get('url', 'N/A')[:80]}...")

# Test Book Source
print("\n" + "=" * 70)
print("📚 TESTING BOOK SOURCE")
print("=" * 70)

if book_sources:
    test_source = book_sources[0]  # Project Gutenberg
    print(f"\n🔄 Crawling: {test_source['name']}")
    print(f"   URL: {test_source['url']}")
    
    temp_source = {
        "_id": "temp_book_test",
        "name": test_source["name"],
        "url": test_source["url"],
        "type": test_source["type"],
        "max_items": 10
    }
    
    if "selectors" in test_source:
        temp_source["selectors"] = test_source["selectors"]
    
    result = crawler.crawl_source(temp_source)
    print(f"\n📊 Results:")
    print(f"   Status: {result['status']}")
    print(f"   Items: {result['items_collected']}")
    
    if result['status'] == 'success':
        recent = db.get_recent_data(limit=3)
        for i, item in enumerate(recent[:3], 1):
            print(f"\n   Book {i}:")
            print(f"      Title: {item.get('title', 'N/A')}")
            content = item.get('content', '')
            if content:
                print(f"      Info: {content[:100]}...")

# Test PDF Source (RSS feed with PDF links)
print("\n" + "=" * 70)
print("📄 TESTING PDF SOURCE")
print("=" * 70)

if pdf_sources:
    # Use arXiv RSS which links to PDFs
    test_source = [s for s in pdf_sources if 'rss' in s['url'].lower()][0] if any('rss' in s['url'].lower() for s in pdf_sources) else pdf_sources[0]
    print(f"\n🔄 Crawling: {test_source['name']}")
    print(f"   URL: {test_source['url']}")
    
    temp_source = {
        "_id": "temp_pdf_test",
        "name": test_source["name"],
        "url": test_source["url"],
        "type": test_source["type"],
        "max_items": 5
    }
    
    result = crawler.crawl_source(temp_source)
    print(f"\n📊 Results:")
    print(f"   Status: {result['status']}")
    print(f"   Items: {result['items_collected']}")
    
    if result['status'] == 'success':
        recent = db.get_recent_data(limit=3)
        for i, item in enumerate(recent[:3], 1):
            print(f"\n   Paper {i}:")
            print(f"      Title: {item.get('title', 'N/A')}")
            if 'link' in item:
                print(f"      Link: {item.get('link', 'N/A')}")

# Summary
print("\n" + "=" * 70)
print("📊 FINAL STATISTICS")
print("=" * 70)

stats = db.get_statistics()
print(f"\n   Total Sources: {stats['total_sources']}")
print(f"   Total Data Items: {stats['total_data_items']}")

print("\n" + "=" * 70)
print("✅ TESTING COMPLETE")
print("=" * 70)
print("\n💡 You can now use these sources in the dashboard:")
print("   1. Open http://localhost:8502")
print("   2. Go to Sources → Quick Crawl")
print("   3. Select from categories:")
print("      • PDF Documents (arXiv papers, WHO reports)")
print("      • Books (Project Gutenberg, Internet Archive)")
print("      • Images (NASA, Unsplash)")
print("   4. Configure and crawl!")
print("=" * 70)

db.close()
