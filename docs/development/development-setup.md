---
title: Development Setup
description: Local development environment configuration for RPGer Content Extractor
tags: [development, setup, environment, configuration]
last_updated: 2025-10-18
author: HL-Auggie Analysis System
---

# Development Setup

## Overview

This guide covers setting up a local development environment for the RPGer Content Extractor. Whether you're contributing to the project or customizing it for your needs, this guide will get you up and running quickly.

## Prerequisites

### System Requirements

**Operating System**:
- Linux (Ubuntu 20.04+ recommended)
- macOS (10.15+ recommended)
- Windows 10/11 with WSL2

**Software Requirements**:
- Python 3.11 or 3.12
- Docker and Docker Compose
- Git
- Text editor or IDE (VS Code recommended)

**Hardware Requirements**:
- **Minimum**: 4GB RAM, 2GB free disk space
- **Recommended**: 8GB RAM, 10GB free disk space
- **For AI Processing**: 16GB RAM recommended

### Development Tools

**Required**:
- Git for version control
- Docker for containerization
- Python virtual environment tools

**Recommended**:
- VS Code with Python extension
- Docker Desktop (for GUI management)
- Postman (for API testing)
- MongoDB Compass (for database inspection)

## Quick Start

### 1. Clone Repository

```bash
# Clone the repository
git clone https://github.com/PadsterH2012/rpger-content-extractor.git
cd rpger-content-extractor

# Check repository status
git status
git log --oneline -5
```

### 2. Environment Setup

#### Python Virtual Environment

```bash
# Create virtual environment
python3 -m venv venv

# Activate virtual environment
# Linux/macOS:
source venv/bin/activate
# Windows:
venv\Scripts\activate

# Verify Python version
python --version  # Should be 3.11 or 3.12
```

#### Install Dependencies

```bash
# Install core dependencies
pip install -r requirements.txt

# Install development dependencies
pip install pytest pytest-cov black flake8 pytest-html pytest-json-report

# Verify installation
pip list | grep -E "(pytest|flask|pymongo|anthropic)"
```

### 3. Configuration

#### Environment Variables

Create `.env` file in project root:

```bash
# Copy example environment file
cp .env.example .env

# Edit configuration
nano .env
```

**Essential Configuration**:
```bash
# Flask Configuration
FLASK_ENV=development
FLASK_SECRET_KEY=your-development-secret-key
MAX_CONTENT_LENGTH=200
UPLOAD_TIMEOUT=300

# AI Provider Configuration (choose one or more)
ANTHROPIC_API_KEY=your-anthropic-key
OPENAI_API_KEY=your-openai-key
OPENROUTER_API_KEY=your-openrouter-key

# Database Configuration (for external databases)
MONGODB_HOST=localhost
MONGODB_PORT=27017
MONGODB_DATABASE=rpger_dev
CHROMA_HOST=localhost
CHROMA_PORT=8000

# Development Settings
DEBUG=true
LOG_LEVEL=DEBUG
PYTHONDONTWRITEBYTECODE=1
```

#### AI Provider Setup

**Anthropic Claude** (Recommended for development):
1. Sign up at https://console.anthropic.com/
2. Create API key
3. Add to `.env` as `ANTHROPIC_API_KEY`

**OpenAI** (Alternative):
1. Sign up at https://platform.openai.com/
2. Create API key
3. Add to `.env` as `OPENAI_API_KEY`

**Mock Provider** (No API key needed):
- Use for testing without API costs
- Set `AI_PROVIDER=mock` in environment

### 4. Database Setup

#### Option A: Docker Containers (Recommended)

```bash
# Start databases in containers
docker-compose -f docker-compose.containers.yml up -d mongodb chromadb

# Verify containers are running
docker ps

# Check logs
docker-compose -f docker-compose.containers.yml logs mongodb
docker-compose -f docker-compose.containers.yml logs chromadb
```

#### Option B: Local Installation

