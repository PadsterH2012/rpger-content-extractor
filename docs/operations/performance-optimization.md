---
title: Performance Optimization
description: Performance tuning and optimization strategies for RPGer Content Extractor
tags: [operations, performance, optimization, tuning]
last_updated: 2025-10-18
author: HL-Auggie Analysis System
---

# Performance Optimization

## Overview

This guide covers performance optimization strategies for the RPGer Content Extractor, including application tuning, database optimization, resource management, and scaling considerations. These optimizations help ensure optimal performance under various load conditions.

## Application Performance Optimization

### Flask Application Tuning

#### Production Server Configuration

```bash
# Use production WSGI server
pip install gunicorn

# Gunicorn configuration
gunicorn --workers 4 --worker-class sync --worker-connections 1000 \
         --max-requests 1000 --max-requests-jitter 100 \
         --timeout 30 --keep-alive 2 \
         --bind 0.0.0.0:5000 ui.app:app
```

#### Environment Variables for Performance

```bash
# Worker configuration
WORKERS=4                              # Number of worker processes
WORKER_CONNECTIONS=1000                # Connections per worker
WORKER_TIMEOUT=30                      # Worker timeout in seconds
KEEPALIVE=2                           # Keep-alive timeout

# Memory management
MAX_MEMORY_USAGE=2GB                  # Maximum memory per worker
MEMORY_CLEANUP_INTERVAL=300           # Cleanup interval in seconds
GC_THRESHOLD=700                      # Garbage collection threshold

# Request handling
REQUEST_TIMEOUT=60                    # General request timeout
UPLOAD_TIMEOUT=300                    # File upload timeout
MAX_CONTENT_LENGTH=200                # Maximum file size in MB
```

### Python Performance Optimization

#### Memory Management

```python
# Optimize garbage collection
import gc
import os

# Configure garbage collection
gc.set_threshold(700, 10, 10)

# Periodic cleanup
def cleanup_memory():
    """Perform memory cleanup."""
    gc.collect()
    
# Use context managers for large objects
class PDFProcessor:
    def __enter__(self):
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        # Cleanup resources
        self.cleanup()
```

#### Async Processing for I/O Operations

```python
import asyncio
import aiohttp
from concurrent.futures import ThreadPoolExecutor

class AsyncAIProvider:
    """Async AI provider for better concurrency."""
    
    def __init__(self):
        self.session = None
        self.executor = ThreadPoolExecutor(max_workers=4)
    
    async def analyze_content_async(self, content):
        """Async content analysis."""
        loop = asyncio.get_event_loop()
        return await loop.run_in_executor(
            self.executor, 
            self.analyze_content, 
            content
        )
```

## Database Performance Optimization

### MongoDB Optimization

#### Index Strategy

```javascript
// Create performance indexes
db.collection.createIndex({ "game_metadata.game_type": 1, "game_metadata.edition": 1 })
db.collection.createIndex({ "sections.category": 1 })
db.collection.createIndex({ "import_date": -1 })
db.collection.createIndex({ "sections.title": "text", "sections.content": "text" })

// Compound indexes for common queries
db.collection.createIndex({
    "game_metadata.game_type": 1,
    "game_metadata.edition": 1,
    "sections.category": 1
})
```

#### Connection Pool Optimization

```bash
# MongoDB connection settings
MONGODB_MAX_POOL_SIZE=50              # Increase pool size
MONGODB_MIN_POOL_SIZE=5               # Minimum connections
MONGODB_MAX_IDLE_TIME=60000           # Max idle time (ms)
MONGODB_CONNECT_TIMEOUT=10000         # Connection timeout
MONGODB_SERVER_SELECTION_TIMEOUT=5000 # Server selection timeout
```

#### Query Optimization

