---
title: Environment Variables
description: Quick reference guide for environment variables in RPGer Content Extractor
tags: [reference, environment-variables, configuration, quick-reference]
last_updated: 2025-10-18
author: HL-Auggie Analysis System
---

# Environment Variables Quick Reference

## Overview

This document provides a quick reference for all environment variables used in the RPGer Content Extractor. Variables are organized alphabetically within categories for easy lookup.

## Essential Variables

### Required for Startup
```bash
FLASK_SECRET_KEY=your-secret-key-here          # Required for security
AI_PROVIDER=anthropic                          # Required: anthropic|openai|openrouter|mock
ANTHROPIC_API_KEY=sk-ant-your-key-here        # Required if using Anthropic
MONGODB_HOST=localhost                         # Required for database
CHROMA_HOST=localhost                          # Required for vector database
```

### Commonly Modified
```bash
FLASK_ENV=production                           # production|development|testing
MAX_CONTENT_LENGTH=200                         # Maximum file size in MB
PORT=5000                                      # Server port
LOG_LEVEL=INFO                                 # DEBUG|INFO|WARNING|ERROR|CRITICAL
```

## Application Settings

### Core Flask Configuration
```bash
FLASK_DEBUG=false                              # Enable debug mode (boolean)
FLASK_ENV=production                           # Environment mode
FLASK_SECRET_KEY=your-secret-key               # Session encryption key (required)
FLASK_TESTING=false                            # Testing mode (boolean)
```

### Server Configuration
```bash
HOST=0.0.0.0                                  # Bind address
KEEPALIVE=2                                    # Keep-alive timeout (seconds)
PORT=5000                                      # Server port
REQUEST_TIMEOUT=60                             # Request timeout (seconds)
UPLOAD_TIMEOUT=300                             # Upload timeout (seconds)
WORKER_CONNECTIONS=1000                        # Connections per worker
WORKERS=1                                      # Number of worker processes
WORKER_TIMEOUT=30                              # Worker timeout (seconds)
```

## AI Provider Settings

### Anthropic Claude
```bash
ANTHROPIC_API_KEY=sk-ant-your-key              # API key (required)
ANTHROPIC_MAX_TOKENS=4000                      # Max tokens per request
ANTHROPIC_MODEL=claude-3-sonnet-20240229       # Model name
ANTHROPIC_RETRY_ATTEMPTS=3                     # Retry attempts
ANTHROPIC_RETRY_DELAY=5                        # Retry delay (seconds)
ANTHROPIC_TEMPERATURE=0.3                      # Response randomness (0.0-1.0)
ANTHROPIC_TIMEOUT=60                           # Request timeout (seconds)
```

### OpenAI
```bash
OPENAI_API_KEY=sk-your-key                     # API key (required)
OPENAI_MAX_TOKENS=4000                         # Max tokens per request
OPENAI_MODEL=gpt-4                             # Model name
OPENAI_ORG_ID=your-org-id                      # Organization ID (optional)
OPENAI_TEMPERATURE=0.3                         # Response randomness (0.0-2.0)
OPENAI_TIMEOUT=60                              # Request timeout (seconds)
```

### OpenRouter
```bash
OPENROUTER_API_KEY=sk-or-your-key              # API key (required)
OPENROUTER_APP_NAME=RPGer Content Extractor    # App name for tracking
OPENROUTER_MAX_TOKENS=4000                     # Max tokens per request
OPENROUTER_MODEL=anthropic/claude-3-sonnet     # Model name
OPENROUTER_SITE_URL=https://yourdomain.com     # Site URL for tracking
OPENROUTER_TEMPERATURE=0.3                     # Response randomness
OPENROUTER_TIMEOUT=60                          # Request timeout (seconds)
```

### AI Provider Selection
```bash
AI_FALLBACK_PROVIDER=openai                    # Fallback provider
AI_MODEL=claude-3-sonnet                       # Override default model
AI_PROVIDER=anthropic                          # Primary provider (required)
AI_RETRY_ATTEMPTS=3                            # Global retry attempts
AI_RETRY_DELAY=5                               # Global retry delay (seconds)
AI_TEMPERATURE=0.3                             # Global temperature override
```

## Database Configuration

### MongoDB
```bash
MONGODB_AUTH_SOURCE=admin                      # Authentication database
MONGODB_CONNECTION_STRING=mongodb://...        # Full connection string
MONGODB_CONNECT_TIMEOUT=10000                  # Connection timeout (ms)
MONGODB_DATABASE=rpger                         # Database name
MONGODB_HOST=localhost                         # Host address (required)
MONGODB_MAX_IDLE_TIME=30000                    # Max idle time (ms)
MONGODB_MAX_POOL_SIZE=10                       # Maximum connections
MONGODB_MIN_POOL_SIZE=1                        # Minimum connections
MONGODB_PASSWORD=secure_password               # Authentication password
MONGODB_PORT=27017                             # Port number
MONGODB_SERVER_SELECTION_TIMEOUT=5000          # Server selection timeout (ms)
MONGODB_USERNAME=rpger_user                    # Authentication username
```