**MongoDB**:
```bash
# Ubuntu/Debian
sudo apt update
sudo apt install mongodb

# macOS with Homebrew
brew tap mongodb/brew
brew install mongodb-community

# Start MongoDB
sudo systemctl start mongodb  # Linux
brew services start mongodb-community  # macOS
```

**ChromaDB**:
```bash
# Install ChromaDB server
pip install chromadb[server]

# Start ChromaDB server
chroma run --host localhost --port 8000
```

## Development Workflow

### 1. Start Development Environment

#### Full Development Stack

```bash
# Start all services (app + databases)
docker-compose -f docker-compose.dev.yml up -d

# Or start with containers
docker-compose -f docker-compose.yml -f docker-compose.containers.yml up -d
```

#### Local Development Server

```bash
# Activate virtual environment
source venv/bin/activate

# Start Flask development server
python ui/start_ui.py

# Or use Flask directly
cd ui
flask run --debug --host=0.0.0.0 --port=5000
```

### 2. Development Tools

#### Code Formatting

```bash
# Format code with Black
black .

# Check formatting
black --check .

# Format specific files
black Modules/ ui/ tests/
```

#### Code Linting

```bash
# Run flake8 linting
flake8 .

# Check specific directories
flake8 Modules/ ui/

# Generate linting report
flake8 --format=html --htmldir=flake8-report .
```

#### Type Checking (Optional)

```bash
# Install mypy
pip install mypy

# Run type checking
mypy Modules/
```

### 3. Testing

#### Run All Tests

```bash
# Run complete test suite
pytest

# Run with coverage
pytest --cov=Modules --cov-report=html

# Run specific test categories
pytest -m unit
pytest -m integration
pytest -m e2e
```

#### Priority Test Suites

```bash
# Run Priority 1 tests (Critical Core Functionality)
python tests/run_priority1_tests.py

# Run Priority 2 tests (Essential Integration)
python tests/run_priority2_tests.py

# Run focused test suite
./test_focused.sh
```

#### Test Configuration

Tests are configured in `pytest.ini`:
- **Test Discovery**: Automatic test file detection
- **Coverage**: Minimum 40% coverage required
- **Markers**: Categorized test execution
- **Reports**: HTML and JSON test reports

### 4. Database Development

#### MongoDB Development

```bash
# Connect to development database
mongosh mongodb://localhost:27017/rpger_dev

# Common development queries
db.collections.find().limit(5)
db.collections.countDocuments()
db.collections.createIndex({"game_metadata.game_type": 1})
```

#### ChromaDB Development

```bash
# Test ChromaDB connection
curl http://localhost:8000/api/v1/heartbeat

# List collections
curl http://localhost:8000/api/v1/collections

# Collection info
curl http://localhost:8000/api/v1/collections/{collection_name}
```

## IDE Configuration

### VS Code Setup

#### Recommended Extensions

```json
{
  "recommendations": [
    "ms-python.python",
    "ms-python.flake8",
    "ms-python.black-formatter",
    "ms-python.pylint",
    "ms-vscode.vscode-json",
    "redhat.vscode-yaml",
    "ms-vscode.docker"
  ]
}
```

#### VS Code Settings

Create `.vscode/settings.json`:

```json
{
  "python.defaultInterpreterPath": "./venv/bin/python",
  "python.formatting.provider": "black",
  "python.linting.enabled": true,
  "python.linting.flake8Enabled": true,
  "python.testing.pytestEnabled": true,
  "python.testing.pytestArgs": ["tests"],
  "files.exclude": {
    "**/__pycache__": true,
    "**/*.pyc": true,
    ".pytest_cache": true,
    "htmlcov": true
  }
}
```

#### Launch Configuration

Create `.vscode/launch.json`:

```json
{
  "version": "0.2.0",
  "configurations": [
    {
      "name": "Flask App",
      "type": "python",
      "request": "launch",
      "program": "${workspaceFolder}/ui/start_ui.py",
      "env": {
        "FLASK_ENV": "development",
        "FLASK_DEBUG": "1"
      },
      "console": "integratedTerminal"
    },
    {
      "name": "Run Tests",
      "type": "python",
      "request": "launch",
      "module": "pytest",
      "args": ["tests/", "-v"],
      "console": "integratedTerminal"
    }
  ]
}
```

