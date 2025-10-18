---
title: Troubleshooting Guide
description: Common issues and solutions for RPGer Content Extractor
tags: [operations, troubleshooting, debugging, support]
last_updated: 2025-10-18
author: HL-Auggie Analysis System
---

# Troubleshooting Guide

## Overview

This guide provides solutions to common issues encountered when deploying, configuring, and using the RPGer Content Extractor. Issues are organized by category with step-by-step resolution procedures.

## Application Startup Issues

### Container Won't Start

#### Symptoms
- Docker container exits immediately
- "Container exited with code 1" error
- Application fails to bind to port

#### Diagnosis
```bash
# Check container logs
docker logs rpger-app

# Check container status
docker ps -a | grep rpger

# Inspect container configuration
docker inspect rpger-app
```

#### Common Causes and Solutions

**Port Already in Use**:
```bash
# Check what's using port 5000
sudo netstat -tulpn | grep :5000
sudo lsof -i :5000

# Kill process using port
sudo kill -9 $(lsof -t -i:5000)

# Or change port in docker-compose.yml
ports:
  - "5001:5000"  # Use different external port
```

**Missing Environment Variables**:
```bash
# Check environment file exists
ls -la .env

# Validate required variables
grep -E "(FLASK_SECRET_KEY|AI_PROVIDER)" .env

# Set missing variables
echo "FLASK_SECRET_KEY=$(openssl rand -hex 32)" >> .env
```

**Permission Issues**:
```bash
# Fix file permissions
sudo chown -R 1000:1000 ./uploads ./extracted ./logs

# Fix directory permissions
chmod 755 ./uploads ./extracted ./logs
```

### Application Health Check Failures

#### Symptoms
- `/health` endpoint returns 500 error
- Health check timeouts
- Container marked as unhealthy

#### Diagnosis
```bash
# Test health endpoint directly
curl -v http://localhost:5000/health

# Check application logs
docker logs rpger-app | grep -i error

# Test internal connectivity
docker exec rpger-app curl localhost:5000/health
```

#### Solutions

**Database Connection Issues**:
```bash
# Test MongoDB connection
docker exec rpger-app mongosh $MONGODB_CONNECTION_STRING --eval "db.adminCommand('ping')"

# Test ChromaDB connection
docker exec rpger-app curl http://$CHROMA_HOST:$CHROMA_PORT/api/v1/heartbeat

# Check network connectivity
docker exec rpger-app ping mongodb
docker exec rpger-app ping chromadb
```

**Memory Issues**:
```bash
# Check memory usage
docker stats rpger-app

# Increase memory limits
# In docker-compose.yml:
deploy:
  resources:
    limits:
      memory: 2G
```

## Database Connection Issues

### MongoDB Connection Problems

#### Symptoms
- "Connection refused" errors
- "Authentication failed" messages
- Timeout errors when connecting to MongoDB

#### Diagnosis
```bash
# Test MongoDB connectivity
mongosh mongodb://localhost:27017/rpger

# Check MongoDB container status
docker ps | grep mongo
docker logs mongodb

# Test from application container
docker exec rpger-app mongosh $MONGODB_CONNECTION_STRING --eval "db.adminCommand('ping')"
```

#### Solutions

**MongoDB Not Running**:
```bash
# Start MongoDB container
docker-compose up -d mongodb

# Check MongoDB startup logs
docker logs mongodb -f

# Restart MongoDB if needed
docker-compose restart mongodb
```

**Authentication Issues**:
```bash
# Check MongoDB authentication settings
docker exec mongodb mongosh --eval "db.runCommand({usersInfo: 1})"

# Create user if needed
docker exec mongodb mongosh --eval "
db.createUser({
  user: 'rpger_user',
  pwd: 'secure_password',
  roles: [{role: 'readWrite', db: 'rpger'}]
})
"

# Update connection string
MONGODB_CONNECTION_STRING=mongodb://rpger_user:secure_password@mongodb:27017/rpger
```

**Network Issues**:
```bash
# Check Docker network
docker network ls
docker network inspect rpger-network

# Verify containers are on same network
docker inspect rpger-app | grep NetworkMode
docker inspect mongodb | grep NetworkMode
```

### ChromaDB Connection Problems

#### Symptoms
- ChromaDB API unreachable
- Vector search failures
- Collection creation errors

#### Diagnosis
```bash
# Test ChromaDB API
curl http://localhost:8000/api/v1/heartbeat

# Check ChromaDB container
docker ps | grep chroma
docker logs chromadb

# Test from application
docker exec rpger-app curl http://chromadb:8000/api/v1/heartbeat
```

