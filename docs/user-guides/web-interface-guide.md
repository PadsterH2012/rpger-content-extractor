---
title: Web Interface Guide
description: Complete guide to using the RPGer Content Extractor web interface
tags: [user-guide, web-interface, ui, tutorial]
last_updated: 2025-10-18
author: HL-Auggie Analysis System
---

# Web Interface Guide

## Overview

The RPGer Content Extractor web interface provides an intuitive, user-friendly way to process RPG PDFs and manage extracted content. This guide covers all features and workflows available through the web UI.

## Getting Started

### Accessing the Web Interface

1. **Start the Application**:
   ```bash
   cd /path/to/rpger-content-extractor
   python ui/start_ui.py
   ```

2. **Open in Browser**:
   - Local access: `http://localhost:5000`
   - Network access: `http://0.0.0.0:5000`

3. **System Requirements**:
   - Modern web browser (Chrome, Firefox, Safari, Edge)
   - JavaScript enabled
   - Stable internet connection for AI processing

## Main Dashboard

### Dashboard Overview

The main dashboard provides:
- **System Status**: Real-time health monitoring
- **Quick Actions**: Direct access to common tasks
- **Recent Activity**: Latest processing results
- **Statistics**: Usage and performance metrics

### Status Indicators

**System Health**:
- 🟢 Green: All systems operational
- 🟡 Yellow: Some services degraded
- 🔴 Red: Critical issues detected

**Database Status**:
- **MongoDB**: Document storage status
- **ChromaDB**: Vector database status
- **Collections**: Number of active collections

**AI Providers**:
- **Available**: Configured providers with API keys
- **Active**: Currently selected provider
- **Models**: Available models for selection

## PDF Processing Workflow

### Step 1: Upload PDF

1. **Drag and Drop**:
   - Drag PDF file directly onto the upload area
   - Visual feedback shows drop zone activation
   - Automatic file validation

2. **Browse and Select**:
   - Click "Choose File" button
   - Navigate to PDF location
   - Select file and confirm

3. **Upload Validation**:
   - File type check (PDF only)
   - Size validation (max 200MB)
   - Content preview generation

**Supported Formats**:
- PDF files only
- Maximum size: 200MB
- Any RPG system or edition

### Step 2: Configure Processing

#### AI Provider Selection

**Anthropic Claude** (Recommended):
- Highest accuracy for RPG content
- Best game detection capabilities
- Premium pricing

**OpenRouter**:
- Access to 300+ models
- Flexible model selection
- Variable pricing

**OpenAI**:
- Reliable performance
- Multiple model options
- Standard pricing

**Mock Provider**:
- Testing and development
- No API costs
- Limited functionality

#### Model Selection (OpenRouter)

When using OpenRouter, select from:
- **Recommended Models**: Pre-selected for RPG content
- **All Models**: Complete model catalog
- **Provider Groups**: Models organized by provider

#### Processing Options

**Content Type**:
- Source Material (default)
- Adventure/Scenario
- Supplement
- Novel/Fiction

**Advanced Options**:
- Run Confidence Test (slower but more accurate)
- Custom Game Type (override detection)
- Custom Edition (override detection)

### Step 3: Analysis Phase

#### Game Detection

The system automatically:
1. **Analyzes Content**: Scans PDF for game indicators
2. **Identifies Game Type**: D&D, Pathfinder, Call of Cthulhu, etc.
3. **Determines Edition**: 5th Edition, 2nd Edition, etc.
4. **Assigns Confidence**: Accuracy score for detection

**Analysis Results Display**:
- Game Type and Edition
- Confidence Score (0-100%)
- Detection Method Used
- Processing Time and Cost

#### Content Preview

Before extraction, review:
- **Detected Sections**: Identified content areas
- **Categories**: Predicted content types
- **Page Count**: Total pages to process
- **Estimated Processing Time**: Based on content size

### Step 4: Content Extraction

#### Extraction Process

1. **Start Extraction**: Click "Extract Content" button
2. **Real-time Progress**: Watch processing status
3. **Section Processing**: Individual section extraction
4. **Quality Enhancement**: Text cleanup and formatting
5. **Categorization**: AI-powered content classification

#### Progress Monitoring

**Progress Indicators**:
- Overall completion percentage
- Current section being processed
- Estimated time remaining
- Token usage and cost tracking

**Real-time Updates**:
- Processing status messages
- Error notifications
- Success confirmations
- Performance metrics

#### Extraction Results

**Content Summary**:
- Total sections extracted
- Categories identified
- Processing statistics
- Quality metrics

**Output Files**:
- JSON format for MongoDB
- ChromaDB format for vector storage
- Raw text extraction
- Processing metadata

### Step 5: Database Import

#### Import Options

**ChromaDB Import**:
- Vector storage for semantic search
- Automatic embedding generation
- Collection organization by game type
- Similarity search capabilities

**MongoDB Import**:
- Document storage for traditional queries
- Hierarchical collection structure
- Full-text search indexing
- Metadata preservation

**Dual Import**:
- Import to both databases
- Cross-reference maintenance
- Comprehensive search capabilities
- Data redundancy for reliability

#### Collection Management

**Automatic Collection Naming**:
- Based on game type and edition
- Hierarchical organization
- Conflict resolution
- Metadata preservation

**Manual Collection Selection**:
- Choose existing collection
- Create new collection
- Merge with existing content
- Override automatic naming

## Database Browsing

### ChromaDB Browser

