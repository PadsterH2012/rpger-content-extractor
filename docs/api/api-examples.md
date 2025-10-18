---
title: API Examples
description: Request/response examples and usage patterns for the RPGer Content Extractor API
tags: [api, examples, usage, integration]
last_updated: 2025-10-18
author: HL-Auggie Analysis System
---

# API Examples

## Overview

This document provides practical examples of using the RPGer Content Extractor API for common workflows and integration patterns.

## Complete Workflow Example

### 1. Upload PDF File

```bash
curl -X POST http://localhost:5000/upload \
  -F "file=@/path/to/dnd_players_handbook.pdf" \
  -H "Content-Type: multipart/form-data"
```

**Response**:
```json
{
  "success": true,
  "filename": "dnd_players_handbook.pdf",
  "filepath": "/tmp/uploads/dnd_players_handbook.pdf",
  "size": 52428800,
  "pages": 320
}
```

### 2. Check Available AI Providers

```bash
curl -X GET http://localhost:5000/api/providers/available
```

**Response**:
```json
{
  "success": true,
  "available_providers": ["anthropic", "openrouter", "mock"],
  "total_providers": 3
}
```

### 3. Analyze PDF Content

```bash
curl -X POST http://localhost:5000/analyze \
  -H "Content-Type: application/json" \
  -d '{
    "filepath": "/tmp/uploads/dnd_players_handbook.pdf",
    "ai_provider": "anthropic",
    "ai_model": "claude-3-sonnet",
    "content_type": "source_material",
    "run_confidence_test": false
  }'
```

**Response**:
```json
{
  "success": true,
  "analysis": {
    "game_type": "D&D",
    "edition": "5th Edition",
    "content_type": "source_material",
    "confidence": 0.98,
    "categories": ["classes", "spells", "equipment", "races"],
    "detected_sections": [
      "Character Creation",
      "Classes",
      "Equipment",
      "Spells",
      "Combat Rules"
    ]
  },
  "processing_time": 42.3,
  "token_usage": {
    "input_tokens": 18500,
    "output_tokens": 650,
    "cost": 0.32
  }
}
```

### 4. Extract Content

```bash
curl -X POST http://localhost:5000/extract \
  -H "Content-Type: application/json" \
  -d '{
    "filepath": "/tmp/uploads/dnd_players_handbook.pdf",
    "ai_provider": "anthropic",
    "ai_model": "claude-3-sonnet",
    "game_type": "D&D",
    "edition": "5th Edition",
    "content_type": "source_material"
  }'
```

**Response**:
```json
{
  "success": true,
  "extraction": {
    "total_sections": 45,
    "extracted_content": {
      "classes": [
        {
          "name": "Fighter",
          "hit_die": "d10",
          "primary_ability": "Strength or Dexterity",
          "saving_throws": ["Strength", "Constitution"]
        }
      ],
      "spells": [
        {
          "name": "Fireball",
          "level": 3,
          "school": "Evocation",
          "casting_time": "1 action",
          "range": "150 feet"
        }
      ]
    },
    "metadata": {
      "title": "Player's Handbook",
      "author": "Wizards of the Coast",
      "pages": 320,
      "isbn": "978-0786965601"
    }
  },
  "processing_time": 185.7,
  "output_files": {
    "json": "/tmp/output/dnd_players_handbook_extraction.json",
    "chromadb": "/tmp/output/dnd_players_handbook_chromadb.json"
  }
}
```

### 5. Import to ChromaDB

```bash
curl -X POST http://localhost:5000/import_chromadb \
  -H "Content-Type: application/json" \
  -d '{
    "filepath": "/tmp/output/dnd_players_handbook_chromadb.json",
    "collection_name": "dnd_5e_source_materials"
  }'
```

**Response**:
```json
{
  "success": true,
  "collection_name": "dnd_5e_source_materials",
  "documents_imported": 245,
  "processing_time": 28.4,
  "collection_info": {
    "total_documents": 245,
    "categories": ["classes", "spells", "equipment", "races"],
    "game_type": "D&D",
    "edition": "5th Edition"
  }
}
```

