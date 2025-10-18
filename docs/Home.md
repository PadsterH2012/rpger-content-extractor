---
title: RPGer Content Extractor Wiki
description: Comprehensive documentation hub for the AI-powered RPG content extraction system
tags: [wiki, documentation, navigation, rpg, content-extraction]
last_updated: 2025-10-18
author: HL-Auggie Analysis System
---

# RPGer Content Extractor Wiki

Welcome to the comprehensive documentation for RPGer Content Extractor - a powerful tool for extracting, categorizing, and managing RPG content from PDF sources.

## What is RPGer Content Extractor?

RPGer Content Extractor is a dockerized solution that helps tabletop RPG enthusiasts and game masters extract valuable content from PDF rulebooks, adventures, and supplements. It uses AI-powered analysis to categorize and organize content for easy reference and use.

## Quick Navigation

### Getting Started
- **[Installation Guide](Installation-Guide.md)** - Complete setup instructions
- **[Quick Start](Quick-Start.md)** - Get up and running in minutes
- **[Environment Configuration](deployment/environment-configuration.md)** - Environment and settings setup

### User Guides
- **[Web Interface Guide](user-guides/web-interface-guide.md)** - Using the web UI
- **[PDF Processing Guide](user-guides/pdf-processing-guide.md)** - How to extract content from PDFs
- **[Content Management Guide](user-guides/content-management-guide.md)** - Organizing extracted content
- **[AI Configuration](AI_CONFIGURATION.md)** - Configuring AI services

### Technical Documentation
- **[Architecture Overview](architecture/architecture-overview.md)** - System design and components
- **[API Documentation](api/api-reference.md)** - REST API reference
- **[Database Schema](architecture/database-schema.md)** - MongoDB and ChromaDB structure
- **[Docker Deployment Guide](deployment/docker-deployment-guide.md)** - Container deployment options

### Development
- **[Development Setup](development/development-setup.md)** - Local development environment
- **[Contributing Guide](development/contributing-guide.md)** - How to contribute
- **[Testing Guide](development/testing-guide.md)** - Running and writing tests
- **[Health Monitoring](operations/health-monitoring.md)** - System monitoring

### Troubleshooting
- **[Troubleshooting Guide](operations/troubleshooting-guide.md)** - Frequently encountered problems
- **[Documentation Index](index.md)** - Complete documentation
- **[GitHub Issues](../issues.md)** - Getting help and reporting issues

## Current Status

- **Version**: 1.0.44 (Build #44)
- **Docker Image**: `padster2012/rpger-content-extractor:latest`
- **CI/CD Status**: All tests passing
- **Documentation**: In progress

## Key Features

### Content Extraction
- **PDF Processing**: Extract text, images, and tables from RPG PDFs
- **AI-Powered Analysis**: Categorize content using advanced AI models
- **Multi-format Support**: Handle various PDF layouts and structures

### Content Organization
- **Smart Categorization**: Automatically organize by game type, edition, and content type
- **Semantic Search**: Find content using natural language queries
- **Metadata Management**: Rich metadata for easy filtering and discovery

### AI Integration
- **Multiple Providers**: Support for Anthropic Claude, OpenAI, and OpenRouter
- **300+ Models**: Access to a wide variety of AI models
- **Flexible Configuration**: Easy switching between providers and models

### Deployment Options
- **Production**: Pre-built Docker images for quick deployment
- **Development**: Source building with live reloading
- **Full Stack**: Self-contained with included databases

## Architecture

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   Web Interface │    │  Processing     │    │   AI Providers  │
│   (Flask)       │◄──►│  Engine         │◄──►│  (Claude/GPT)   │
└─────────────────┘    └─────────────────┘    └─────────────────┘
         │                       │                       
         ▼                       ▼                       
┌─────────────────┐    ┌─────────────────┐              
│   MongoDB       │    │   ChromaDB      │              
│   (Documents)   │    │   (Vectors)     │              
└─────────────────┘    └─────────────────┘              
```

## External Links

- **GitHub Repository**: [PadsterH2012/rpger-content-extractor](https://github.com/PadsterH2012/rpger-content-extractor)
- **Docker Hub**: [padster2012/rpger-content-extractor](https://hub.docker.com/r/padster2012/rpger-content-extractor)
- **Issues & Support**: [GitHub Issues](https://github.com/PadsterH2012/rpger-content-extractor/issues)

## Recent Updates

- **v1.0.44**: All tests passing, improved CI/CD pipeline
- **Docker Images**: Automated builds with version tagging
- **Install Script**: One-line installation with interactive setup
- **Documentation**: Comprehensive wiki and user guides

---

**Last Updated**: June 2025  
**Maintained by**: PadsterH2012  
**License**: MIT License
