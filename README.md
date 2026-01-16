# Web Crawler System with AI Assistant

A professional web crawling system with MongoDB storage, Flask UI, and AI-powered analysis using Hugging Face models.

## Features

### Core Functionality
- **Multi-Format Crawling**: HTML, RSS, PDF, XML, TXT, Dynamic JavaScript pages
- **MongoDB Storage**: Scalable NoSQL database with authentication
- **Docker Integration**: Containerized MongoDB deployment
- **Scheduler**: Automated crawling with configurable frequencies
- **Enhanced Image Support**: Extract and display images from crawled content

### Professional UI
- **Flask-Based Dashboard**: Modern, responsive interface
- **SVG Icons**: Professional design without emojis
- **Type Filtering**: Search by content type (HTML, RSS, PDF, etc.)
- **Image Gallery**: Grid layout with modal preview
- **PDF Viewer**: Direct links to PDF documents
- **Real-time Statistics**: Dashboard with crawl metrics

### AI Assistant (NEW)
- **Chat Interface**: Ask questions about your crawled data
- **Data Summarization**: AI-powered content summaries using BART (via API)
- **Data Analysis**: Automated insights and statistics
- **Context-Aware**: Uses recent data for intelligent responses
- **Hugging Face API**: Uses Inference API (no local model loading required)
- **Free Tier**: Works without API key (with rate limits)

## Quick Start

### 1. Prerequisites
- Python 3.8+
- Docker Desktop
- 4GB+ RAM

### 2. Installation

```bash
# Clone or navigate to project directory
cd "E:\Web Crawling"

# Activate virtual environment
.\venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

### 3. Start MongoDB

```bash
# Start Docker container
docker-compose up -d

# Verify container is running
docker ps
```

### 4. Run Application

```bash
# Activate venv and start Flask
.\venv\Scripts\activate
python app.py
```

### 5. Access Dashboard

Open browser: **http://localhost:5000**

## Project Structure

```
├── app.py                      # Flask application with AI endpoints
├── ai_service.py               # AI service (chat, summarization, analysis)
├── crawler_enhanced.py         # Enhanced crawler with image support
├── database.py                 # MongoDB integration
├── default_sources.py          # 22 pre-configured sources
├── scheduler.py                # Automated crawling scheduler
├── docker-compose.yml          # MongoDB container configuration
├── .env                        # Environment variables
├── requirements.txt            # Python dependencies
├── templates/
│   ├── base.html              # Base template with professional styling
│   ├── index.html             # Dashboard
│   ├── sources.html           # Source management with Quick Crawl
│   ├── search.html            # Enhanced search with type filtering
│   ├── reports.html           # Analytics and charts
│   ├── ai.html                # AI Assistant interface
│   ├── 404.html               # Error page
│   └── 500.html               # Error page
└── scripts/
    ├── add_default_sources.py # Add default sources to database
    └── mongo-init.js          # MongoDB initialization script
