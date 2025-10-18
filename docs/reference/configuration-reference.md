---
title: Configuration Reference
description: Complete reference for all configuration options and environment variables
tags: [reference, configuration, environment-variables, settings]
last_updated: 2025-10-18
author: HL-Auggie Analysis System
---

# Configuration Reference

## Overview

This document provides a comprehensive reference for all configuration options, environment variables, and settings available in the RPGer Content Extractor. All settings are organized by category with detailed descriptions, default values, and usage examples.

## Application Configuration

### Core Flask Settings

| Variable | Type | Default | Description |
|----------|------|---------|-------------|
| `FLASK_ENV` | string | `production` | Flask environment mode |
| `FLASK_SECRET_KEY` | string | **Required** | Secret key for session encryption |
| `FLASK_DEBUG` | boolean | `false` | Enable Flask debug mode |
| `HOST` | string | `0.0.0.0` | Server bind address |
| `PORT` | integer | `5000` | Server port number |
| `WORKERS` | integer | `1` | Number of worker processes |

**Example**:
```bash
FLASK_ENV=production
FLASK_SECRET_KEY=your-secret-key-here
FLASK_DEBUG=false
HOST=0.0.0.0
PORT=5000
WORKERS=4
```

### Request and Upload Settings

| Variable | Type | Default | Description |
|----------|------|---------|-------------|
| `MAX_CONTENT_LENGTH` | integer | `200` | Maximum file size in MB |
| `UPLOAD_TIMEOUT` | integer | `300` | Upload timeout in seconds |
| `REQUEST_TIMEOUT` | integer | `60` | General request timeout |
| `UPLOAD_FOLDER` | string | `./uploads` | Upload directory path |
| `UPLOAD_ALLOWED_EXTENSIONS` | string | `pdf` | Allowed file extensions |
| `UPLOAD_TEMP_CLEANUP` | boolean | `true` | Clean up temporary files |
| `UPLOAD_TEMP_RETENTION` | integer | `3600` | Temp file retention in seconds |

**Example**:
```bash
MAX_CONTENT_LENGTH=200
UPLOAD_TIMEOUT=300
REQUEST_TIMEOUT=60
UPLOAD_FOLDER=./uploads
UPLOAD_ALLOWED_EXTENSIONS=pdf
UPLOAD_TEMP_CLEANUP=true
UPLOAD_TEMP_RETENTION=3600
```

### Output Configuration

| Variable | Type | Default | Description |
|----------|------|---------|-------------|
| `OUTPUT_FOLDER` | string | `./extracted` | Output directory path |
| `OUTPUT_FORMATS` | string | `json,chromadb,text` | Available output formats |
| `OUTPUT_COMPRESSION` | boolean | `true` | Compress output files |
| `OUTPUT_RETENTION_DAYS` | integer | `30` | Output file retention period |

## AI Provider Configuration

### Anthropic Claude

| Variable | Type | Default | Description |
|----------|------|---------|-------------|
| `ANTHROPIC_API_KEY` | string | **Required** | Anthropic API key |
| `ANTHROPIC_MODEL` | string | `claude-3-sonnet-20240229` | Default model |
| `ANTHROPIC_MAX_TOKENS` | integer | `4000` | Maximum tokens per request |
| `ANTHROPIC_TEMPERATURE` | float | `0.3` | Response randomness (0.0-1.0) |
| `ANTHROPIC_TIMEOUT` | integer | `60` | Request timeout in seconds |
| `ANTHROPIC_RETRY_ATTEMPTS` | integer | `3` | Number of retry attempts |
| `ANTHROPIC_RETRY_DELAY` | integer | `5` | Delay between retries |

**Example**:
```bash
ANTHROPIC_API_KEY=sk-ant-your-key-here
ANTHROPIC_MODEL=claude-3-sonnet-20240229
ANTHROPIC_MAX_TOKENS=4000
ANTHROPIC_TEMPERATURE=0.3
ANTHROPIC_TIMEOUT=60
```

