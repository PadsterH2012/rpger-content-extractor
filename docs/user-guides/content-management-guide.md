---
title: Content Management Guide
description: Guide to organizing, searching, and managing extracted RPG content
tags: [user-guide, content-management, search, organization]
last_updated: 2025-10-18
author: HL-Auggie Analysis System
---

# Content Management Guide

## Overview

This guide covers how to effectively organize, search, and manage your extracted RPG content using the dual database system (MongoDB and ChromaDB). Learn to maximize the value of your processed content through efficient organization and powerful search capabilities.

## Understanding the Storage System

### Dual Database Architecture

The system uses two complementary databases:

**MongoDB (Document Storage)**:
- Traditional document database
- Hierarchical organization
- Full-text search capabilities
- Complex queries and aggregations
- Structured data relationships

**ChromaDB (Vector Storage)**:
- AI-powered semantic search
- Similarity matching
- Context-aware queries
- Natural language search
- Content discovery

### Collection Organization

#### Hierarchical Structure

Collections are organized using a hierarchical naming convention:
```
rpger.source_material.{game_type}.{edition}.{book_type}.{collection_name}
```

**Examples**:
- `rpger.source_material.dnd.5th_edition.phb.core_rules`
- `rpger.source_material.pathfinder.2nd_edition.crb.character_creation`
- `rpger.source_material.call_of_cthulhu.7th_edition.keeper.investigation`

#### Automatic Organization

**Game Type Grouping**:
- All content automatically grouped by detected game system
- Consistent naming across all content
- Easy navigation and discovery

**Edition Separation**:
- Different editions stored separately
- Prevents confusion between rule sets
- Maintains version integrity

**Content Type Classification**:
- Source materials vs. adventures
- Core rules vs. supplements
- Official vs. third-party content

## Content Browsing

### Web Interface Navigation

#### Collection Browser

**MongoDB Collections**:
1. Navigate to "Browse MongoDB" section
2. Select game type from dropdown
3. Choose specific collection
4. Browse documents with pagination

**ChromaDB Collections**:
1. Navigate to "Browse ChromaDB" section
2. View collections organized by game type
3. See document counts and metadata
4. Access similarity search features

#### Document Viewing

**Document Details**:
- Full content display
- Metadata information
- Source file references
- Processing details
- Category assignments

**Navigation Features**:
- Page-by-page browsing
- Section jumping
- Category filtering
- Search within document

### Command Line Browsing

#### Collection Status
```bash
python Extraction.py status
```
Shows:
- Available collections
- Document counts
- Storage statistics
- Health status

#### Browse Specific Collection
```bash
python Extraction.py browse "collection_name"
```
Displays:
- Collection contents
- Document summaries
- Metadata overview
- Search capabilities

## Search Capabilities

### MongoDB Text Search

#### Simple Text Search

**Web Interface**:
1. Enter search terms in search box
2. Select target collections
3. Choose search scope (title, content, or both)
4. Review results with relevance scoring

**Command Line**:
```bash
python Extraction.py search "fireball spell"
```

#### Advanced Query Options

**Field-Specific Search**:
- Search within specific fields
- Combine multiple criteria
- Use regular expressions
- Apply date ranges

**Boolean Operators**:
- AND: `spell AND damage`
- OR: `sword OR weapon`
- NOT: `magic NOT spell`
- Phrases: `"magic missile"`

**Metadata Filtering**:
- Filter by game type
- Filter by edition
- Filter by category
- Filter by page range

### ChromaDB Semantic Search

#### Natural Language Queries

**How It Works**:
- Converts queries to vector embeddings
- Finds semantically similar content
- Returns contextually relevant results
- Understands intent and meaning

**Example Queries**:
- "How to create a character"
- "Combat rules for spellcasters"
- "Treasure and magic items"
- "Social interaction mechanics"

#### Similarity Search

**Find Similar Content**:
1. Select a document or section
2. Click "Find Similar"
3. Review semantically related content
4. Explore connections and relationships

**Use Cases**:
- Find related rules across different books
- Discover similar spells or abilities
- Locate comparable character options
- Identify thematic content