## Python Integration Example

```python
import requests
import json
from pathlib import Path

class RPGExtractorClient:
    def __init__(self, base_url="http://localhost:5000"):
        self.base_url = base_url
        
    def upload_pdf(self, pdf_path):
        """Upload a PDF file"""
        with open(pdf_path, 'rb') as f:
            files = {'file': f}
            response = requests.post(f"{self.base_url}/upload", files=files)
        return response.json()
    
    def analyze_pdf(self, filepath, ai_provider="anthropic", ai_model="claude-3-sonnet"):
        """Analyze PDF content"""
        data = {
            "filepath": filepath,
            "ai_provider": ai_provider,
            "ai_model": ai_model,
            "content_type": "source_material",
            "run_confidence_test": False
        }
        response = requests.post(f"{self.base_url}/analyze", json=data)
        return response.json()
    
    def extract_content(self, filepath, game_type, edition, ai_provider="anthropic"):
        """Extract content from PDF"""
        data = {
            "filepath": filepath,
            "ai_provider": ai_provider,
            "game_type": game_type,
            "edition": edition,
            "content_type": "source_material"
        }
        response = requests.post(f"{self.base_url}/extract", json=data)
        return response.json()
    
    def import_to_chromadb(self, filepath, collection_name):
        """Import extracted content to ChromaDB"""
        data = {
            "filepath": filepath,
            "collection_name": collection_name
        }
        response = requests.post(f"{self.base_url}/import_chromadb", json=data)
        return response.json()

# Usage example
client = RPGExtractorClient()

# Complete workflow
pdf_path = "dnd_players_handbook.pdf"

# 1. Upload
upload_result = client.upload_pdf(pdf_path)
filepath = upload_result["filepath"]

# 2. Analyze
analysis = client.analyze_pdf(filepath)
game_type = analysis["analysis"]["game_type"]
edition = analysis["analysis"]["edition"]

# 3. Extract
extraction = client.extract_content(filepath, game_type, edition)
chromadb_file = extraction["output_files"]["chromadb"]

# 4. Import
import_result = client.import_to_chromadb(chromadb_file, "dnd_5e_source")

print(f"Successfully processed {pdf_path}")
print(f"Imported {import_result['documents_imported']} documents")
```

## JavaScript/Node.js Integration Example

```javascript
const axios = require('axios');
const FormData = require('form-data');
const fs = require('fs');

class RPGExtractorClient {
    constructor(baseUrl = 'http://localhost:5000') {
        this.baseUrl = baseUrl;
    }
    
    async uploadPdf(pdfPath) {
        const form = new FormData();
        form.append('file', fs.createReadStream(pdfPath));
        
        const response = await axios.post(`${this.baseUrl}/upload`, form, {
            headers: form.getHeaders()
        });
        return response.data;
    }
    
    async analyzePdf(filepath, aiProvider = 'anthropic', aiModel = 'claude-3-sonnet') {
        const data = {
            filepath,
            ai_provider: aiProvider,
            ai_model: aiModel,
            content_type: 'source_material',
            run_confidence_test: false
        };
        
        const response = await axios.post(`${this.baseUrl}/analyze`, data);
        return response.data;
    }
    
    async extractContent(filepath, gameType, edition, aiProvider = 'anthropic') {
        const data = {
            filepath,
            ai_provider: aiProvider,
            game_type: gameType,
            edition,
            content_type: 'source_material'
        };
        
        const response = await axios.post(`${this.baseUrl}/extract`, data);
        return response.data;
    }
    
    async importToChromaDB(filepath, collectionName) {
        const data = {
            filepath,
            collection_name: collectionName
        };
        
        const response = await axios.post(`${this.baseUrl}/import_chromadb`, data);
        return response.data;
    }
}

// Usage example
async function processRPGPdf() {
    const client = new RPGExtractorClient();
    
    try {
        // Upload PDF
        const uploadResult = await client.uploadPdf('dnd_players_handbook.pdf');
        console.log('Upload successful:', uploadResult.filename);
        
        // Analyze content
        const analysis = await client.analyzePdf(uploadResult.filepath);
        console.log('Analysis complete:', analysis.analysis.game_type, analysis.analysis.edition);
        
        // Extract content
        const extraction = await client.extractContent(
            uploadResult.filepath,
            analysis.analysis.game_type,
            analysis.analysis.edition
        );
        console.log('Extraction complete:', extraction.extraction.total_sections, 'sections');
        
        // Import to ChromaDB
        const importResult = await client.importToChromaDB(
            extraction.output_files.chromadb,
            'dnd_5e_source'
        );
        console.log('Import complete:', importResult.documents_imported, 'documents');
        
    } catch (error) {
        console.error('Error processing PDF:', error.response?.data || error.message);
    }
}

processRPGPdf();
```

