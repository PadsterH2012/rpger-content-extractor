---
title: Health Monitoring
description: System health checks and monitoring for RPGer Content Extractor
tags: [operations, monitoring, health-checks, observability]
last_updated: 2025-10-18
author: HL-Auggie Analysis System
---

# Health Monitoring

## Overview

This guide covers comprehensive health monitoring for the RPGer Content Extractor, including built-in health checks, external monitoring integration, and alerting strategies. Proper monitoring ensures system reliability and early detection of issues.

## Built-in Health Checks

### Application Health Endpoint

The system provides a comprehensive health check endpoint at `/health`:

```bash
# Basic health check
curl http://localhost:5000/health

# Expected response
{
  "status": "healthy",
  "timestamp": "2025-10-18T10:30:00.000Z",
  "version": "v1.0.44",
  "environment": "production",
  "checks": {
    "database": "healthy",
    "ai_providers": "healthy",
    "disk_space": "healthy",
    "memory": "healthy"
  }
}
```

### Detailed Status Endpoint

For comprehensive system status, use `/api/status`:

```bash
# Detailed system status
curl http://localhost:5000/api/status

# Response includes
{
  "chroma_status": {
    "connected": true,
    "collections": 5,
    "response_time": 45
  },
  "mongodb_status": {
    "connected": true,
    "collections": 3,
    "response_time": 23
  },
  "ai_providers": {
    "available": ["anthropic", "openrouter"],
    "configured": ["anthropic"],
    "active": "anthropic"
  },
  "active_sessions": 2,
  "completed_extractions": 15,
  "token_tracking": {
    "total_sessions": 10,
    "total_cost": 2.45
  },
  "system_resources": {
    "memory_usage": "45%",
    "disk_usage": "23%",
    "cpu_usage": "12%"
  }
}
```

## Component Health Monitoring

### Database Health Checks

#### MongoDB Health Monitoring

```bash
# MongoDB connection test
mongosh mongodb://localhost:27017/rpger --eval "db.adminCommand('ping')"

# MongoDB status check
mongosh mongodb://localhost:27017/rpger --eval "db.runCommand({serverStatus: 1})"

# Check replica set status (if using replica sets)
mongosh mongodb://localhost:27017/rpger --eval "rs.status()"
```

**MongoDB Health Metrics**:
- Connection status
- Response time
- Active connections
- Database size
- Index usage
- Replication lag (if applicable)

#### ChromaDB Health Monitoring

```bash
# ChromaDB heartbeat
curl http://localhost:8000/api/v1/heartbeat

# ChromaDB version and status
curl http://localhost:8000/api/v1/version

# Collection health
curl http://localhost:8000/api/v1/collections
```

**ChromaDB Health Metrics**:
- API availability
- Response time
- Collection count
- Memory usage
- Query performance

### AI Provider Health Checks

#### Provider Availability Testing

```python
# AI provider health check script
import requests
import os
from datetime import datetime

def check_anthropic_health():
    """Check Anthropic API health."""
    try:
        headers = {
            'x-api-key': os.getenv('ANTHROPIC_API_KEY'),
            'content-type': 'application/json'
        }
        
        # Simple API test
        response = requests.post(
            'https://api.anthropic.com/v1/messages',
            headers=headers,
            json={
                'model': 'claude-3-sonnet-20240229',
                'max_tokens': 10,
                'messages': [{'role': 'user', 'content': 'test'}]
            },
            timeout=10
        )
        
        return {
            'status': 'healthy' if response.status_code == 200 else 'unhealthy',
            'response_time': response.elapsed.total_seconds(),
            'status_code': response.status_code
        }
    except Exception as e:
        return {
            'status': 'unhealthy',
            'error': str(e)
        }

def check_openai_health():
    """Check OpenAI API health."""
    try:
        headers = {
            'Authorization': f'Bearer {os.getenv("OPENAI_API_KEY")}',
            'Content-Type': 'application/json'
        }
        
        response = requests.post(
            'https://api.openai.com/v1/chat/completions',
            headers=headers,
            json={
                'model': 'gpt-3.5-turbo',
                'messages': [{'role': 'user', 'content': 'test'}],
                'max_tokens': 5
            },
            timeout=10
        )
        
        return {
            'status': 'healthy' if response.status_code == 200 else 'unhealthy',
            'response_time': response.elapsed.total_seconds(),
            'status_code': response.status_code
        }
    except Exception as e:
        return {
            'status': 'unhealthy',
            'error': str(e)
        }
```

