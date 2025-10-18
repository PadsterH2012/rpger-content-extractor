---
title: Technology Stack
description: Complete technology stack documentation for RPGer Content Extractor
tags: [reference, technology, stack, dependencies]
last_updated: 2025-10-18
author: HL-Auggie Analysis System
---

# Technology Stack

## Overview

The RPGer Content Extractor is built using a modern, scalable technology stack designed for reliability, performance, and maintainability. This document provides comprehensive information about all technologies, frameworks, and tools used in the project.

## Core Technologies

### Runtime Environment

#### Python 3.12
- **Purpose**: Primary application runtime
- **Version**: 3.12+ (recommended 3.12.0)
- **Features Used**:
  - Type hints and annotations
  - Async/await support
  - Dataclasses and Pydantic models
  - Context managers
  - Exception handling

**Key Benefits**:
- Mature ecosystem for AI/ML libraries
- Excellent PDF processing libraries
- Strong web framework support
- Rich database connectivity options

### Web Framework

#### Flask 2.3.3+
- **Purpose**: Web application framework and API server
- **Components Used**:
  - Core Flask application
  - Blueprint organization
  - Request/response handling
  - Template rendering with Jinja2
  - Session management
  - Error handling

**Extensions**:
- **Flask-CORS**: Cross-origin resource sharing
- **Werkzeug**: WSGI utilities and development server
- **Jinja2**: Template engine for HTML rendering

**Configuration**:
```python
# Core Flask settings
FLASK_ENV=production
FLASK_SECRET_KEY=secure-random-key
MAX_CONTENT_LENGTH=200MB
UPLOAD_TIMEOUT=300s
```

## PDF Processing Stack

### PyMuPDF (fitz) 1.23.0+
- **Purpose**: Primary PDF processing library
- **Capabilities**:
  - Text extraction with formatting preservation
  - Page-by-page processing
  - Metadata extraction
  - Multi-column layout detection
  - Table structure recognition

**Features Used**:
- Document opening and parsing
- Text extraction with coordinates
- Page rendering for analysis
- Font and style information
- Annotation processing

### pdfplumber 0.9.0+
- **Purpose**: Advanced PDF analysis and table extraction
- **Capabilities**:
  - Precise table detection
  - Character-level text analysis
  - Layout analysis
  - Visual debugging tools

**Use Cases**:
- Complex table extraction
- Layout validation
- Text quality assessment
- Debugging PDF structure issues

### Additional PDF Tools
- **PyPDF2/PyPDF4**: Backup PDF processing
- **pdf2image**: PDF to image conversion
- **Tesseract OCR**: Optical character recognition for scanned PDFs

## AI and Machine Learning

### AI Provider Integrations

#### Anthropic Claude API
- **Purpose**: Primary AI provider for content analysis
- **Models Supported**:
  - Claude 3 Sonnet (claude-3-sonnet-20240229)
  - Claude 3 Haiku (claude-3-haiku-20240307)
  - Claude 3 Opus (claude-3-opus-20240229)

**Client Library**: `anthropic>=0.25.0`

**Features**:
- Game system detection
- Content categorization
- Text quality analysis
- Confidence scoring

#### OpenAI API
- **Purpose**: Alternative AI provider
- **Models Supported**:
  - GPT-4 (gpt-4)
  - GPT-4 Turbo (gpt-4-turbo-preview)
  - GPT-3.5 Turbo (gpt-3.5-turbo)

**Client Library**: `openai>=1.0.0`

**Features**:
- Structured output generation
- Function calling
- Streaming responses
- Token usage tracking

#### OpenRouter API
- **Purpose**: Access to 300+ AI models
- **Supported Providers**:
  - Anthropic models
  - OpenAI models
  - Google models
  - Meta models
  - Open source models

**Client Library**: Custom implementation with `requests`

**Benefits**:
- Model diversity
- Cost optimization
- Fallback options
- Performance comparison

### Text Processing

#### pyspellchecker 0.7.0+
- **Purpose**: Spell checking and text correction
- **Features**:
  - OCR error correction
  - Dictionary-based validation
  - Custom word lists
  - Language detection

#### Natural Language Processing
- **NLTK**: Natural language toolkit (optional)
- **spaCy**: Advanced NLP processing (optional)
- **TextBlob**: Simple text processing (optional)

## Database Technologies

### MongoDB 7.0+
- **Purpose**: Primary document database
- **Driver**: `pymongo>=4.5.0`
- **Features Used**:
  - Document storage and retrieval
  - Hierarchical collection organization
  - Full-text search indexing
  - Aggregation pipelines
  - GridFS for large files

