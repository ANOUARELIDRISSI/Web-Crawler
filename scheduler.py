"""
Crawler Scheduler Module

This module provides scheduling functionality for automated web crawling.
It manages scheduled crawling tasks using the schedule library and runs
them in a background thread.

Classes:
    CrawlerScheduler: Main scheduler class for managing crawl jobs

Example:
    >>> db = CrawlerDatabase()
    >>> crawler = WebCrawler(db)
    >>> scheduler = CrawlerScheduler(db, crawler)
    >>> scheduler.schedule_all_sources()
    >>> scheduler.start()
"""
import schedule
import time
import threading
from datetime import datetime
from typing import Dict, Any
from crawler import WebCrawler
from database import CrawlerDatabase

class CrawlerScheduler:
    def __init__(self, database: CrawlerDatabase, crawler: WebCrawler):
        """Initialize scheduler"""
        self.db = database
        self.crawler = crawler
        self.running = False
        self.thread = None
        self.jobs = {}
    
    def schedule_source(self, source: Dict[str, Any]):
        """Schedule a source for crawling"""
        source_id = source.get("_id")
        frequency = source.get("frequency", "daily")
        schedule_time = source.get("schedule_time", "00:00")
        
        # Clear existing job if any
        if source_id in self.jobs:
            schedule.cancel_job(self.jobs[source_id])
        
        # Create crawl job
        def crawl_job():
            print(f"[{datetime.now()}] Crawling source: {source.get('name')}")
            self.crawler.crawl_source(source)
        
        # Schedule based on frequency
        if frequency == "hourly":
            job = schedule.every().hour.do(crawl_job)
        elif frequency == "daily":
            job = schedule.every().day.at(schedule_time).do(crawl_job)
        elif frequency == "weekly":
            job = schedule.every().week.do(crawl_job)
        elif frequency == "monthly":
            job = schedule.every(30).days.do(crawl_job)
        else:
            # Custom interval in minutes
            try:
                interval = int(frequency)
                job = schedule.every(interval).minutes.do(crawl_job)
            except:
                job = schedule.every().day.do(crawl_job)
        
        self.jobs[source_id] = job
        print(f"Scheduled source: {source.get('name')} ({frequency})")
    
    def schedule_all_sources(self):
        """Schedule all active sources"""
        sources = self.db.get_all_sources(status="active")
        for source in sources:
            self.schedule_source(source)
        print(f"Scheduled {len(sources)} sources")
    
    def start(self):
        """Start the scheduler in a background thread"""
        if self.running:
            print("Scheduler already running")
            return
        
        self.running = True
        
        def run_scheduler():
            print("Scheduler started")
            while self.running:
                schedule.run_pending()
                time.sleep(1)
        
        self.thread = threading.Thread(target=run_scheduler, daemon=True)
        self.thread.start()
    
    def stop(self):
        """Stop the scheduler"""
        self.running = False
        if self.thread:
            self.thread.join(timeout=5)
        print("Scheduler stopped")
    
    def get_next_runs(self) -> Dict[str, Any]:
        """Get next scheduled run times"""
        next_runs = {}
        for source_id, job in self.jobs.items():
            next_runs[source_id] = str(job.next_run) if job.next_run else "Not scheduled"
        return next_runs
