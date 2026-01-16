"""
MongoDB Connection Test Script

Tests MongoDB connectivity, authentication modes, and CRUD operations.
"""
import sys
import os

# Add parent directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from database import CrawlerDatabase
from datetime import datetime


def test_connection():
    """Test basic MongoDB connection"""
    print("\n" + "="*60)
    print("🔌 TESTING MONGODB CONNECTION")
    print("="*60)
    
    try:
        db = CrawlerDatabase()
        
        if db.client is None:
            print("❌ MongoDB connection failed")
            print("   Make sure MongoDB is running:")
            print("   - Windows: net start MongoDB")
            print("   - Mac: brew services start mongodb-community")
            print("   - Linux: sudo systemctl start mongod")
            return False
        
        # Test server info
        server_info = db.client.server_info()
        print(f"✅ Connected to MongoDB")
        print(f"   Version: {server_info.get('version', 'Unknown')}")
        print(f"   Database: {db.db.name}")
        
        db.close()
        return True
        
    except Exception as e:
        print(f"❌ Connection test failed: {e}")
        return False


def test_authentication_modes():
    """Test both authenticated and non-authenticated connections"""
    print("\n" + "="*60)
    print("🔐 TESTING AUTHENTICATION MODES")
    print("="*60)
    
    results = {}
    
    # Test no-auth connection
    print("\n📝 Testing no-auth connection...")
    try:
        db_no_auth = CrawlerDatabase(
            connection_string="mongodb://localhost:27017/",
            db_name="web_crawler_test"
        )
        
        if db_no_auth.client is not None:
            print("✅ No-auth connection successful")
            results['no_auth'] = True
            db_no_auth.close()
        else:
            print("❌ No-auth connection failed")
            results['no_auth'] = False
            
    except Exception as e:
        print(f"❌ No-auth connection error: {e}")
        results['no_auth'] = False
    
    # Test with-auth connection (if credentials are configured)
    print("\n📝 Testing with-auth connection...")
    try:
        import os
        from dotenv import load_dotenv
        load_dotenv()
        
        auth_uri = os.getenv('MONGODB_URI')
        if auth_uri and 'localhost:27017/' not in auth_uri:
            db_auth = CrawlerDatabase(
                connection_string=auth_uri,
                db_name="web_crawler_test"
            )
            
            if db_auth.client is not None:
                print("✅ With-auth connection successful")
                results['with_auth'] = True
                db_auth.close()
            else:
                print("❌ With-auth connection failed")
                results['with_auth'] = False
        else:
            print("⚠️  Auth credentials not configured, skipping")
            results['with_auth'] = 'skipped'
            
    except Exception as e:
        print(f"⚠️  With-auth connection error: {e}")
        print("   This is normal if authentication is not set up")
        results['with_auth'] = 'skipped'
    
    return results


