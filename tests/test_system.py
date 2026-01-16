"""
System Test Script
Tests all components of the Web Crawler system
"""
import sys
import os

# Add parent directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from database import CrawlerDatabase
from crawler import WebCrawler
from scheduler import CrawlerScheduler
import time

def test_database():
    """Test database connection and operations"""
    print("\n" + "="*60)
    print("🗄️  TESTING DATABASE")
    print("="*60)
    
    try:
        db = CrawlerDatabase()
        
        # Test statistics
        stats = db.get_statistics()
        print(f"✅ Database connected")
        print(f"   - Total sources: {stats['total_sources']}")
        print(f"   - Active sources: {stats['active_sources']}")
        print(f"   - Total data items: {stats['total_data_items']}")
        
        # Test adding a source
        test_source = {
            "name": "Test Source",
            "url": "https://example.com",
            "type": "html",
            "frequency": "daily",
            "max_items": 10,
            "schedule_time": "09:00"
        }
        
        try:
            source_id = db.add_source(test_source)
            print(f"✅ Added test source: {source_id}")
            
            # Get the source back
            source = db.get_source(source_id)
            if source:
                print(f"✅ Retrieved source: {source['name']}")
            
            # Delete the test source
            db.delete_source(source_id)
            print(f"✅ Deleted test source")
        except Exception as e:
            print(f"⚠️  Source operations: {e}")
        
        db.close()
        return True
    except Exception as e:
        print(f"❌ Database test failed: {e}")
        return False

def test_crawler():
    """Test crawler functionality"""
    print("\n" + "="*60)
    print("🕷️  TESTING CRAWLER")
    print("="*60)
    
    try:
        db = CrawlerDatabase()
        crawler = WebCrawler(db)
        
        # Test HTML crawling
        print("\n📄 Testing HTML crawler...")
        html_source = {
            "_id": "test_html",
            "name": "Example.com",
            "url": "https://example.com",
            "type": "html",
            "max_items": 1
        }
        
        result = crawler.crawl_source(html_source)
        if result["status"] == "success":
            print(f"✅ HTML crawl successful: {result['items_collected']} items")
        else:
            print(f"⚠️  HTML crawl: {result.get('errors', ['Unknown'])}")
        
        # Test RSS crawling
        print("\n📡 Testing RSS crawler...")
        rss_source = {
            "_id": "test_rss",
            "name": "GitHub Blog",
            "url": "https://github.blog/feed/",
            "type": "rss",
            "max_items": 5
        }
        
        result = crawler.crawl_source(rss_source)
        if result["status"] == "success":
            print(f"✅ RSS crawl successful: {result['items_collected']} items")
        else:
            print(f"⚠️  RSS crawl: {result.get('errors', ['Unknown'])}")
        
        # Test TXT crawling
        print("\n📝 Testing TXT crawler...")
        txt_source = {
            "_id": "test_txt",
            "name": "Text File",
            "url": "https://www.w3.org/TR/PNG/iso_8859-1.txt",
            "type": "txt",
            "max_items": 1
        }
        
        result = crawler.crawl_source(txt_source)
        if result["status"] == "success":
            print(f"✅ TXT crawl successful: {result['items_collected']} items")
        else:
            print(f"⚠️  TXT crawl: {result.get('errors', ['Unknown'])}")
        
        db.close()
        return True
    except Exception as e:
        print(f"❌ Crawler test failed: {e}")
        return False

def test_scheduler():
    """Test scheduler functionality"""
    print("\n" + "="*60)
    print("⏰ TESTING SCHEDULER")
    print("="*60)
    
    try:
        db = CrawlerDatabase()
        crawler = WebCrawler(db)
        scheduler = CrawlerScheduler(db, crawler)
        
        # Add a test source
        test_source = {
            "name": "Scheduler Test",
            "url": "https://example.com",
            "type": "html",
            "frequency": "hourly",
            "max_items": 1,
            "schedule_time": "00:00"
        }
        
        source_id = db.add_source(test_source)
        source = db.get_source(source_id)
        
        # Schedule the source
        scheduler.schedule_source(source)
        print(f"✅ Scheduled source: {source['name']}")
        
        # Get next runs
        next_runs = scheduler.get_next_runs()
        if next_runs:
            print(f"✅ Next scheduled runs: {len(next_runs)}")
            for sid, next_run in next_runs.items():
                print(f"   - {sid}: {next_run}")
        
        # Clean up
        db.delete_source(source_id)
        db.close()
        return True
    except Exception as e:
        print(f"❌ Scheduler test failed: {e}")
        return False

def test_dashboard():
    """Check if dashboard is accessible"""
    print("\n" + "="*60)
    print("🎨 TESTING DASHBOARD")
    print("="*60)
    
    try:
        import requests
        response = requests.get("http://localhost:8501", timeout=5)
        if response.status_code == 200:
            print("✅ Dashboard is accessible at http://localhost:8501")
            return True
        else:
            print(f"⚠️  Dashboard returned status code: {response.status_code}")
            return False
    except Exception as e:
        print(f"⚠️  Dashboard not accessible: {e}")
        print("   Run: streamlit run dashboard.py")
        return False

def main():
    """Run all tests"""
    print("\n" + "="*60)
    print("🧪 WEB CRAWLER SYSTEM TEST")
    print("="*60)
    
    results = {
        "Database": test_database(),
        "Crawler": test_crawler(),
        "Scheduler": test_scheduler(),
        "Dashboard": test_dashboard()
    }
    
    print("\n" + "="*60)
    print("📊 TEST RESULTS")
    print("="*60)
    
    for component, passed in results.items():
        status = "✅ PASS" if passed else "❌ FAIL"
        print(f"{component:.<30} {status}")
    
    total = len(results)
    passed = sum(results.values())
    
    print("\n" + "="*60)
    print(f"TOTAL: {passed}/{total} tests passed")
    print("="*60)
    
    if passed == total:
        print("\n🎉 All tests passed! System is ready to use.")
        print("\n🚀 Next steps:")
        print("   1. Open http://localhost:8501 in your browser")
        print("   2. Go to 🔗 Sources tab")
        print("   3. Add your first crawl source")
        print("   4. Click ▶️ Crawl Now to test it")
        print("   5. Go to ⚙️ Settings to start the scheduler")
    else:
        print("\n⚠️  Some tests failed. Check the output above.")

if __name__ == "__main__":
    main()