### System Resource Monitoring

#### Memory Monitoring

```python
import psutil
import os

def get_memory_usage():
    """Get system memory usage."""
    memory = psutil.virtual_memory()
    process = psutil.Process(os.getpid())
    
    return {
        'system_memory': {
            'total': memory.total,
            'available': memory.available,
            'percent': memory.percent,
            'used': memory.used
        },
        'process_memory': {
            'rss': process.memory_info().rss,
            'vms': process.memory_info().vms,
            'percent': process.memory_percent()
        }
    }
```

#### Disk Space Monitoring

```python
def get_disk_usage():
    """Get disk usage for important paths."""
    paths = [
        '/app/uploads',
        '/app/extracted',
        '/app/logs',
        '/data/db',  # MongoDB data
        '/chroma/data'  # ChromaDB data
    ]
    
    disk_usage = {}
    for path in paths:
        if os.path.exists(path):
            usage = psutil.disk_usage(path)
            disk_usage[path] = {
                'total': usage.total,
                'used': usage.used,
                'free': usage.free,
                'percent': (usage.used / usage.total) * 100
            }
    
    return disk_usage
```

## Docker Health Checks

### Container Health Configuration

```yaml
# docker-compose.yml health checks
services:
  app:
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:5000/health"]
      interval: 30s
      timeout: 10s
      retries: 3
      start_period: 40s
  
  mongodb:
    healthcheck:
      test: ["CMD", "mongosh", "--eval", "db.adminCommand('ping')"]
      interval: 30s
      timeout: 10s
      retries: 3
      start_period: 40s
  
  chromadb:
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:8000/api/v1/heartbeat"]
      interval: 30s
      timeout: 10s
      retries: 3
      start_period: 40s
```

### Health Check Monitoring Script

```bash
#!/bin/bash
# health-check.sh

echo "=== RPGer Content Extractor Health Check ==="
echo "Timestamp: $(date)"
echo

# Check container health
echo "Container Health:"
docker ps --format "table {{.Names}}\t{{.Status}}\t{{.Ports}}" | grep rpger

echo
echo "Application Health:"
if curl -s -f http://localhost:5000/health > /dev/null; then
    echo "✅ Application: Healthy"
    curl -s http://localhost:5000/health | jq .
else
    echo "❌ Application: Unhealthy"
fi

echo
echo "MongoDB Health:"
if docker exec mongodb mongosh --quiet --eval "db.adminCommand('ping')" > /dev/null 2>&1; then
    echo "✅ MongoDB: Healthy"
else
    echo "❌ MongoDB: Unhealthy"
fi

echo
echo "ChromaDB Health:"
if curl -s -f http://localhost:8000/api/v1/heartbeat > /dev/null; then
    echo "✅ ChromaDB: Healthy"
else
    echo "❌ ChromaDB: Unhealthy"
fi

echo
echo "System Resources:"
echo "Memory Usage: $(free | grep Mem | awk '{printf "%.1f%%", $3/$2 * 100.0}')"
echo "Disk Usage: $(df -h / | awk 'NR==2{printf "%s", $5}')"
echo "Load Average: $(uptime | awk -F'load average:' '{print $2}')"
```

## External Monitoring Integration

### Prometheus Metrics

#### Metrics Endpoint Configuration

```python
# metrics.py
from prometheus_client import Counter, Histogram, Gauge, generate_latest
from flask import Response

# Define metrics
REQUEST_COUNT = Counter('rpger_requests_total', 'Total requests', ['method', 'endpoint'])
REQUEST_DURATION = Histogram('rpger_request_duration_seconds', 'Request duration')
ACTIVE_SESSIONS = Gauge('rpger_active_sessions', 'Active processing sessions')
DATABASE_CONNECTIONS = Gauge('rpger_database_connections', 'Database connections', ['database'])

@app.route('/metrics')
def metrics():
    """Prometheus metrics endpoint."""
    return Response(generate_latest(), mimetype='text/plain')
```

#### Prometheus Configuration