### ChromaDB
```bash
CHROMA_BASE_URL=http://localhost:8000/api/v1   # Full base URL
CHROMA_BATCH_SIZE=100                          # Batch operation size
CHROMA_DATABASE=default_database               # Database name
CHROMA_HOST=localhost                          # Host address (required)
CHROMA_MAX_CONNECTIONS=20                      # Max connections
CHROMA_MAX_RETRIES=3                           # Maximum retries
CHROMA_PORT=8000                               # Port number
CHROMA_TENANT=default_tenant                   # Tenant name
CHROMA_TIMEOUT=30                              # Request timeout (seconds)
```

## File and Storage Settings

### Upload Configuration
```bash
MAX_CONTENT_LENGTH=200                         # Max file size (MB)
UPLOAD_ALLOWED_EXTENSIONS=pdf                  # Allowed extensions
UPLOAD_FOLDER=./uploads                        # Upload directory
UPLOAD_TEMP_CLEANUP=true                       # Clean temp files (boolean)
UPLOAD_TEMP_RETENTION=3600                     # Temp retention (seconds)
UPLOAD_TIMEOUT=300                             # Upload timeout (seconds)
```

### Output Configuration
```bash
OUTPUT_COMPRESSION=true                        # Compress outputs (boolean)
OUTPUT_FOLDER=./extracted                      # Output directory
OUTPUT_FORMATS=json,chromadb,text              # Available formats
OUTPUT_RETENTION_DAYS=30                       # Retention period (days)
```

## Security Settings

### CORS Configuration
```bash
CORS_CREDENTIALS=false                         # Allow credentials (boolean)
CORS_HEADERS=Content-Type,Authorization        # Allowed headers
CORS_METHODS=GET,POST,PUT,DELETE,OPTIONS       # Allowed methods
CORS_ORIGINS=https://yourdomain.com            # Allowed origins
```

### Rate Limiting
```bash
RATE_LIMIT_DEFAULT=100 per hour                # Default rate limit
RATE_LIMIT_ENABLED=true                        # Enable rate limiting (boolean)
RATE_LIMIT_STORAGE_URL=redis://redis:6379      # Storage backend
RATE_LIMIT_UPLOAD=10 per minute                # Upload rate limit
```

### Security Headers
```bash
CSP_POLICY=default-src 'self'                  # Content Security Policy
HSTS_MAX_AGE=31536000                          # HSTS max age (seconds)
SECURITY_HEADERS_ENABLED=true                  # Enable headers (boolean)
X_FRAME_OPTIONS=DENY                           # X-Frame-Options header
```

### Authentication (Optional)
```bash
API_KEY_ENABLED=false                          # Enable API key auth (boolean)
API_KEY_HEADER=X-API-Key                       # API key header name
JWT_ALGORITHM=HS256                            # JWT algorithm
JWT_EXPIRATION=3600                            # JWT expiration (seconds)
JWT_REFRESH_EXPIRATION=86400                   # Refresh expiration (seconds)
JWT_SECRET_KEY=your-jwt-secret                 # JWT secret key
```

## Logging Configuration

### Basic Logging
```bash
LOG_BACKUP_COUNT=5                             # Number of backup files
LOG_FILE=./logs/app.log                        # Log file path
LOG_FORMAT=json                                # Log format (json|text)
LOG_LEVEL=INFO                                 # Global log level
LOG_MAX_SIZE=10MB                              # Max log file size
LOG_ROTATION=daily                             # Rotation schedule
```

### Component Logging
```bash
LOG_LEVEL_AI=INFO                              # AI provider log level
LOG_LEVEL_DB=INFO                              # Database log level
LOG_LEVEL_PDF=INFO                             # PDF processing log level
LOG_LEVEL_WEB=INFO                             # Web server log level
```

## Performance Settings

### Application Performance
```bash
GC_THRESHOLD=700                               # Garbage collection threshold
MAX_MEMORY_USAGE=2GB                           # Maximum memory usage
MEMORY_CLEANUP_INTERVAL=300                    # Cleanup interval (seconds)
WORKERS=4                                      # Number of workers
WORKER_CONNECTIONS=1000                        # Connections per worker
WORKER_TIMEOUT=30                              # Worker timeout (seconds)
```

### Caching
```bash
CACHE_DEFAULT_TIMEOUT=300                      # Default timeout (seconds)
CACHE_KEY_PREFIX=rpger_                        # Cache key prefix
CACHE_REDIS_URL=redis://redis:6379             # Redis cache URL
CACHE_TYPE=memory                              # Cache type (memory|redis|filesystem)
```

## Monitoring Settings

### Health Checks
```bash
HEALTH_CHECK_CHROMADB=true                     # Check ChromaDB (boolean)
HEALTH_CHECK_DISK_SPACE=true                   # Check disk space (boolean)
HEALTH_CHECK_ENABLED=true                      # Enable health checks (boolean)
HEALTH_CHECK_INTERVAL=30                       # Check interval (seconds)
HEALTH_CHECK_MONGODB=true                      # Check MongoDB (boolean)
HEALTH_CHECK_RETRIES=3                         # Number of retries
HEALTH_CHECK_TIMEOUT=10                        # Check timeout (seconds)
```

