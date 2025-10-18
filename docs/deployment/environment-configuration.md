---
title: Environment Configuration
description: Complete guide to environment variables and configuration options
tags: [deployment, configuration, environment, settings]
last_updated: 2025-10-18
author: HL-Auggie Analysis System
---

# Environment Configuration

## Overview

This guide covers all environment variables and configuration options for the RPGer Content Extractor. Proper configuration is essential for optimal performance, security, and functionality across different deployment environments.

## Configuration Methods

### 1. Environment Files (.env)

The primary configuration method uses `.env` files:

```bash
# Create environment file
cp .env.example .env

# Edit configuration
nano .env
```

### 2. Environment Variables

Direct environment variable setting:

```bash
# Set environment variables
export FLASK_ENV=production
export ANTHROPIC_API_KEY=your-api-key

# Run application
python ui/start_ui.py
```

### 3. Docker Environment

Docker-specific configuration:

```yaml
# docker-compose.yml
services:
  app:
    environment:
      - FLASK_ENV=production
      - ANTHROPIC_API_KEY=${ANTHROPIC_API_KEY}
    env_file:
      - .env
```

## Core Configuration

### Application Settings

#### Flask Configuration

```bash
# Flask Environment
FLASK_ENV=production                    # production, development, testing
FLASK_SECRET_KEY=your-secret-key-here   # Required for sessions and security
FLASK_DEBUG=false                       # Enable debug mode (development only)

# Server Configuration
HOST=0.0.0.0                           # Bind address (0.0.0.0 for all interfaces)
PORT=5000                              # Server port
WORKERS=4                              # Number of worker processes

# Request Limits
MAX_CONTENT_LENGTH=200                 # Maximum file size in MB
UPLOAD_TIMEOUT=300                     # Upload timeout in seconds
REQUEST_TIMEOUT=60                     # General request timeout
```

#### Security Configuration

```bash
# CORS Settings
CORS_ORIGINS=https://yourdomain.com,https://app.yourdomain.com
CORS_METHODS=GET,POST,PUT,DELETE,OPTIONS
CORS_HEADERS=Content-Type,Authorization,X-API-Key

# Rate Limiting
RATE_LIMIT_STORAGE_URL=redis://redis:6379
RATE_LIMIT_DEFAULT=100 per hour
RATE_LIMIT_UPLOAD=10 per minute

# Security Headers
SECURITY_HEADERS_ENABLED=true
HSTS_MAX_AGE=31536000
CSP_POLICY=default-src 'self'
```

### AI Provider Configuration

#### Anthropic Claude

```bash
# Anthropic Configuration
ANTHROPIC_API_KEY=sk-ant-your-key-here
ANTHROPIC_MODEL=claude-3-sonnet-20240229
ANTHROPIC_MAX_TOKENS=4000
ANTHROPIC_TEMPERATURE=0.3
ANTHROPIC_TIMEOUT=60
```

#### OpenAI

```bash
# OpenAI Configuration
OPENAI_API_KEY=sk-your-key-here
OPENAI_MODEL=gpt-4
OPENAI_MAX_TOKENS=4000
OPENAI_TEMPERATURE=0.3
OPENAI_TIMEOUT=60
OPENAI_ORG_ID=your-org-id              # Optional organization ID
```

#### OpenRouter

```bash
# OpenRouter Configuration
OPENROUTER_API_KEY=sk-or-your-key-here
OPENROUTER_MODEL=anthropic/claude-3-sonnet
OPENROUTER_MAX_TOKENS=4000
OPENROUTER_TEMPERATURE=0.3
OPENROUTER_TIMEOUT=60
OPENROUTER_SITE_URL=https://yourdomain.com
OPENROUTER_APP_NAME=RPGer Content Extractor
```

#### Local LLM

```bash
# Local LLM Configuration
LOCAL_LLM_URL=http://localhost:11434
LOCAL_LLM_MODEL=llama2
LOCAL_LLM_MAX_TOKENS=4000
LOCAL_LLM_TEMPERATURE=0.3
LOCAL_LLM_TIMEOUT=120
```