### Cross-Database Search

#### Unified Search Interface

**Combined Results**:
- Search both databases simultaneously
- Merge and rank results
- Eliminate duplicates
- Provide comprehensive coverage

**Search Strategy**:
1. Start with semantic search for discovery
2. Use text search for specific terms
3. Combine results for complete coverage
4. Refine with metadata filters

## Content Organization

### Collection Management

#### Creating Collections

**Automatic Creation**:
- Collections created during import
- Based on detected game metadata
- Follows naming conventions
- Includes proper categorization

**Manual Collection Creation**:
1. Choose "Create Collection" option
2. Specify game type and edition
3. Define collection purpose
4. Set metadata and tags

#### Collection Maintenance

**Regular Tasks**:
- Remove duplicate content
- Update metadata
- Reorganize misplaced content
- Optimize search indexes

**Quality Assurance**:
- Verify categorization accuracy
- Check for missing content
- Validate cross-references
- Monitor search performance

### Content Categorization

#### Category System

**Primary Categories**:
- **Character**: Creation, classes, races, advancement
- **Combat**: Rules, actions, conditions, tactics
- **Magic**: Spells, magical items, supernatural abilities
- **Equipment**: Weapons, armor, gear, vehicles
- **Setting**: Locations, history, cultures, organizations
- **Rules**: Core mechanics, optional rules, variants
- **Adventure**: Scenarios, encounters, plot hooks

**Subcategories**:
- Detailed classification within primary categories
- Game-specific subcategories
- Custom user-defined categories
- Hierarchical organization

#### Tagging System

**Automatic Tags**:
- Generated during AI processing
- Based on content analysis
- Game-specific terminology
- Contextual relevance

**Manual Tags**:
- User-defined descriptors
- Campaign-specific tags
- Personal organization system
- Cross-reference markers

### Metadata Management

#### Core Metadata Fields

**Source Information**:
- Game type and edition
- Source book and page
- Publisher and author
- Publication date

**Content Metadata**:
- Category and subcategory
- Tags and keywords
- Word count and complexity
- Quality scores

**Processing Metadata**:
- Extraction method
- AI provider used
- Processing date
- Confidence scores

#### Metadata Editing

**Bulk Operations**:
- Update multiple documents
- Apply consistent tagging
- Correct categorization errors
- Standardize metadata

**Individual Editing**:
- Correct specific errors
- Add custom metadata
- Update categorization
- Enhance descriptions

## Advanced Search Techniques

### Query Optimization

#### Search Strategy

**Start Broad, Narrow Down**:
1. Begin with general terms
2. Add specific criteria
3. Use filters to refine
4. Combine search types

**Use Multiple Approaches**:
- Text search for exact terms
- Semantic search for concepts
- Metadata filters for precision
- Cross-reference for completeness

#### Search Tips

**Effective Keywords**:
- Use game-specific terminology
- Include synonyms and variants
- Try different phrasings
- Consider abbreviations

**Filter Usage**:
- Combine multiple filters
- Use date ranges effectively
- Apply confidence thresholds
- Leverage category filters

### Complex Queries

#### MongoDB Aggregation

**Statistical Queries**:
```javascript
// Count spells by level
db.collection.aggregate([
  { $match: { "category": "Spells" } },
  { $group: { 
    _id: "$metadata.spell_level", 
    count: { $sum: 1 } 
  }}
])
```

**Cross-Collection Analysis**:
```javascript
// Compare content across editions
db.collection.aggregate([
  { $group: { 
    _id: "$game_metadata.edition", 
    total_spells: { $sum: 1 },
    avg_level: { $avg: "$metadata.spell_level" }
  }}
])
```

#### ChromaDB Advanced Queries

**Multi-Criteria Search**:
```python
# Search with multiple filters
results = collection.query(
    query_texts=["character creation"],
    n_results=10,
    where={
        "$and": [
            {"game_type": {"$eq": "D&D"}},
            {"edition": {"$eq": "5th Edition"}},
            {"category": {"$eq": "Character"}}
        ]
    }
)
```