```yaml
# prometheus.yml
global:
  scrape_interval: 15s

scrape_configs:
  - job_name: 'rpger-content-extractor'
    static_configs:
      - targets: ['localhost:5000']
    metrics_path: '/metrics'
    scrape_interval: 30s
```

### Grafana Dashboard

#### Dashboard Configuration

```json
{
  "dashboard": {
    "title": "RPGer Content Extractor",
    "panels": [
      {
        "title": "Request Rate",
        "type": "graph",
        "targets": [
          {
            "expr": "rate(rpger_requests_total[5m])",
            "legendFormat": "{{method}} {{endpoint}}"
          }
        ]
      },
      {
        "title": "Response Time",
        "type": "graph",
        "targets": [
          {
            "expr": "histogram_quantile(0.95, rate(rpger_request_duration_seconds_bucket[5m]))",
            "legendFormat": "95th percentile"
          }
        ]
      },
      {
        "title": "Active Sessions",
        "type": "singlestat",
        "targets": [
          {
            "expr": "rpger_active_sessions",
            "legendFormat": "Sessions"
          }
        ]
      },
      {
        "title": "Database Health",
        "type": "table",
        "targets": [
          {
            "expr": "rpger_database_connections",
            "legendFormat": "{{database}}"
          }
        ]
      }
    ]
  }
}
```

### Uptime Monitoring

#### External Uptime Checks

```bash
# uptime-check.sh
#!/bin/bash

ENDPOINTS=(
    "http://localhost:5000/health"
    "http://localhost:5000/api/version"
    "http://localhost:8000/api/v1/heartbeat"
)

for endpoint in "${ENDPOINTS[@]}"; do
    if curl -s -f "$endpoint" > /dev/null; then
        echo "✅ $endpoint: UP"
    else
        echo "❌ $endpoint: DOWN"
        # Send alert (email, Slack, etc.)
        send_alert "Endpoint $endpoint is down"
    fi
done
```

## Alerting and Notifications

### Alert Configuration

#### Prometheus Alerting Rules

```yaml
# alerts.yml
groups:
  - name: rpger-alerts
    rules:
      - alert: ApplicationDown
        expr: up{job="rpger-content-extractor"} == 0
        for: 1m
        labels:
          severity: critical
        annotations:
          summary: "RPGer Content Extractor is down"
          description: "Application has been down for more than 1 minute"
      
      - alert: HighMemoryUsage
        expr: (process_resident_memory_bytes / node_memory_MemTotal_bytes) * 100 > 80
        for: 5m
        labels:
          severity: warning
        annotations:
          summary: "High memory usage detected"
          description: "Memory usage is above 80% for 5 minutes"
      
      - alert: DatabaseConnectionFailed
        expr: rpger_database_connections == 0
        for: 2m
        labels:
          severity: critical
        annotations:
          summary: "Database connection failed"
          description: "No active database connections detected"
```

#### Slack Notifications

```python
# notifications.py
import requests
import json

def send_slack_alert(webhook_url, message, severity="info"):
    """Send alert to Slack."""
    colors = {
        "info": "#36a64f",
        "warning": "#ff9900",
        "critical": "#ff0000"
    }
    
    payload = {
        "attachments": [
            {
                "color": colors.get(severity, "#36a64f"),
                "title": "RPGer Content Extractor Alert",
                "text": message,
                "footer": "Health Monitoring System",
                "ts": int(time.time())
            }
        ]
    }
    
    response = requests.post(webhook_url, json=payload)
    return response.status_code == 200
```

#### Email Notifications

```python
# email_alerts.py
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

def send_email_alert(smtp_server, smtp_port, username, password, 
                    to_email, subject, message):
    """Send email alert."""
    msg = MIMEMultipart()
    msg['From'] = username
    msg['To'] = to_email
    msg['Subject'] = subject
    
    msg.attach(MIMEText(message, 'plain'))
    
    try:
        server = smtplib.SMTP(smtp_server, smtp_port)
        server.starttls()
        server.login(username, password)
        text = msg.as_string()
        server.sendmail(username, to_email, text)
        server.quit()
        return True
    except Exception as e:
        print(f"Failed to send email: {e}")
        return False
```

## Log Monitoring

### Centralized Logging

#### ELK Stack Integration

