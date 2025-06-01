# Container Stack Setup Guide

This guide covers setting up rpger-content-extractor with the full container stack (app + databases).

## 🎯 Overview

The container stack includes:
- **App Container**: Flask web UI and processing engine
- **MongoDB Container**: Document database for extracted content  
- **ChromaDB Container**: Vector database for semantic search
- **Nginx Proxy** (optional): Load balancing and SSL termination

## 📋 Prerequisites

- Docker Engine 20.10+
- Docker Compose 2.0+
- 2GB+ available RAM
- 4GB+ available disk space

## 🚀 Quick Setup

### 1. Environment Configuration
```bash
# Copy container template
cp examples/.env.containers.example .env

# Edit configuration
nano .env
```

### 2. Required Environment Variables
```bash
# AI Provider (choose one)
ANTHROPIC_API_KEY=sk-ant-your-key-here
# OR
OPENAI_API_KEY=sk-your-key-here
# OR  
OPENROUTER_API_KEY=sk-or-your-key-here
```

### 3. Start Services
```bash
# Start all containers
./scripts/start-containers.sh

# Or manually
docker-compose -f docker-compose.yml -f docker-compose.containers.yml up -d
```

### 4. Verify Setup
```bash
# Check service health
curl http://localhost:5000/health

# View service status
docker-compose ps
```

## 🔧 Configuration Details

### MongoDB Configuration
- **Port**: 27017
- **Database**: rpger
- **Data Volume**: `mongodb_data`
- **Health Check**: MongoDB ping command

### ChromaDB Configuration  
- **Port**: 8000
- **API Endpoint**: http://localhost:8000
- **Data Volume**: `chromadb_data`
- **Health Check**: Heartbeat endpoint

### Application Configuration
- **Port**: 5000
- **Upload Directory**: `./uploads`
- **Extraction Output**: `./extracted`
- **Logs**: `./logs`

## 🔍 Monitoring & Logs

### View Logs
```bash
# All services
docker-compose logs -f

# Specific service
docker-compose logs -f app
docker-compose logs -f mongodb
docker-compose logs -f chromadb
```

### Health Checks
```bash
# Application health
curl http://localhost:5000/health

# MongoDB health
docker exec rpger-content-extractor-mongodb-1 mongosh --eval "db.adminCommand('ping')"

# ChromaDB health
curl http://localhost:8000/api/v1/heartbeat
```

## 🛠️ Maintenance

### Backup Data
```bash
# MongoDB backup
docker exec rpger-content-extractor-mongodb-1 mongodump --out /backup
docker cp rpger-content-extractor-mongodb-1:/backup ./mongodb-backup

# ChromaDB backup
docker cp rpger-content-extractor-chromadb-1:/chroma/data ./chromadb-backup
```

### Update Services
```bash
# Pull latest images
docker-compose pull

# Restart with new images
docker-compose down
docker-compose up -d
```

### Reset Data (⚠️ Destructive)
```bash
# Stop and remove all data
docker-compose down -v

# Restart fresh
docker-compose up -d
```

## 🚨 Troubleshooting

### Common Issues

#### Port Conflicts
```bash
# Check port usage
netstat -tulpn | grep :5000
netstat -tulpn | grep :27017
netstat -tulpn | grep :8000

# Change ports in docker-compose.yml if needed
```

#### Memory Issues
```bash
# Check available memory
free -h

# Monitor container memory usage
docker stats
```

#### Database Connection Issues
```bash
# Check container networking
docker network ls
docker network inspect rpger-content-extractor_rpger-network

# Test internal connectivity
docker exec rpger-content-extractor-app-1 ping mongodb
docker exec rpger-content-extractor-app-1 ping chromadb
```

## 🔒 Security Considerations

### Production Deployment
- Change default passwords
- Use environment files for secrets
- Enable MongoDB authentication
- Configure firewall rules
- Use HTTPS with reverse proxy

### Network Security
```yaml
# Add to docker-compose.yml for production
networks:
  rpger-network:
    driver: bridge
    internal: true  # Isolate from external networks
```

## 📈 Performance Tuning

### MongoDB Optimization
```yaml
mongodb:
  command: mongod --wiredTigerCacheSizeGB 0.5
  deploy:
    resources:
      limits:
        memory: 1G
      reservations:
        memory: 512M
```

### ChromaDB Optimization
```yaml
chromadb:
  environment:
    - CHROMA_SERVER_CORS_ALLOW_ORIGINS=["http://localhost:5000"]
  deploy:
    resources:
      limits:
        memory: 1G
      reservations:
        memory: 512M
```

## 🔄 Scaling

### Horizontal Scaling
```yaml
# Scale app containers
docker-compose up -d --scale app=3

# Add load balancer
nginx:
  image: nginx:alpine
  ports:
    - "80:80"
  depends_on:
    - app
```

### Resource Limits
```yaml
services:
  app:
    deploy:
      resources:
        limits:
          cpus: '1.0'
          memory: 512M
        reservations:
          cpus: '0.5'
          memory: 256M
```
