"""
Flask Web Crawler Dashboard
Modern UI for web crawling system
"""
from flask import Flask, render_template, request, jsonify, send_file
from database import CrawlerDatabase
from crawler_enhanced import EnhancedWebCrawler
from default_sources import DEFAULT_SOURCES, get_sources_by_category
from datetime import datetime, timedelta
from bson import ObjectId
import json

app = Flask(__name__)
app.config['SECRET_KEY'] = 'web-crawler-secret-key-2026'

# Custom JSON encoder for MongoDB ObjectId
class JSONEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, ObjectId):
            return str(obj)
        if isinstance(obj, datetime):
            return obj.isoformat()
        return super().default(obj)

app.json_encoder = JSONEncoder

# Initialize database and crawler
db = CrawlerDatabase()
crawler = EnhancedWebCrawler(db)

@app.route('/')
def index():
    """Dashboard home page"""
    stats = db.get_statistics()
    recent_logs = db.get_crawl_logs(limit=10)
    
    return render_template('index.html', 
                         stats=stats, 
                         recent_logs=recent_logs)

@app.route('/sources')
def sources():
    """Sources management page"""
    configured_sources = db.get_all_sources()
    categories = get_sources_by_category()
    
    return render_template('sources.html', 
                         configured_sources=configured_sources,
                         default_sources=DEFAULT_SOURCES,
                         categories=categories)

@app.route('/api/sources', methods=['GET'])
def get_sources():
    """API: Get all sources"""
    sources = db.get_all_sources()
    return jsonify(sources)

@app.route('/api/sources/add', methods=['POST'])
def add_source():
    """API: Add a new source"""
    data = request.json
    try:
        source_id = db.add_source(data)
        return jsonify({'success': True, 'source_id': source_id})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 400

@app.route('/api/sources/<source_id>/delete', methods=['DELETE'])
def delete_source(source_id):
    """API: Delete a source"""
    try:
        success = db.delete_source(source_id)
        return jsonify({'success': success})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 400

@app.route('/api/crawl', methods=['POST'])
def crawl_now():
    """API: Crawl a source immediately"""
    data = request.json
    
    try:
        # Check database connection
        if not db.client:
            return jsonify({
                'success': False,
                'error': 'Database not connected. Please restart the application.'
            }), 500
        
        # Create temporary source for crawling
        temp_source = {
            "_id": data.get('_id', 'temp_crawl'),
            "name": data.get('name'),
            "url": data.get('url'),
            "type": data.get('type'),
            "max_items": data.get('max_items', 20),
            "frequency": data.get('frequency', 'daily')
        }
        
        if 'selectors' in data:
            temp_source['selectors'] = data['selectors']
        
        # Crawl
        result = crawler.crawl_source(temp_source)
        
        # Check for errors
        if result['status'] == 'error':
            error_msg = ', '.join(result.get('errors', ['Unknown error']))
            return jsonify({
                'success': False,
                'error': error_msg,
                'result': result
            }), 400
        
        if result['status'] == 'no_data':
            error_msg = 'No data found. ' + ', '.join(result.get('errors', ['The source may be empty or unavailable']))
            return jsonify({
                'success': False,
                'error': error_msg,
                'result': result
            }), 400
        
        # Get recent data and convert ObjectId to string
        recent_data = []
        if result['status'] == 'success':
            raw_data = db.get_recent_data(limit=3)
            for item in raw_data:
                # Convert ObjectId to string
                if '_id' in item:
                    item['_id'] = str(item['_id'])
                if 'source_id' in item and isinstance(item['source_id'], ObjectId):
                    item['source_id'] = str(item['source_id'])
                # Convert datetime to string
                if 'timestamp' in item and isinstance(item['timestamp'], datetime):
                    item['timestamp'] = item['timestamp'].isoformat()
                recent_data.append(item)
        
        # Convert result ObjectIds
        if '_id' in result:
            result['_id'] = str(result['_id'])
        if 'source_id' in result:
            result['source_id'] = str(result['source_id'])
        if 'timestamp' in result and isinstance(result['timestamp'], datetime):
            result['timestamp'] = result['timestamp'].isoformat()
        
        return jsonify({
            'success': result['status'] == 'success',
            'result': result,
            'recent_data': recent_data
        })
    except Exception as e:
        import traceback
        error_trace = traceback.format_exc()
        print(error_trace)
        return jsonify({
            'success': False,
            'error': str(e),
            'trace': error_trace
        }), 400

@app.route('/api/sources/<source_id>/crawl', methods=['POST'])
def crawl_source_by_id(source_id):
    """API: Crawl a configured source"""
    try:
        source = db.get_source(source_id)
        if not source:
            return jsonify({'success': False, 'error': 'Source not found'}), 404
        
        result = crawler.crawl_source(source)
        return jsonify({
            'success': result['status'] == 'success',
            'result': result
        })
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 400

@app.route('/search')
def search():
    """Search page"""
    return render_template('search.html')