### OpenAI

| Variable | Type | Default | Description |
|----------|------|---------|-------------|
| `OPENAI_API_KEY` | string | **Required** | OpenAI API key |
| `OPENAI_MODEL` | string | `gpt-4` | Default model |
| `OPENAI_MAX_TOKENS` | integer | `4000` | Maximum tokens per request |
| `OPENAI_TEMPERATURE` | float | `0.3` | Response randomness (0.0-2.0) |
| `OPENAI_TIMEOUT` | integer | `60` | Request timeout in seconds |
| `OPENAI_ORG_ID` | string | `null` | Organization ID (optional) |

**Example**:
```bash
OPENAI_API_KEY=sk-your-key-here
OPENAI_MODEL=gpt-4
OPENAI_MAX_TOKENS=4000
OPENAI_TEMPERATURE=0.3
OPENAI_TIMEOUT=60
```

### OpenRouter

| Variable | Type | Default | Description |
|----------|------|---------|-------------|
| `OPENROUTER_API_KEY` | string | **Required** | OpenRouter API key |
| `OPENROUTER_MODEL` | string | `anthropic/claude-3-sonnet` | Default model |
| `OPENROUTER_MAX_TOKENS` | integer | `4000` | Maximum tokens per request |
| `OPENROUTER_TEMPERATURE` | float | `0.3` | Response randomness |
| `OPENROUTER_TIMEOUT` | integer | `60` | Request timeout in seconds |
| `OPENROUTER_SITE_URL` | string | `null` | Site URL for tracking |
| `OPENROUTER_APP_NAME` | string | `RPGer Content Extractor` | App name for tracking |

### AI Provider Selection

| Variable | Type | Default | Description |
|----------|------|---------|-------------|
| `AI_PROVIDER` | string | `anthropic` | Primary AI provider |
| `AI_MODEL` | string | `null` | Override default model |
| `AI_FALLBACK_PROVIDER` | string | `null` | Fallback provider |
| `AI_RETRY_ATTEMPTS` | integer | `3` | Global retry attempts |
| `AI_RETRY_DELAY` | integer | `5` | Global retry delay |

**Valid AI_PROVIDER values**: `anthropic`, `openai`, `openrouter`, `local`, `mock`

## Database Configuration

### MongoDB Settings

| Variable | Type | Default | Description |
|----------|------|---------|-------------|
| `MONGODB_HOST` | string | `localhost` | MongoDB host address |
| `MONGODB_PORT` | integer | `27017` | MongoDB port number |
| `MONGODB_DATABASE` | string | `rpger` | Database name |
| `MONGODB_USERNAME` | string | `null` | Authentication username |
| `MONGODB_PASSWORD` | string | `null` | Authentication password |
| `MONGODB_AUTH_SOURCE` | string | `admin` | Authentication database |
| `MONGODB_CONNECTION_STRING` | string | `null` | Full connection string |

**Connection Pool Settings**:

| Variable | Type | Default | Description |
|----------|------|---------|-------------|
| `MONGODB_MAX_POOL_SIZE` | integer | `10` | Maximum connections |
| `MONGODB_MIN_POOL_SIZE` | integer | `1` | Minimum connections |
| `MONGODB_MAX_IDLE_TIME` | integer | `30000` | Max idle time (ms) |
| `MONGODB_CONNECT_TIMEOUT` | integer | `10000` | Connection timeout (ms) |
| `MONGODB_SERVER_SELECTION_TIMEOUT` | integer | `5000` | Server selection timeout (ms) |

**Example**:
```bash
MONGODB_HOST=localhost
MONGODB_PORT=27017
MONGODB_DATABASE=rpger
MONGODB_USERNAME=rpger_user
MONGODB_PASSWORD=secure_password
MONGODB_MAX_POOL_SIZE=10
```

