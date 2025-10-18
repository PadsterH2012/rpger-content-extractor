---
title: Quick Start Guide - RPGer Content Extractor
description: Get RPGer Content Extractor up and running in under 5 minutes
tags: [quick-start, setup, installation, getting-started]
last_updated: 2025-10-18
author: HL-Auggie Analysis System
---

# Quick Start Guide

Get RPGer Content Extractor up and running in under 5 minutes!

## 5-Minute Setup

### Step 1: Install (30 seconds)

```bash
# One command installation
curl -sSL https://raw.githubusercontent.com/PadsterH2012/rpger-content-extractor/main/install.sh | bash
cd rpger-extractor
```

### Step 2: Choose Your Mode (1 minute)

#### Quick Demo (Full Stack)
Perfect for trying out the application:

```bash
./start-fullstack.sh
```
- Everything included (databases, app)
- No external setup required
- Ready in ~2 minutes

#### Production Setup
For real usage with your own databases:

```bash
# Edit configuration
nano .env

# Add your database URLs:
# MONGODB_URL=mongodb://your-host:27017
# CHROMADB_URL=http://your-host:8000

./start-production.sh
```

### Step 3: Access the Application (30 seconds)

Open your browser and navigate to:
- **Web Interface**: http://localhost:5000
- **Health Check**: http://localhost:5000/health

You should see the RPGer Content Extractor dashboard!

## First Steps

### 1. Check System Status

Navigate to the **System Status** section to verify:
- AI Provider connection
- Database connections (MongoDB & ChromaDB)
- Available models

### 2. Configure AI Provider (Optional)

For AI-powered content analysis:

1. Go to **Settings** → **AI Providers**
2. Add API keys for your preferred provider:
   - **OpenRouter**: 300+ models (recommended for variety)
   - **Anthropic Claude**: Best for reasoning and analysis
   - **OpenAI**: GPT models for general use

### 3. Upload Your First PDF

1. Navigate to **Upload** section
2. Select an RPG PDF file (rulebook, adventure, supplement)
3. Choose processing options:
   - **Content Type**: Rulebook, Adventure, Supplement
   - **Game System**: D&D 5e, Pathfinder, etc.
   - **AI Analysis**: Enable for smart categorization

4. Click **Upload & Process**

### 4. Explore Extracted Content

Once processing completes:
- **Browse** extracted content by category
- **Search** using natural language queries
- **Export** content in various formats
- **Organize** into collections

## Configuration Essentials

### Database URLs (Production Mode)

Edit `.env` file with your database connections:

```bash
# MongoDB - for document storage
MONGODB_URL=mongodb://localhost:27017

# ChromaDB - for vector search
CHROMADB_URL=http://localhost:8000
```

### AI Provider Setup

Add API keys to enable AI features:

```bash
# Choose one or more providers
ANTHROPIC_API_KEY=sk-ant-api03-...
OPENAI_API_KEY=sk-...
OPENROUTER_API_KEY=sk-or-v1-...
```

### Performance Tuning

Adjust based on your system:

```bash
# Upload limits
MAX_CONTENT_LENGTH=200  # MB
UPLOAD_TIMEOUT=300      # seconds

# Processing
WORKERS=1               # CPU cores to use
LOG_LEVEL=INFO         # DEBUG for troubleshooting
```

## Understanding the Interface

### Dashboard Overview

The main dashboard shows:
- **System Status**: Health of all components
- **Recent Activity**: Latest uploads and processing
- **Quick Actions**: Common tasks and shortcuts
- **Statistics**: Usage metrics and insights

### Navigation Menu

| Section | Purpose |
|---------|---------|
| **Upload** | Add new PDF files for processing |
| **Library** | Browse and search extracted content |
| **Collections** | Organize content into groups |
| **Search** | Advanced search with filters |
| **Settings** | Configure AI providers and preferences |
| **Admin** | System management and monitoring |

### Content Types

RPGer Content Extractor recognizes:
- **Rules**: Game mechanics, character creation, combat
- **Lore**: World building, history, cultures
- **Adventures**: Scenarios, encounters, plot hooks
- **NPCs**: Characters, stats, descriptions
- **Items**: Equipment, magic items, artifacts
- **Spells**: Magic systems, spell descriptions
- **Monsters**: Creatures, stats, abilities

## Common Workflows

### Workflow 1: Processing a Rulebook

1. **Upload** the PDF with "Rulebook" content type
2. **Enable AI analysis** for automatic categorization
3. **Wait** for processing (5-15 minutes depending on size)
4. **Review** extracted content in the Library
5. **Organize** into collections by chapter/topic
6. **Search** for specific rules or mechanics

### Workflow 2: Adventure Preparation

1. **Upload** adventure PDF
2. **Extract** NPCs, locations, and encounters
3. **Create collection** for the adventure
4. **Export** key information for quick reference
5. **Use search** to find related content from other sources

### Workflow 3: Building a Campaign

1. **Upload** multiple sourcebooks
2. **Create collections** by theme or location
3. **Use semantic search** to find related content
4. **Export** compiled information
5. **Track** what content you've used

## 🔍 Troubleshooting Quick Fixes

### Application Won't Start

```bash
# Check Docker is running
docker --version
docker compose --version

# Check ports aren't in use
netstat -tulpn | grep :5000

# View logs
docker compose logs app
```

### Upload Fails

```bash
# Check file size (default limit: 200MB)
ls -lh your-file.pdf

# Check disk space
df -h

# Increase limits in .env
MAX_CONTENT_LENGTH=500
```

### AI Processing Fails

```bash
# Verify API keys in .env
grep API_KEY .env

# Check AI provider status in web interface
curl http://localhost:5000/api/providers/status

# Try different model
# Go to Settings → AI Providers → Change Model
```

### Database Connection Issues

```bash
# Test MongoDB connection
docker compose exec app python -c "import pymongo; print(pymongo.MongoClient('mongodb://mongodb:27017').admin.command('ping'))"

# Test ChromaDB connection
curl http://localhost:8000/api/v1/heartbeat
```

## Next Steps

### Learn More
- **[Web Interface Guide](user-guides/web-interface-guide.md)** - Detailed UI walkthrough
- **[PDF Processing Guide](user-guides/pdf-processing-guide.md)** - Advanced processing options
- **[Environment Configuration](deployment/environment-configuration.md)** - Detailed AI configuration

### Advanced Usage
- **[API Documentation](api/api-reference.md)** - REST API reference
- **[Content Management Guide](user-guides/content-management-guide.md)** - Organization strategies
- **[Development Setup](development/development-setup.md)** - Contributing to the project

### Get Help
- **[Troubleshooting Guide](operations/troubleshooting-guide.md)** - Troubleshooting guide
- **[Documentation Index](index.md)** - Complete documentation
- **[GitHub Issues](https://github.com/PadsterH2012/rpger-content-extractor/issues)** - Report problems

---

**Congratulations!** You now have RPGer Content Extractor running and ready to process your RPG content. Start by uploading a PDF and exploring the extracted content!