### Metrics and Tracing
```bash
METRICS_ENABLED=false                          # Enable metrics (boolean)
METRICS_NAMESPACE=rpger                        # Metrics namespace
METRICS_PATH=/metrics                          # Metrics endpoint
METRICS_PORT=9090                              # Metrics port
TRACING_ENABLED=false                          # Enable tracing (boolean)
TRACING_JAEGER_ENDPOINT=http://jaeger:14268    # Jaeger endpoint
TRACING_SAMPLE_RATE=0.1                        # Sampling rate (0.0-1.0)
TRACING_SERVICE_NAME=rpger-content-extractor   # Service name
```

## PDF Processing Settings

### Processing Options
```bash
AGGRESSIVE_CLEANUP=false                       # Aggressive text cleanup (boolean)
ENABLE_LAYOUT_ANALYSIS=true                    # Enable layout analysis (boolean)
ENABLE_TEXT_ENHANCEMENT=true                   # Enable text enhancement (boolean)
LAYOUT_TOLERANCE=0.5                           # Layout detection tolerance
MULTI_COLUMN_DETECTION=true                    # Multi-column detection (boolean)
PDF_PROCESSING_MODE=standard                   # Processing mode (standard|advanced|fast)
```

### OCR Configuration
```bash
OCR_CONFIDENCE_THRESHOLD=0.8                   # Minimum confidence
OCR_DPI=300                                    # OCR resolution
OCR_ENABLED=false                              # Enable OCR (boolean)
OCR_LANGUAGE=eng                               # OCR language
```

## Environment-Specific Presets

### Development Environment
```bash
# Quick development setup
FLASK_ENV=development
FLASK_DEBUG=true
LOG_LEVEL=DEBUG
AI_PROVIDER=mock
MONGODB_DATABASE=rpger_dev
CORS_ORIGINS=*
RATE_LIMIT_ENABLED=false
```

### Production Environment
```bash
# Production setup
FLASK_ENV=production
FLASK_DEBUG=false
LOG_LEVEL=INFO
AI_PROVIDER=anthropic
CORS_ORIGINS=https://yourdomain.com
RATE_LIMIT_ENABLED=true
SECURITY_HEADERS_ENABLED=true
METRICS_ENABLED=true
```

### Docker Environment
```bash
# Docker-specific settings
HOST=0.0.0.0
MONGODB_HOST=mongodb
CHROMA_HOST=chromadb
LOG_FILE=/app/logs/app.log
UPLOAD_FOLDER=/app/uploads
OUTPUT_FOLDER=/app/extracted
```

### Testing Environment
```bash
# Testing setup
FLASK_ENV=testing
FLASK_TESTING=true
AI_PROVIDER=mock
MONGODB_DATABASE=rpger_test
RATE_LIMIT_ENABLED=false
METRICS_ENABLED=false
LOG_LEVEL=WARNING
```

## Variable Types and Formats

### Boolean Values
Use `true` or `false` (lowercase):
```bash
FLASK_DEBUG=true
RATE_LIMIT_ENABLED=false
```

### Numeric Values
Use plain numbers (no quotes):
```bash
PORT=5000
MAX_CONTENT_LENGTH=200
WORKERS=4
```

### String Values
Use plain text (quotes optional):
```bash
FLASK_ENV=production
AI_PROVIDER=anthropic
LOG_LEVEL=INFO
```

### List Values
Use comma-separated values:
```bash
CORS_ORIGINS=https://domain1.com,https://domain2.com
OUTPUT_FORMATS=json,chromadb,text
```

### URL Values
Use full URLs:
```bash
MONGODB_CONNECTION_STRING=mongodb://user:pass@host:port/db
CHROMA_BASE_URL=http://localhost:8000/api/v1
```

## Validation and Debugging

### Check Environment Variables
```bash
# List all RPGer-related variables
env | grep -E "(FLASK|AI|MONGODB|CHROMA|LOG)" | sort

# Check specific variable
echo $ANTHROPIC_API_KEY | head -c 20

# Validate required variables
python -c "
import os
required = ['FLASK_SECRET_KEY', 'AI_PROVIDER', 'MONGODB_HOST', 'CHROMA_HOST']
missing = [var for var in required if not os.getenv(var)]
if missing: print(f'Missing: {missing}')
else: print('All required variables set')
"
```

### Common Issues
- **API keys**: Must start with correct prefix (sk-ant-, sk-, sk-or-)
- **Boolean values**: Use lowercase `true`/`false`
- **Paths**: Use absolute paths in production
- **URLs**: Include protocol (http:// or https://)
- **Ports**: Ensure ports are not in use by other services

This quick reference provides easy lookup for all environment variables in the RPGer Content Extractor.
