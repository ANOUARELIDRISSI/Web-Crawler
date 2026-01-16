"""
Default Crawl Sources Configuration

This module provides pre-configured website sources for easy setup.
It includes popular technology news sites, blogs, and RSS feeds.

Constants:
    DEFAULT_SOURCES: List of pre-configured source dictionaries

Functions:
    get_sources_by_category: Group sources by category
    get_source_by_name: Retrieve a specific source by name

Example:
    >>> from default_sources import DEFAULT_SOURCES
    >>> for source in DEFAULT_SOURCES:
    ...     print(source['name'], source['type'])
"""

DEFAULT_SOURCES = [
    {
        "name": "Python Official Blog",
        "url": "https://blog.python.org/",
        "type": "html",
        "description": "Official Python Software Foundation blog",
        "category": "Technology",
        "selectors": {
            "container": ".post",
            "title": ".post-title",
            "content": ".post-body"
        }
    },
    {
        "name": "GitHub Blog RSS",
        "url": "https://github.blog/feed/",
        "type": "rss",
        "description": "GitHub's official blog feed",
        "category": "Technology"
    },
    {
        "name": "TechCrunch RSS",
        "url": "https://techcrunch.com/feed/",
        "type": "rss",
        "description": "Latest technology news",
        "category": "News"
    },
    {
        "name": "Hacker News RSS",
        "url": "https://news.ycombinator.com/rss",
        "type": "rss",
        "description": "Tech and startup news",
        "category": "News"
    },
    {
        "name": "BBC News RSS",
        "url": "http://feeds.bbci.co.uk/news/rss.xml",
        "type": "rss",
        "description": "BBC World News feed",
        "category": "News"
    },
    {
        "name": "Reddit Programming",
        "url": "https://www.reddit.com/r/programming/.rss",
        "type": "rss",
        "description": "Programming subreddit feed",
        "category": "Technology"
    },
    {
        "name": "Dev.to RSS",
        "url": "https://dev.to/feed",
        "type": "rss",
        "description": "Developer community articles",
        "category": "Technology"
    },
    {
        "name": "Medium Technology",
        "url": "https://medium.com/feed/tag/technology",
        "type": "rss",
        "description": "Technology articles on Medium",
        "category": "Technology"
    },
    {
        "name": "Stack Overflow Blog",
        "url": "https://stackoverflow.blog/feed/",
        "type": "rss",
        "description": "Stack Overflow engineering blog",
        "category": "Technology"
    },
    {
        "name": "NASA Breaking News",
        "url": "https://www.nasa.gov/rss/dyn/breaking_news.rss",
        "type": "rss",
        "description": "NASA latest news",
        "category": "Science"
    },
    {
        "name": "arXiv Computer Science Papers (PDF)",
        "url": "https://arxiv.org/pdf/2301.00001",
        "type": "pdf",
        "description": "Academic research papers in PDF format from arXiv",
        "category": "PDF Documents"
    },
    {
        "name": "Python PEP Documents (PDF)",
        "url": "https://www.python.org/dev/peps/pep-0008/",
        "type": "html",
        "description": "Python Enhancement Proposals documentation",
        "category": "PDF Documents",
        "selectors": {
            "container": ".section",
            "title": "h1, h2",
            "content": "p"
        }
    },
    {
        "name": "Project Gutenberg - Free Books",
        "url": "https://www.gutenberg.org/ebooks/search/?sort_order=downloads",
        "type": "html",
        "description": "Free ebooks from Project Gutenberg",
        "category": "Books",
        "selectors": {
            "container": ".booklink",
            "title": ".title",
            "content": ".subtitle"
        }
    },
    {
        "name": "Open Library Books",
        "url": "https://openlibrary.org/search.json?q=python&limit=20",
        "type": "html",
        "description": "Open Library book database",
        "category": "Books"
    },
    {
        "name": "NASA Image of the Day",
        "url": "https://www.nasa.gov/rss/dyn/lg_image_of_the_day.rss",
        "type": "rss",
        "description": "NASA's daily featured images",
        "category": "Images"
    },
    {
        "name": "Flickr Explore",
        "url": "https://www.flickr.com/explore",
        "type": "html",
        "description": "Trending photos on Flickr",
        "category": "Images",
        "selectors": {
            "container": ".photo-list-photo-view",
            "title": "img",
            "content": "img"
        }
    },
    {
        "name": "Internet Archive Books",
        "url": "https://archive.org/details/texts",
        "type": "html",
        "description": "Free books from Internet Archive",
        "category": "Books",
        "selectors": {
            "container": ".item-ia",
            "title": ".ttl",
            "content": ".by"
        }
    },
    {
        "name": "Standard Ebooks",
        "url": "https://standardebooks.org/ebooks/",
        "type": "html",
        "description": "High-quality free ebooks",
        "category": "Books",
        "selectors": {
            "container": "li[typeof='schema:Book']",
            "title": "span[property='schema:name']",
            "content": "span[property='schema:author']"
        }
    },
    {
        "name": "WHO PDF Reports",
        "url": "https://www.who.int/publications/i",
        "type": "html",
        "description": "World Health Organization reports and documents",
        "category": "PDF Documents"
    },
    {
        "name": "arXiv Recent Papers RSS",
        "url": "http://export.arxiv.org/rss/cs",
        "type": "rss",
        "description": "Recent computer science papers from arXiv",
        "category": "PDF Documents"
    },
    {
        "name": "Reuters Technology News",
        "url": "https://www.reutersagency.com/feed/?taxonomy=best-topics&post_type=best",
        "type": "rss",
        "description": "Reuters technology news feed",
        "category": "News"
    },
    {
        "name": "Wired RSS Feed",
        "url": "https://www.wired.com/feed/rss",
        "type": "rss",
        "description": "Wired technology and science news",
        "category": "News"
    }
]

def get_sources_by_category():
    """
    Group sources by category.
    
    Returns:
        dict: Dictionary mapping category names to lists of sources
        
    Example:
        >>> categories = get_sources_by_category()
        >>> print(categories['Technology'])
    """
    categories = {}
    for source in DEFAULT_SOURCES:
        category = source.get("category", "Other")
        if category not in categories:
            categories[category] = []
        categories[category].append(source)
    return categories

def get_source_by_name(name):
    """
    Get a specific source by name.
    
    Args:
        name (str): The name of the source to retrieve
        
    Returns:
        dict or None: Source dictionary if found, None otherwise
        
    Example:
        >>> source = get_source_by_name("GitHub Blog RSS")
        >>> print(source['url'])
    """
    for source in DEFAULT_SOURCES:
        if source["name"] == name:
            return source
    return None
