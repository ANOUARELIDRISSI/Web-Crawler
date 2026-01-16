"""
MongoDB Setup Script
Creates MongoDB user with credentials from .env file
"""
from pymongo import MongoClient
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

def setup_mongodb():
    """Setup MongoDB with authentication"""
    print("🔧 MongoDB Setup Script")
    print("=" * 60)
    
    # Get credentials from .env
    username = os.getenv('MONGODB_USERNAME', 'crawler_admin')
    password = os.getenv('MONGODB_PASSWORD')
    database = os.getenv('MONGODB_DATABASE', 'web_crawler')
    
    if not password:
        print("❌ Error: MONGODB_PASSWORD not found in .env file")
        return False
    
    print(f"📝 Setting up MongoDB user: {username}")
    print(f"📝 Database: {database}")
    
    try:
        # Connect without authentication first
        print("\n🔌 Connecting to MongoDB...")
        client = MongoClient('mongodb://localhost:27017/', serverSelectionTimeoutMS=5000)
        client.server_info()
        print("✅ Connected to MongoDB")
        
        # Check if authentication is already enabled
        try:
            # Try to access admin database
            admin_db = client.admin
            admin_db.command('ping')
            print("✅ MongoDB is accessible")
            
            # Create user
            print(f"\n👤 Creating user '{username}'...")
            try:
                admin_db.command(
                    "createUser",
                    username,
                    pwd=password,
                    roles=[
                        {"role": "readWrite", "db": database},
                        {"role": "dbAdmin", "db": database}
                    ]
                )
                print(f"✅ User '{username}' created successfully!")
            except Exception as e:
                if "already exists" in str(e):
                    print(f"⚠️  User '{username}' already exists")
                    # Update password
                    try:
                        admin_db.command(
                            "updateUser",
                            username,
                            pwd=password
                        )
                        print(f"✅ Password updated for user '{username}'")
                    except Exception as update_error:
                        print(f"⚠️  Could not update password: {update_error}")
                else:
                    print(f"❌ Error creating user: {e}")
                    return False
            
            # Test the new credentials
            print(f"\n🔐 Testing authentication...")
            auth_uri = f"mongodb://{username}:{password}@localhost:27017/{database}?authSource=admin"
            test_client = MongoClient(auth_uri, serverSelectionTimeoutMS=5000)
            test_db = test_client[database]
            test_db.command('ping')
            print("✅ Authentication successful!")
            
            print("\n" + "=" * 60)
            print("✅ MongoDB setup complete!")
            print("=" * 60)
            print("\n📝 Connection details saved in .env file")
            print(f"   Username: {username}")
            print(f"   Database: {database}")
            print(f"   Connection URI: {auth_uri}")
            print("\n🚀 You can now run: streamlit run dashboard.py")
            
            test_client.close()
            client.close()
            return True
            
        except Exception as e:
            print(f"⚠️  MongoDB authentication check: {e}")
            print("\n📝 MongoDB may already have authentication enabled.")
            print("   If you're getting authentication errors, try:")
            print("   1. Stop MongoDB")
            print("   2. Run: mongod --noauth --dbpath C:\\data\\db")
            print("   3. Run this script again")
            print("   4. Stop mongod and restart with authentication")
            return False
            
    except Exception as e:
        print(f"❌ Error: {e}")
        print("\n📝 Make sure MongoDB is running:")
        print("   Windows: net start MongoDB")
        print("   Mac: brew services start mongodb-community")
        print("   Linux: sudo systemctl start mongod")
        return False

def test_connection():
    """Test connection with credentials from .env"""
    print("\n" + "=" * 60)
    print("🧪 Testing Database Connection")
    print("=" * 60)
    
    load_dotenv()
    
    # Try with authentication
    auth_uri = os.getenv('MONGODB_URI')
    if auth_uri:
        print(f"\n🔐 Testing with authentication...")
        try:
            client = MongoClient(auth_uri, serverSelectionTimeoutMS=5000)
            client.server_info()
            db = client[os.getenv('MONGODB_DATABASE', 'web_crawler')]
            db.command('ping')
            print("✅ Authenticated connection successful!")
            client.close()
            return True
        except Exception as e:
            print(f"⚠️  Authenticated connection failed: {e}")
    
    # Try without authentication
    no_auth_uri = os.getenv('MONGODB_URI_NO_AUTH', 'mongodb://localhost:27017/')
    print(f"\n🔓 Testing without authentication...")
    try:
        client = MongoClient(no_auth_uri, serverSelectionTimeoutMS=5000)
        client.server_info()
        print("✅ No-auth connection successful!")
        print("⚠️  MongoDB is running without authentication")
        client.close()
        return True
    except Exception as e:
        print(f"❌ Connection failed: {e}")
        return False

if __name__ == "__main__":
    import sys
    
    if len(sys.argv) > 1 and sys.argv[1] == "test":
        test_connection()
    else:
        setup_mongodb()
        print("\n" + "=" * 60)
        test_connection()
