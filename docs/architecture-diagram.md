# PDF Extractor Application Architecture

## System Overview

```mermaid
graph TB
    %% User Interface Layer
    subgraph "Frontend (UI)"
        UI[Web Interface<br/>Flask Templates + JavaScript]
        UPLOAD[File Upload]
        PROGRESS[Progress Tracking]
        SETTINGS[Settings Panel]
        BROWSER[Database Browser]
    end

    %% API Layer
    subgraph "Flask API Layer"
        FLASK[Flask App<br/>ui/app.py]
        ROUTES[API Routes]
        STATUS[Status Endpoint]
        MODELS_API[Models API]
    end

    %% Core Processing Modules
    subgraph "Core Processing"
        PDF_PROC[PDF Processor<br/>MultiGamePDFProcessor]
        AI_DETECTOR[AI Game Detector<br/>Game Metadata Analysis]
        AI_CAT[AI Categorizer<br/>Content Classification]
        TEXT_EXT[Text Extractor<br/>PDF Content Extraction]
    end

    %% AI Provider Integration
    subgraph "AI Providers"
        OPENROUTER[OpenRouter API<br/>Multiple Models]
        ANTHROPIC[Anthropic Claude]
        OPENAI[OpenAI GPT]
        LOCAL[Local LLM]
        MOCK[Mock Provider]
    end

    %% Database Layer
    subgraph "Database Storage"
        MONGODB[MongoDB<br/>Document Storage]
        CHROMADB[ChromaDB<br/>Vector Database]
        COLLECTIONS[Collection Manager<br/>Multi-Game Collections]
    end

    %% Monitoring & Tracking
    subgraph "Monitoring"
        TOKEN_TRACKER[Token Usage Tracker<br/>API Call Monitoring]
        PROGRESS_TRACKER[Progress Tracker<br/>Real-time Updates]
        SESSION_MGR[Session Manager<br/>User Sessions]
    end

    %% External Services
    subgraph "External APIs"
        OR_MODELS[OpenRouter Models API]
        OR_INFERENCE[OpenRouter Inference API]
        ANTHROPIC_API[Anthropic API]
        OPENAI_API[OpenAI API]
    end

    %% Data Flow Connections
    UI --> FLASK
    UPLOAD --> PDF_PROC
    FLASK --> ROUTES
    ROUTES --> STATUS
    ROUTES --> MODELS_API
    
    PDF_PROC --> AI_DETECTOR
    PDF_PROC --> AI_CAT
    PDF_PROC --> TEXT_EXT
    
    AI_DETECTOR --> OPENROUTER
    AI_CAT --> OPENROUTER
    
    OPENROUTER --> OR_MODELS
    OPENROUTER --> OR_INFERENCE
    ANTHROPIC --> ANTHROPIC_API
    OPENAI --> OPENAI_API
    
    PDF_PROC --> MONGODB
    PDF_PROC --> CHROMADB
    COLLECTIONS --> MONGODB
    COLLECTIONS --> CHROMADB
    
    FLASK --> TOKEN_TRACKER
    FLASK --> PROGRESS_TRACKER
    FLASK --> SESSION_MGR
    
    BROWSER --> MONGODB
    BROWSER --> CHROMADB
    
    STATUS --> TOKEN_TRACKER
    MODELS_API --> OR_MODELS

    %% Styling
    classDef frontend fill:#e1f5fe
    classDef api fill:#f3e5f5
    classDef processing fill:#e8f5e8
    classDef ai fill:#fff3e0
    classDef database fill:#fce4ec
    classDef monitoring fill:#f1f8e9
    classDef external fill:#ffebee

    class UI,UPLOAD,PROGRESS,SETTINGS,BROWSER frontend
    class FLASK,ROUTES,STATUS,MODELS_API api
    class PDF_PROC,AI_DETECTOR,AI_CAT,TEXT_EXT processing
    class OPENROUTER,ANTHROPIC,OPENAI,LOCAL,MOCK ai
    class MONGODB,CHROMADB,COLLECTIONS database
    class TOKEN_TRACKER,PROGRESS_TRACKER,SESSION_MGR monitoring
    class OR_MODELS,OR_INFERENCE,ANTHROPIC_API,OPENAI_API external
```

## Data Flow Architecture

