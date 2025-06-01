#!/bin/bash
# Start with container databases

echo "🚀 Starting rpger-content-extractor with container databases..."
docker-compose -f docker-compose.yml -f docker-compose.containers.yml up -d

echo "⏳ Waiting for services to be ready..."
sleep 30

echo "🔍 Checking service health..."
docker-compose -f docker-compose.yml -f docker-compose.containers.yml ps

echo "✅ Container stack started!"
echo "🌐 Web UI available at: http://localhost:5000"
echo "📊 MongoDB available at: localhost:27017"
echo "🔍 ChromaDB available at: http://localhost:8000"
