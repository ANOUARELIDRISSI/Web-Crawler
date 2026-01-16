"""
MongoDB Authentication Fix Script
Helps disable authentication for local development
"""
import subprocess
import os
import sys

def find_mongod_config():
    """Try to find MongoDB config file"""
    possible_paths = [
        r"C:\Program Files\MongoDB\Server\7.0\bin\mongod.cfg",
        r"C:\Program Files\MongoDB\Server\6.0\bin\mongod.cfg",
        r"C:\Program Files\MongoDB\Server\5.0\bin\mongod.cfg",
        r"C:\Program Files\MongoDB\Server\4.4\bin\mongod.cfg",
    ]
    
    for path in possible_paths:
        if os.path.exists(path):
            return path
    
    return None

def check_mongodb_status():
    """Check if MongoDB is running"""
    try:
        from pymongo import MongoClient
        client = MongoClient('mongodb://localhost:27017/', serverSelectionTimeoutMS=2000)
        client.server_info()
        print("✅ MongoDB is running")
        
        # Test if authentication is required
        try:
            db = client['test_db']
            db.test_collection.insert_one({"test": "data"})
            db.test_collection.delete_one({"test": "data"})
            print("✅ MongoDB allows operations without authentication")
            return "no_auth"
        except Exception as e:
            if "authentication" in str(e).lower():
                print("⚠️  MongoDB requires authentication")
                return "auth_required"
            else:
                print(f"⚠️  MongoDB error: {e}")
                return "error"
    except Exception as e:
        print(f"❌ MongoDB is not running: {e}")
        return "not_running"

def main():
    print("🔧 MongoDB Authentication Fix")
    print("=" * 60)
    
    status = check_mongodb_status()
    
    if status == "not_running":
        print("\n📝 MongoDB is not running. Start it first:")
        print("   Windows: net start MongoDB")
        print("   Mac: brew services start mongodb-community")
        print("   Linux: sudo systemctl start mongod")
        return
    
    if status == "no_auth":
        print("\n✅ MongoDB is already configured correctly!")
        print("   You can now use the web crawler without issues.")
        return
    
    if status == "auth_required":
        print("\n📝 MongoDB requires authentication. Here's how to fix it:")
        print("\n**Option 1: Edit MongoDB Config (Recommended)**")
        
        config_path = find_mongod_config()
        if config_path:
            print(f"\n   1. Open this file in a text editor (as Administrator):")
            print(f"      {config_path}")
        else:
            print("\n   1. Find your mongod.cfg file:")
            print("      Usually in: C:\\Program Files\\MongoDB\\Server\\<version>\\bin\\")
        
        print("\n   2. Find the 'security:' section and comment it out:")
        print("      # security:")
        print("      #   authorization: enabled")
        
        print("\n   3. Save the file")
        
        print("\n   4. Restart MongoDB:")
        print("      - Open Services (services.msc)")
        print("      - Find 'MongoDB' service")
        print("      - Right-click → Restart")
        
        print("\n**Option 2: Run MongoDB without Auth (Temporary)**")
        print("\n   1. Stop MongoDB service")
        print("   2. Run in command prompt:")
        print("      mongod --noauth --dbpath C:\\data\\db")
        
        print("\n**Option 3: Use Authentication (Advanced)**")
        print("\n   Run: python scripts/setup_mongodb.py")
        print("   This will create a user with credentials from .env file")
    
    print("\n" + "=" * 60)
    print("After fixing, run this script again to verify!")

if __name__ == "__main__":
    main()