### ChromaDB Settings

| Variable | Type | Default | Description |
|----------|------|---------|-------------|
| `CHROMA_HOST` | string | `localhost` | ChromaDB host address |
| `CHROMA_PORT` | integer | `8000` | ChromaDB port number |
| `CHROMA_TENANT` | string | `default_tenant` | Tenant name |
| `CHROMA_DATABASE` | string | `default_database` | Database name |
| `CHROMA_BASE_URL` | string | `null` | Full base URL |

**Performance Settings**:

| Variable | Type | Default | Description |
|----------|------|---------|-------------|
| `CHROMA_TIMEOUT` | integer | `30` | Request timeout |
| `CHROMA_MAX_RETRIES` | integer | `3` | Maximum retries |
| `CHROMA_BATCH_SIZE` | integer | `100` | Batch operation size |
| `CHROMA_MAX_CONNECTIONS` | integer | `20` | Max connections |

**Example**:
```bash
CHROMA_HOST=localhost
CHROMA_PORT=8000
CHROMA_TENANT=default_tenant
CHROMA_DATABASE=default_database
CHROMA_TIMEOUT=30
```

## Security Configuration

### CORS Settings

| Variable | Type | Default | Description |
|----------|------|---------|-------------|
| `CORS_ORIGINS` | string | `*` | Allowed origins (comma-separated) |
| `CORS_METHODS` | string | `GET,POST,PUT,DELETE,OPTIONS` | Allowed methods |
| `CORS_HEADERS` | string | `Content-Type,Authorization,X-API-Key` | Allowed headers |
| `CORS_CREDENTIALS` | boolean | `false` | Allow credentials |

**Example**:
```bash
CORS_ORIGINS=https://yourdomain.com,https://app.yourdomain.com
CORS_METHODS=GET,POST,PUT,DELETE,OPTIONS
CORS_HEADERS=Content-Type,Authorization,X-API-Key
```

### Rate Limiting

| Variable | Type | Default | Description |
|----------|------|---------|-------------|
| `RATE_LIMIT_ENABLED` | boolean | `true` | Enable rate limiting |
| `RATE_LIMIT_STORAGE_URL` | string | `memory://` | Storage backend URL |
| `RATE_LIMIT_DEFAULT` | string | `100 per hour` | Default rate limit |
| `RATE_LIMIT_UPLOAD` | string | `10 per minute` | Upload rate limit |

**Example**:
```bash
RATE_LIMIT_ENABLED=true
RATE_LIMIT_STORAGE_URL=redis://redis:6379
RATE_LIMIT_DEFAULT=100 per hour
RATE_LIMIT_UPLOAD=10 per minute
```

### Security Headers

| Variable | Type | Default | Description |
|----------|------|---------|-------------|
| `SECURITY_HEADERS_ENABLED` | boolean | `true` | Enable security headers |
| `HSTS_MAX_AGE` | integer | `31536000` | HSTS max age in seconds |
| `CSP_POLICY` | string | `default-src 'self'` | Content Security Policy |
| `X_FRAME_OPTIONS` | string | `DENY` | X-Frame-Options header |

### Authentication (Optional)

| Variable | Type | Default | Description |
|----------|------|---------|-------------|
| `API_KEY_ENABLED` | boolean | `false` | Enable API key auth |
| `API_KEY_HEADER` | string | `X-API-Key` | API key header name |
| `JWT_SECRET_KEY` | string | `null` | JWT secret key |
| `JWT_ALGORITHM` | string | `HS256` | JWT algorithm |
| `JWT_EXPIRATION` | integer | `3600` | JWT expiration (seconds) |

## Logging Configuration

### Basic Logging