#### Solutions

**ChromaDB Service Down**:
```bash
# Start ChromaDB container
docker-compose up -d chromadb

# Check ChromaDB logs
docker logs chromadb -f

# Restart if needed
docker-compose restart chromadb
```

**API Version Mismatch**:
```bash
# Check ChromaDB version
curl http://localhost:8000/api/v1/version

# Update API endpoints in application
# Ensure using correct API version in configuration
CHROMA_BASE_URL=http://chromadb:8000/api/v1
```

**Data Volume Issues**:
```bash
# Check data volume
docker volume ls | grep chroma
docker volume inspect chromadb_data

# Fix volume permissions
docker exec chromadb chown -R 1000:1000 /chroma/data
```

## AI Provider Issues

### API Key Problems

#### Symptoms
- "Invalid API key" errors
- "Authentication failed" messages
- 401 Unauthorized responses

#### Diagnosis
```bash
# Check API key configuration
echo $ANTHROPIC_API_KEY | head -c 20
echo $OPENAI_API_KEY | head -c 20

# Test API key directly
curl -H "x-api-key: $ANTHROPIC_API_KEY" https://api.anthropic.com/v1/messages

# Check application logs
docker logs rpger-app | grep -i "api.*key"
```

#### Solutions

**Missing or Invalid API Keys**:
```bash
# Set correct API key
export ANTHROPIC_API_KEY=sk-ant-your-actual-key-here

# Update environment file
echo "ANTHROPIC_API_KEY=sk-ant-your-actual-key-here" >> .env

# Restart application
docker-compose restart app
```

**API Key Format Issues**:
```bash
# Anthropic keys start with: sk-ant-
# OpenAI keys start with: sk-
# OpenRouter keys start with: sk-or-

# Verify key format
if [[ $ANTHROPIC_API_KEY =~ ^sk-ant- ]]; then
    echo "Anthropic key format correct"
else
    echo "Invalid Anthropic key format"
fi
```

### Rate Limiting Issues

#### Symptoms
- "Rate limit exceeded" errors
- 429 Too Many Requests responses
- Slow AI processing

#### Diagnosis
```bash
# Check rate limit headers in logs
docker logs rpger-app | grep -i "rate.*limit"

# Monitor API usage
curl -H "x-api-key: $ANTHROPIC_API_KEY" https://api.anthropic.com/v1/usage
```

#### Solutions

**Reduce Request Frequency**:
```bash
# Add delays between requests
AI_RETRY_DELAY=10  # Increase delay between retries

# Use batch processing
# Process multiple files with delays
for file in *.pdf; do
    python Extraction.py extract "$file"
    sleep 30  # Wait 30 seconds between files
done
```

**Switch AI Providers**:
```bash
# Use alternative provider
AI_PROVIDER=openrouter
AI_FALLBACK_PROVIDER=anthropic

# Configure multiple providers
ANTHROPIC_API_KEY=your-anthropic-key
OPENAI_API_KEY=your-openai-key
OPENROUTER_API_KEY=your-openrouter-key
```

### AI Response Quality Issues

#### Symptoms
- Poor game detection accuracy
- Incorrect categorization
- Low confidence scores

#### Diagnosis
```bash
# Check AI provider configuration
echo "Provider: $AI_PROVIDER"
echo "Model: $AI_MODEL"
echo "Temperature: $AI_TEMPERATURE"

# Review processing logs
docker logs rpger-app | grep -i "confidence\|detection"
```

#### Solutions

**Optimize AI Parameters**:
```bash
# Use recommended models
ANTHROPIC_MODEL=claude-3-sonnet-20240229
OPENAI_MODEL=gpt-4
OPENROUTER_MODEL=anthropic/claude-3-sonnet

# Adjust temperature for consistency
AI_TEMPERATURE=0.1  # Lower for more consistent results

# Increase max tokens for complex content
AI_MAX_TOKENS=8000
```

**Enable Confidence Testing**:
```bash
# Run with confidence testing
python Extraction.py extract file.pdf --confidence-test

# Or via web interface
# Enable "Run Confidence Test" option
```

## File Processing Issues

### PDF Upload Problems

#### Symptoms
- "File too large" errors
- Upload timeouts
- Corrupted file errors

#### Diagnosis
```bash
# Check file size
ls -lh your-file.pdf

# Test file integrity
file your-file.pdf
pdfinfo your-file.pdf

# Check upload limits
grep MAX_CONTENT_LENGTH .env
```

