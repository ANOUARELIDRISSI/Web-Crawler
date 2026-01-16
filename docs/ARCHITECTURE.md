# 📋 Architecture Report - Web Crawler System

## 📖 Table of Contents

1. [Overview](#overview)
2. [System Architecture](#system-architecture)
3. [File Structure](#file-structure)
4. [Main Components](#main-components)
5. [Workflow](#workflow)
6. [Database](#database)
7. [Data Sources](#data-sources)
8. [AI Service](#ai-service)
9. [User Interface](#user-interface)
10. [Configuration and Deployment](#configuration-and-deployment)
11. [Diagrams](#diagrams)

---

## Overview

**Web Crawler System** is a professional web scraping application with MongoDB storage, Flask UI, and AI-powered analysis. The system allows automatic data collection from various web sources (HTML, RSS, PDF, XML, TXT, dynamic JavaScript pages).

### Key Features

| Feature | Description |
|---------|-------------|
| 🌐 Multi-Format | Support for HTML, RSS, PDF, XML, TXT, Dynamic JS |
| 🗄️ MongoDB | NoSQL database with authentication |
| 🐳 Docker | Containerized MongoDB deployment |
| ⏰ Scheduler | Configurable automated crawling |
| 🖼️ Images | Image extraction and display |
| 🤖 AI | Chat and summarization with Hugging Face (DistilBART, GPT-2) |

---

## System Architecture

```
┌─────────────────────────────────────────────────────────────────────┐
│                         PRESENTATION LAYER                           │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌────────┐ │
│  │  index   │  │ sources  │  │  search  │  │ reports  │  │   ai   │ │
│  │  .html   │  │  .html   │  │  .html   │  │  .html   │  │  .html │ │
│  └────┬─────┘  └────┬─────┘  └────┬─────┘  └────┬─────┘  └───┬────┘ │
│       │             │             │             │             │      │
│       └─────────────┴──────┬──────┴─────────────┴─────────────┘      │
│                            │                                         │
│                      ┌─────┴─────┐                                   │
│                      │ base.html │  (Base Template)                  │
│                      └───────────┘                                   │
└─────────────────────────────────────────────────────────────────────┘
                                    │
                                    ▼
┌─────────────────────────────────────────────────────────────────────┐
│                         APPLICATION LAYER                            │
│                                                                      │
│  ┌────────────────────────────────────────────────────────────────┐ │
│  │                         app.py                                  │ │
│  │  • Flask Routes (/, /sources, /search, /reports, /ai)          │ │
│  │  • REST API (/api/sources, /api/crawl, /api/search, /api/ai)   │ │
│  │  • Custom JSON Encoder (ObjectId, datetime)                    │ │
│  └────────────────────────────────────────────────────────────────┘ │
│                            │                                         │
│          ┌─────────────────┼─────────────────┐                      │
│          ▼                 ▼                 ▼                      │
│  ┌───────────────┐ ┌───────────────┐ ┌───────────────┐              │
│  │   crawler_    │ │  scheduler.py │ │  ai_service   │              │
│  │ enhanced.py   │ │               │ │     .py       │              │
│  │               │ │  • Threading  │ │               │              │
│  │  • HTML/RSS   │ │  • Schedule   │ │  • DistilBART │              │
│  │  • PDF/XML    │ │  • Frequencies│ │  • GPT-2      │              │
│  │  • Dynamic JS │ │               │ │  • Chat/Summary│             │
│  └───────┬───────┘ └───────┬───────┘ └───────────────┘              │
│          │                 │                                         │
│          └────────┬────────┘                                         │
│                   ▼                                                  │
│  ┌────────────────────────────────────────────────────────────────┐ │
│  │                       database.py                               │ │
│  │  • CrawlerDatabase class                                        │ │
│  │  • CRUD Sources, Crawled Data, Logs                            │ │
│  │  • Text index for search                                        │ │
│  └────────────────────────────────────────────────────────────────┘ │
└─────────────────────────────────────────────────────────────────────┘
                                    │
                                    ▼
┌─────────────────────────────────────────────────────────────────────┐
│                           DATA LAYER                                 │
│                                                                      │
│  ┌────────────────────────────────────────────────────────────────┐ │
│  │                   MongoDB (Docker)                              │ │
│  │                                                                  │ │
│  │  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐             │ │
│  │  │   sources   │  │crawled_data │  │ crawl_logs  │             │ │
│  │  │             │  │             │  │             │             │ │
│  │  │ • name      │  │ • source_id │  │ • source_id │             │ │
│  │  │ • url       │  │ • title     │  │ • url       │             │ │
│  │  │ • type      │  │ • content   │  │ • status    │             │ │
│  │  │ • selectors │  │ • images    │  │ • items     │             │ │
│  │  │ • frequency │  │ • timestamp │  │ • errors    │             │ │
│  │  └─────────────┘  └─────────────┘  └─────────────┘             │ │
│  └────────────────────────────────────────────────────────────────┘ │
└─────────────────────────────────────────────────────────────────────┘
```

---

## File Structure

```
E:\Web Crawling\
│
├── 📄 app.py                    # Main Flask application
├── 📄 ai_service.py             # AI service (chat, summarization)
├── 📄 crawler_enhanced.py       # Enhanced crawler with image support
├── 📄 crawler.py                # Base crawling engine
├── 📄 database.py               # MongoDB access layer
├── 📄 default_sources.py        # 22 pre-configured sources
├── 📄 scheduler.py              # Task scheduler
│
├── 📄 docker-compose.yml        # Docker MongoDB configuration
├── 📄 requirements.txt          # Python dependencies
├── 📄 .env.template             # Environment variables template
├── 📄 .gitignore                # Git ignored files
│
├── 📁 templates/                # Jinja2 HTML templates
│   ├── base.html               # Base template
│   ├── index.html              # Dashboard
│   ├── sources.html            # Source management
│   ├── search.html             # Search with filters
│   ├── reports.html            # Reports and charts
│   ├── ai.html                 # AI Assistant
│   ├── 404.html                # 404 error page
│   └── 500.html                # 500 error page
│
├── 📁 scripts/                  # Utility scripts
│   ├── demo.py                 # Demonstration
│   ├── mongo-init.js           # MongoDB initialization
│   ├── setup_mongodb.py        # MongoDB setup
│   └── fix_mongodb*.py         # Repair scripts
│
├── 📁 tests/                    # Automated tests
│   ├── test_ai.py              # AI service tests
│   ├── test_crawl.py           # Crawling tests
│   ├── test_mongodb_connection.py
│   ├── test_sources.py         # Sources tests
│   └── verify_system.py        # System verification
│
├── 📁 docs/                     # Documentation
│   └── ARCHITECTURE_REPORT.md  # This document
│
└── 📁 venv/                     # Python virtual environment
```

---

## Main Components

### 1. app.py - Flask Application

The heart of the application, responsible for:

```python
# Initialization
db = CrawlerDatabase()           # MongoDB connection
crawler = EnhancedWebCrawler(db) # Crawling engine

# Main Routes
@app.route('/')          → index.html      # Dashboard
@app.route('/sources')   → sources.html    # Source management
@app.route('/search')    → search.html     # Search
@app.route('/reports')   → reports.html    # Reports
@app.route('/ai')        → ai.html         # AI Assistant

# REST API
POST /api/sources/add      # Add a source
DELETE /api/sources/<id>   # Delete a source
POST /api/crawl            # Start a crawl
POST /api/search           # Search data
POST /api/ai/chat          # Chat with AI
POST /api/ai/summarize     # Summarize data
```

### 2. database.py - Data Access Layer

```python
class CrawlerDatabase:
    # MongoDB Collections
    self.sources       # Source configuration
    self.crawled_data  # Collected data
    self.crawl_logs    # Execution logs
    
    # Main Methods
    add_source()           # Add source
    update_source()        # Update source
    delete_source()        # Delete source
    store_crawled_data()   # Store data
    bulk_store_data()      # Bulk storage
    search_by_keyword()    # Text search
    get_statistics()       # Statistics
    log_crawl()            # Logging
```

### 3. crawler.py & crawler_enhanced.py - Crawling Engine

```python
class WebCrawler:
    # Supported crawling types
    _crawl_html()     # Static HTML pages
    _crawl_dynamic()  # JavaScript pages (Selenium)
    _crawl_rss()      # RSS/Atom feeds
    _crawl_pdf()      # PDF documents
    _crawl_xml()      # XML files
    _crawl_txt()      # Text files

class EnhancedWebCrawler(WebCrawler):
    # Extension with image support
    _make_absolute_url()  # Relative → absolute URLs
    # Image extraction from containers
```

### 4. ai_service.py - Artificial Intelligence Service

```python
class AIService:
    # Models used
    summarizer = DistilBART  # Text summarization
    chat_model = GPT-2       # Conversation
    
    # Features
    summarize_text()         # Summarize text
    summarize_data_items()   # Summarize multiple items
    chat()                   # Contextual conversation
    analyze_data()           # Statistical analysis
```

### 5. scheduler.py - Scheduler

```python
class CrawlerScheduler:
    # Supported frequencies
    "hourly"   → Every hour
    "daily"    → Every day
    "weekly"   → Every week
    "monthly"  → Every 30 days
    "N"        → Every N minutes (custom)
    
    # Methods
    schedule_source()      # Schedule a source
    schedule_all_sources() # Schedule all sources
    start()                # Start in background
    stop()                 # Stop the scheduler
```

---

## Workflow

### Crawling Workflow

```
┌──────────────┐    ┌─────────────────┐    ┌──────────────────┐
│     User     │    │    Flask API    │    │     Crawler      │
│              │    │                 │    │                  │
└──────┬───────┘    └────────┬────────┘    └────────┬─────────┘
       │                     │                      │
       │  POST /api/crawl    │                      │
       │────────────────────>│                      │
       │                     │                      │
       │                     │  crawl_source()      │
       │                     │─────────────────────>│
       │                     │                      │
       │                     │                      │  ┌─────────────┐
       │                     │                      │─>│   Website   │
       │                     │                      │  │   (HTTP)    │
       │                     │                      │<─│             │
       │                     │                      │  └─────────────┘
       │                     │                      │
       │                     │                      │  Parse HTML/RSS/PDF
       │                     │                      │  Extract data
       │                     │                      │
       │                     │                      │  ┌─────────────┐
       │                     │                      │─>│   MongoDB   │
       │                     │                      │  │ store_data()│
       │                     │                      │<─│             │
       │                     │                      │  └─────────────┘
       │                     │                      │
       │                     │  {success, items}    │
       │                     │<─────────────────────│
       │                     │                      │
       │  JSON Response      │                      │
       │<────────────────────│                      │
       │                     │                      │
```

### Search Workflow

```
┌──────────────┐    ┌─────────────────┐    ┌──────────────────┐
│     User     │    │    Flask API    │    │     MongoDB      │
└──────┬───────┘    └────────┬────────┘    └────────┬─────────┘
       │                     │                      │
       │  POST /api/search   │                      │
       │  {keyword: "python"}│                      │
       │────────────────────>│                      │
       │                     │                      │
       │                     │ search_by_keyword()  │
       │                     │─────────────────────>│
       │                     │                      │
       │                     │                      │ $text index
       │                     │                      │ search
       │                     │                      │
       │                     │   [results...]       │
       │                     │<─────────────────────│
       │                     │                      │
       │  JSON Results       │                      │
       │<────────────────────│                      │
```

### AI Workflow (Chat/Summary)

```
┌──────────────┐    ┌─────────────────┐    ┌──────────────────┐
│     User     │    │    Flask API    │    │   AI Service     │
└──────┬───────┘    └────────┬────────┘    └────────┬─────────┘
       │                     │                      │
       │  POST /api/ai/chat  │                      │
       │  {message: "..."}   │                      │
       │────────────────────>│                      │
       │                     │                      │
       │                     │ 1. get_recent_data() │
       │                     │    (context)         │
       │                     │                      │
       │                     │ 2. chat(msg, context)│
       │                     │─────────────────────>│
       │                     │                      │
       │                     │                      │ GPT-2 generates
       │                     │                      │ response
       │                     │                      │
       │                     │   AI response        │
       │                     │<─────────────────────│
       │                     │                      │
       │  JSON Response      │                      │
       │<────────────────────│                      │
```

---

## Database

### MongoDB Configuration

```yaml
# docker-compose.yml
services:
  mongodb:
    image: mongo:7.0
    container_name: web_crawler_mongodb
    ports:
      - "27017:27017"
    environment:
      MONGO_INITDB_ROOT_USERNAME: admin
      MONGO_INITDB_ROOT_PASSWORD: AdminPass2026
      MONGO_INITDB_DATABASE: web_crawler
    volumes:
      - mongodb_data:/data/db
      - ./scripts/mongo-init.js:/docker-entrypoint-initdb.d/mongo-init.js
```

### Collection Schemas

#### `sources` Collection
```json
{
  "_id": ObjectId,
  "name": "GitHub Blog RSS",
  "url": "https://github.blog/feed/",
  "type": "rss",                    // html, rss, pdf, xml, txt, dynamic
  "description": "GitHub's official blog",
  "category": "Technology",
  "selectors": {                    // For HTML
    "container": ".post",
    "title": ".post-title",
    "content": ".post-body"
  },
  "frequency": "daily",             // hourly, daily, weekly, monthly
  "schedule_time": "00:00",
  "max_items": 50,
  "status": "active",
  "created_at": ISODate,
  "updated_at": ISODate
}
```

#### `crawled_data` Collection
```json
{
  "_id": ObjectId,
  "source_id": "source_ObjectId",
  "source_url": "https://...",
  "type": "html",
  "title": "Article Title",
  "content": "Article content...",
  "data": {
    "title": "...",
    "author": "...",
    "custom_field": "..."
  },
  "images": [
    {"url": "https://...", "alt": "Image description"}
  ],
  "link": "https://...",            // For RSS
  "published": "2026-01-15",        // For RSS
  "pages": 10,                      // For PDF
  "timestamp": ISODate
}
```

#### `crawl_logs` Collection
```json
{
  "_id": ObjectId,
  "source_id": "source_ObjectId",
  "url": "https://...",
  "status": "success",              // success, error, no_data
  "items_collected": 25,
  "errors": [],
  "timestamp": ISODate
}
```

### MongoDB Indexes

```javascript
// Text index for full-text search
crawled_data.createIndex({ content: "text", title: "text" })

// Index for queries by source and date
crawled_data.createIndex({ source_id: 1, timestamp: 1 })

// Unique index to avoid duplicate sources
sources.createIndex({ url: 1 }, { unique: true })
```

---

## Data Sources

### Pre-configured Sources (22 sources)

The `default_sources.py` file contains 22 sources organized by category:

| Category | Sources | Type |
|----------|---------|------|
| **Technology** | Python Blog, GitHub Blog, Reddit Programming, Dev.to, Stack Overflow, Medium | HTML, RSS |
| **News** | TechCrunch, Hacker News, BBC News, Reuters, Wired | RSS |
| **Science** | NASA Breaking News | RSS |
| **PDF Documents** | arXiv Papers, WHO Reports | PDF, HTML |
| **Books** | Project Gutenberg, Open Library, Internet Archive, Standard Ebooks | HTML |
| **Images** | NASA Image of the Day, Flickr Explore | RSS, HTML |

### Supported Source Types

| Type | Description | Library |
|------|-------------|---------|
| `html` | Static web pages | BeautifulSoup |
| `dynamic` | JavaScript pages | SeleniumBase |
| `rss` | RSS/Atom feeds | feedparser |
| `pdf` | PDF documents | PyPDF2 |
| `xml` | XML files | BeautifulSoup (xml) |
| `txt` | Text files | requests |

### CSS Selector Configuration

```python
{
    "name": "Example Site",
    "url": "https://example.com",
    "type": "html",
    "selectors": {
        "container": ".article",      # Parent element (required)
        "title": "h2.title",          # Title selector
        "content": ".body p",         # Content selector
        "author": ".meta .author",    # Custom fields
        "date": ".meta .date"
    },
    "max_items": 50                    # Items limit
}
```

---

## AI Service

### Models Used

| Model | Usage | Size |
|-------|-------|------|
| **DistilBART** (`sshleifer/distilbart-cnn-12-6`) | Text summarization | ~1.2 GB |
| **GPT-2** (`gpt2`) | Chat/Generation | ~500 MB |

### Features

1. **Text Summarization**
   - Input: Raw text (max 1000 characters)
   - Output: Summary (30-130 words)
   
2. **Multi-item Summarization**
   - Combines content from multiple items
   - Generates a global summary

3. **Contextual Chat**
   - Uses recent data as context
   - Answers questions about crawled data
   
4. **Data Analysis**
   - Statistics by content type
   - Count by source
   - Temporal distribution

### Rule-Based Fallback

If AI models fail, a rule-based system takes over:

```python
if "how many" in message → Count response
if "summarize" in message → Simple summary
if "what" in message     → Data description
else                     → Generic help message
```

---

## User Interface

### HTML Templates

| Template | Route | Description |
|----------|-------|-------------|
| `base.html` | - | Common layout, navigation, CSS/JS |
| `index.html` | `/` | Dashboard with statistics |
| `sources.html` | `/sources` | Source CRUD management |
| `search.html` | `/search` | Search with type filters |
| `reports.html` | `/reports` | Charts and analytics |
| `ai.html` | `/ai` | AI chat interface |
| `404.html` | - | 404 error page |
| `500.html` | - | 500 error page |

### UI Features

- **Responsive Design**: Adaptive for mobile/desktop
- **SVG Icons**: Professional design without emojis
- **Real-time Stats**: Updated metrics
- **Image Gallery**: Grid layout with modal preview
- **PDF Viewer**: Direct links to PDFs
- **Type Filtering**: Filter by content type

---

## Configuration and Deployment

### Environment Variables (.env)

```bash
# MongoDB
MONGODB_URI=mongodb://crawler_admin:password@localhost:27017/web_crawler?authSource=admin
MONGODB_DATABASE=web_crawler

# Flask
FLASK_ENV=development
FLASK_DEBUG=True
SECRET_KEY=your-secret-key

# AI (optional)
OPENAI_API_KEY=your-api-key
AI_MODEL=gpt-3.5-turbo

# Crawler
CRAWLER_USER_AGENT=WebCrawler/1.0
CRAWLER_DELAY=1
CRAWLER_TIMEOUT=30

# Scheduler
SCHEDULER_ENABLED=True
CRAWL_INTERVAL_HOURS=24
```

### Quick Start

```bash
# 1. Activate virtual environment
.\venv\Scripts\activate

# 2. Install dependencies
pip install -r requirements.txt

# 3. Start MongoDB (Docker)
docker-compose up -d

# 4. Launch application
python app.py

# 5. Access dashboard
# http://localhost:5000
```

### Docker Commands

```bash
# Start MongoDB
docker-compose up -d

# Check status
docker ps

# View logs
docker logs web_crawler_mongodb

# Stop
docker-compose down

# Delete data
docker-compose down -v
```

---

## Diagrams

### Sequence Diagram - Full Crawl

```
┌────────┐     ┌─────────┐     ┌──────────┐     ┌──────────┐     ┌─────────┐
│  User  │     │  Flask  │     │ Crawler  │     │ Website  │     │ MongoDB │
└───┬────┘     └────┬────┘     └────┬─────┘     └────┬─────┘     └────┬────┘
    │               │               │                │                │
    │ Click "Crawl" │               │                │                │
    │──────────────>│               │                │                │
    │               │               │                │                │
    │               │ crawl_source()│                │                │
    │               │──────────────>│                │                │
    │               │               │                │                │
    │               │               │  GET request   │                │
    │               │               │───────────────>│                │
    │               │               │                │                │
    │               │               │  HTML response │                │
    │               │               │<───────────────│                │
    │               │               │                │                │
    │               │               │ Parse & Extract│                │
    │               │               │────────┐       │                │
    │               │               │        │       │                │
    │               │               │<───────┘       │                │
    │               │               │                │                │
    │               │               │    store_data()│                │
    │               │               │────────────────────────────────>│
    │               │               │                │                │
    │               │               │    log_crawl() │                │
    │               │               │────────────────────────────────>│
    │               │               │                │                │
    │               │   {success}   │                │                │
    │               │<──────────────│                │                │
    │               │               │                │                │
    │  Show results │               │                │                │
    │<──────────────│               │                │                │
    │               │               │                │                │
```

### Component Diagram

```
┌─────────────────────────────────────────────────────────────────────────┐
│                              WEB CRAWLER SYSTEM                          │
│                                                                          │
│  ┌─────────────────────────────────────────────────────────────────┐    │
│  │                         FRONTEND (Templates)                     │    │
│  │  ┌─────────┐ ┌─────────┐ ┌─────────┐ ┌─────────┐ ┌─────────┐   │    │
│  │  │Dashboard│ │ Sources │ │ Search  │ │ Reports │ │   AI    │   │    │
│  │  └─────────┘ └─────────┘ └─────────┘ └─────────┘ └─────────┘   │    │
│  └─────────────────────────────────────────────────────────────────┘    │
│                                    │                                     │
│                                    ▼                                     │
│  ┌─────────────────────────────────────────────────────────────────┐    │
│  │                         BACKEND (Python)                         │    │
│  │                                                                  │    │
│  │  ┌──────────────────────────────────────────────────────────┐   │    │
│  │  │                     app.py (Flask)                        │   │    │
│  │  │           Routes + API + JSON Encoder                     │   │    │
│  │  └──────────────────────────────────────────────────────────┘   │    │
│  │           │                │                │                    │    │
│  │           ▼                ▼                ▼                    │    │
│  │  ┌──────────────┐ ┌──────────────┐ ┌──────────────┐             │    │
│  │  │   Crawler    │ │  Scheduler   │ │  AI Service  │             │    │
│  │  │  Enhanced    │ │              │ │              │             │    │
│  │  │              │ │  • schedule  │ │  • DistilBART│             │    │
│  │  │ • HTML/RSS   │ │  • threading │ │  • GPT-2     │             │    │
│  │  │ • PDF/XML    │ │              │ │              │             │    │
│  │  │ • Selenium   │ │              │ │              │             │    │
│  │  └──────────────┘ └──────────────┘ └──────────────┘             │    │
│  │           │                │                                     │    │
│  │           └────────────────┼─────────────────────────────────   │    │
│  │                            ▼                                     │    │
│  │  ┌──────────────────────────────────────────────────────────┐   │    │
│  │  │                    database.py                            │   │    │
│  │  │              CrawlerDatabase (PyMongo)                    │   │    │
│  │  └──────────────────────────────────────────────────────────┘   │    │
│  └─────────────────────────────────────────────────────────────────┘    │
│                                    │                                     │
│                                    ▼                                     │
│  ┌─────────────────────────────────────────────────────────────────┐    │
│  │                         DATABASE (Docker)                        │    │
│  │  ┌──────────────────────────────────────────────────────────┐   │    │
│  │  │                    MongoDB 7.0                            │   │    │
│  │  │  ┌──────────┐  ┌──────────────┐  ┌────────────┐          │   │    │
│  │  │  │ sources  │  │ crawled_data │  │ crawl_logs │          │   │    │
│  │  │  └──────────┘  └──────────────┘  └────────────┘          │   │    │
│  │  └──────────────────────────────────────────────────────────┘   │    │
│  └─────────────────────────────────────────────────────────────────┘    │
│                                                                          │
└─────────────────────────────────────────────────────────────────────────┘
```

---

## Summary

The **Web Crawler System** is a complete and modular solution for:

1. ✅ **Collecting** data from various web sources
2. ✅ **Storing** in a structured way in MongoDB
3. ✅ **Scheduling** automatic crawls
4. ✅ **Searching** with full-text index
5. ✅ **Analyzing** with AI (summary, chat)
6. ✅ **Visualizing** via a modern web interface

### Key Technologies

| Category | Technologies |
|----------|--------------|
| **Backend** | Python 3.8+, Flask, PyMongo |
| **Crawling** | BeautifulSoup, SeleniumBase, feedparser, PyPDF2 |
| **Database** | MongoDB 7.0, Docker |
| **AI** | Hugging Face Transformers (DistilBART, GPT-2) |
| **Frontend** | Jinja2, HTML5, CSS3, JavaScript |
| **Scheduling** | schedule, threading |

---

*Document generated on January 16, 2026*
