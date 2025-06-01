# 🎮 RPGer Content Extractor

**AI-Powered Multi-Game RPG PDF Content Extraction & Management System**

A dockerized solution for extracting, categorizing, and managing RPG content from PDF sources with dual deployment options.

## 🚀 Quick Start

### Option 1: Container Stack (Recommended for Development)
```bash
# Clone and setup
git clone <repository-url>
cd rpger-content-extractor

# Configure environment
cp examples/.env.containers.example .env
# Edit .env with your AI API keys

# Start all services
./scripts/start-containers.sh

# Access web UI
open http://localhost:5000
```

### Option 2: External Databases (Production)
```bash
# Configure external databases
cp examples/.env.external.example .env
# Edit .env with your external database URLs and AI API keys

# Start app container only
./scripts/start-external.sh
```

## 🏗️ Architecture

### Dual Deployment Options

#### 🐳 Container Stack
- **App Container**: Flask web UI + processing engine
- **MongoDB Container**: Document database for extracted content
- **ChromaDB Container**: Vector database for semantic search
- **Resource Usage**: ~1.5GB RAM, 2GB storage

#### 🌐 External Databases
- **App Container**: Flask web UI + processing engine only
- **External MongoDB**: Atlas, self-hosted, or managed service
- **External ChromaDB**: Hosted or managed vector database
- **Resource Usage**: ~200MB RAM, 500MB storage

## 🎯 Features

- **Multi-Game Support**: D&D, Pathfinder, Call of Cthulhu, and more
- **AI-Powered Detection**: Automatic game type and edition detection
- **Smart Categorization**: AI-driven content classification
- **Dual Database Storage**: MongoDB for documents, ChromaDB for vectors
- **Web Interface**: User-friendly upload and management UI
- **Docker Ready**: Both container stack and external DB modes
- **Health Monitoring**: Built-in health checks and monitoring

## 📋 Requirements

### Container Stack Mode
- Docker & Docker Compose
- 2GB+ RAM available
- 4GB+ disk space

### External DB Mode
- Docker & Docker Compose
- External MongoDB instance
- External ChromaDB instance
- 1GB+ RAM available

### AI Providers (Optional)
- Anthropic Claude API key
- OpenAI API key
- OpenRouter API key
- Or local LLM setup

## 🔧 Configuration

### Environment Variables

| Variable | Description | Container Mode | External Mode |
|----------|-------------|----------------|---------------|
| `SETUP_MODE` | Deployment mode | `containers` | `external` |
| `MONGODB_URL` | MongoDB connection | `mongodb://mongodb:27017` | External URL |
| `CHROMADB_URL` | ChromaDB connection | `http://chromadb:8000` | External URL |
| `ANTHROPIC_API_KEY` | Claude API key | Optional | Optional |
| `OPENAI_API_KEY` | OpenAI API key | Optional | Optional |

### Database Configuration

#### MongoDB Collections Structure
```
rpger.source_material.{game_type}.{edition}.{book_type}.{collection_name}
```

#### ChromaDB Collections
- Organized by game type and edition
- Vector embeddings for semantic search
- Metadata filtering capabilities

## 🐳 Docker Commands

### Container Stack
```bash
# Start all services
docker-compose -f docker-compose.yml -f docker-compose.containers.yml up -d

# View logs
docker-compose logs -f app

# Stop services
docker-compose down

# Reset data (WARNING: Deletes all data)
docker-compose down -v
```

### External Databases
```bash
# Start app only
docker-compose -f docker-compose.yml -f docker-compose.external.yml up -d

# View logs
docker-compose logs -f app

# Stop app
docker-compose down
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

- [Container Stack Setup](docs/deployment/container-stack-setup.md)
- [External Database Setup](docs/deployment/external-db-setup.md)
- [Migration Guide](docs/deployment/migration-guide.md)
- [API Documentation](docs/api/endpoints.md)
- [Architecture Overview](docs/architecture/system-overview.md)

## 🔧 Development

### Local Development Setup
```bash
# Use container stack for development
cp examples/.env.containers.example .env
./scripts/start-containers.sh

# Install development dependencies
pip install -r requirements.txt
pip install pytest pytest-cov black flake8

# Run tests
pytest tests/
```

### Contributing
1. Fork the repository
2. Create feature branch
3. Add tests for new features
4. Ensure all tests pass
5. Submit pull request

## 📄 License

[Add your license information here]

## 🆘 Support

- [Troubleshooting Guide](docs/deployment/troubleshooting.md)
- [GitHub Issues](https://github.com/your-org/rpger-content-extractor/issues)
- [Documentation](docs/)

---

**Built with ❤️ for the RPG community**