#### AI Provider Selection

```bash
# Default AI Provider
AI_PROVIDER=anthropic                  # anthropic, openai, openrouter, local, mock
AI_MODEL=claude-3-sonnet              # Model name (provider-specific)
AI_FALLBACK_PROVIDER=openai          # Fallback provider if primary fails
AI_RETRY_ATTEMPTS=3                   # Number of retry attempts
AI_RETRY_DELAY=5                      # Delay between retries in seconds
```

### Database Configuration

#### MongoDB Settings

```bash
# MongoDB Connection
MONGODB_HOST=localhost
MONGODB_PORT=27017
MONGODB_DATABASE=rpger
MONGODB_USERNAME=rpger_user
MONGODB_PASSWORD=secure_password
MONGODB_AUTH_SOURCE=admin

# Alternative: Full connection string
MONGODB_CONNECTION_STRING=mongodb://user:pass@host:port/database

# MongoDB Options
MONGODB_MAX_POOL_SIZE=10
MONGODB_MIN_POOL_SIZE=1
MONGODB_MAX_IDLE_TIME=30000
MONGODB_CONNECT_TIMEOUT=10000
MONGODB_SERVER_SELECTION_TIMEOUT=5000
```

#### ChromaDB Settings

```bash
# ChromaDB Connection
CHROMA_HOST=localhost
CHROMA_PORT=8000
CHROMA_TENANT=default_tenant
CHROMA_DATABASE=default_database

# Alternative: Full URL
CHROMA_BASE_URL=http://localhost:8000/api/v2

# ChromaDB Options
CHROMA_TIMEOUT=30
CHROMA_MAX_RETRIES=3
CHROMA_BATCH_SIZE=100
```

### File Storage Configuration

#### Upload Settings

```bash
# Upload Configuration
UPLOAD_FOLDER=./uploads
UPLOAD_MAX_SIZE=200                    # Maximum file size in MB
UPLOAD_ALLOWED_EXTENSIONS=pdf
UPLOAD_TEMP_CLEANUP=true              # Clean up temporary files
UPLOAD_TEMP_RETENTION=3600            # Temp file retention in seconds
```

#### Output Settings

```bash
# Output Configuration
OUTPUT_FOLDER=./extracted
OUTPUT_FORMATS=json,chromadb,text     # Available output formats
OUTPUT_COMPRESSION=true               # Compress output files
OUTPUT_RETENTION_DAYS=30              # Output file retention period
```

#### Log Settings

```bash
# Logging Configuration
LOG_LEVEL=INFO                        # DEBUG, INFO, WARNING, ERROR, CRITICAL
LOG_FORMAT=json                       # json, text
LOG_FILE=./logs/app.log
LOG_MAX_SIZE=10MB
LOG_BACKUP_COUNT=5
LOG_ROTATION=daily                    # daily, weekly, size-based

# Specific Logger Levels
LOG_LEVEL_PDF=DEBUG
LOG_LEVEL_AI=INFO
LOG_LEVEL_DB=WARNING
```

## Environment-Specific Configurations

### Development Environment

```bash
# Development Configuration (.env.development)
FLASK_ENV=development
FLASK_DEBUG=true
LOG_LEVEL=DEBUG

# Use mock AI provider for development
AI_PROVIDER=mock
AI_MODEL=mock-model

# Local database connections
MONGODB_HOST=localhost
MONGODB_PORT=27017
MONGODB_DATABASE=rpger_dev

CHROMA_HOST=localhost
CHROMA_PORT=8000

# Relaxed security for development
CORS_ORIGINS=*
RATE_LIMIT_ENABLED=false
```

### Testing Environment

```bash
# Testing Configuration (.env.testing)
FLASK_ENV=testing
FLASK_TESTING=true
LOG_LEVEL=WARNING

# Use mock providers for testing
AI_PROVIDER=mock
AI_MODEL=mock-model

# Test database connections
MONGODB_HOST=localhost
MONGODB_PORT=27017
MONGODB_DATABASE=rpger_test

CHROMA_HOST=localhost
CHROMA_PORT=8000

# Disable external services
RATE_LIMIT_ENABLED=false
METRICS_ENABLED=false
```

