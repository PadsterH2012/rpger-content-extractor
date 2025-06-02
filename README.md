# 🎮 RPGer Content Extractor

**AI-Powered Multi-Game RPG PDF Content Extraction & Management System**

A dockerized solution for extracting, categorizing, and managing RPG content from PDF sources with dual deployment options.

## 🚀 Quick Start

### ⚡ Quick Install

#### 🚀 **One-Line Install (Auto-mode)**
```bash
# Automatic installation with Production defaults
curl -sSL https://raw.githubusercontent.com/PadsterH2012/rpger-content-extractor/main/install.sh | bash

# Navigate to installation directory
cd rpger-extractor

# Start production mode
./start-production.sh
```

#### 🎯 **Interactive Install (Full Setup)**
```bash
# Download and run for interactive configuration
wget https://raw.githubusercontent.com/PadsterH2012/rpger-content-extractor/main/install.sh
chmod +x install.sh
./install.sh

# Navigate to installation directory
cd rpger-extractor

# Start your chosen deployment mode
./start-production.sh    # 🚀 Production (pre-built images)
./start-development.sh   # 🛠️ Development (build from source)
./start-fullstack.sh     # 🗄️ Full Stack (includes databases)

# Stop all services
./stop.sh

# Check status and logs
docker compose ps
docker compose logs -f app
```

**Installer Features:**
- 🎯 **Interactive menu** - Choose Production/Development/Full Stack
- 🔧 **Auto-configuration** - Database URLs and API keys setup
- 📁 **Clean installation** - Creates `/rpger-extractor/` directory
- 🛡️ **Safe .env handling** - Backs up existing, creates new if missing
- 🚀 **Ready-to-run scripts** - Start/stop scripts for each mode
- ✅ **Dependency checking** - Verifies Docker & Docker Compose
- 🎨 **Beautiful UI** - Colored output with progress indicators

### 🎯 Manual Production Setup
Use pre-built Docker images - **Latest: v1.0.44**

```bash
# Download docker-compose.yml only
curl -O https://raw.githubusercontent.com/PadsterH2012/rpger-content-extractor/main/docker-compose.yml

# Start with latest stable image
docker-compose up -d

# Access web UI
open http://localhost:5000
```

### 🛠️ Development
Full source code with live reloading

```bash
# Clone repository
git clone https://github.com/PadsterH2012/rpger-content-extractor.git
cd rpger-content-extractor

# Start development environment
docker-compose -f docker-compose.dev.yml up -d

# Access web UI
open http://localhost:5000
```

### 🗄️ Full Stack (with Databases)
Complete setup including MongoDB and ChromaDB

```bash
# Clone repository (if not already done)
git clone https://github.com/PadsterH2012/rpger-content-extractor.git
cd rpger-content-extractor

# Start complete stack
docker-compose -f docker-compose.yml -f docker-compose.containers.yml up -d

# Access web UI
open http://localhost:5000
```

## 🏗️ Architecture

### Three Deployment Options

#### 🚀 Production (Pre-built Images)
- **App Container**: Uses CI/CD built images (v1.0.44)
- **External Databases**: Connect to your MongoDB/ChromaDB
- **Resource Usage**: ~200MB RAM, 500MB storage
- **Best For**: Production deployments, quick testing

#### 🛠️ Development (Build from Source)
- **App Container**: Built locally with live code reloading
- **External Databases**: Connect to your MongoDB/ChromaDB
- **Resource Usage**: ~300MB RAM, 1GB storage
- **Best For**: Local development, code changes

#### 🗄️ Full Stack (Complete Environment)
- **App Container**: Flask web UI + processing engine
- **MongoDB Container**: Document database for extracted content
- **ChromaDB Container**: Vector database for semantic search
- **Resource Usage**: ~1.5GB RAM, 2GB storage
- **Best For**: Self-contained testing, demos

## 🎯 Features

- **Multi-Game Support**: D&D, Pathfinder, Call of Cthulhu, and more
- **AI-Powered Detection**: Automatic game type and edition detection
- **Smart Categorization**: AI-driven content classification
- **Dual Database Storage**: MongoDB for documents, ChromaDB for vectors
- **Web Interface**: User-friendly upload and management UI
- **Docker Ready**: Both container stack and external DB modes
- **Health Monitoring**: Built-in health checks and monitoring