@app.route('/api/search', methods=['POST'])
def search_data():
    """API: Search crawled data"""
    data = request.json
    search_type = data.get('type', 'keyword')
    content_type = data.get('content_type', 'all')  # New: filter by content type
    
    try:
        if search_type == 'keyword':
            keyword = data.get('keyword', '')
            results = db.search_by_keyword(keyword, limit=100)
        elif search_type == 'source':
            source_id = data.get('source_id', '')
            results = db.get_data_by_source(source_id, limit=100)
        elif search_type == 'recent':
            limit = data.get('limit', 50)
            results = db.get_recent_data(limit=limit)
        elif search_type == 'date_range':
            start_date = datetime.fromisoformat(data.get('start_date'))
            end_date = datetime.fromisoformat(data.get('end_date'))
            results = db.get_data_by_date_range(start_date, end_date)
        else:
            results = []
        
        # Filter by content type if specified
        if content_type != 'all':
            results = [r for r in results if r.get('type') == content_type]
        
        # Convert ObjectId and datetime to strings
        clean_results = []
        for item in results:
            if '_id' in item:
                item['_id'] = str(item['_id'])
            if 'source_id' in item and isinstance(item['source_id'], ObjectId):
                item['source_id'] = str(item['source_id'])
            if 'timestamp' in item and isinstance(item['timestamp'], datetime):
                item['timestamp'] = item['timestamp'].isoformat()
            clean_results.append(item)
        
        return jsonify({'success': True, 'results': clean_results})
    except Exception as e:
        import traceback
        traceback.print_exc()
        return jsonify({'success': False, 'error': str(e)}), 400

@app.route('/reports')
def reports():
    """Reports and analytics page"""
    stats = db.get_statistics()
    logs = db.get_crawl_logs(limit=100)
    
    return render_template('reports.html', stats=stats, logs=logs)

@app.route('/api/stats', methods=['GET'])
def get_stats():
    """API: Get statistics"""
    stats = db.get_statistics()
    return jsonify(stats)

@app.route('/api/logs', methods=['GET'])
def get_logs():
    """API: Get crawl logs"""
    limit = request.args.get('limit', 100, type=int)
    logs = db.get_crawl_logs(limit=limit)
    return jsonify(logs)

@app.route('/ai')
def ai_page():
    """AI Chat and Summarization page"""
    return render_template('ai.html')

@app.route('/api/ai/summarize', methods=['POST'])
def ai_summarize():
    """API: Summarize data"""
    data = request.json
    item_ids = data.get('item_ids', [])
    
    try:
        # Get AI service
        from ai_service import get_ai_service
        ai = get_ai_service()
        
        # Check if models are loaded
        if not ai.summarizer:
            return jsonify({
                'success': False,
                'error': 'Summarization model is still loading. Please wait a moment and try again.'
            }), 503
        
        # Get items from database
        items = []
        for item_id in item_ids[:10]:  # Limit to 10 items
            item_data = db.crawled_data.find_one({"_id": ObjectId(item_id)})
            if item_data:
                items.append(item_data)
        
        if not items:
            return jsonify({'success': False, 'error': 'No items found'}), 400
        
        # Summarize
        summary = ai.summarize_data_items(items)
        
        return jsonify({'success': True, 'summary': summary})
    except Exception as e:
        import traceback
        error_trace = traceback.format_exc()
        print("AI Summarize Error:")
        print(error_trace)
        return jsonify({
            'success': False,
            'error': f'Summarization error: {str(e)}'
        }), 500

@app.route('/api/ai/chat', methods=['POST'])
def ai_chat():
    """API: Chat with AI about data"""
    data = request.json
    message = data.get('message', '')
    
    if not message:
        return jsonify({'success': False, 'error': 'No message provided'}), 400
    
    try:
        # Get AI service
        from ai_service import get_ai_service
        ai = get_ai_service()
        
        # Check if models are loaded
        if not ai.summarizer and not ai.chat_model:
            return jsonify({
                'success': False,
                'error': 'AI models are still loading. Please wait a moment and try again.'
            }), 503
        
        # Get recent data for context
        recent_items = db.get_recent_data(limit=5)
        context = ""
        for item in recent_items:
            context += f"{item.get('title', '')}: {item.get('content', '')[:200]} "
        
        # Chat with AI
        response = ai.chat(message, context[:500])
        
        return jsonify({'success': True, 'response': response})
    except Exception as e:
        import traceback
        error_trace = traceback.format_exc()
        print("AI Chat Error:")
        print(error_trace)
        return jsonify({
            'success': False,
            'error': f'AI error: {str(e)}. Models may still be loading.'
        }), 500

@app.route('/api/ai/analyze', methods=['POST'])
def ai_analyze():
    """API: Analyze data with AI"""
    data = request.json
    search_query = data.get('query', '')
    
    try:
        # Get AI service
        from ai_service import get_ai_service
        ai = get_ai_service()
        
        # Get data based on query
        if search_query:
            items = db.search_by_keyword(search_query, limit=50)
        else:
            items = db.get_recent_data(limit=50)
        
        if not items:
            return jsonify({'success': False, 'error': 'No data found'}), 400
        
        # Analyze
        analysis = ai.analyze_data(items)
        
        return jsonify({'success': True, 'analysis': analysis})
    except Exception as e:
        import traceback
        error_trace = traceback.format_exc()
        print("AI Analyze Error:")
        print(error_trace)
        return jsonify({
            'success': False,
            'error': f'Analysis error: {str(e)}'
        }), 500

@app.errorhandler(404)
def not_found(error):
    return render_template('404.html'), 404

@app.errorhandler(500)
def internal_error(error):
    return render_template('500.html'), 500

if __name__ == '__main__':
    print("=" * 70)
    print("🚀 WEB CRAWLER DASHBOARD")
    print("=" * 70)
    print(f"\n✅ MongoDB: {'Connected' if db.client else 'Not Connected'}")
    print(f"✅ Flask: Starting server...")
    print(f"\n🌐 Open your browser and go to:")
    print(f"   http://localhost:5000")
    print("\n" + "=" * 70)
    
    # Disable reloader to prevent AI model loading issues
    app.run(debug=True, host='0.0.0.0', port=5000, use_reloader=False)