```yaml
# docker-compose.logging.yml
version: '3.8'

services:
  elasticsearch:
    image: docker.elastic.co/elasticsearch/elasticsearch:8.10.0
    environment:
      - discovery.type=single-node
      - xpack.security.enabled=false
    ports:
      - "9200:9200"
  
  logstash:
    image: docker.elastic.co/logstash/logstash:8.10.0
    volumes:
      - ./logstash.conf:/usr/share/logstash/pipeline/logstash.conf
    depends_on:
      - elasticsearch
  
  kibana:
    image: docker.elastic.co/kibana/kibana:8.10.0
    ports:
      - "5601:5601"
    depends_on:
      - elasticsearch
  
  app:
    logging:
      driver: "json-file"
      options:
        max-size: "10m"
        max-file: "3"
```

#### Log Analysis Queries

```bash
# Search for errors in logs
grep -i error /app/logs/app.log | tail -20

# Monitor API response times
grep "response_time" /app/logs/app.log | awk '{print $NF}' | sort -n

# Check for failed AI requests
grep "AI_ERROR" /app/logs/app.log | wc -l
```

### Log-based Alerts

```python
# log_monitor.py
import re
import time
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

class LogMonitor(FileSystemEventHandler):
    """Monitor log files for specific patterns."""
    
    def __init__(self, alert_patterns):
        self.alert_patterns = alert_patterns
    
    def on_modified(self, event):
        if event.src_path.endswith('.log'):
            self.check_log_file(event.src_path)
    
    def check_log_file(self, file_path):
        """Check log file for alert patterns."""
        try:
            with open(file_path, 'r') as f:
                # Read only new lines
                f.seek(0, 2)  # Go to end of file
                while True:
                    line = f.readline()
                    if not line:
                        break
                    
                    for pattern, severity in self.alert_patterns.items():
                        if re.search(pattern, line, re.IGNORECASE):
                            self.send_alert(line.strip(), severity)
        except Exception as e:
            print(f"Error reading log file: {e}")
    
    def send_alert(self, message, severity):
        """Send alert based on log pattern match."""
        print(f"ALERT [{severity}]: {message}")
        # Implement actual alerting logic here

# Usage
alert_patterns = {
    r'ERROR.*database.*connection': 'critical',
    r'WARNING.*memory.*usage': 'warning',
    r'CRITICAL.*': 'critical'
}

monitor = LogMonitor(alert_patterns)
observer = Observer()
observer.schedule(monitor, '/app/logs', recursive=True)
observer.start()
```

## Performance Monitoring

### Response Time Monitoring

```python
# performance_monitor.py
import time
import statistics
from collections import deque

class PerformanceMonitor:
    """Monitor application performance metrics."""
    
    def __init__(self, window_size=100):
        self.response_times = deque(maxlen=window_size)
        self.error_count = 0
        self.request_count = 0
    
    def record_request(self, response_time, success=True):
        """Record request metrics."""
        self.response_times.append(response_time)
        self.request_count += 1
        if not success:
            self.error_count += 1
    
    def get_metrics(self):
        """Get current performance metrics."""
        if not self.response_times:
            return {}
        
        return {
            'avg_response_time': statistics.mean(self.response_times),
            'median_response_time': statistics.median(self.response_times),
            'p95_response_time': statistics.quantiles(self.response_times, n=20)[18],
            'error_rate': (self.error_count / self.request_count) * 100,
            'total_requests': self.request_count
        }
```

### Resource Usage Monitoring

```bash
#!/bin/bash
# resource-monitor.sh

while true; do
    echo "=== Resource Usage $(date) ==="
    
    # CPU usage
    echo "CPU Usage:"
    top -bn1 | grep "Cpu(s)" | awk '{print $2}' | cut -d'%' -f1
    
    # Memory usage
    echo "Memory Usage:"
    free -h | grep Mem | awk '{printf "Used: %s/%s (%.1f%%)\n", $3, $2, $3/$2*100}'
    
    # Disk usage
    echo "Disk Usage:"
    df -h / | awk 'NR==2{printf "Used: %s/%s (%s)\n", $3, $2, $5}'
    
    # Network connections
    echo "Network Connections:"
    netstat -an | grep :5000 | wc -l
    
    echo "=========================="
    sleep 60
done
```

This comprehensive health monitoring guide provides all the tools and strategies needed to maintain a healthy and reliable RPGer Content Extractor deployment.