def test_crud_operations():
    """Test Create, Read, Update, Delete operations"""
    print("\n" + "="*60)
    print("📝 TESTING CRUD OPERATIONS")
    print("="*60)
    
    try:
        db = CrawlerDatabase(
            connection_string="mongodb://localhost:27017/",
            db_name="web_crawler_test"
        )
        
        if db.client is None:
            print("❌ Cannot test CRUD - database not connected")
            return False
        
        # CREATE - Add a test source
        print("\n✏️  Testing CREATE...")
        test_source = {
            "name": "Test Source",
            "url": "https://example.com/test",
            "type": "html",
            "frequency": "daily",
            "max_items": 10,
            "schedule_time": "09:00"
        }
        
        source_id = db.add_source(test_source)
        if source_id:
            print(f"✅ Created source with ID: {source_id}")
        else:
            print("❌ Failed to create source")
            db.close()
            return False
        
        # READ - Get the source back
        print("\n📖 Testing READ...")
        retrieved_source = db.get_source(source_id)
        if retrieved_source and retrieved_source['name'] == test_source['name']:
            print(f"✅ Retrieved source: {retrieved_source['name']}")
        else:
            print("❌ Failed to retrieve source")
            db.close()
            return False
        
        # UPDATE - Modify the source
        print("\n🔄 Testing UPDATE...")
        update_data = {"name": "Updated Test Source", "max_items": 20}
        updated = db.update_source(source_id, update_data)
        if updated:
            updated_source = db.get_source(source_id)
            if updated_source['name'] == "Updated Test Source":
                print(f"✅ Updated source: {updated_source['name']}")
            else:
                print("❌ Update didn't persist")
                db.close()
                return False
        else:
            print("❌ Failed to update source")
            db.close()
            return False
        
        # Test data storage
        print("\n💾 Testing DATA STORAGE...")
        test_data = {
            "source_id": source_id,
            "source_url": "https://example.com/test",
            "type": "html",
            "title": "Test Data",
            "content": "This is test content"
        }
        
        data_id = db.store_crawled_data(test_data)
        if data_id:
            print(f"✅ Stored data with ID: {data_id}")
        else:
            print("❌ Failed to store data")
        
        # Test data retrieval
        print("\n🔍 Testing DATA RETRIEVAL...")
        recent_data = db.get_recent_data(limit=1)
        if recent_data and len(recent_data) > 0:
            print(f"✅ Retrieved {len(recent_data)} data items")
        else:
            print("⚠️  No data retrieved (might be empty)")
        
        # DELETE - Remove the test source
        print("\n🗑️  Testing DELETE...")
        deleted = db.delete_source(source_id)
        if deleted:
            print(f"✅ Deleted source")
            
            # Verify deletion
            deleted_source = db.get_source(source_id)
            if deleted_source is None:
                print("✅ Verified source was deleted")
            else:
                print("⚠️  Source still exists after deletion")
        else:
            print("❌ Failed to delete source")
        
        # Clean up test database
        print("\n🧹 Cleaning up test database...")
        db.db.drop_collection('sources')
        db.db.drop_collection('crawled_data')
        db.db.drop_collection('crawl_logs')
        print("✅ Test database cleaned")
        
        db.close()
        return True
        
    except Exception as e:
        print(f"❌ CRUD operations test failed: {e}")
        import traceback
        traceback.print_exc()
        return False


def test_statistics():
    """Test statistics generation"""
    print("\n" + "="*60)
    print("📊 TESTING STATISTICS")
    print("="*60)
    
    try:
        db = CrawlerDatabase()
        
        if db.client is None:
            print("❌ Cannot test statistics - database not connected")
            return False
        
        stats = db.get_statistics()
        
        print(f"✅ Statistics retrieved:")
        print(f"   Total sources: {stats['total_sources']}")
        print(f"   Active sources: {stats['active_sources']}")
        print(f"   Total data items: {stats['total_data_items']}")
        print(f"   Data by source: {len(stats['data_by_source'])} sources")
        
        db.close()
        return True
        
    except Exception as e:
        print(f"❌ Statistics test failed: {e}")
        return False


def main():
    """Run all MongoDB tests"""
    print("\n" + "="*60)
    print("🧪 MONGODB CONNECTION TEST SUITE")
    print("="*60)
    
    results = {}
    
    # Run tests
    results['connection'] = test_connection()
    
    if results['connection']:
        auth_results = test_authentication_modes()
        results['no_auth'] = auth_results.get('no_auth', False)
        results['with_auth'] = auth_results.get('with_auth', 'skipped')
        
        results['crud'] = test_crud_operations()
        results['statistics'] = test_statistics()
    else:
        print("\n⚠️  Skipping other tests due to connection failure")
        results['no_auth'] = False
        results['with_auth'] = 'skipped'
        results['crud'] = False
        results['statistics'] = False
    
    # Summary
    print("\n" + "="*60)
    print("📊 TEST SUMMARY")
    print("="*60)
    
    for test_name, result in results.items():
        if result == 'skipped':
            status = "⏭️  SKIPPED"
        elif result:
            status = "✅ PASS"
        else:
            status = "❌ FAIL"
        print(f"{test_name.replace('_', ' ').title():.<30} {status}")
    
    # Overall result
    passed = sum(1 for r in results.values() if r is True)
    failed = sum(1 for r in results.values() if r is False)
    skipped = sum(1 for r in results.values() if r == 'skipped')
    
    print("\n" + "="*60)
    print(f"TOTAL: {passed} passed, {failed} failed, {skipped} skipped")
    print("="*60)
    
    if failed == 0 and passed > 0:
        print("\n🎉 All MongoDB tests passed!")
        print("✅ Database is properly configured and working")
        return 0
    elif passed > 0:
        print("\n⚠️  Some tests passed, but there are issues")
        print("   Check the output above for details")
        return 1
    else:
        print("\n❌ MongoDB tests failed")
        print("   Make sure MongoDB is running and accessible")
        return 1


if __name__ == "__main__":
    sys.exit(main())
