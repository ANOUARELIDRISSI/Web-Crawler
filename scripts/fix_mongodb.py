"""
MongoDB Setup Helper
This script helps configure MongoDB for the web crawler
"""
import subprocess
import sys

def check_mongodb():
    """Check if MongoDB is running"""
    try:
        from pymongo import MongoClient
        client = MongoClient('mongodb://localhost:27017/', serverSelectionTimeoutMS=2000)
        client.server_info()
        print("✅ MongoDB is running")
        
        # Try to access without auth
        try:
            db = client['test_db']
            db.test_collection.insert_one({"test": "data"})
            db.test_collection.delete_one({"test": "data"})
            print("✅ MongoDB allows operations without authentication")
            return True
        except Exception as e:
            print(f"⚠️  MongoDB requires authentication: {e}")
            print("\n📝 To disable authentication for local development:")
            print("   1. Find your MongoDB config file (mongod.cfg)")
            print("   2. Comment out or remove the 'security' section")
            print("   3. Restart MongoDB service")
            print("\n   OR use MongoDB without authentication:")
            print("   mongod --noauth --dbpath C:\\data\\db")
            return False
    except Exception as e:
        print(f"❌ MongoDB is not running: {e}")
        print("\n📝 To start MongoDB:")
        print("   Windows: net start MongoDB")
        print("   Mac: brew services start mongodb-community")
        print("   Linux: sudo systemctl start mongod")
        return False

if __name__ == "__main__":
    print("🔧 MongoDB Setup Helper")
    print("=" * 60)
    check_mongodb()