```python
# Use projection to limit returned fields
def get_document_summary(collection_name):
    """Get document summary with projection."""
    return collection.find(
        {},
        {
            "title": 1,
            "game_metadata.game_type": 1,
            "game_metadata.edition": 1,
            "summary.total_pages": 1
        }
    ).limit(100)

# Use aggregation for complex queries
def get_game_statistics():
    """Get game statistics using aggregation."""
    pipeline = [
        {
            "$group": {
                "_id": "$game_metadata.game_type",
                "total_documents": {"$sum": 1},
                "total_pages": {"$sum": "$summary.total_pages"}
            }
        },
        {"$sort": {"total_documents": -1}}
    ]
    return collection.aggregate(pipeline)
```

### ChromaDB Optimization

#### Collection Management

```python
# Optimize ChromaDB settings
CHROMA_BATCH_SIZE=1000                # Larger batch size
CHROMA_MAX_CONNECTIONS=20             # More connections
CHROMA_CONNECTION_POOL_SIZE=10        # Connection pooling
CHROMA_QUERY_TIMEOUT=30               # Query timeout

# Batch operations for better performance
def batch_add_documents(collection, documents, batch_size=1000):
    """Add documents in batches."""
    for i in range(0, len(documents), batch_size):
        batch = documents[i:i + batch_size]
        collection.add(
            documents=[doc['content'] for doc in batch],
            metadatas=[doc['metadata'] for doc in batch],
            ids=[doc['id'] for doc in batch]
        )
```

#### Query Optimization

```python
# Use metadata filtering before vector search
def optimized_search(collection, query, filters=None):
    """Optimized search with pre-filtering."""
    return collection.query(
        query_texts=[query],
        n_results=10,
        where=filters,  # Pre-filter with metadata
        include=["documents", "metadatas", "distances"]
    )

# Cache frequent queries
from functools import lru_cache

@lru_cache(maxsize=128)
def cached_similarity_search(query_hash, collection_name):
    """Cache similarity search results."""
    # Implementation with caching
    pass
```

## PDF Processing Optimization

### Memory-Efficient Processing

```python
# Stream processing for large PDFs
def process_large_pdf(file_path):
    """Process large PDF with memory optimization."""
    import fitz
    
    doc = fitz.open(file_path)
    try:
        for page_num in range(doc.page_count):
            page = doc[page_num]
            
            # Process page immediately
            text = page.get_text()
            process_page_text(text)
            
            # Clear page from memory
            page = None
            
            # Periodic garbage collection
            if page_num % 10 == 0:
                gc.collect()
    finally:
        doc.close()
```

### Parallel Processing

```python
from concurrent.futures import ProcessPoolExecutor
import multiprocessing

def parallel_pdf_processing(pdf_files):
    """Process multiple PDFs in parallel."""
    max_workers = min(multiprocessing.cpu_count(), len(pdf_files))
    
    with ProcessPoolExecutor(max_workers=max_workers) as executor:
        futures = [
            executor.submit(process_single_pdf, pdf_file)
            for pdf_file in pdf_files
        ]
        
        results = []
        for future in futures:
            try:
                result = future.result(timeout=300)  # 5 minute timeout
                results.append(result)
            except Exception as e:
                print(f"PDF processing failed: {e}")
                
        return results
```

## Caching Strategies

### Redis Caching

```bash
# Redis configuration
CACHE_TYPE=redis
CACHE_REDIS_URL=redis://redis:6379
CACHE_DEFAULT_TIMEOUT=300
CACHE_KEY_PREFIX=rpger_
```

```python
import redis
from functools import wraps

# Redis client
redis_client = redis.Redis.from_url(os.getenv('CACHE_REDIS_URL'))

def cache_result(timeout=300):
    """Cache function results in Redis."""
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            # Create cache key
            cache_key = f"rpger_{func.__name__}_{hash(str(args) + str(kwargs))}"
            
            # Try to get from cache
            cached_result = redis_client.get(cache_key)
            if cached_result:
                return json.loads(cached_result)
            
            # Execute function and cache result
            result = func(*args, **kwargs)
            redis_client.setex(
                cache_key, 
                timeout, 
                json.dumps(result, default=str)
            )
            
            return result
        return wrapper
    return decorator

# Usage
@cache_result(timeout=600)
def get_game_detection_result(content_hash):
    """Cache AI game detection results."""
    # Expensive AI operation
    pass
```