#### Solutions

**File Size Issues**:
```bash
# Increase upload limit
MAX_CONTENT_LENGTH=500  # Increase to 500MB

# Compress PDF
gs -sDEVICE=pdfwrite -dCompatibilityLevel=1.4 -dPDFSETTINGS=/ebook \
   -dNOPAUSE -dQUIET -dBATCH -sOutputFile=compressed.pdf input.pdf

# Split large PDFs
pdftk large-file.pdf burst output page_%02d.pdf
```

**File Format Issues**:
```bash
# Verify PDF format
file your-file.pdf

# Repair corrupted PDF
pdftk broken.pdf output repaired.pdf

# Convert other formats to PDF
libreoffice --headless --convert-to pdf document.docx
```

### Text Extraction Problems

#### Symptoms
- Empty or garbled text extraction
- Missing content sections
- Poor text quality

#### Diagnosis
```bash
# Test PDF text extraction manually
pdftotext your-file.pdf test-output.txt
cat test-output.txt | head -20

# Check PDF structure
pdfinfo your-file.pdf
pdffonts your-file.pdf
```

#### Solutions

**OCR Issues**:
```bash
# Enable text enhancement
ENABLE_TEXT_ENHANCEMENT=true
AGGRESSIVE_CLEANUP=true

# Use OCR for scanned PDFs
# Install tesseract
sudo apt-get install tesseract-ocr

# Convert PDF to images and OCR
pdftoppm -png your-file.pdf page
tesseract page-01.png output
```

**Multi-Column Layout Issues**:
```bash
# Enable advanced layout detection
ENABLE_LAYOUT_ANALYSIS=true
MULTI_COLUMN_DETECTION=true

# Adjust processing parameters
PDF_PROCESSING_MODE=advanced
LAYOUT_TOLERANCE=0.5
```

## Performance Issues

### Slow Processing

#### Symptoms
- Long processing times
- High CPU/memory usage
- Timeouts during extraction

#### Diagnosis
```bash
# Monitor resource usage
docker stats rpger-app

# Check processing logs
docker logs rpger-app | grep -i "processing.*time"

# Profile application performance
docker exec rpger-app top
```

#### Solutions

**Resource Optimization**:
```bash
# Increase container resources
deploy:
  resources:
    limits:
      cpus: '4.0'
      memory: 4G

# Optimize AI parameters
AI_MAX_TOKENS=2000  # Reduce for faster processing
AI_TEMPERATURE=0.5  # Balance speed and quality

# Use faster AI provider
AI_PROVIDER=openai  # Often faster than Anthropic
```

**Batch Processing Optimization**:
```bash
# Process files in parallel
python Extraction.py batch ./pdfs --parallel 4

# Use background processing
nohup python Extraction.py batch ./pdfs > processing.log 2>&1 &
```

### Memory Issues

#### Symptoms
- Out of memory errors
- Container restarts
- Slow performance

#### Diagnosis
```bash
# Check memory usage
docker stats rpger-app
free -h

# Monitor memory leaks
docker exec rpger-app ps aux --sort=-%mem | head -10
```

#### Solutions

**Memory Optimization**:
```bash
# Increase memory limits
deploy:
  resources:
    limits:
      memory: 4G

# Enable garbage collection
PYTHONOPTIMIZE=1
GC_THRESHOLD=700

# Process smaller batches
BATCH_SIZE=10  # Reduce batch size
MEMORY_CLEANUP_INTERVAL=300  # Clean up every 5 minutes
```

## Network and Connectivity Issues

### Docker Network Problems

#### Symptoms
- Services can't communicate
- DNS resolution failures
- Connection timeouts

#### Diagnosis
```bash
# Check Docker networks
docker network ls
docker network inspect rpger-network

# Test connectivity between containers
docker exec rpger-app ping mongodb
docker exec rpger-app nslookup mongodb
```

#### Solutions

**Network Configuration**:
```bash
# Recreate network
docker network rm rpger-network
docker network create rpger-network

# Restart all services
docker-compose down
docker-compose up -d

# Check service discovery
docker exec rpger-app cat /etc/hosts
```

### External API Connectivity

#### Symptoms
- AI API timeouts
- SSL certificate errors
- DNS resolution failures

#### Diagnosis
```bash
# Test external connectivity
docker exec rpger-app curl -I https://api.anthropic.com
docker exec rpger-app nslookup api.anthropic.com

# Check SSL certificates
docker exec rpger-app openssl s_client -connect api.anthropic.com:443
```