```mermaid
sequenceDiagram
    participant User
    participant UI as Web UI
    participant Flask as Flask API
    participant Processor as PDF Processor
    participant AI as AI Services
    participant DB as Databases
    participant Tracker as Token Tracker

    User->>UI: Upload PDF
    UI->>Flask: POST /upload
    Flask->>Flask: Save file
    Flask-->>UI: Upload success

    User->>UI: Start Analysis
    UI->>Flask: POST /analyze
    Flask->>Tracker: Start session
    Flask->>Processor: Initialize
    Processor->>AI: Analyze game metadata
    AI->>AI: OpenRouter API call
    AI->>Tracker: Record API usage
    AI-->>Processor: Game metadata
    Processor-->>Flask: Analysis results
    Flask-->>UI: Analysis complete

    User->>UI: Start Extraction
    UI->>Flask: POST /extract
    Flask->>Processor: Extract content
    Processor->>AI: Game detection (duplicate)
    AI->>Tracker: Record API usage
    Processor->>Processor: Extract sections
    Processor->>DB: Store in MongoDB
    Processor->>DB: Store in ChromaDB
    Processor-->>Flask: Extraction complete
    Flask->>Tracker: Get session summary
    Flask-->>UI: Results + token usage

    UI->>Flask: GET /status (periodic)
    Flask->>Tracker: Get session data
    Tracker-->>Flask: Token summary
    Flask-->>UI: Status + costs
```

## Token Tracking System

```mermaid
graph LR
    subgraph "Session Types"
        UI_SESSION[UI Session<br/>Models API calls]
        EXTRACT_SESSION[Extraction Session<br/>Analysis + Extraction calls]
    end

    subgraph "API Call Types"
        MODELS_CALL[Models API<br/>0 tokens, $0.00]
        ANALYSIS_CALL[Analysis AI<br/>~3,750 tokens, ~$0.0007]
        EXTRACTION_CALL[Extraction AI<br/>~3,750 tokens, ~$0.0007]
    end

    subgraph "Token Tracker"
        TRACKER[Token Usage Tracker]
        SESSION_STORE[Session Storage]
        COST_CALC[Cost Calculator]
    end

    subgraph "UI Display"
        API_COUNT[API Calls Count]
        TOKEN_COUNT[Session Tokens]
        COST_DISPLAY[Session Cost]
    end

    MODELS_CALL --> UI_SESSION
    ANALYSIS_CALL --> EXTRACT_SESSION
    EXTRACTION_CALL --> EXTRACT_SESSION

    UI_SESSION --> TRACKER
    EXTRACT_SESSION --> TRACKER

    TRACKER --> SESSION_STORE
    TRACKER --> COST_CALC

    SESSION_STORE --> API_COUNT
    SESSION_STORE --> TOKEN_COUNT
    COST_CALC --> COST_DISPLAY

    classDef session fill:#e3f2fd
    classDef calls fill:#f3e5f5
    classDef tracker fill:#e8f5e8
    classDef display fill:#fff3e0

    class UI_SESSION,EXTRACT_SESSION session
    class MODELS_CALL,ANALYSIS_CALL,EXTRACTION_CALL calls
    class TRACKER,SESSION_STORE,COST_CALC tracker
    class API_COUNT,TOKEN_COUNT,COST_DISPLAY display
```

## Database Architecture

```mermaid
graph TB
    subgraph "MongoDB Collections"
        MONGO_HIER[Hierarchical Structure<br/>rpger.source_material.{game}.{edition}.{book}.{collection}]
        MONGO_DOCS[Document Storage<br/>Sections, Metadata, Content]
        MONGO_INDEX[Indexes<br/>Game, Edition, Category]
    end

    subgraph "ChromaDB Collections"
        CHROMA_VECTOR[Vector Storage<br/>Embeddings for Similarity Search]
        CHROMA_META[Metadata Storage<br/>Game Type, Edition, Category]
        CHROMA_SEARCH[Semantic Search<br/>Content Similarity]
    end

    subgraph "Collection Manager"
        MULTI_MGR[Multi-Game Collection Manager]
        COLLECTION_PARSER[Collection Name Parser]
        METADATA_HANDLER[Metadata Handler]
    end

    subgraph "Data Sources"
        PDF_CONTENT[PDF Content<br/>Extracted Sections]
        GAME_META[Game Metadata<br/>Type, Edition, Book]
        AI_CATEGORIES[AI Categories<br/>Spells, Classes, Items]
    end

    PDF_CONTENT --> MULTI_MGR
    GAME_META --> MULTI_MGR
    AI_CATEGORIES --> MULTI_MGR

    MULTI_MGR --> COLLECTION_PARSER
    MULTI_MGR --> METADATA_HANDLER

    COLLECTION_PARSER --> MONGO_HIER
    METADATA_HANDLER --> MONGO_DOCS
    METADATA_HANDLER --> CHROMA_META

    MONGO_DOCS --> MONGO_INDEX
    CHROMA_META --> CHROMA_VECTOR
    CHROMA_VECTOR --> CHROMA_SEARCH

    classDef mongodb fill:#4caf50,color:#fff
    classDef chromadb fill:#2196f3,color:#fff
    classDef manager fill:#ff9800,color:#fff
    classDef source fill:#9c27b0,color:#fff

    class MONGO_HIER,MONGO_DOCS,MONGO_INDEX mongodb
    class CHROMA_VECTOR,CHROMA_META,CHROMA_SEARCH chromadb
    class MULTI_MGR,COLLECTION_PARSER,METADATA_HANDLER manager
    class PDF_CONTENT,GAME_META,AI_CATEGORIES source
```

