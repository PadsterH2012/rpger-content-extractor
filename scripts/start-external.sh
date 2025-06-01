#!/bin/bash
# Start with external databases

echo "🚀 Starting rpger-content-extractor with external databases..."

# Check if external environment variables are set
if [ -z "$EXTERNAL_MONGODB_URL" ] || [ -z "$EXTERNAL_CHROMADB_URL" ]; then
    echo "❌ Error: External database URLs not configured"
    echo "Please set EXTERNAL_MONGODB_URL and EXTERNAL_CHROMADB_URL environment variables"
    echo "Or create a .env file with these values"
    exit 1
fi

docker-compose -f docker-compose.yml -f docker-compose.external.yml up -d

echo "⏳ Waiting for service to be ready..."
sleep 15

echo "🔍 Checking service health..."
docker-compose -f docker-compose.yml -f docker-compose.external.yml ps

echo "✅ External DB mode started!"
echo "🌐 Web UI available at: http://localhost:5000"