#### Solutions

**Proxy Configuration**:
```bash
# Configure HTTP proxy
HTTP_PROXY=http://proxy.company.com:8080
HTTPS_PROXY=http://proxy.company.com:8080

# Add proxy to Docker
# In docker-compose.yml:
environment:
  - HTTP_PROXY=${HTTP_PROXY}
  - HTTPS_PROXY=${HTTPS_PROXY}
```

**DNS Issues**:
```bash
# Use custom DNS
# In docker-compose.yml:
dns:
  - 8.8.8.8
  - 8.8.4.4

# Or system DNS
dns:
  - 127.0.0.11
```

## Data and Storage Issues

### Volume Mount Problems

#### Symptoms
- Permission denied errors
- Files not persisting
- Volume mount failures

#### Diagnosis
```bash
# Check volume mounts
docker inspect rpger-app | grep -A 10 Mounts

# Check permissions
ls -la ./uploads ./extracted ./logs

# Test file creation
docker exec rpger-app touch /app/uploads/test.txt
```

#### Solutions

**Permission Fixes**:
```bash
# Fix ownership
sudo chown -R 1000:1000 ./uploads ./extracted ./logs

# Fix permissions
chmod 755 ./uploads ./extracted ./logs

# Use correct user in container
# In Dockerfile:
USER 1000:1000
```

### Database Storage Issues

#### Symptoms
- Database out of space
- Slow database operations
- Data corruption

#### Diagnosis
```bash
# Check disk usage
df -h
docker system df

# Check database size
docker exec mongodb mongosh --eval "db.stats()"

# Check ChromaDB storage
docker exec chromadb du -sh /chroma/data
```

#### Solutions

**Storage Cleanup**:
```bash
# Clean up old data
docker exec mongodb mongosh --eval "db.old_collection.drop()"

# Compact database
docker exec mongodb mongosh --eval "db.runCommand({compact: 'collection_name'})"

# Clean Docker system
docker system prune -a
docker volume prune
```

## Getting Help

### Diagnostic Information Collection

```bash
#!/bin/bash
# collect-diagnostics.sh

echo "=== RPGer Content Extractor Diagnostics ==="
echo "Timestamp: $(date)"
echo

echo "=== System Information ==="
uname -a
docker --version
docker-compose --version

echo "=== Container Status ==="
docker ps -a | grep rpger

echo "=== Container Logs (last 50 lines) ==="
docker logs rpger-app --tail 50

echo "=== Environment Configuration ==="
grep -v "API_KEY\|PASSWORD\|SECRET" .env

echo "=== Resource Usage ==="
docker stats --no-stream

echo "=== Network Configuration ==="
docker network ls
docker network inspect rpger-network

echo "=== Volume Information ==="
docker volume ls | grep rpger
```

### Support Channels

**GitHub Issues**:
- Bug reports: https://github.com/PadsterH2012/rpger-content-extractor/issues
- Feature requests: Use issue templates
- Include diagnostic information

**Documentation**:
- Check existing documentation first
- Search for similar issues
- Review configuration guides

**Community Support**:
- GitHub Discussions
- Stack Overflow (tag: rpger-content-extractor)
- Reddit: r/RPG or r/DMAcademy

### Creating Effective Bug Reports

**Include This Information**:
1. **Environment Details**: OS, Docker version, deployment method
2. **Configuration**: Relevant environment variables (redact secrets)
3. **Steps to Reproduce**: Exact steps that cause the issue
4. **Expected Behavior**: What should happen
5. **Actual Behavior**: What actually happens
6. **Logs**: Relevant log entries
7. **Diagnostic Output**: Run collect-diagnostics.sh

**Example Bug Report**:
```markdown
## Bug Description
PDF processing fails with "Connection timeout" error

## Environment
- OS: Ubuntu 20.04
- Docker: 24.0.6
- Deployment: docker-compose production mode

## Steps to Reproduce
1. Upload 50MB PDF file
2. Select Anthropic provider
3. Click "Analyze Content"
4. Wait 2 minutes

## Expected Behavior
PDF should be analyzed and game type detected

## Actual Behavior
Request times out with 504 error

## Logs
[Include relevant log entries]

## Configuration
AI_PROVIDER=anthropic
MAX_CONTENT_LENGTH=200
UPLOAD_TIMEOUT=300
```

This troubleshooting guide covers the most common issues and their solutions. For issues not covered here, collect diagnostic information and reach out through the appropriate support channels.
