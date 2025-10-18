---
title: API Authentication
description: Authentication and security documentation for the RPGer Content Extractor API
tags: [api, authentication, security, authorization]
last_updated: 2025-10-18
author: HL-Auggie Analysis System
---

# API Authentication

## Overview

The RPGer Content Extractor API currently operates in development mode without authentication requirements for local deployments. This document outlines the current security model and recommendations for production deployments.

## Current Security Model

### Local Development
- **No Authentication Required**: All endpoints are accessible without authentication
- **Local Access Only**: Default configuration binds to localhost (127.0.0.1)
- **File Upload Restrictions**: 200MB maximum file size limit
- **File Type Validation**: Only PDF files are accepted for upload

### Network Access
When configured for network access (0.0.0.0 binding):
- **Open Access**: All endpoints remain accessible without authentication
- **IP-based Restrictions**: Consider implementing firewall rules
- **Reverse Proxy**: Recommended to use nginx or similar for SSL termination

## Production Security Recommendations

### 1. API Key Authentication

For production deployments, implement API key authentication:

```python
# Example implementation
from functools import wraps
from flask import request, jsonify
import os

def require_api_key(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        api_key = request.headers.get('X-API-Key')
        if not api_key or api_key != os.getenv('API_KEY'):
            return jsonify({'error': 'Invalid or missing API key'}), 401
        return f(*args, **kwargs)
    return decorated_function

# Apply to protected endpoints
@app.route('/api/extract')
@require_api_key
def extract_content():
    # Protected endpoint logic
    pass
```

**Usage**:
```bash
curl -X POST http://localhost:5000/api/extract \
  -H "X-API-Key: your-secret-api-key" \
  -H "Content-Type: application/json" \
  -d '{"filepath": "/path/to/file.pdf"}'
```

### 2. JWT Token Authentication

For more sophisticated authentication:

```python
import jwt
from datetime import datetime, timedelta

def generate_token(user_id):
    payload = {
        'user_id': user_id,
        'exp': datetime.utcnow() + timedelta(hours=24)
    }
    return jwt.encode(payload, os.getenv('JWT_SECRET'), algorithm='HS256')

def verify_token(token):
    try:
        payload = jwt.decode(token, os.getenv('JWT_SECRET'), algorithms=['HS256'])
        return payload['user_id']
    except jwt.ExpiredSignatureError:
        return None
    except jwt.InvalidTokenError:
        return None

def require_jwt(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        token = request.headers.get('Authorization', '').replace('Bearer ', '')
        user_id = verify_token(token)
        if not user_id:
            return jsonify({'error': 'Invalid or expired token'}), 401
        request.user_id = user_id
        return f(*args, **kwargs)
    return decorated_function
```

**Usage**:
```bash
# Login to get token
curl -X POST http://localhost:5000/auth/login \
  -H "Content-Type: application/json" \
  -d '{"username": "user", "password": "pass"}'

# Use token for API calls
curl -X POST http://localhost:5000/api/extract \
  -H "Authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9..." \
  -H "Content-Type: application/json" \
  -d '{"filepath": "/path/to/file.pdf"}'
```

### 3. OAuth2 Integration

For enterprise deployments, consider OAuth2 integration:

```python
from authlib.integrations.flask_oauth2 import ResourceProtector
from authlib.oauth2.rfc6750 import BearerTokenValidator

class MyBearerTokenValidator(BearerTokenValidator):
    def authenticate_token(self, token_string):
        # Validate token with OAuth2 provider
        return validate_oauth_token(token_string)

require_oauth = ResourceProtector()
require_oauth.register_token_validator(MyBearerTokenValidator())

@app.route('/api/extract')
@require_oauth()
def extract_content():
    # OAuth2 protected endpoint
    pass
```

## Rate Limiting

### Implementation Example

```python
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address

limiter = Limiter(
    app,
    key_func=get_remote_address,
    default_limits=["200 per day", "50 per hour"]
)

@app.route('/api/extract')
@limiter.limit("5 per minute")
def extract_content():
    # Rate limited endpoint
    pass
```

### Rate Limit Headers

Implement standard rate limit headers:

```python
@app.after_request
def after_request(response):
    # Add rate limit headers
    response.headers['X-RateLimit-Limit'] = '50'
    response.headers['X-RateLimit-Remaining'] = '45'
    response.headers['X-RateLimit-Reset'] = '1640995200'
    return response
```

## CORS Configuration

For web application integration:

```python
from flask_cors import CORS

# Configure CORS
CORS(app, origins=[
    'https://yourdomain.com',
    'https://app.yourdomain.com'
])

# Or for development
CORS(app, origins=['http://localhost:3000'])
```

## Input Validation and Sanitization

### File Upload Security

