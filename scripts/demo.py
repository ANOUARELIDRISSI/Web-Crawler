"""
Demo script to populate the database with sample data
"""
from database import CrawlerDatabase
from crawler import WebCrawler
import time

def main():
    print("🕷️ Web Crawler Demo")
    print("=" * 50)
    
    # Initialize
    db = CrawlerDatabase()
    crawler = WebCrawler(db)
    
    print("\n📝 Adding sample sources...")
    
    # Sample sources
    sources = [
        {
            "name": "Python.org News",
            "url": "https://www.python.org/blogs/",
            "type": "html",
            "frequency": "daily",
            "max_items": 10,
            "schedule_time": "09:00"
        },
        {
            "name": "GitHub Blog RSS",
            "url": "https://github.blog/feed/",
            "type": "rss",
            "frequency": "hourly",
            "max_items": 20,
            "schedule_time": "00:00"
        },
        {
            "name": "Example Text File",
            "url": "https://www.w3.org/TR/PNG/iso_8859-1.txt",
            "type": "txt",
            "frequency": "weekly",
            "max_items": 1,
            "schedule_time": "00:00"
        }
    ]
    
    added_sources = []
    for source_data in sources:
        try:
            source_id = db.add_source(source_data)
            added_sources.append(source_id)
            print(f"✅ Added: {source_data['name']}")
        except Exception as e:
            print(f"❌ Error adding {source_data['name']}: {e}")
    
    print(f"\n📊 Added {len(added_sources)} sources")
    
    # Crawl the sources
    print("\n🔄 Crawling sources...")
    
    for source_id in added_sources:
        source = db.get_source(source_id)
        if source:
            print(f"\n📄 Crawling: {source['name']}")
            try:
                result = crawler.crawl_source(source)
                if result["status"] == "success":
                    print(f"   ✅ Success! Collected {result['items_collected']} items")
                else:
                    print(f"   ❌ Failed: {result.get('errors', ['Unknown error'])}")
            except Exception as e:
                print(f"   ❌ Error: {e}")
            
            time.sleep(2)  # Be polite
    
    # Show statistics
    print("\n📈 Statistics:")
    stats = db.get_statistics()
    print(f"   Total Sources: {stats['total_sources']}")
    print(f"   Active Sources: {stats['active_sources']}")
    print(f"   Total Data Items: {stats['total_data_items']}")
    
    print("\n✅ Demo complete!")
    print("\n🚀 Run the dashboard:")
    print("   streamlit run dashboard.py")
    
    db.close()

if __name__ == "__main__":
    main()