### Application-Level Caching

```python
from functools import lru_cache
import time

class TimedLRUCache:
    """LRU cache with time-based expiration."""
    
    def __init__(self, maxsize=128, ttl=300):
        self.cache = {}
        self.maxsize = maxsize
        self.ttl = ttl
    
    def get(self, key):
        if key in self.cache:
            value, timestamp = self.cache[key]
            if time.time() - timestamp < self.ttl:
                return value
            else:
                del self.cache[key]
        return None
    
    def set(self, key, value):
        if len(self.cache) >= self.maxsize:
            # Remove oldest entry
            oldest_key = min(self.cache.keys(), 
                           key=lambda k: self.cache[k][1])
            del self.cache[oldest_key]
        
        self.cache[key] = (value, time.time())

# Global cache instance
app_cache = TimedLRUCache(maxsize=256, ttl=600)
```

## Resource Monitoring and Optimization

### Memory Monitoring

```python
import psutil
import os

def monitor_memory_usage():
    """Monitor application memory usage."""
    process = psutil.Process(os.getpid())
    memory_info = process.memory_info()
    
    return {
        'rss': memory_info.rss,  # Resident Set Size
        'vms': memory_info.vms,  # Virtual Memory Size
        'percent': process.memory_percent(),
        'available': psutil.virtual_memory().available
    }

def memory_cleanup_if_needed(threshold=80):
    """Cleanup memory if usage exceeds threshold."""
    memory_percent = psutil.virtual_memory().percent
    
    if memory_percent > threshold:
        gc.collect()
        
        # Clear application caches
        if hasattr(app_cache, 'clear'):
            app_cache.clear()
        
        print(f"Memory cleanup performed. Usage: {memory_percent}%")
```

### CPU Optimization

```python
import threading
import queue
from concurrent.futures import ThreadPoolExecutor

class WorkerPool:
    """Optimized worker pool for CPU-intensive tasks."""
    
    def __init__(self, max_workers=None):
        self.max_workers = max_workers or multiprocessing.cpu_count()
        self.executor = ThreadPoolExecutor(max_workers=self.max_workers)
        self.task_queue = queue.Queue()
    
    def submit_task(self, func, *args, **kwargs):
        """Submit task to worker pool."""
        future = self.executor.submit(func, *args, **kwargs)
        return future
    
    def shutdown(self):
        """Shutdown worker pool."""
        self.executor.shutdown(wait=True)
```

## Network and I/O Optimization

### HTTP Client Optimization

```python
import httpx
import asyncio

class OptimizedHTTPClient:
    """Optimized HTTP client for AI API calls."""
    
    def __init__(self):
        self.client = httpx.AsyncClient(
            timeout=httpx.Timeout(30.0),
            limits=httpx.Limits(
                max_keepalive_connections=20,
                max_connections=100
            )
        )
    
    async def make_request(self, url, data):
        """Make optimized HTTP request."""
        try:
            response = await self.client.post(url, json=data)
            response.raise_for_status()
            return response.json()
        except httpx.TimeoutException:
            # Handle timeout with retry logic
            await asyncio.sleep(1)
            return await self.make_request(url, data)
```

### File I/O Optimization

```python
import aiofiles
import asyncio

async def async_file_operations(file_paths):
    """Async file operations for better I/O performance."""
    async def read_file(file_path):
        async with aiofiles.open(file_path, 'rb') as f:
            return await f.read()
    
    # Process files concurrently
    tasks = [read_file(path) for path in file_paths]
    results = await asyncio.gather(*tasks)
    
    return results
```

## Container Performance Optimization

### Docker Configuration