```python
import os
from werkzeug.utils import secure_filename

ALLOWED_EXTENSIONS = {'pdf'}
MAX_FILE_SIZE = 200 * 1024 * 1024  # 200MB

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def validate_file_upload(file):
    if not file or file.filename == '':
        return False, "No file selected"
    
    if not allowed_file(file.filename):
        return False, "Only PDF files are allowed"
    
    # Check file size (if possible)
    file.seek(0, os.SEEK_END)
    size = file.tell()
    file.seek(0)
    
    if size > MAX_FILE_SIZE:
        return False, f"File too large. Maximum size is {MAX_FILE_SIZE // (1024*1024)}MB"
    
    return True, "Valid file"

@app.route('/upload', methods=['POST'])
def upload_file():
    file = request.files.get('file')
    valid, message = validate_file_upload(file)
    
    if not valid:
        return jsonify({'error': message}), 400
    
    # Secure filename
    filename = secure_filename(file.filename)
    # Process file...
```

### Request Validation

```python
from marshmallow import Schema, fields, ValidationError

class ExtractRequestSchema(Schema):
    filepath = fields.Str(required=True)
    ai_provider = fields.Str(required=True, validate=lambda x: x in ['anthropic', 'openai', 'openrouter', 'mock'])
    ai_model = fields.Str(missing=None)
    game_type = fields.Str(required=True)
    edition = fields.Str(required=True)
    content_type = fields.Str(missing='source_material')

@app.route('/api/extract', methods=['POST'])
def extract_content():
    schema = ExtractRequestSchema()
    try:
        data = schema.load(request.json)
    except ValidationError as err:
        return jsonify({'error': 'Validation error', 'details': err.messages}), 400
    
    # Process validated data...
```

## SSL/TLS Configuration

### Production Deployment

```nginx
# nginx configuration
server {
    listen 443 ssl http2;
    server_name api.yourdomain.com;
    
    ssl_certificate /path/to/certificate.crt;
    ssl_certificate_key /path/to/private.key;
    
    ssl_protocols TLSv1.2 TLSv1.3;
    ssl_ciphers ECDHE-RSA-AES256-GCM-SHA512:DHE-RSA-AES256-GCM-SHA512;
    ssl_prefer_server_ciphers off;
    
    location / {
        proxy_pass http://localhost:5000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
```

### Docker SSL Configuration

```yaml
# docker-compose.yml
version: '3.8'
services:
  nginx:
    image: nginx:alpine
    ports:
      - "443:443"
      - "80:80"
    volumes:
      - ./nginx.conf:/etc/nginx/nginx.conf
      - ./ssl:/etc/nginx/ssl
    depends_on:
      - app
  
  app:
    image: rpger-content-extractor
    environment:
      - FLASK_ENV=production
      - API_KEY=${API_KEY}
      - JWT_SECRET=${JWT_SECRET}
```

## Security Headers

```python
@app.after_request
def security_headers(response):
    response.headers['X-Content-Type-Options'] = 'nosniff'
    response.headers['X-Frame-Options'] = 'DENY'
    response.headers['X-XSS-Protection'] = '1; mode=block'
    response.headers['Strict-Transport-Security'] = 'max-age=31536000; includeSubDomains'
    response.headers['Content-Security-Policy'] = "default-src 'self'"
    return response
```

## Audit Logging

```python
import logging
from datetime import datetime

# Configure audit logger
audit_logger = logging.getLogger('audit')
audit_handler = logging.FileHandler('audit.log')
audit_formatter = logging.Formatter('%(asctime)s - %(message)s')
audit_handler.setFormatter(audit_formatter)
audit_logger.addHandler(audit_handler)
audit_logger.setLevel(logging.INFO)

def log_api_access(endpoint, user_id=None, ip_address=None):
    audit_logger.info(f"API_ACCESS - Endpoint: {endpoint}, User: {user_id}, IP: {ip_address}")

@app.before_request
def log_request():
    log_api_access(
        endpoint=request.endpoint,
        user_id=getattr(request, 'user_id', None),
        ip_address=request.remote_addr
    )
```

## Environment Variables

For production security configuration:

```bash
# .env file
API_KEY=your-secret-api-key-here
JWT_SECRET=your-jwt-secret-key-here
FLASK_SECRET_KEY=your-flask-secret-key-here
DATABASE_URL=your-secure-database-url
ALLOWED_ORIGINS=https://yourdomain.com,https://app.yourdomain.com
RATE_LIMIT_STORAGE_URL=redis://localhost:6379
```

## Security Checklist

- [ ] Implement authentication for production deployments
- [ ] Configure rate limiting to prevent abuse
- [ ] Set up CORS for web application integration
- [ ] Validate and sanitize all input data
- [ ] Use HTTPS/SSL for all communications
- [ ] Implement security headers
- [ ] Set up audit logging
- [ ] Configure proper file upload restrictions
- [ ] Use environment variables for sensitive configuration
- [ ] Regular security updates and dependency scanning
