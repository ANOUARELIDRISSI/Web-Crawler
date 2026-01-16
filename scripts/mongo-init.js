// MongoDB initialization script for Docker
// This creates the application user with proper permissions

// Switch to admin database for user creation
db = db.getSiblingDB('admin');

// Create the application user with proper roles
try {
    db.createUser({
        user: 'crawler_admin',
        pwd: 'Crawler2026SecurePass',
        roles: [
            {
                role: 'readWrite',
                db: 'web_crawler'
            },
            {
                role: 'dbAdmin',
                db: 'web_crawler'
            }
        ]
    });
    print('✅ MongoDB user "crawler_admin" created successfully');
} catch (error) {
    if (error.code === 11000) {
        print('ℹ️  User "crawler_admin" already exists');
    } else {
        print('❌ Error creating user:', error);
    }
}

// Switch to the application database
db = db.getSiblingDB('web_crawler');

// Create initial collections with some basic structure
try {
    db.createCollection('sources');
    db.createCollection('crawled_data');
    db.createCollection('crawl_logs');
    
    // Create indexes for better performance
    db.crawled_data.createIndex({ "content": "text", "title": "text" });
    db.crawled_data.createIndex({ "source_id": 1, "timestamp": 1 });
    db.sources.createIndex({ "url": 1 }, { unique: true });
    
    print('✅ Collections and indexes created successfully');
} catch (error) {
    print('ℹ️  Collections may already exist:', error.message);
}
