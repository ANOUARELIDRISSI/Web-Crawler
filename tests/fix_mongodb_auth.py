"""
Quick Fix for MongoDB Authentication

This script helps you disable MongoDB authentication for local development.
"""
import os
import subprocess
import sys

def find_mongod_config():
    """Find the MongoDB configuration file"""
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

def main():
    print("\n" + "="*60)
    print("🔧 MongoDB Authentication Fix")
    print("="*60)
    
    print("\n⚠️  MongoDB is running with authentication enabled.")
    print("   This prevents the crawler from storing data.")
    print("\n📋 To fix this, you need to disable authentication.")
    
    config_path = find_mongod_config()
    
    if config_path:
        print(f"\n✅ Found MongoDB config: {config_path}")
    else:
        print("\n⚠️  Could not find MongoDB config file automatically.")
        print("   Common locations:")
        print("   - C:\\Program Files\\MongoDB\\Server\\7.0\\bin\\mongod.cfg")
        print("   - C:\\Program Files\\MongoDB\\Server\\6.0\\bin\\mongod.cfg")
    
    print("\n" + "="*60)
    print("📝 MANUAL FIX STEPS")
    print("="*60)
    
    print("\n1️⃣  Open MongoDB config file:")
    if config_path:
        print(f"   {config_path}")
    else:
        print("   Find mongod.cfg in your MongoDB installation folder")
    
    print("\n2️⃣  Find the 'security:' section and comment it out:")
    print("   Change this:")
    print("   ```")
    print("   security:")
    print("     authorization: enabled")
    print("   ```")
    print("   To this:")
    print("   ```")
    print("   # security:")
    print("   #   authorization: enabled")
    print("   ```")
    
    print("\n3️⃣  Restart MongoDB service:")
    print("   - Press Win + R")
    print("   - Type: services.msc")
    print("   - Find 'MongoDB' service")
    print("   - Right-click → Restart")
    
    print("\n   OR use command line:")
    print("   ```")
    print("   net stop MongoDB")
    print("   net start MongoDB")
    print("   ```")
    
    print("\n4️⃣  Restart the dashboard:")
    print("   - Stop the current dashboard (Ctrl+C)")
    print("   - Run: streamlit run dashboard.py")
    
    print("\n" + "="*60)
    print("🚀 ALTERNATIVE: Run MongoDB without auth (Temporary)")
    print("="*60)
    
    print("\n1️⃣  Stop MongoDB service:")
    print("   net stop MongoDB")
    
    print("\n2️⃣  Run MongoDB without authentication:")
    print("   mongod --noauth --dbpath C:\\data\\db")
    
    print("\n3️⃣  Keep that terminal open and restart the dashboard")
    
    print("\n" + "="*60)
    print("❓ NEED HELP?")
    print("="*60)
    
    print("\nSee TESTING.md for detailed instructions with screenshots.")
    print("The issue is documented in TEST_REPORT.md")
    
    print("\n" + "="*60)
    
    # Ask if user wants to try restarting MongoDB
    print("\n🔄 Would you like to try restarting MongoDB now?")
    print("   This will attempt to restart the MongoDB service.")
    print("   (You'll still need to edit the config file manually)")
    
    response = input("\nRestart MongoDB? (y/n): ").lower().strip()
    
    if response == 'y':
        print("\n🔄 Attempting to restart MongoDB...")
        try:
            # Stop MongoDB
            print("   Stopping MongoDB...")
            subprocess.run(["net", "stop", "MongoDB"], check=False, capture_output=True)
            
            # Start MongoDB
            print("   Starting MongoDB...")
            result = subprocess.run(["net", "start", "MongoDB"], check=False, capture_output=True)
            
            if result.returncode == 0:
                print("✅ MongoDB restarted successfully!")
                print("\n⚠️  Remember: You still need to edit mongod.cfg to disable auth permanently")
            else:
                print("⚠️  Could not restart MongoDB automatically")
                print("   Please restart manually using services.msc")
        except Exception as e:
            print(f"❌ Error: {e}")
            print("   Please restart MongoDB manually")
    
    print("\n" + "="*60)
    print("✅ Once MongoDB auth is disabled, your dashboard will work perfectly!")
    print("="*60)

if __name__ == "__main__":
    main()