**Similarity Threshold**:
```python
# Find highly similar content only
results = collection.query(
    query_texts=["spell casting rules"],
    n_results=5,
    where={"similarity_threshold": 0.8}
)
```

## Data Export and Backup

### Export Options

#### Format Selection

**JSON Export**:
- Complete data structure
- Preserves all metadata
- Easy to process programmatically
- Standard interchange format

**CSV Export**:
- Spreadsheet compatibility
- Statistical analysis
- Simplified data view
- Custom field selection

**Text Export**:
- Human-readable format
- Content-only extraction
- Documentation generation
- Simple backup

#### Export Scope

**Full Collection Export**:
- Complete collection data
- All documents and metadata
- Preserves relationships
- Comprehensive backup

**Filtered Export**:
- Specific search results
- Category-based selection
- Date range filtering
- Custom criteria

**Individual Document Export**:
- Single document extraction
- Specific content needs
- Sharing and collaboration
- Reference material

### Backup Strategies

#### Automated Backups

**Scheduled Exports**:
- Daily incremental backups
- Weekly full backups
- Monthly archive creation
- Automated cloud storage

**Backup Verification**:
- Integrity checking
- Restoration testing
- Version validation
- Error monitoring

#### Manual Backup Procedures

**Before Major Changes**:
- Export current state
- Document changes planned
- Create restoration point
- Test backup integrity

**Regular Maintenance**:
- Monthly full exports
- Quarterly archive creation
- Annual system backup
- Disaster recovery testing

## Performance Optimization

### Search Performance

#### Index Optimization

**MongoDB Indexes**:
- Text search indexes
- Compound field indexes
- Category-specific indexes
- Performance monitoring

**ChromaDB Optimization**:
- Collection size management
- Embedding optimization
- Query caching
- Memory management

#### Query Optimization

**Efficient Queries**:
- Use specific filters first
- Limit result sets appropriately
- Cache frequent queries
- Monitor performance metrics

**Avoid Performance Issues**:
- Don't use overly broad searches
- Limit wildcard usage
- Use pagination for large results
- Monitor resource usage

### Storage Management

#### Database Maintenance

**Regular Cleanup**:
- Remove duplicate content
- Archive old data
- Optimize indexes
- Compact databases

**Capacity Planning**:
- Monitor storage growth
- Plan for expansion
- Optimize data structures
- Implement retention policies

#### Content Lifecycle

**Content Aging**:
- Identify outdated content
- Archive superseded versions
- Maintain current editions
- Plan for new releases

**Quality Improvement**:
- Refine categorizations
- Improve metadata
- Enhance search terms
- Update relationships

## Best Practices

### Organization Best Practices

#### Consistent Naming
1. **Use Standard Conventions**: Follow established naming patterns
2. **Descriptive Names**: Make collection purposes clear
3. **Version Control**: Track different editions and updates
4. **Logical Grouping**: Organize by logical relationships

#### Metadata Standards
1. **Complete Information**: Fill all relevant metadata fields
2. **Consistent Terminology**: Use standardized terms
3. **Regular Updates**: Keep metadata current
4. **Quality Control**: Verify accuracy regularly

### Search Best Practices

#### Effective Searching
1. **Start Simple**: Begin with basic terms
2. **Refine Gradually**: Add filters and criteria
3. **Use Multiple Methods**: Combine different search types
4. **Save Useful Queries**: Bookmark effective searches

#### Result Management
1. **Review Thoroughly**: Check result relevance
2. **Use Filters**: Narrow down large result sets
3. **Export When Needed**: Save important results
4. **Share Findings**: Collaborate with others

### Maintenance Best Practices

#### Regular Tasks
1. **Weekly Reviews**: Check for new content and issues
2. **Monthly Cleanup**: Remove duplicates and errors
3. **Quarterly Optimization**: Improve performance
4. **Annual Archives**: Create long-term backups

#### Quality Assurance
1. **Verify Accuracy**: Check categorization and metadata
2. **Test Searches**: Ensure findability
3. **Monitor Performance**: Track system health
4. **User Feedback**: Incorporate user suggestions