```yaml
# docker-compose.yml optimizations
services:
  app:
    deploy:
      resources:
        limits:
          cpus: '2.0'
          memory: 2G
        reservations:
          cpus: '1.0'
          memory: 1G
    environment:
      - PYTHONOPTIMIZE=1
      - PYTHONDONTWRITEBYTECODE=1
    volumes:
      - type: tmpfs
        target: /tmp
        tmpfs:
          size: 100M
```

### Health Check Optimization

```yaml
healthcheck:
  test: ["CMD", "curl", "-f", "http://localhost:5000/health"]
  interval: 30s
  timeout: 10s
  retries: 3
  start_period: 40s
```

## Performance Monitoring

### Metrics Collection

```python
import time
from collections import defaultdict

class PerformanceMetrics:
    """Collect and track performance metrics."""
    
    def __init__(self):
        self.metrics = defaultdict(list)
        self.counters = defaultdict(int)
    
    def time_function(self, func_name):
        """Decorator to time function execution."""
        def decorator(func):
            @wraps(func)
            def wrapper(*args, **kwargs):
                start_time = time.time()
                try:
                    result = func(*args, **kwargs)
                    self.counters[f"{func_name}_success"] += 1
                    return result
                except Exception as e:
                    self.counters[f"{func_name}_error"] += 1
                    raise
                finally:
                    duration = time.time() - start_time
                    self.metrics[func_name].append(duration)
            return wrapper
        return decorator
    
    def get_stats(self, func_name):
        """Get performance statistics."""
        durations = self.metrics[func_name]
        if not durations:
            return None
        
        return {
            'count': len(durations),
            'avg': sum(durations) / len(durations),
            'min': min(durations),
            'max': max(durations),
            'success_rate': self.counters[f"{func_name}_success"] / 
                          (self.counters[f"{func_name}_success"] + 
                           self.counters[f"{func_name}_error"]) * 100
        }

# Global metrics instance
metrics = PerformanceMetrics()
```

## Performance Testing

### Load Testing Script

```python
import asyncio
import aiohttp
import time

async def load_test(url, concurrent_requests=10, total_requests=100):
    """Simple load testing for API endpoints."""
    
    async def make_request(session, request_id):
        try:
            start_time = time.time()
            async with session.get(f"{url}/health") as response:
                duration = time.time() - start_time
                return {
                    'request_id': request_id,
                    'status': response.status,
                    'duration': duration
                }
        except Exception as e:
            return {
                'request_id': request_id,
                'error': str(e),
                'duration': time.time() - start_time
            }
    
    async with aiohttp.ClientSession() as session:
        semaphore = asyncio.Semaphore(concurrent_requests)
        
        async def bounded_request(request_id):
            async with semaphore:
                return await make_request(session, request_id)
        
        tasks = [bounded_request(i) for i in range(total_requests)]
        results = await asyncio.gather(*tasks)
    
    # Analyze results
    successful = [r for r in results if 'error' not in r and r['status'] == 200]
    failed = [r for r in results if 'error' in r or r['status'] != 200]
    
    if successful:
        avg_duration = sum(r['duration'] for r in successful) / len(successful)
        max_duration = max(r['duration'] for r in successful)
        min_duration = min(r['duration'] for r in successful)
    else:
        avg_duration = max_duration = min_duration = 0
    
    print(f"Load Test Results:")
    print(f"  Total Requests: {total_requests}")
    print(f"  Successful: {len(successful)}")
    print(f"  Failed: {len(failed)}")
    print(f"  Success Rate: {len(successful)/total_requests*100:.1f}%")
    print(f"  Avg Duration: {avg_duration:.3f}s")
    print(f"  Min Duration: {min_duration:.3f}s")
    print(f"  Max Duration: {max_duration:.3f}s")

# Run load test
if __name__ == "__main__":
    asyncio.run(load_test("http://localhost:5000"))
```

This performance optimization guide provides comprehensive strategies for improving the performance of the RPGer Content Extractor across all system components.