## 📋 Requirements

### 🚀 Production Mode
- Docker & Docker Compose (standalone or plugin)
- 500MB+ RAM available
- 1GB+ disk space
- External MongoDB instance
- External ChromaDB instance

### 🛠️ Development Mode
- Docker & Docker Compose (standalone or plugin)
- 1GB+ RAM available
- 2GB+ disk space
- External MongoDB instance
- External ChromaDB instance

### 🗄️ Full Stack Mode
- Docker & Docker Compose (standalone or plugin)
- 2GB+ RAM available
- 4GB+ disk space
- No external databases needed

### AI Providers (Optional)
- Anthropic Claude API key
- OpenAI API key
- OpenRouter API key
- Or local LLM setup

## � Installation Script Features

The one-line installer (`install.sh`) provides a comprehensive setup experience:

### 🎯 **Interactive Setup**
- **Deployment Mode Selection**: Choose between Production, Development, or Full Stack
- **Database Configuration**: Guided setup for MongoDB and ChromaDB URLs
- **API Key Management**: Secure input for AI provider keys (Anthropic, OpenAI, OpenRouter)
- **Smart .env Handling**: Preserves existing configuration, creates backup before changes

### 🚀 **Generated Scripts**
After installation, you'll have these ready-to-use scripts:

| Script | Purpose | Command |
|--------|---------|---------|
| `start-production.sh` | 🚀 Production mode with pre-built images | `./start-production.sh` |
| `start-development.sh` | 🛠️ Development mode with source building | `./start-development.sh` |
| `start-fullstack.sh` | 🗄️ Full stack with included databases | `./start-fullstack.sh` |
| `stop.sh` | 🛑 Universal stop script for all modes | `./stop.sh` |

### 📁 **Directory Structure**
```
rpger-extractor/
├── docker-compose.yml           # Production configuration
├── docker-compose.dev.yml       # Development configuration
├── docker-compose.containers.yml # Full stack with databases
├── .env                         # Environment variables
├── .env.backup                  # Backup of existing .env (if any)
├── start-production.sh          # Production startup script
├── start-development.sh         # Development startup script
├── start-fullstack.sh           # Full stack startup script
└── stop.sh                      # Universal stop script
```

### 🛡️ **Safety Features**
- **Dependency Checking**: Verifies Docker and Docker Compose installation (both standalone and plugin versions)
- **Non-destructive**: Won't overwrite existing `.env` files without permission
- **Backup Creation**: Automatically backs up existing configuration
- **Error Handling**: Graceful failure with helpful error messages
- **Version Compatibility**: Automatically detects and uses correct Docker Compose command
- **Interactive Input**: Properly handles user input when piped through curl

---

## �🔧 Configuration

### Environment Variables

| Variable | Description | Production/Dev | Full Stack |
|----------|-------------|----------------|------------|
| `MONGODB_URL` | MongoDB connection | External URL | `mongodb://mongodb:27017` |
| `CHROMADB_URL` | ChromaDB connection | External URL | `http://chromadb:8000` |
| `FLASK_ENV` | Flask environment | `production` | `production` |
| `MAX_CONTENT_LENGTH` | Upload limit (MB) | `200` | `200` |
| `UPLOAD_TIMEOUT` | Upload timeout (sec) | `300` | `300` |
| `ANTHROPIC_API_KEY` | Claude API key | Optional | Optional |
| `OPENAI_API_KEY` | OpenAI API key | Optional | Optional |
| `OPENROUTER_API_KEY` | OpenRouter API key | Optional | Optional |

### Database Configuration

#### MongoDB Collections Structure
```
rpger.source_material.{game_type}.{edition}.{book_type}.{collection_name}
```

#### ChromaDB Collections
- Organized by game type and edition
- Vector embeddings for semantic search
- Metadata filtering capabilities

## 🐳 Docker Deployment Options

### 🚀 Production (Recommended)
Uses pre-built images from CI/CD pipeline - **Latest: v1.0.44**