### Production Environment

```bash
# Production Configuration (.env.production)
FLASK_ENV=production
FLASK_DEBUG=false
LOG_LEVEL=INFO

# Production AI provider
AI_PROVIDER=anthropic
AI_MODEL=claude-3-sonnet
ANTHROPIC_API_KEY=your-production-key

# Production database connections
MONGODB_HOST=prod-mongodb.yourdomain.com
MONGODB_PORT=27017
MONGODB_DATABASE=rpger
MONGODB_USERNAME=rpger_prod
MONGODB_PASSWORD=secure-production-password

CHROMA_HOST=prod-chromadb.yourdomain.com
CHROMA_PORT=8000

# Production security settings
CORS_ORIGINS=https://yourdomain.com
RATE_LIMIT_ENABLED=true
SECURITY_HEADERS_ENABLED=true
HSTS_MAX_AGE=31536000
```

### Staging Environment

```bash
# Staging Configuration (.env.staging)
FLASK_ENV=production
FLASK_DEBUG=false
LOG_LEVEL=DEBUG

# Staging AI provider (can use production keys)
AI_PROVIDER=anthropic
AI_MODEL=claude-3-sonnet
ANTHROPIC_API_KEY=your-staging-key

# Staging database connections
MONGODB_HOST=staging-mongodb.yourdomain.com
MONGODB_PORT=27017
MONGODB_DATABASE=rpger_staging

CHROMA_HOST=staging-chromadb.yourdomain.com
CHROMA_PORT=8000

# Staging-specific settings
CORS_ORIGINS=https://staging.yourdomain.com
RATE_LIMIT_ENABLED=true
METRICS_ENABLED=true
```

## Advanced Configuration

### Performance Tuning

#### Application Performance

```bash
# Performance Configuration
WORKERS=4                             # Number of worker processes
WORKER_CONNECTIONS=1000               # Connections per worker
WORKER_TIMEOUT=30                     # Worker timeout in seconds
KEEPALIVE=2                          # Keep-alive timeout

# Memory Management
MAX_MEMORY_USAGE=2GB                 # Maximum memory usage
MEMORY_CLEANUP_INTERVAL=300          # Memory cleanup interval in seconds
GC_THRESHOLD=700                     # Garbage collection threshold

# Caching
CACHE_TYPE=redis                     # redis, memory, filesystem
CACHE_REDIS_URL=redis://redis:6379
CACHE_DEFAULT_TIMEOUT=300
CACHE_KEY_PREFIX=rpger_
```

#### Database Performance

```bash
# MongoDB Performance
MONGODB_MAX_POOL_SIZE=50
MONGODB_MIN_POOL_SIZE=5
MONGODB_MAX_IDLE_TIME=60000
MONGODB_WRITE_CONCERN=1
MONGODB_READ_PREFERENCE=primary

# ChromaDB Performance
CHROMA_BATCH_SIZE=1000
CHROMA_MAX_CONNECTIONS=20
CHROMA_CONNECTION_POOL_SIZE=10
CHROMA_QUERY_TIMEOUT=30
```

### Monitoring and Observability

#### Metrics Configuration

```bash
# Metrics Collection
METRICS_ENABLED=true
METRICS_PORT=9090
METRICS_PATH=/metrics
METRICS_NAMESPACE=rpger

# Prometheus Configuration
PROMETHEUS_MULTIPROC_DIR=/tmp/prometheus
PROMETHEUS_REGISTRY=default
```

#### Health Check Configuration

```bash
# Health Checks
HEALTH_CHECK_ENABLED=true
HEALTH_CHECK_INTERVAL=30
HEALTH_CHECK_TIMEOUT=10
HEALTH_CHECK_RETRIES=3

# Component Health Checks
HEALTH_CHECK_MONGODB=true
HEALTH_CHECK_CHROMADB=true
HEALTH_CHECK_AI_PROVIDERS=true
HEALTH_CHECK_DISK_SPACE=true
```

#### Tracing Configuration