**Schema Design**:
- Flexible document structure
- Game-specific metadata
- Hierarchical collection naming
- Efficient indexing strategy

**Configuration**:
```python
# MongoDB connection settings
MONGODB_HOST=localhost
MONGODB_PORT=27017
MONGODB_DATABASE=rpger
MONGODB_MAX_POOL_SIZE=10
```

### ChromaDB 0.4.0+
- **Purpose**: Vector database for semantic search
- **Client**: `chromadb>=0.4.0`
- **Features Used**:
  - Vector embeddings storage
  - Similarity search
  - Metadata filtering
  - Collection management
  - Batch operations

**Embedding Models**:
- Default: all-MiniLM-L6-v2
- Custom: OpenAI text-embedding-ada-002
- Local: sentence-transformers models

**Configuration**:
```python
# ChromaDB settings
CHROMA_HOST=localhost
CHROMA_PORT=8000
CHROMA_TENANT=default_tenant
CHROMA_DATABASE=default_database
```

## Frontend Technologies

### HTML5 and CSS3
- **Purpose**: Modern web standards for UI
- **Features Used**:
  - Semantic HTML5 elements
  - CSS Grid and Flexbox
  - Responsive design
  - CSS custom properties
  - Modern form controls

### Bootstrap 5.3+
- **Purpose**: CSS framework for responsive design
- **Components Used**:
  - Grid system
  - Navigation components
  - Form controls
  - Modal dialogs
  - Progress bars
  - Alert components

**Customization**:
- Custom color scheme
- Modified component styles
- Responsive breakpoints
- Utility classes

### JavaScript (ES6+)
- **Purpose**: Client-side interactivity
- **Features Used**:
  - Fetch API for AJAX requests
  - Async/await for asynchronous operations
  - DOM manipulation
  - Event handling
  - File upload with progress
  - Real-time updates

**Libraries**:
- **No external JavaScript frameworks** (vanilla JS approach)
- **Chart.js**: Data visualization (optional)
- **Prism.js**: Code syntax highlighting (optional)

## Development and Testing

### Testing Framework

#### pytest 7.4.0+
- **Purpose**: Primary testing framework
- **Plugins Used**:
  - `pytest-cov`: Coverage reporting
  - `pytest-xdist`: Parallel test execution
  - `pytest-html`: HTML test reports
  - `pytest-json-report`: JSON test reports
  - `pytest-timeout`: Test timeout handling

**Test Categories**:
- Unit tests
- Integration tests
- End-to-end tests
- Performance tests

#### Mock and Fixtures
- **unittest.mock**: Python standard library mocking
- **pytest fixtures**: Test data and setup
- **Custom fixtures**: Application-specific test data

### Code Quality Tools

#### Black 23.0.0+
- **Purpose**: Code formatting
- **Configuration**: Default settings with 88-character line length
- **Integration**: Pre-commit hooks and CI/CD

#### Flake8 6.0.0+
- **Purpose**: Code linting and style checking
- **Rules**: PEP 8 compliance with custom exceptions
- **Integration**: Development workflow and CI/CD

#### Type Checking (Optional)
- **mypy**: Static type checking
- **Type hints**: Comprehensive type annotations
- **Protocols**: Interface definitions

## DevOps and Deployment

### Containerization

#### Docker 24.0+
- **Purpose**: Application containerization
- **Base Images**:
  - `python:3.12-slim`: Application container
  - `mongo:7-jammy`: MongoDB container
  - `chromadb/chroma:latest`: ChromaDB container
  - `nginx:alpine`: Reverse proxy

**Multi-stage Builds**:
- Development stage with debugging tools
- Production stage with optimized size
- Testing stage with test dependencies

#### Docker Compose 2.20+
- **Purpose**: Multi-container orchestration
- **Configurations**:
  - `docker-compose.yml`: Production deployment
  - `docker-compose.dev.yml`: Development environment
  - `docker-compose.containers.yml`: Full stack with databases

### CI/CD Pipeline

#### Jenkins
- **Purpose**: Continuous integration and deployment
- **Pipeline Stages**:
  - Code quality checks
  - Automated testing
  - Security scanning
  - Docker image building
  - Deployment automation

**Pipeline Configuration**:
- Jenkinsfile with declarative syntax
- Parallel test execution
- Artifact management
- Deployment strategies

#### GitHub Actions (Alternative)
- **Purpose**: Alternative CI/CD platform
- **Workflows**:
  - Pull request validation
  - Automated testing
  - Security scanning
  - Release automation

