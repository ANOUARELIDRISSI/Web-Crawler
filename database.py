"""
Database module for storing and retrieving crawled data
Uses MongoDB for NoSQL storage
"""
from pymongo import MongoClient, ASCENDING, TEXT
from datetime import datetime
import json
import os
from typing import List, Dict, Any, Optional
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

class CrawlerDatabase:
    def __init__(self, connection_string=None, db_name=None):
        """Initialize MongoDB connection"""
        # Use environment variables if not provided
        if connection_string is None:
            # Use authenticated connection string for Docker
            connection_string = os.getenv('MONGODB_URI', 'mongodb://crawler_admin:Crawler2026SecurePass@localhost:27017/web_crawler?authSource=admin')
        
        if db_name is None:
            db_name = os.getenv('MONGODB_DATABASE', 'web_crawler')
        
        try:
            self.client = MongoClient(connection_string, serverSelectionTimeoutMS=5000)
            # Test connection
            self.client.server_info()
            self.db = self.client[db_name]
            
            # Collections
            self.sources = self.db.sources
            self.crawled_data = self.db.crawled_data
            self.crawl_logs = self.db.crawl_logs
            
            # Create indexes
            self._create_indexes()
            print("✅ Connected to MongoDB successfully!")
        except Exception as e:
            print(f"❌ MongoDB connection failed: {e}")
            print("⚠️  The dashboard will run with limited functionality.")
            print("   To fix: Make sure MongoDB is running without authentication")
            # Initialize with None to handle gracefully
            self.client = None
            self.db = None
            self.sources = None
            self.crawled_data = None
            self.crawl_logs = None
    
    def _create_indexes(self):
        """Create indexes for better query performance"""
        try:
            # Text index for keyword search
            self.crawled_data.create_index([("content", TEXT), ("title", TEXT)])
            
            # Index for source_id and timestamp
            self.crawled_data.create_index([("source_id", ASCENDING), ("timestamp", ASCENDING)])
            
            # Index for sources
            self.sources.create_index([("url", ASCENDING)], unique=True)
        except Exception as e:
            print(f"Warning: Could not create indexes: {e}")
            print("Database will work but searches may be slower.")
    
    # ==================== SOURCE MANAGEMENT ====================
    
    def add_source(self, source_data: Dict[str, Any]) -> str:
        """Add a new crawl source"""
        if self.sources is None:
            raise Exception("Database not connected")
        
        source_data["created_at"] = datetime.now()
        source_data["updated_at"] = datetime.now()
        source_data["status"] = "active"
        
        result = self.sources.insert_one(source_data)
        return str(result.inserted_id)
    
    def update_source(self, source_id: str, update_data: Dict[str, Any]) -> bool:
        """Update an existing source"""
        from bson.objectid import ObjectId
        
        update_data["updated_at"] = datetime.now()
        result = self.sources.update_one(
            {"_id": ObjectId(source_id)},
            {"$set": update_data}
        )
        return result.modified_count > 0
    
    def delete_source(self, source_id: str) -> bool:
        """Delete a source"""
        from bson.objectid import ObjectId
        
        result = self.sources.delete_one({"_id": ObjectId(source_id)})
        return result.deleted_count > 0
    
    def get_source(self, source_id: str) -> Optional[Dict]:
        """Get a single source by ID"""
        from bson.objectid import ObjectId
        
        source = self.sources.find_one({"_id": ObjectId(source_id)})
        if source:
            source["_id"] = str(source["_id"])
        return source
    
    def get_all_sources(self, status: Optional[str] = None) -> List[Dict]:
        """Get all sources, optionally filtered by status"""
        if self.sources is None:
            return []
        
        try:
            query = {}
            if status:
                query["status"] = status
            
            sources = list(self.sources.find(query))
            for source in sources:
                source["_id"] = str(source["_id"])
            return sources
        except Exception as e:
            print(f"Warning: Could not get sources: {e}")
            return []
    
    # ==================== DATA STORAGE ====================
    
    def store_crawled_data(self, data: Dict[str, Any]) -> str:
        """Store crawled data"""
        if self.crawled_data is None:
            return ""
        
        try:
            data["timestamp"] = datetime.now()
            result = self.crawled_data.insert_one(data)
            return str(result.inserted_id)
        except Exception as e:
            print(f"Warning: Could not store data: {e}")
            return ""
    
    def bulk_store_data(self, data_list: List[Dict[str, Any]]) -> List[str]:
        """Store multiple crawled data items"""
        if self.crawled_data is None:
            return []
        
        try:
            for data in data_list:
                data["timestamp"] = datetime.now()
            
            result = self.crawled_data.insert_many(data_list)
            return [str(id) for id in result.inserted_ids]
        except Exception as e:
            print(f"Warning: Could not bulk store data: {e}")
            return []
    
    # ==================== DATA RETRIEVAL ====================
    
    def search_by_keyword(self, keyword: str, limit: int = 100) -> List[Dict]:
        """Search crawled data by keyword"""
        if self.crawled_data is None:
            return []
        
        try:
            results = self.crawled_data.find(
                {"$text": {"$search": keyword}},
                {"score": {"$meta": "textScore"}}
            ).sort([("score", {"$meta": "textScore"})]).limit(limit)
            
            data = []
            for doc in results:
                doc["_id"] = str(doc["_id"])
                data.append(doc)
            return data
        except Exception as e:
            print(f"Warning: Could not search by keyword: {e}")
            return []
    
    def get_data_by_source(self, source_id: str, limit: int = 100) -> List[Dict]:
        """Get all data from a specific source"""
        if self.crawled_data is None:
            return []
        
        try:
            results = self.crawled_data.find(
                {"source_id": source_id}
            ).sort("timestamp", -1).limit(limit)
            
            data = []
            for doc in results:
                doc["_id"] = str(doc["_id"])
                data.append(doc)
            return data
        except Exception as e:
            print(f"Warning: Could not get data by source: {e}")
            return []
    
    def get_recent_data(self, limit: int = 100) -> List[Dict]:
        """Get most recent crawled data"""
        if self.crawled_data is None:
            return []
        
        try:
            results = self.crawled_data.find().sort("timestamp", -1).limit(limit)
            
            data = []
            for doc in results:
                doc["_id"] = str(doc["_id"])
                data.append(doc)
            return data
        except Exception as e:
            print(f"Warning: Could not get recent data: {e}")
            return []
    
    def get_data_by_date_range(self, start_date: datetime, end_date: datetime) -> List[Dict]:
        """Get data within a date range"""
        if self.crawled_data is None:
            return []
        
        try:
            results = self.crawled_data.find({
                "timestamp": {
                    "$gte": start_date,
                    "$lte": end_date
                }
            }).sort("timestamp", -1)
            
            data = []
            for doc in results:
                doc["_id"] = str(doc["_id"])
                data.append(doc)
            return data
        except Exception as e:
            print(f"Warning: Could not get data by date range: {e}")
            return []
    
    # ==================== STATISTICS ====================
    
    def get_statistics(self) -> Dict[str, Any]:
        """Get crawler statistics"""
        if self.sources is None or self.crawled_data is None:
            return {
                "total_sources": 0,
                "active_sources": 0,
                "total_data_items": 0,
                "data_by_source": []
            }
        
        try:
            return {
                "total_sources": self.sources.count_documents({}),
                "active_sources": self.sources.count_documents({"status": "active"}),
                "total_data_items": self.crawled_data.count_documents({}),
                "data_by_source": list(self.crawled_data.aggregate([
                    {"$group": {"_id": "$source_id", "count": {"$sum": 1}}}
                ]))
            }
        except Exception as e:
            print(f"Warning: Could not get statistics: {e}")
            return {
                "total_sources": 0,
                "active_sources": 0,
                "total_data_items": 0,
                "data_by_source": []
            }
    
    # ==================== LOGGING ====================
    
    def log_crawl(self, log_data: Dict[str, Any]) -> str:
        """Log a crawl operation"""
        if self.crawl_logs is None:
            return ""
        
        try:
            log_data["timestamp"] = datetime.now()
            result = self.crawl_logs.insert_one(log_data)
            return str(result.inserted_id)
        except Exception as e:
            print(f"Warning: Could not log crawl: {e}")
            return ""
    
    def get_crawl_logs(self, limit: int = 100) -> List[Dict]:
        """Get recent crawl logs"""
        if self.crawl_logs is None:
            return []
        
        try:
            logs = self.crawl_logs.find().sort("timestamp", -1).limit(limit)
            
            data = []
            for log in logs:
                log["_id"] = str(log["_id"])
                data.append(log)
            return data
        except Exception as e:
            print(f"Warning: Could not get logs: {e}")
            return []
    
    def close(self):
        """Close database connection"""
        self.client.close()
