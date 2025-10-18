---
title: Installation Guide - RPGer Content Extractor
description: Comprehensive installation guide for all deployment modes
tags: [installation, setup, deployment, docker, configuration]
last_updated: 2025-10-18
author: HL-Auggie Analysis System
---

# Installation Guide

This guide covers all installation methods for RPGer Content Extractor, from quick one-line setup to advanced configurations.

## 🚀 Quick Installation

### ⚡ One-Line Install (Recommended)

The fastest way to get started:

```bash
# Automatic installation with Production defaults
curl -sSL https://raw.githubusercontent.com/PadsterH2012/rpger-content-extractor/main/install.sh | bash

# Navigate to installation directory
cd rpger-extractor

# Start the application
./start-production.sh
```

**What this does:**
- ✅ Downloads all necessary Docker Compose files
- ✅ Creates `/rpger-extractor/` directory
- ✅ Configures Production mode with external databases
- ✅ Generates startup scripts for all deployment modes
- ✅ Creates `.env` file with default settings

### 🎯 Interactive Installation

For full control over configuration:

```bash
# Download the installer
wget https://raw.githubusercontent.com/PadsterH2012/rpger-content-extractor/main/install.sh
chmod +x install.sh

# Run interactive installer
./install.sh
```

**Interactive features:**
- 🎯 Choose deployment mode (Production/Development/Full Stack)
- 🔧 Configure database URLs (MongoDB/ChromaDB)
- 🔑 Set up AI provider API keys
- 🛡️ Safe .env handling (preserves existing files)

## 📋 Prerequisites

### System Requirements

| Component | Requirement |
|-----------|-------------|
| **Docker** | Latest version |
| **Docker Compose** | v2.0+ (plugin or standalone) |
| **RAM** | 500MB+ (Production), 2GB+ (Full Stack) |
| **Storage** | 1GB+ (Production), 4GB+ (Full Stack) |
| **Network** | Internet access for Docker images |

### External Services (Production/Development)

| Service | Purpose | Example |
|---------|---------|---------|
| **MongoDB** | Document storage | `mongodb://localhost:27017` |
| **ChromaDB** | Vector database | `http://localhost:8000` |

## 🐳 Deployment Options

### 🚀 Production Mode (Recommended)

**Best for**: Production deployments, quick testing

```bash
# Using install script
./start-production.sh

# Manual setup
docker compose up -d
```

**Features:**
- ✅ Pre-built Docker images (v1.0.44)
- ✅ Minimal resource usage (~200MB RAM)
- ✅ Fast startup (no build time)
- ✅ Requires external MongoDB & ChromaDB

### 🛠️ Development Mode

**Best for**: Local development, code changes

```bash
# Using install script
./start-development.sh

# Manual setup
docker compose -f docker-compose.dev.yml up -d --build
```

**Features:**
- ✅ Builds from source with live reloading
- ✅ Code changes reflected immediately
- ✅ Development environment variables
- ✅ Requires external MongoDB & ChromaDB

### 🗄️ Full Stack Mode

**Best for**: Self-contained testing, demos

```bash
# Using install script
./start-fullstack.sh

# Manual setup
docker compose -f docker-compose.yml -f docker-compose.containers.yml up -d
```

**Features:**
- ✅ Includes MongoDB & ChromaDB containers
- ✅ Self-contained (no external dependencies)
- ✅ Higher resource usage (~2GB RAM)
- ✅ Complete testing environment

## ⚙️ Configuration

### Environment Variables

The `.env` file contains all configuration options:

```bash
# Flask Configuration
FLASK_ENV=production
MAX_CONTENT_LENGTH=200
UPLOAD_TIMEOUT=300

# Database Configuration
MONGODB_URL=mongodb://localhost:27017
CHROMADB_URL=http://localhost:8000

# AI Provider API Keys (Optional)
ANTHROPIC_API_KEY=your_claude_api_key
OPENAI_API_KEY=your_openai_api_key
OPENROUTER_API_KEY=your_openrouter_api_key

# Advanced Configuration
LOG_LEVEL=INFO
WORKERS=1
```

### Database Setup

#### MongoDB Setup
```bash
# Using Docker
docker run -d --name mongodb -p 27017:27017 mongo:7-jammy

# Using MongoDB Atlas (cloud)
MONGODB_URL=mongodb+srv://username:password@cluster.mongodb.net/rpger
```

#### ChromaDB Setup
```bash
# Using Docker
docker run -d --name chromadb -p 8000:8000 chromadb/chroma:latest

# Using hosted ChromaDB
CHROMADB_URL=http://your-chromadb-host:8000
```

## 🔧 Post-Installation

### Verify Installation

```bash
# Check services are running
docker compose ps

# Check application health
curl http://localhost:5000/health

# View logs
docker compose logs -f app
```

### Access the Application

- **Web Interface**: http://localhost:5000
- **Health Check**: http://localhost:5000/health
- **API Documentation**: http://localhost:5000/api/docs

### Configure AI Providers

1. Navigate to Settings in the web interface
2. Add your API keys for desired providers:
   - **Anthropic Claude**: For advanced reasoning
   - **OpenAI**: For GPT models
   - **OpenRouter**: For 300+ model access

## 🛠️ Management Commands

### Start/Stop Services

```bash
# Start (choose your mode)
./start-production.sh     # Production mode
./start-development.sh    # Development mode
./start-fullstack.sh      # Full stack mode

# Stop all services
./stop.sh

# Restart
./stop.sh && ./start-production.sh
```

### Update to Latest Version

```bash
# Pull latest images
docker compose pull

# Restart with new images
docker compose up -d
```

### Backup Data

```bash
# Backup MongoDB (if using Full Stack)
docker compose exec mongodb mongodump --out /backup

# Backup ChromaDB (if using Full Stack)
docker compose exec chromadb cp -r /chroma/chroma /backup
```

## 🔍 Troubleshooting

### Common Issues

| Issue | Solution |
|-------|----------|
| **Port conflicts** | Change ports in `docker-compose.yml` |
| **Permission denied** | Run with `sudo` or fix Docker permissions |
| **Out of memory** | Increase Docker memory limits |
| **Database connection** | Verify database URLs in `.env` |

### Debug Commands

```bash
# Check Docker Compose version
docker compose version

# View detailed logs
docker compose logs --tail=100 app

# Check container status
docker compose ps -a

# Inspect container
docker compose exec app bash
```

### Getting Help

- **GitHub Issues**: [Report problems](https://github.com/PadsterH2012/rpger-content-extractor/issues)
- **Discussions**: [Community support](https://github.com/PadsterH2012/rpger-content-extractor/discussions)
- **Documentation**: [Full wiki](https://github.com/PadsterH2012/rpger-content-extractor/wiki)

---

**Next Steps**: [Quick Start Guide](Quick-Start.md) | [Configuration Guide](reference/configuration-reference.md)