## Processing Workflow

```mermaid
flowchart TD
    START([User Uploads PDF]) --> UPLOAD[File Upload & Validation]
    UPLOAD --> ANALYSIS{Analysis Phase}

    ANALYSIS --> AI_DETECT[AI Game Detection<br/>~3,750 tokens]
    AI_DETECT --> GAME_META[Extract Game Metadata<br/>Type, Edition, Book]
    GAME_META --> ANALYSIS_COMPLETE[Analysis Complete]

    ANALYSIS_COMPLETE --> EXTRACTION{Extraction Phase}

    EXTRACTION --> PDF_PARSE[PDF Text Extraction]
    PDF_PARSE --> AI_DETECT2[AI Game Detection<br/>~3,750 tokens<br/>(Duplicate)]
    AI_DETECT2 --> SECTION_EXTRACT[Section Extraction<br/>Rules-based]

    SECTION_EXTRACT --> CATEGORIZE{Categorization}
    CATEGORIZE -->|AI Enabled| AI_CAT[AI Categorization<br/>Per Section]
    CATEGORIZE -->|AI Disabled| RULE_CAT[Rule-based Categorization<br/>Fast Processing]

    AI_CAT --> ENHANCE{Text Enhancement}
    RULE_CAT --> ENHANCE

    ENHANCE -->|Enabled| TEXT_ENHANCE[Text Quality Enhancement<br/>Spell Check, OCR Cleanup]
    ENHANCE -->|Disabled| SKIP_ENHANCE[Skip Enhancement<br/>Raw Text]

    TEXT_ENHANCE --> STORAGE[Database Storage]
    SKIP_ENHANCE --> STORAGE

    STORAGE --> MONGO_STORE[MongoDB Storage<br/>Hierarchical Collections]
    STORAGE --> CHROMA_STORE[ChromaDB Storage<br/>Vector Embeddings]

    MONGO_STORE --> COMPLETE[Processing Complete]
    CHROMA_STORE --> COMPLETE

    COMPLETE --> RESULTS[Display Results<br/>Token Usage & Costs]

    %% Styling
    classDef startEnd fill:#4caf50,color:#fff
    classDef process fill:#2196f3,color:#fff
    classDef ai fill:#ff9800,color:#fff
    classDef decision fill:#9c27b0,color:#fff
    classDef storage fill:#f44336,color:#fff

    class START,COMPLETE,RESULTS startEnd
    class UPLOAD,PDF_PARSE,SECTION_EXTRACT,TEXT_ENHANCE,SKIP_ENHANCE process
    class AI_DETECT,AI_DETECT2,AI_CAT ai
    class ANALYSIS,EXTRACTION,CATEGORIZE,ENHANCE decision
    class MONGO_STORE,CHROMA_STORE,STORAGE storage
```

## Key Features & Optimizations

### Performance Optimizations
- **AI Categorization**: Disabled by default for 97% speed improvement
- **Confidence Testing**: Disabled by default for 95% speed improvement
- **Text Enhancement**: Moved to post-processing for 40% speed improvement
- **Caching**: OpenRouter models cached for 1 hour
- **Session Management**: Efficient token tracking across phases

### Cost Optimizations
- **Token Reduction**: From ~70,000 to ~7,500 tokens (89% reduction)
- **Cost Reduction**: From ~$0.35 to ~$0.0014 (99.8% reduction)
- **API Call Reduction**: From 68+ to 2 calls (97% reduction)
- **Smart Caching**: Avoid redundant API calls

### Monitoring & Transparency
- **Real-time Token Tracking**: All API calls monitored
- **Cost Calculation**: Accurate pricing using OpenRouter rates
- **Session Management**: UI and extraction sessions tracked separately
- **Progress Updates**: Real-time extraction progress
- **Debug Logging**: Comprehensive logging for troubleshooting

### Database Features
- **Hierarchical Collections**: Organized by game/edition/book
- **Dual Storage**: MongoDB for documents, ChromaDB for vectors
- **Metadata Preservation**: Game detection results stored
- **Search Capabilities**: Both text and semantic search
- **Collection Management**: Browse, query, and manage collections