```bash
# Distributed Tracing
TRACING_ENABLED=true
TRACING_SERVICE_NAME=rpger-content-extractor
TRACING_JAEGER_ENDPOINT=http://jaeger:14268/api/traces
TRACING_SAMPLE_RATE=0.1
```

### Security Configuration

#### Authentication and Authorization

```bash
# API Authentication
API_KEY_ENABLED=false
API_KEY_HEADER=X-API-Key
API_KEY_QUERY_PARAM=api_key

# JWT Configuration
JWT_SECRET_KEY=your-jwt-secret
JWT_ALGORITHM=HS256
JWT_EXPIRATION=3600
JWT_REFRESH_EXPIRATION=86400

# OAuth Configuration
OAUTH_ENABLED=false
OAUTH_PROVIDER=google
OAUTH_CLIENT_ID=your-client-id
OAUTH_CLIENT_SECRET=your-client-secret
```

#### Encryption and Secrets

```bash
# Encryption Configuration
ENCRYPTION_KEY=your-encryption-key
ENCRYPTION_ALGORITHM=AES-256-GCM

# Secrets Management
SECRETS_BACKEND=vault                # vault, aws, azure, gcp
VAULT_URL=https://vault.yourdomain.com
VAULT_TOKEN=your-vault-token
VAULT_MOUNT_POINT=secret
```

## Configuration Validation

### Environment Validation Script

```bash
#!/bin/bash
# validate-config.sh

echo "Validating RPGer Content Extractor Configuration..."

# Check required environment variables
required_vars=(
    "FLASK_SECRET_KEY"
    "AI_PROVIDER"
    "MONGODB_HOST"
    "CHROMA_HOST"
)

for var in "${required_vars[@]}"; do
    if [ -z "${!var}" ]; then
        echo "ERROR: Required environment variable $var is not set"
        exit 1
    fi
done

# Validate AI provider configuration
case "$AI_PROVIDER" in
    "anthropic")
        if [ -z "$ANTHROPIC_API_KEY" ]; then
            echo "ERROR: ANTHROPIC_API_KEY required for Anthropic provider"
            exit 1
        fi
        ;;
    "openai")
        if [ -z "$OPENAI_API_KEY" ]; then
            echo "ERROR: OPENAI_API_KEY required for OpenAI provider"
            exit 1
        fi
        ;;
    "openrouter")
        if [ -z "$OPENROUTER_API_KEY" ]; then
            echo "ERROR: OPENROUTER_API_KEY required for OpenRouter provider"
            exit 1
        fi
        ;;
esac

# Test database connections
echo "Testing MongoDB connection..."
if ! mongosh "$MONGODB_CONNECTION_STRING" --eval "db.adminCommand('ping')" >/dev/null 2>&1; then
    echo "WARNING: Cannot connect to MongoDB"
fi

echo "Testing ChromaDB connection..."
if ! curl -s "$CHROMA_BASE_URL/heartbeat" >/dev/null; then
    echo "WARNING: Cannot connect to ChromaDB"
fi

echo "Configuration validation completed"
```

### Python Configuration Validation