```bash
# Using install script (recommended)
./start-production.sh

# Manual commands
docker-compose pull
docker-compose up -d

# Check status
docker-compose ps

# View logs
docker-compose logs -f app

# Update to latest version
docker-compose pull && docker-compose up -d

# Stop services
./stop.sh
# or manually: docker-compose down
```

**Image Details:**
- 📦 **Latest**: `padster2012/rpger-content-extractor:latest`
- 🏷️ **Current Version**: `padster2012/rpger-content-extractor:1.0.44`
- 🔄 **Auto-updated**: Every successful CI/CD build
- ✅ **Build Status**: All tests passing (Build #44)
- 🐳 **Registry**: [Docker Hub](https://hub.docker.com/r/padster2012/rpger-content-extractor)

### 🛠️ Development
Build from source with live code reloading

```bash
# Using install script (recommended)
./start-development.sh

# Manual commands
docker-compose -f docker-compose.dev.yml up -d --build

# View logs with live updates
docker-compose -f docker-compose.dev.yml logs -f app

# Rebuild after code changes
docker-compose -f docker-compose.dev.yml up -d --build

# Stop development environment
./stop.sh
# or manually: docker-compose -f docker-compose.dev.yml down
```

### 🗄️ Full Stack (with Databases)
Includes MongoDB and ChromaDB containers

```bash
# Using install script (recommended)
./start-fullstack.sh

# Manual commands
docker-compose -f docker-compose.yml -f docker-compose.containers.yml up -d

# Check all services
docker-compose ps

# Reset all data (WARNING: Deletes everything)
./stop.sh && docker-compose down -v
# or manually: docker-compose -f docker-compose.yml -f docker-compose.containers.yml down -v
```

## 🔍 Health Checks

### Application Health
```bash
curl http://localhost:5000/health
```

### Service Status
```bash
# Check all services
docker-compose ps

# Check specific service logs
docker-compose logs mongodb
docker-compose logs chromadb
docker-compose logs app
```

## 📊 Monitoring

### Built-in Monitoring
- Application health endpoint: `/health`
- Database connectivity tests
- AI provider status checks
- Resource usage tracking

### External Monitoring
- Docker health checks
- Container restart policies
- Log aggregation ready

## 🧪 Testing

```bash
# Run test suite
pytest tests/

# Run specific test categories
pytest tests/test_pdf_processor.py
pytest tests/test_web_ui.py

# Run with coverage
pytest --cov=Modules tests/
```

## 📚 Documentation

### Quick References
- **Docker Hub**: [padster2012/rpger-content-extractor](https://hub.docker.com/r/padster2012/rpger-content-extractor)
- **GitHub Repository**: [PadsterH2012/rpger-content-extractor](https://github.com/PadsterH2012/rpger-content-extractor)
- **CI/CD Status**: Jenkins Build #44 ✅
- **Latest Version**: v1.0.44

### API Endpoints
- **Health Check**: `GET /health`
- **Upload PDF**: `POST /upload`
- **Extract Content**: `POST /extract`
- **View Results**: `GET /results`

## 🔧 Development

### Local Development Setup
```bash
# Clone repository
git clone https://github.com/PadsterH2012/rpger-content-extractor.git
cd rpger-content-extractor

# Start development environment
docker-compose -f docker-compose.dev.yml up -d

# Install development dependencies (optional, for local testing)
pip install -r requirements.txt
pip install pytest pytest-cov black flake8

# Run tests locally
pytest tests/

# Or run tests in container
docker-compose -f docker-compose.dev.yml exec app pytest tests/
```

### Contributing
1. Fork the repository
2. Create feature branch
3. Add tests for new features
4. Ensure all tests pass
5. Submit pull request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🆘 Support

### Getting Help
- **GitHub Issues**: [Report bugs or request features](https://github.com/PadsterH2012/rpger-content-extractor/issues)
- **Discussions**: [Community discussions](https://github.com/PadsterH2012/rpger-content-extractor/discussions)
- **Docker Hub**: [Container registry](https://hub.docker.com/r/padster2012/rpger-content-extractor)

### Troubleshooting
- Check Docker container logs: `docker-compose logs -f app`
- Verify database connections: `curl http://localhost:5000/health`
- Ensure sufficient resources (see Requirements section)
- Check Jenkins CI/CD status for latest builds

---

**Built with ❤️ for the RPG community**