```

## Configuration

### Environment Variables (.env)
```env
MONGODB_HOST=localhost
MONGODB_PORT=27017
MONGODB_DATABASE=web_crawler
MONGODB_USERNAME=crawler_admin
MONGODB_PASSWORD=Crawler2026SecurePass
MONGODB_URI=mongodb://crawler_admin:Crawler2026SecurePass@localhost:27017/web_crawler?authSource=admin
```

### MongoDB Docker
- Container: `web_crawler_mongodb`
- Port: 27017
- Authentication: Enabled
- Health Check: Automatic

## Usage Guide

### Dashboard
- View real-time statistics
- Monitor crawl activity
- Success rate metrics
- Quick action cards

### Sources Management

#### Quick Crawl
1. Select source from dropdown (organized by category)
2. Configure max items (1-200)
3. Set frequency (hourly/daily/weekly/monthly)
4. Click "Crawl Now" for immediate results
5. View preview of collected data
6. Optionally add to sources for scheduling

#### Categories
- **Technology** (6 sources): Python Blog, GitHub, Reddit, Dev.to, Medium, Stack Overflow
- **News** (5 sources): TechCrunch, Hacker News, BBC, Reuters, Wired
- **Science** (1 source): NASA
- **PDF Documents** (4 sources): arXiv papers, Python PEPs, WHO reports
- **Books** (4 sources): Project Gutenberg ✅ (tested), Internet Archive, Open Library, Standard Ebooks
- **Images** (2 sources): NASA Images, Flickr

**Note**: Some sources may return "No data found" if:
- The RSS feed is empty or unavailable
- The website structure has changed
- The URL requires authentication
- The site blocks automated requests

**Recommended sources** (tested and working):
- GitHub Blog RSS ✅
- TechCrunch RSS ✅
- Hacker News RSS ✅
- Project Gutenberg ✅
- NASA Breaking News ✅

### Search with Type Filtering

#### Search Options
- **Keyword Search**: Full-text search across all content
- **Recent Data**: View latest crawled items
- **Type Filter**: Filter by HTML, RSS, PDF, XML, TXT, Dynamic

#### Data Display
- **Images**: Grid gallery with modal preview
- **PDFs**: Prominent "View PDF" button
- **Content**: Expandable text with "Show more"
- **Metadata**: Source URL, timestamp, type badge

### AI Assistant

#### Chat
- Ask questions about your data
- Context-aware responses
- Natural language interface
- Examples:
  - "What data do we have?"
  - "Tell me about recent items"
  - "Summarize the content"

#### Data Analysis
- Automated insights
- Content type distribution
- Source statistics
- Image counts
- AI-generated summary

#### Quick Summarize
- One-click summarization
- Uses recent data (last 10 items)
- BART model for quality summaries
- Displays key points

## API Endpoints

### Web Pages
- `GET /` - Dashboard
- `GET /sources` - Sources management
- `GET /search` - Search interface
- `GET /reports` - Analytics
- `GET /ai` - AI Assistant

### Data APIs
- `POST /api/crawl` - Crawl source immediately
- `POST /api/search` - Search with type filtering
- `POST /api/sources/add` - Add new source
- `DELETE /api/sources/<id>/delete` - Delete source
- `POST /api/sources/<id>/crawl` - Crawl specific source
- `GET /api/stats` - Get statistics
- `GET /api/logs` - Get crawl logs

### AI APIs
- `POST /api/ai/chat` - Chat with AI
- `POST /api/ai/summarize` - Summarize data items
- `POST /api/ai/analyze` - Analyze data with AI

## AI Models

### Summarization
- **Model**: sshleifer/distilbart-cnn-12-6 (DistilBART - lightweight)
- **Purpose**: Generate concise summaries
- **Size**: ~300MB
- **Speed**: 2-5 seconds on CPU
- **Max Length**: 130 tokens

### Chat
- **Model**: gpt2 (GPT-2 small)
- **Purpose**: Answer questions about crawled data
- **Size**: ~500MB
- **Speed**: 1-3 seconds on CPU
- **Features**: Context-aware responses with fallback to rule-based

### Performance
- **Local Models**: Runs entirely on your machine
- **CPU Optimized**: No GPU required
- **Memory**: ~1GB RAM for both models
- **First Load**: Models download automatically (takes 2-5 minutes)
- **Subsequent Loads**: Instant (models cached locally)

### Model Loading
Models are downloaded automatically on first use to:
- Windows: `C:\Users\<username>\.cache\huggingface\`
- The download happens once and models are reused

### Troubleshooting AI
If AI features don't work:
1. Check console for "AI models loaded" message
2. Wait for models to download (first time only)
3. Ensure you have ~1GB free RAM
4. Check internet connection (for first download)

## Database Schema

### Sources Collection
```json
{
  "_id": "ObjectId",
  "name": "Source Name",
  "url": "https://example.com",
  "type": "html|rss|pdf|xml|txt|dynamic",
  "frequency": "hourly|daily|weekly|monthly",
  "max_items": 50,
  "schedule_time": "09:00",
  "selectors": {
    "container": ".article",
    "title": "h2",
    "content": "p"
  },
  "status": "active",
  "created_at": "ISODate",
  "updated_at": "ISODate"
}
```

### Crawled Data Collection
```json
{
  "_id": "ObjectId",
  "source_id": "ObjectId",
  "source_url": "https://example.com",
  "type": "html",
  "title": "Article Title",
  "content": "Article content...",
  "images": [
    {
      "url": "https://example.com/image.jpg",
      "alt": "Image description"
    }
  ],
  "link": "https://example.com/article",
  "timestamp": "ISODate"
}
```

### Crawl Logs Collection
```json
{
  "_id": "ObjectId",
  "source_id": "ObjectId",
  "url": "https://example.com",
  "status": "success|error|no_data",
  "items_collected": 10,
  "errors": [],
  "timestamp": "ISODate"
}
```

## Docker Commands

```bash
# Start MongoDB
docker-compose up -d

