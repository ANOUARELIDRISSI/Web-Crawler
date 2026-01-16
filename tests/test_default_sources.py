"""
Default Sources Test Script

Tests all default sources to verify they can be crawled successfully.
"""
import sys
import os
import time
from datetime import datetime

# Add parent directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from database import CrawlerDatabase
from crawler import WebCrawler
from default_sources import DEFAULT_SOURCES


def test_single_source(crawler, source_config, source_index, total_sources):
    """
    Test a single source and return results.
    
    Args:
        crawler: WebCrawler instance
        source_config: Source configuration dictionary
        source_index: Current source number (for display)
        total_sources: Total number of sources being tested
        
    Returns:
        dict: Test result with status, items collected, and errors
    """
    print(f"\n[{source_index}/{total_sources}] Testing: {source_config['name']}")
    print("-" * 60)
    print(f"   URL: {source_config['url']}")
    print(f"   Type: {source_config['type']}")
    
    # Create a test source object
    test_source = {
        "_id": f"test_{source_index}",
        "name": source_config['name'],
        "url": source_config['url'],
        "type": source_config['type'],
        "max_items": 5  # Limit to 5 items for testing
    }
    
    # Add selectors if present
    if 'selectors' in source_config:
        test_source['selectors'] = source_config['selectors']
    
    start_time = time.time()
    
    try:
        # Crawl the source
        result = crawler.crawl_source(test_source)
        
        elapsed_time = time.time() - start_time
        
        test_result = {
            "name": source_config['name'],
            "url": source_config['url'],
            "type": source_config['type'],
            "category": source_config.get('category', 'Unknown'),
            "status": result["status"],
            "items_collected": result["items_collected"],
            "response_time_ms": int(elapsed_time * 1000),
            "errors": result.get("errors", [])
        }
        
        # Display result
        if result["status"] == "success":
            print(f"   ✅ SUCCESS: Collected {result['items_collected']} items in {elapsed_time:.2f}s")
        elif result["status"] == "no_data":
            print(f"   ⚠️  NO DATA: {result.get('errors', ['No data found'])}")
        else:
            print(f"   ❌ FAILED: {result.get('errors', ['Unknown error'])}")
        
        return test_result
        
    except Exception as e:
        elapsed_time = time.time() - start_time
        print(f"   ❌ EXCEPTION: {e}")
        
        return {
            "name": source_config['name'],
            "url": source_config['url'],
            "type": source_config['type'],
            "category": source_config.get('category', 'Unknown'),
            "status": "error",
            "items_collected": 0,
            "response_time_ms": int(elapsed_time * 1000),
            "errors": [str(e)]
        }


def test_all_default_sources():
    """Test all default sources and generate a comprehensive report"""
    print("\n" + "="*60)
    print("🧪 TESTING ALL DEFAULT SOURCES")
    print("="*60)
    print(f"\nTotal sources to test: {len(DEFAULT_SOURCES)}")
    print("Note: Testing with max 5 items per source")
    
    # Initialize database and crawler
    db = CrawlerDatabase()
    crawler = WebCrawler(db)
    
    results = []
    
    # Test each source
    for i, source_config in enumerate(DEFAULT_SOURCES, 1):
        result = test_single_source(crawler, source_config, i, len(DEFAULT_SOURCES))
        results.append(result)
        
        # Be polite - wait between requests
        if i < len(DEFAULT_SOURCES):
            time.sleep(2)
    
    # Generate summary
    print("\n" + "="*60)
    print("📊 TEST SUMMARY")
    print("="*60)
    
    success_count = sum(1 for r in results if r["status"] == "success")
    no_data_count = sum(1 for r in results if r["status"] == "no_data")
    error_count = sum(1 for r in results if r["status"] == "error")
    total_items = sum(r["items_collected"] for r in results)
    avg_response_time = sum(r["response_time_ms"] for r in results) / len(results)
    
    print(f"\nTotal Tests: {len(results)}")
    print(f"✅ Successful: {success_count}")
    print(f"⚠️  No Data: {no_data_count}")
    print(f"❌ Failed: {error_count}")
    print(f"📦 Total Items Collected: {total_items}")
    print(f"⏱️  Average Response Time: {avg_response_time:.0f}ms")
    
    # Results by category
    print("\n" + "="*60)
    print("📋 RESULTS BY CATEGORY")
    print("="*60)
    
    categories = {}
    for result in results:
        category = result['category']
        if category not in categories:
            categories[category] = []
        categories[category].append(result)
    
    for category, cat_results in sorted(categories.items()):
        print(f"\n{category}:")
        for result in cat_results:
            status_icon = "✅" if result["status"] == "success" else "⚠️" if result["status"] == "no_data" else "❌"
            print(f"  {status_icon} {result['name']}")
            print(f"     Type: {result['type']}, Items: {result['items_collected']}, Time: {result['response_time_ms']}ms")
            if result["errors"]:
                print(f"     Errors: {', '.join(result['errors'][:1])}")
    
    # Results by type
    print("\n" + "="*60)
    print("📋 RESULTS BY TYPE")
    print("="*60)
    
    types = {}
    for result in results:
        source_type = result['type']
        if source_type not in types:
            types[source_type] = {'success': 0, 'failed': 0, 'no_data': 0}
        
        if result['status'] == 'success':
            types[source_type]['success'] += 1
        elif result['status'] == 'no_data':
            types[source_type]['no_data'] += 1
        else:
            types[source_type]['failed'] += 1
    
    for source_type, counts in sorted(types.items()):
        total = counts['success'] + counts['failed'] + counts['no_data']
        print(f"\n{source_type.upper()}:")
        print(f"  Total: {total}")
        print(f"  ✅ Success: {counts['success']}")
        print(f"  ⚠️  No Data: {counts['no_data']}")
        print(f"  ❌ Failed: {counts['failed']}")
    
    # Detailed results
    print("\n" + "="*60)
    print("📋 DETAILED RESULTS")
    print("="*60)
    
    for i, result in enumerate(results, 1):
        status_icon = "✅" if result["status"] == "success" else "⚠️" if result["status"] == "no_data" else "❌"
        print(f"\n{i}. {status_icon} {result['name']}")
        print(f"   URL: {result['url']}")
        print(f"   Type: {result['type']}")
        print(f"   Category: {result['category']}")
        print(f"   Status: {result['status']}")
        print(f"   Items: {result['items_collected']}")
        print(f"   Response Time: {result['response_time_ms']}ms")
        if result["errors"]:
            print(f"   Errors: {', '.join(result['errors'][:2])}")
    
    # Final verdict
    print("\n" + "="*60)
    print("🎯 FINAL VERDICT")
    print("="*60)
    
    if success_count == len(results):
        print("\n🎉 ALL TESTS PASSED!")
        print("✅ All default sources are working perfectly")
        return 0
    elif success_count >= len(results) * 0.8:  # 80% success rate
        print(f"\n✅ MOSTLY SUCCESSFUL: {success_count}/{len(results)} sources working")
        print("   Most sources are working well")
        return 0
    elif success_count > 0:
        print(f"\n⚠️  PARTIAL SUCCESS: {success_count}/{len(results)} sources working")
        print("   Some sources may need adjustment or may be temporarily unavailable")
        return 1
    else:
        print("\n❌ ALL TESTS FAILED")
        print("   Check network connection and MongoDB authentication")
        return 1
    
    db.close()


def main():
    """Main entry point"""
    return test_all_default_sources()


if __name__ == "__main__":
    sys.exit(main())