### PyCharm Setup

#### Project Configuration

1. **Open Project**: File → Open → Select project directory
2. **Python Interpreter**: Settings → Project → Python Interpreter → Add → Existing environment → Select `venv/bin/python`
3. **Code Style**: Settings → Editor → Code Style → Python → Set to Black
4. **Testing**: Settings → Tools → Python Integrated Tools → Default test runner → pytest

#### Run Configurations

**Flask Application**:
- Script path: `ui/start_ui.py`
- Environment variables: `FLASK_ENV=development`
- Working directory: Project root

**Tests**:
- Target: Custom
- Additional arguments: `tests/ -v`
- Working directory: Project root

## Debugging

### Flask Application Debugging

#### Debug Mode

```bash
# Enable Flask debug mode
export FLASK_ENV=development
export FLASK_DEBUG=1

# Start with debugging
python ui/start_ui.py
```

#### VS Code Debugging

1. Set breakpoints in code
2. Press F5 or use "Run and Debug"
3. Select "Flask App" configuration
4. Debug through web interface

#### Print Debugging

```python
# Add debug prints
print(f"DEBUG: Variable value = {variable}")

# Use logging for better debugging
import logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)
logger.debug(f"Debug message: {data}")
```

### Database Debugging

#### MongoDB Debugging

```bash
# Enable MongoDB logging
mongosh --eval "db.setLogLevel(2)"

# Monitor operations
mongosh --eval "db.runCommand({profile: 2})"

# View slow operations
mongosh --eval "db.system.profile.find().limit(5).sort({ts:-1})"
```

#### ChromaDB Debugging

```bash
# Check ChromaDB logs
docker logs chromadb_container

# Test API endpoints
curl -v http://localhost:8000/api/v1/heartbeat
```

## Performance Optimization

### Development Performance

#### Python Optimization

```bash
# Use faster JSON library
pip install orjson

# Enable Python optimizations
export PYTHONOPTIMIZE=1

# Use faster HTTP client
pip install httpx
```

#### Database Optimization

**MongoDB**:
- Use indexes for frequent queries
- Enable profiling for slow operations
- Use projection to limit returned fields

**ChromaDB**:
- Batch operations when possible
- Use appropriate collection sizes
- Monitor memory usage

### Resource Monitoring

#### System Resources

```bash
# Monitor Python processes
ps aux | grep python

# Monitor memory usage
free -h

# Monitor disk usage
df -h
```

#### Application Monitoring

```bash
# Monitor Flask application
curl http://localhost:5000/health

# Check database connections
curl http://localhost:5000/api/status
```

## Troubleshooting

### Common Issues

#### Import Errors

```bash
# Verify Python path
python -c "import sys; print(sys.path)"

# Check installed packages
pip list

# Reinstall dependencies
pip install -r requirements.txt --force-reinstall
```

#### Database Connection Issues

```bash
# Test MongoDB connection
mongosh mongodb://localhost:27017/rpger_dev

# Test ChromaDB connection
curl http://localhost:8000/api/v1/heartbeat

# Check Docker containers
docker ps
docker logs container_name
```

#### Port Conflicts

```bash
# Check port usage
netstat -tulpn | grep :5000
lsof -i :5000

# Kill processes using port
sudo kill -9 $(lsof -t -i:5000)
```

### Getting Help

#### Documentation Resources

- **API Documentation**: `docs/api/`
- **Architecture Guide**: `docs/architecture/`
- **User Guides**: `docs/user-guides/`
- **Test Documentation**: `tests/README.md`

#### Community Support

- **GitHub Issues**: Report bugs and request features
- **Discussions**: Ask questions and share ideas
- **Wiki**: Community-maintained documentation

#### Development Support

- **Code Review**: Submit pull requests for review
- **Pair Programming**: Collaborate with other developers
- **Mentoring**: Get help from experienced contributors
