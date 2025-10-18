FROM python:3.11-slim

# Accept build arguments from CI/CD
ARG VERSION_STRING=unknown
ARG BUILD_DATE=unknown
ARG GIT_COMMIT=unknown

# Set working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements and install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Create necessary directories
RUN mkdir -p uploads extracted logs

# Set build information as environment variables
ENV BUILD_VERSION=$VERSION_STRING
ENV BUILD_DATE=$BUILD_DATE  
ENV GIT_COMMIT=$GIT_COMMIT
ENV ENVIRONMENT=production

# Create version file for runtime access
RUN echo "$VERSION_STRING" > /app/VERSION

# Add metadata labels for Docker image inspection
LABEL version="$VERSION_STRING"
LABEL build.date="$BUILD_DATE"
LABEL git.commit="$GIT_COMMIT"
LABEL maintainer="PadsterH2012"
LABEL description="RPGer Content Extractor"

# Expose port
EXPOSE 5000

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:5000/health || exit 1

# Default command
CMD ["python", "ui/start_ui.py"]