| Variable | Type | Default | Description |
|----------|------|---------|-------------|
| `LOG_LEVEL` | string | `INFO` | Global log level |
| `LOG_FORMAT` | string | `json` | Log format (json/text) |
| `LOG_FILE` | string | `./logs/app.log` | Log file path |
| `LOG_MAX_SIZE` | string | `10MB` | Max log file size |
| `LOG_BACKUP_COUNT` | integer | `5` | Number of backup files |
| `LOG_ROTATION` | string | `daily` | Rotation schedule |

**Valid LOG_LEVEL values**: `DEBUG`, `INFO`, `WARNING`, `ERROR`, `CRITICAL`

### Component-Specific Logging

| Variable | Type | Default | Description |
|----------|------|---------|-------------|
| `LOG_LEVEL_PDF` | string | `INFO` | PDF processing log level |
| `LOG_LEVEL_AI` | string | `INFO` | AI provider log level |
| `LOG_LEVEL_DB` | string | `INFO` | Database log level |
| `LOG_LEVEL_WEB` | string | `INFO` | Web server log level |

**Example**:
```bash
LOG_LEVEL=INFO
LOG_FORMAT=json
LOG_FILE=./logs/app.log
LOG_LEVEL_PDF=DEBUG
LOG_LEVEL_AI=INFO
LOG_LEVEL_DB=WARNING
```

## Performance Configuration

### Application Performance

| Variable | Type | Default | Description |
|----------|------|---------|-------------|
| `WORKERS` | integer | `1` | Number of worker processes |
| `WORKER_CONNECTIONS` | integer | `1000` | Connections per worker |
| `WORKER_TIMEOUT` | integer | `30` | Worker timeout (seconds) |
| `KEEPALIVE` | integer | `2` | Keep-alive timeout |

### Memory Management

| Variable | Type | Default | Description |
|----------|------|---------|-------------|
| `MAX_MEMORY_USAGE` | string | `2GB` | Maximum memory usage |
| `MEMORY_CLEANUP_INTERVAL` | integer | `300` | Cleanup interval (seconds) |
| `GC_THRESHOLD` | integer | `700` | Garbage collection threshold |

### Caching

| Variable | Type | Default | Description |
|----------|------|---------|-------------|
| `CACHE_TYPE` | string | `memory` | Cache backend type |
| `CACHE_REDIS_URL` | string | `null` | Redis cache URL |
| `CACHE_DEFAULT_TIMEOUT` | integer | `300` | Default cache timeout |
| `CACHE_KEY_PREFIX` | string | `rpger_` | Cache key prefix |

**Valid CACHE_TYPE values**: `memory`, `redis`, `filesystem`

## Monitoring Configuration

### Health Checks

| Variable | Type | Default | Description |
|----------|------|---------|-------------|
| `HEALTH_CHECK_ENABLED` | boolean | `true` | Enable health checks |
| `HEALTH_CHECK_INTERVAL` | integer | `30` | Check interval (seconds) |
| `HEALTH_CHECK_TIMEOUT` | integer | `10` | Check timeout (seconds) |
| `HEALTH_CHECK_RETRIES` | integer | `3` | Number of retries |

### Component Health Checks

| Variable | Type | Default | Description |
|----------|------|---------|-------------|
| `HEALTH_CHECK_MONGODB` | boolean | `true` | Check MongoDB health |
| `HEALTH_CHECK_CHROMADB` | boolean | `true` | Check ChromaDB health |
| `HEALTH_CHECK_AI_PROVIDERS` | boolean | `true` | Check AI provider health |
| `HEALTH_CHECK_DISK_SPACE` | boolean | `true` | Check disk space |

### Metrics

| Variable | Type | Default | Description |
|----------|------|---------|-------------|
| `METRICS_ENABLED` | boolean | `false` | Enable metrics collection |
| `METRICS_PORT` | integer | `9090` | Metrics server port |
| `METRICS_PATH` | string | `/metrics` | Metrics endpoint path |
| `METRICS_NAMESPACE` | string | `rpger` | Metrics namespace |

### Tracing (Optional)