#### Collection Overview

**Collection List**:
- Game type organization
- Document counts
- Last update timestamps
- Collection health status

**Collection Details**:
- Total documents
- Categories present
- Game metadata
- Storage statistics

#### Document Browsing

**Document List**:
- Paginated results (10 per page)
- Title and content preview
- Metadata display
- Page references

**Document Details**:
- Full content view
- Complete metadata
- Source information
- Processing details

#### Search Functionality

**Similarity Search**:
- Natural language queries
- Semantic matching
- Relevance scoring
- Context-aware results

**Metadata Filtering**:
- Filter by game type
- Filter by category
- Filter by page range
- Filter by confidence score

### MongoDB Browser

#### Collection Navigation

**Hierarchical View**:
- Game type organization
- Edition grouping
- Book type classification
- Collection listing

**Collection Statistics**:
- Document counts
- Storage size
- Index information
- Query performance

#### Document Management

**Document Viewing**:
- Structured data display
- Section navigation
- Metadata inspection
- Source file tracking

**Query Interface**:
- Simple text search
- Advanced filtering
- Aggregation queries
- Export capabilities

## System Monitoring

### Health Dashboard

#### System Status

**Service Health**:
- Web application status
- Database connectivity
- AI provider availability
- File system health

**Performance Metrics**:
- Response times
- Processing speeds
- Memory usage
- Storage utilization

#### Error Monitoring

**Error Display**:
- Recent errors and warnings
- Error categorization
- Resolution suggestions
- Contact information

**Troubleshooting**:
- Common issue solutions
- Diagnostic tools
- Log file access
- Support resources

### Usage Analytics

#### Processing Statistics

**File Processing**:
- Total files processed
- Success/failure rates
- Average processing times
- Popular game types

**AI Usage**:
- Token consumption
- Cost tracking
- Provider performance
- Model effectiveness

#### Database Statistics

**Storage Metrics**:
- Total documents stored
- Storage space used
- Collection growth
- Query performance

**Search Analytics**:
- Popular search terms
- Search success rates
- User behavior patterns
- Content discovery trends

## Advanced Features

### Batch Processing

#### Multiple File Upload

**Drag and Drop Multiple Files**:
- Select multiple PDFs
- Batch upload progress
- Individual file status
- Collective processing

**Folder Upload**:
- Upload entire directories
- Recursive file discovery
- Automatic organization
- Progress tracking

#### Batch Configuration

**Global Settings**:
- Default AI provider
- Processing options
- Output preferences
- Error handling

**Per-File Overrides**:
- Individual game type
- Custom editions
- Specific categories
- Processing priorities

### API Integration

#### API Key Management

**Generate API Keys**:
- Create access tokens
- Set permissions
- Monitor usage
- Revoke access

**Integration Examples**:
- Python client code
- JavaScript examples
- cURL commands
- Postman collections

### Export and Backup

#### Data Export

**Export Formats**:
- JSON data export
- CSV for spreadsheets
- XML for integration
- Custom formats

**Export Scope**:
- Individual documents
- Complete collections
- Filtered results
- Metadata only

#### Backup Management

**Automated Backups**:
- Scheduled exports
- Incremental backups
- Cloud storage integration
- Restoration procedures

## Troubleshooting

### Common Issues

#### Upload Problems

**File Too Large**:
- Maximum size is 200MB
- Compress PDF if possible
- Split large documents
- Contact support for exceptions

**Invalid File Type**:
- Only PDF files accepted
- Check file extension
- Verify file integrity
- Convert other formats to PDF

#### Processing Errors

**AI Provider Issues**:
- Check API key configuration
- Verify provider availability
- Try alternative provider
- Check rate limits

**Memory Issues**:
- Large files may timeout
- Try smaller sections
- Restart application
- Increase system resources

#### Database Problems

**Connection Failures**:
- Check database status
- Verify network connectivity
- Restart database services
- Check configuration

**Import Errors**:
- Verify data format
- Check collection permissions
- Monitor storage space
- Review error logs

### Getting Help

#### Support Resources

**Documentation**:
- Complete user guides
- API documentation
- Troubleshooting guides
- FAQ section

**Community Support**:
- GitHub issues
- Discussion forums
- User community
- Feature requests

**Professional Support**:
- Email support
- Priority assistance
- Custom development
- Training services

## Best Practices

### Optimal Usage

#### File Preparation

**PDF Quality**:
- Use high-quality scans
- Ensure text is searchable
- Avoid password protection
- Check for corruption

**Organization**:
- Consistent naming conventions
- Logical folder structure
- Metadata preparation
- Version control

#### Processing Efficiency

**Provider Selection**:
- Use Claude for best results
- OpenRouter for cost optimization
- Mock for testing
- Consider rate limits

**Batch Processing**:
- Group similar content
- Process during off-peak hours
- Monitor resource usage
- Plan for long processing times

#### Data Management

**Collection Organization**:
- Use descriptive names
- Maintain consistent structure
- Regular cleanup
- Backup important data

**Search Optimization**:
- Use specific search terms
- Leverage metadata filters
- Understand search types
- Save common queries

### Security Considerations

#### Data Protection

**File Security**:
- Temporary file cleanup
- Secure upload handling
- Access control
- Audit logging

**API Security**:
- Secure API keys
- Rate limiting
- Input validation
- Error handling

#### Privacy

**Content Handling**:
- Temporary processing only
- No permanent storage of uploads
- Secure deletion
- Privacy compliance