## Monitoring and Observability

### Logging

#### Python Logging
- **Purpose**: Application logging
- **Configuration**: Structured JSON logging
- **Levels**: DEBUG, INFO, WARNING, ERROR, CRITICAL
- **Handlers**: File, console, and external systems

#### Log Aggregation (Optional)
- **ELK Stack**: Elasticsearch, Logstash, Kibana
- **Fluentd**: Log collection and forwarding
- **Grafana Loki**: Log aggregation and querying

### Metrics and Monitoring

#### Prometheus (Optional)
- **Purpose**: Metrics collection and alerting
- **Client**: `prometheus_client`
- **Metrics Types**:
  - Counters: Request counts, error counts
  - Histograms: Response times, processing duration
  - Gauges: Active sessions, memory usage

#### Grafana (Optional)
- **Purpose**: Metrics visualization and dashboards
- **Data Sources**: Prometheus, InfluxDB
- **Dashboards**: Application performance, system health

### Health Checks
- **Built-in**: `/health` endpoint
- **Docker**: Container health checks
- **External**: Uptime monitoring services

## Security Technologies

### Authentication and Authorization

#### JWT (Optional)
- **Library**: `PyJWT`
- **Purpose**: Token-based authentication
- **Features**: Token generation, validation, refresh

#### OAuth2 (Optional)
- **Library**: `authlib`
- **Providers**: Google, GitHub, Microsoft
- **Purpose**: Third-party authentication

### Security Headers
- **Flask-Talisman**: Security headers middleware
- **CORS**: Cross-origin resource sharing
- **CSP**: Content Security Policy
- **HSTS**: HTTP Strict Transport Security

### Encryption
- **cryptography**: Encryption library
- **bcrypt**: Password hashing
- **secrets**: Secure random generation

## Performance Optimization

### Caching

#### Redis (Optional)
- **Purpose**: Caching and session storage
- **Client**: `redis-py`
- **Use Cases**:
  - API response caching
  - Session storage
  - Rate limiting
  - Background job queues

#### Memory Caching
- **functools.lru_cache**: Function result caching
- **Custom caching**: Application-specific caching

### Async Processing

#### Celery (Optional)
- **Purpose**: Distributed task queue
- **Broker**: Redis or RabbitMQ
- **Use Cases**:
  - Background PDF processing
  - Batch operations
  - Scheduled tasks

## External Services

### AI Provider APIs
- **Anthropic Claude API**: Primary AI service
- **OpenAI API**: Alternative AI service
- **OpenRouter API**: Multi-model access

### Cloud Services (Optional)
- **AWS S3**: File storage
- **Google Cloud Storage**: File storage
- **Azure Blob Storage**: File storage

### Monitoring Services (Optional)
- **Sentry**: Error tracking and performance monitoring
- **DataDog**: Application performance monitoring
- **New Relic**: Full-stack observability

## Development Tools

### IDE and Editors
- **VS Code**: Recommended IDE with Python extension
- **PyCharm**: Professional Python IDE
- **Vim/Neovim**: Terminal-based editing

### Version Control
- **Git**: Source code management
- **GitHub**: Repository hosting and collaboration
- **Git LFS**: Large file storage (for test PDFs)

### Package Management
- **pip**: Python package installer
- **venv**: Virtual environment management
- **requirements.txt**: Dependency specification

## System Requirements

### Minimum Requirements
- **CPU**: 2 cores
- **RAM**: 2GB
- **Storage**: 4GB
- **Network**: Stable internet connection for AI APIs

### Recommended Requirements
- **CPU**: 4+ cores
- **RAM**: 8GB+
- **Storage**: 20GB+ SSD
- **Network**: High-speed internet for optimal AI performance

### Production Requirements
- **CPU**: 8+ cores
- **RAM**: 16GB+
- **Storage**: 100GB+ SSD with backup
- **Network**: Redundant internet connections
- **Monitoring**: Comprehensive observability stack

## Version Compatibility

### Python Versions
- **Supported**: 3.11, 3.12
- **Recommended**: 3.12.0+
- **Not Supported**: <3.11

### Database Versions
- **MongoDB**: 5.0+ (recommended 7.0+)
- **ChromaDB**: 0.4.0+ (recommended latest)

### Docker Versions
- **Docker Engine**: 20.10+ (recommended 24.0+)
- **Docker Compose**: 2.0+ (recommended 2.20+)

This technology stack provides a robust, scalable foundation for the RPGer Content Extractor, balancing modern capabilities with proven reliability.