| Variable | Type | Default | Description |
|----------|------|---------|-------------|
| `TRACING_ENABLED` | boolean | `false` | Enable distributed tracing |
| `TRACING_SERVICE_NAME` | string | `rpger-content-extractor` | Service name |
| `TRACING_JAEGER_ENDPOINT` | string | `null` | Jaeger endpoint URL |
| `TRACING_SAMPLE_RATE` | float | `0.1` | Sampling rate (0.0-1.0) |

## PDF Processing Configuration

### Processing Options

| Variable | Type | Default | Description |
|----------|------|---------|-------------|
| `ENABLE_TEXT_ENHANCEMENT` | boolean | `true` | Enable text quality enhancement |
| `AGGRESSIVE_CLEANUP` | boolean | `false` | Aggressive text cleanup |
| `ENABLE_LAYOUT_ANALYSIS` | boolean | `true` | Enable layout analysis |
| `MULTI_COLUMN_DETECTION` | boolean | `true` | Detect multi-column layouts |
| `PDF_PROCESSING_MODE` | string | `standard` | Processing mode |
| `LAYOUT_TOLERANCE` | float | `0.5` | Layout detection tolerance |

**Valid PDF_PROCESSING_MODE values**: `standard`, `advanced`, `fast`

### OCR Configuration

| Variable | Type | Default | Description |
|----------|------|---------|-------------|
| `OCR_ENABLED` | boolean | `false` | Enable OCR processing |
| `OCR_LANGUAGE` | string | `eng` | OCR language |
| `OCR_DPI` | integer | `300` | OCR resolution |
| `OCR_CONFIDENCE_THRESHOLD` | float | `0.8` | Minimum confidence |

## Development Configuration

### Development Mode

| Variable | Type | Default | Description |
|----------|------|---------|-------------|
| `FLASK_ENV` | string | `development` | Development environment |
| `FLASK_DEBUG` | boolean | `true` | Enable debug mode |
| `LOG_LEVEL` | string | `DEBUG` | Debug logging |
| `AI_PROVIDER` | string | `mock` | Use mock AI provider |

### Testing Configuration

| Variable | Type | Default | Description |
|----------|------|---------|-------------|
| `FLASK_TESTING` | boolean | `true` | Enable testing mode |
| `MONGODB_DATABASE` | string | `rpger_test` | Test database |
| `RATE_LIMIT_ENABLED` | boolean | `false` | Disable rate limiting |
| `METRICS_ENABLED` | boolean | `false` | Disable metrics |

## Environment-Specific Examples

### Development Environment
```bash
# Development configuration
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
# Production configuration
FLASK_ENV=production
FLASK_DEBUG=false
LOG_LEVEL=INFO
AI_PROVIDER=anthropic
ANTHROPIC_API_KEY=your-production-key
MONGODB_HOST=prod-mongodb.yourdomain.com
CORS_ORIGINS=https://yourdomain.com
RATE_LIMIT_ENABLED=true
SECURITY_HEADERS_ENABLED=true
```

### Docker Environment
```bash
# Docker-specific configuration
HOST=0.0.0.0
PORT=5000
MONGODB_HOST=mongodb
CHROMA_HOST=chromadb
LOG_FILE=/app/logs/app.log
UPLOAD_FOLDER=/app/uploads
OUTPUT_FOLDER=/app/extracted
```

## Configuration Validation

### Required Variables
The following variables are required for the application to start:
- `FLASK_SECRET_KEY`
- At least one AI provider API key
- Database connection settings

### Validation Script
```bash
# Validate configuration
python -c "
import os
required = ['FLASK_SECRET_KEY', 'AI_PROVIDER']
missing = [var for var in required if not os.getenv(var)]
if missing:
    print(f'Missing required variables: {missing}')
    exit(1)
print('Configuration validation passed')
"
```

This configuration reference provides complete documentation for all available settings in the RPGer Content Extractor.