# Stop MongoDB
docker-compose down

# View logs
docker logs web_crawler_mongodb

# Check status
docker ps

# Access MongoDB shell
docker exec -it web_crawler_mongodb mongosh -u admin -p AdminPass2026 --authenticationDatabase admin
```

## Testing

```bash
# Test MongoDB connection
python -c "from database import CrawlerDatabase; db = CrawlerDatabase(); print('Connected!' if db.client else 'Failed')"

# Test crawler
python test_quick_crawl.py

# Test special sources (PDFs, Books, Images)
python test_special_sources.py
```

## Troubleshooting

### MongoDB Connection Failed
```bash
# Check if Docker is running
docker ps

# Restart container
docker-compose restart

# Check logs
docker logs web_crawler_mongodb
```

### AI Models Not Loading
```bash
# Install dependencies
pip install transformers torch huggingface-hub

# Check disk space (models need ~2GB)
# Models download automatically on first use
```

### Flask App Won't Start
```bash
# Activate venv
.\venv\Scripts\activate

# Check dependencies
pip install -r requirements.txt

# Run with debug
python app.py
```

## Performance Tips

1. **Crawling**: Start with small max_items (10-20) for testing
2. **AI**: First request is slow (model loading), subsequent requests are faster
3. **Images**: Large galleries may slow page load
4. **Database**: Create indexes for better search performance
5. **Memory**: Close unused browser tabs when running AI

## Security

- MongoDB authentication enabled
- CSRF protection in Flask
- Input sanitization
- XSS prevention
- Secure password storage in .env
- Docker network isolation

## Future Enhancements

- [ ] User authentication
- [ ] Data export (CSV/JSON)
- [ ] Scheduling UI
- [ ] Email notifications
- [ ] Advanced AI features (sentiment analysis, entity extraction)
- [ ] Multi-language support
- [ ] API rate limiting
- [ ] Webhook integrations

## Dependencies

### Core
- Flask 3.1+
- PyMongo 4.6+
- BeautifulSoup4 4.12+
- Requests 2.32+

### AI
- Transformers 4.57+ (optional, for local models)
- PyTorch 2.9+ (optional, for local models)
- Hugging Face Hub 0.36+ (for API access)

### Utilities
- python-dotenv 1.0+
- schedule 1.2+
- feedparser 6.0+
- PyPDF2 3.0+

## License

MIT License - Free for personal and commercial use

## Support

For issues or questions:
1. Check troubleshooting section
2. Review error logs
3. Verify MongoDB is running
4. Check .env configuration

## Credits

- **AI Models**: Hugging Face (facebook/BART, microsoft/DialoGPT)
- **UI Framework**: Bootstrap 5
- **Database**: MongoDB 7.0
- **Icons**: Heroicons (SVG)

---

**Version**: 2.0.0  
**Last Updated**: January 2026  
**Status**: Production Ready ✓