```python
# config_validator.py
import os
import sys
from typing import List, Dict, Any

class ConfigValidator:
    """Validate application configuration."""
    
    def __init__(self):
        self.errors: List[str] = []
        self.warnings: List[str] = []
    
    def validate_required_vars(self, required_vars: List[str]) -> None:
        """Validate required environment variables."""
        for var in required_vars:
            if not os.getenv(var):
                self.errors.append(f"Required environment variable {var} is not set")
    
    def validate_ai_provider(self) -> None:
        """Validate AI provider configuration."""
        provider = os.getenv('AI_PROVIDER', '').lower()
        
        if provider == 'anthropic' and not os.getenv('ANTHROPIC_API_KEY'):
            self.errors.append("ANTHROPIC_API_KEY required for Anthropic provider")
        elif provider == 'openai' and not os.getenv('OPENAI_API_KEY'):
            self.errors.append("OPENAI_API_KEY required for OpenAI provider")
        elif provider == 'openrouter' and not os.getenv('OPENROUTER_API_KEY'):
            self.errors.append("OPENROUTER_API_KEY required for OpenRouter provider")
    
    def validate_database_config(self) -> None:
        """Validate database configuration."""
        # MongoDB validation
        if not os.getenv('MONGODB_HOST'):
            self.errors.append("MONGODB_HOST is required")
        
        # ChromaDB validation
        if not os.getenv('CHROMA_HOST'):
            self.errors.append("CHROMA_HOST is required")
    
    def validate_security_config(self) -> None:
        """Validate security configuration."""
        if os.getenv('FLASK_ENV') == 'production':
            if not os.getenv('FLASK_SECRET_KEY'):
                self.errors.append("FLASK_SECRET_KEY is required for production")
            
            if os.getenv('FLASK_DEBUG', '').lower() == 'true':
                self.warnings.append("Debug mode should be disabled in production")
    
    def validate_all(self) -> bool:
        """Run all validations."""
        required_vars = [
            'FLASK_SECRET_KEY',
            'AI_PROVIDER',
            'MONGODB_HOST',
            'CHROMA_HOST'
        ]
        
        self.validate_required_vars(required_vars)
        self.validate_ai_provider()
        self.validate_database_config()
        self.validate_security_config()
        
        # Print results
        if self.errors:
            print("Configuration Errors:")
            for error in self.errors:
                print(f"  ERROR: {error}")
        
        if self.warnings:
            print("Configuration Warnings:")
            for warning in self.warnings:
                print(f"  WARNING: {warning}")
        
        return len(self.errors) == 0

if __name__ == "__main__":
    validator = ConfigValidator()
    if not validator.validate_all():
        sys.exit(1)
    print("Configuration validation passed")
```

## Configuration Templates

### Complete Production Template

```bash
# .env.production.template
# Copy this file to .env and fill in your values

# ============================================================================
# CORE APPLICATION SETTINGS
# ============================================================================
FLASK_ENV=production
FLASK_SECRET_KEY=CHANGE_THIS_TO_A_SECURE_RANDOM_STRING
FLASK_DEBUG=false
HOST=0.0.0.0
PORT=5000

# ============================================================================
# AI PROVIDER CONFIGURATION (Choose one or more)
# ============================================================================
# Anthropic Claude (Recommended)
ANTHROPIC_API_KEY=sk-ant-your-key-here
ANTHROPIC_MODEL=claude-3-sonnet-20240229

# OpenAI (Alternative)
# OPENAI_API_KEY=sk-your-key-here
# OPENAI_MODEL=gpt-4

# OpenRouter (Multiple models)
# OPENROUTER_API_KEY=sk-or-your-key-here
# OPENROUTER_MODEL=anthropic/claude-3-sonnet

# Default AI Provider
AI_PROVIDER=anthropic

# ============================================================================
# DATABASE CONFIGURATION
# ============================================================================
# MongoDB
MONGODB_HOST=your-mongodb-host
MONGODB_PORT=27017
MONGODB_DATABASE=rpger
MONGODB_USERNAME=rpger_user
MONGODB_PASSWORD=CHANGE_THIS_PASSWORD

# ChromaDB
CHROMA_HOST=your-chromadb-host
CHROMA_PORT=8000
CHROMA_TENANT=default_tenant
CHROMA_DATABASE=default_database

# ============================================================================
# SECURITY CONFIGURATION
# ============================================================================
CORS_ORIGINS=https://yourdomain.com
RATE_LIMIT_ENABLED=true
SECURITY_HEADERS_ENABLED=true

# ============================================================================
# PERFORMANCE CONFIGURATION
# ============================================================================
MAX_CONTENT_LENGTH=200
UPLOAD_TIMEOUT=300
WORKERS=4

# ============================================================================
# MONITORING CONFIGURATION
# ============================================================================
LOG_LEVEL=INFO
METRICS_ENABLED=true
HEALTH_CHECK_ENABLED=true
```

This comprehensive environment configuration guide provides all the necessary information to properly configure the RPGer Content Extractor for any deployment scenario.
