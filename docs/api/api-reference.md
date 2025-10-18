---
title: API Reference
description: Complete REST API documentation for RPGer Content Extractor
tags: [api, rest, endpoints, reference]
last_updated: 2025-10-18
author: HL-Auggie Analysis System
---

# API Reference

## Overview

The RPGer Content Extractor provides a comprehensive REST API for programmatic access to all system functionality. The API is built on Flask and provides endpoints for PDF processing, content analysis, database management, and system monitoring.

**Base URL**: `http://localhost:5000` (default)

## Authentication

Currently, the API does not require authentication for local deployments. For production deployments, consider implementing API key authentication or OAuth2.

## Core Endpoints

### Health & Status

#### GET /health
Health check endpoint for monitoring and CI/CD.

**Response**:
```json
{
  "status": "healthy",
  "timestamp": "2025-10-18T10:30:00.000Z",
  "version": "v1.0.44",
  "environment": "production"
}
```

#### GET /api/version
Get application version information.

**Response**:
```json
{
  "version": "v1.0.44",
  "build_date": "2025-10-18",
  "commit_hash": "abc123",
  "branch": "main",
  "environment": "production"
}
```

#### GET /api/status
Get comprehensive system status including databases and AI providers.

**Response**:
```json
{
  "chroma_status": {
    "connected": true,
    "collections": 5
  },
  "mongodb_status": {
    "connected": true,
    "collections": 3
  },
  "ai_providers": {
    "available": ["anthropic", "openai", "openrouter"],
    "configured": ["anthropic", "openrouter"]
  },
  "active_sessions": 2,
  "completed_extractions": 15,
  "token_tracking": {
    "total_sessions": 10,
    "total_cost": 2.45
  }
}
```

### AI Provider Management

#### GET /api/providers/available
Get list of AI providers with configured API keys.

**Response**:
```json
{
  "success": true,
  "available_providers": ["anthropic", "openrouter", "mock"],
  "total_providers": 3
}
```

#### GET /api/openrouter/models
Get available OpenRouter models for selection.

**Query Parameters**:
- `refresh` (boolean): Force refresh model cache
- `group` (boolean): Group models by provider

**Response**:
```json
{
  "success": true,
  "models": [
    {
      "id": "anthropic/claude-3-sonnet",
      "name": "Claude 3 Sonnet",
      "provider": "Anthropic",
      "type": "option"
    }
  ],
  "recommended": ["anthropic/claude-3-sonnet"],
  "total_models": 150,
  "cache_info": {
    "cached": true,
    "cache_age": 3600
  }
}
```

### PDF Processing

#### POST /upload
Upload a PDF file for processing.

**Content-Type**: `multipart/form-data`

**Form Data**:
- `file`: PDF file (max 200MB)

**Response**:
```json
{
  "success": true,
  "filename": "document.pdf",
  "filepath": "/tmp/uploads/document.pdf",
  "size": 1024000,
  "pages": 150
}
```

#### POST /analyze
Analyze PDF content using AI.

**Request Body**:
```json
{
  "filepath": "/tmp/uploads/document.pdf",
  "ai_provider": "anthropic",
  "ai_model": "claude-3-sonnet",
  "content_type": "source_material",
  "run_confidence_test": false
}
```

**Response**:
```json
{
  "success": true,
  "analysis": {
    "game_type": "D&D",
    "edition": "5th Edition",
    "content_type": "source_material",
    "confidence": 0.95,
    "categories": ["spells", "classes", "equipment"]
  },
  "processing_time": 45.2,
  "token_usage": {
    "input_tokens": 15000,
    "output_tokens": 500,
    "cost": 0.25
  }
}
```

#### POST /extract
Extract content from analyzed PDF.

**Request Body**:
```json
{
  "filepath": "/tmp/uploads/document.pdf",
  "ai_provider": "anthropic",
  "ai_model": "claude-3-sonnet",
  "game_type": "D&D",
  "edition": "5th Edition",
  "content_type": "source_material"
}
```

**Response**:
```json
{
  "success": true,
  "extraction": {
    "total_sections": 25,
    "extracted_content": {
      "spells": [...],
      "classes": [...],
      "equipment": [...]
    },
    "metadata": {
      "title": "Player's Handbook",
      "author": "Wizards of the Coast",
      "pages": 320
    }
  },
  "processing_time": 120.5,
  "output_files": {
    "json": "/tmp/output/extraction.json",
    "chromadb": "/tmp/output/chromadb.json"
  }
}
```

### Database Operations

#### POST /import_chromadb
Import extracted content to ChromaDB.

**Request Body**:
```json
{
  "filepath": "/tmp/output/chromadb.json",
  "collection_name": "dnd_5e_source"
}
```

**Response**:
```json
{
  "success": true,
  "collection_name": "dnd_5e_source",
  "documents_imported": 150,
  "processing_time": 30.2
}
```

#### POST /import_mongodb
Import extracted content to MongoDB.

**Request Body**:
```json
{
  "filepath": "/tmp/output/extraction.json",
  "collection_name": "dnd_5e_content"
}
```

**Response**:
```json
{
  "success": true,
  "collection_name": "dnd_5e_content",
  "documents_imported": 150,
  "processing_time": 25.8
}
```

### Database Browsing

#### GET /browse_chromadb
List all ChromaDB collections.

**Response**:
```json
{
  "success": true,
  "collections": [
    {
      "name": "dnd_5e_source",
      "document_count": 150,
      "game_type": "D&D"
    }
  ],
  "total_collections": 5
}
```

#### GET /browse_chromadb/{collection_name}
Browse specific ChromaDB collection.

**Query Parameters**:
- `limit` (int): Number of documents to return (default: 10)
- `offset` (int): Offset for pagination (default: 0)

**Response**:
```json
{
  "success": true,
  "collection_name": "dnd_5e_source",
  "documents": [
    {
      "id": "doc_001",
      "content": "Spell description...",
      "metadata": {
        "category": "spells",
        "level": 3
      }
    }
  ],
  "total_documents": 150,
  "pagination": {
    "limit": 10,
    "offset": 0,
    "has_more": true
  }
}
```

#### GET /browse_mongodb
List all MongoDB collections.

**Response**:
```json
{
  "success": true,
  "collections": [
    {
      "name": "dnd_5e_content",
      "document_count": 150,
      "game_type": "D&D"
    }
  ],
  "total_collections": 3
}
```

## Error Handling

All API endpoints return consistent error responses:

```json
{
  "error": "Error description",
  "code": "ERROR_CODE",
  "timestamp": "2025-10-18T10:30:00.000Z"
}
```

### Common HTTP Status Codes

- `200 OK`: Successful request
- `400 Bad Request`: Invalid request parameters
- `404 Not Found`: Resource not found
- `413 Payload Too Large`: File size exceeds 200MB limit
- `500 Internal Server Error`: Server error

## Rate Limiting

Currently no rate limiting is implemented. For production deployments, consider implementing rate limiting based on IP address or API key.

## WebSocket Support

Real-time updates for long-running operations are provided through WebSocket connections for progress tracking during PDF processing and extraction.

## SDK and Client Libraries

Currently, no official SDKs are available. The API follows REST conventions and can be easily integrated with any HTTP client library.