## Batch Processing Example

```bash
#!/bin/bash
# Batch process multiple PDFs

BASE_URL="http://localhost:5000"
PDF_DIR="/path/to/rpg/pdfs"
COLLECTION_PREFIX="rpg_collection"

for pdf_file in "$PDF_DIR"/*.pdf; do
    echo "Processing: $(basename "$pdf_file")"
    
    # Upload
    upload_response=$(curl -s -X POST "$BASE_URL/upload" -F "file=@$pdf_file")
    filepath=$(echo "$upload_response" | jq -r '.filepath')
    
    # Analyze
    analyze_response=$(curl -s -X POST "$BASE_URL/analyze" \
        -H "Content-Type: application/json" \
        -d "{\"filepath\":\"$filepath\",\"ai_provider\":\"anthropic\"}")
    
    game_type=$(echo "$analyze_response" | jq -r '.analysis.game_type')
    edition=$(echo "$analyze_response" | jq -r '.analysis.edition')
    
    # Extract
    extract_response=$(curl -s -X POST "$BASE_URL/extract" \
        -H "Content-Type: application/json" \
        -d "{\"filepath\":\"$filepath\",\"ai_provider\":\"anthropic\",\"game_type\":\"$game_type\",\"edition\":\"$edition\"}")
    
    chromadb_file=$(echo "$extract_response" | jq -r '.output_files.chromadb')
    
    # Import
    collection_name="${COLLECTION_PREFIX}_$(echo "$game_type" | tr ' ' '_' | tr '[:upper:]' '[:lower:]')"
    curl -s -X POST "$BASE_URL/import_chromadb" \
        -H "Content-Type: application/json" \
        -d "{\"filepath\":\"$chromadb_file\",\"collection_name\":\"$collection_name\"}"
    
    echo "Completed: $(basename "$pdf_file") -> $collection_name"
done
```

## Error Handling Examples

```python
import requests
from requests.exceptions import RequestException

def safe_api_call(url, method='GET', **kwargs):
    """Make API call with proper error handling"""
    try:
        response = requests.request(method, url, **kwargs)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.HTTPError as e:
        if response.status_code == 413:
            print("Error: File too large (max 200MB)")
        elif response.status_code == 400:
            print(f"Error: Bad request - {response.json().get('error', 'Unknown error')}")
        elif response.status_code == 500:
            print(f"Error: Server error - {response.json().get('error', 'Internal server error')}")
        else:
            print(f"HTTP Error {response.status_code}: {e}")
        return None
    except RequestException as e:
        print(f"Request failed: {e}")
        return None

# Example usage
result = safe_api_call("http://localhost:5000/api/status")
if result:
    print("System status:", result)
```

## Monitoring and Health Checks

```bash
# Simple health check script
#!/bin/bash

check_health() {
    response=$(curl -s -w "%{http_code}" http://localhost:5000/health)
    http_code="${response: -3}"
    
    if [ "$http_code" = "200" ]; then
        echo "✅ Service is healthy"
        return 0
    else
        echo "❌ Service is unhealthy (HTTP $http_code)"
        return 1
    fi
}

# Check every 30 seconds
while true; do
    check_health
    sleep 30
done
```
