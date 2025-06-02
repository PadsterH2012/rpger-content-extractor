# Module-Specific Complexity Analysis

## Detailed Analysis of High-Priority Modules

### 1. ai_game_detector.py - Critical Complexity Issues

**Overall Stats:**
- **Lines:** 1,182
- **Methods:** 43
- **Classes:** 6
- **Critical Complexity:** 2 functions with F-level complexity

#### **Critical Issue: MockAIClient._analyze_content (Complexity: 45)**

**Location:** Lines 882-1112 (~230 lines)
**Problem:** Massive conditional logic for game detection simulation

**Current Structure:**
```python
def _analyze_content(self, prompt: str) -> Dict[str, Any]:
    # 200+ lines of nested if/elif/else statements
    # Hardcoded responses for different game systems
    # Complex pattern matching logic
    # Duplicate fallback handling
```

**Specific Issues:**
1. **45 conditional branches** - highest complexity in codebase
2. **200+ lines** of hardcoded game detection logic
3. **Duplicate pattern matching** across different games
4. **No abstraction** for game-specific rules
5. **Difficult to test** individual detection paths
6. **Hard to extend** for new game systems

**Refactoring Strategy:**
```python
# Current approach (simplified):
if "D&D" in text or "Dungeons" in text:
    if "5th Edition" in text or "5e" in text:
        return dnd_5e_response()
    elif "3.5" in text:
        return dnd_35_response()
    # ... 40+ more conditions

# Proposed approach:
class GameDetectionRules:
    def __init__(self):
        self.rule_sets = [
            DnD5eRules(),
            DnD35Rules(),
            PathfinderRules(),
            # ... extensible rule system
        ]
    
    def detect(self, content: str) -> Dict[str, Any]:
        for rule_set in self.rule_sets:
            if rule_set.matches(content):
                return rule_set.generate_response(content)
        return self.unknown_response()
```

**Effort Estimate:** 3-4 days
**Risk:** Medium (affects test mocking, but isolated)
**Impact:** High (enables easy extension, improves maintainability)

#### **Secondary Issue: AIGameDetector._validate_ai_result (Complexity: 13)**

**Location:** Lines 346-408 (~62 lines)
**Problem:** Complex validation and enhancement logic

**Current Issues:**
1. **Multiple validation paths** for different game types
2. **Nested dictionary manipulation**
3. **Special case handling** for novels vs games
4. **Mixed concerns** (validation + enhancement)

**Refactoring Strategy:**
```python
# Extract validation rules
class ValidationRules:
    @staticmethod
    def validate_confidence(value: Any) -> float:
        try:
            confidence = float(value)
            return max(0.0, min(1.0, confidence))
        except (ValueError, TypeError):
            return 0.5
    
    @staticmethod
    def validate_game_type(value: Any) -> str:
        if not value or not isinstance(value, str):
            return "Unknown"
        return value.strip()

# Simplified validation method
def _validate_ai_result(self, ai_result: Dict[str, Any], pdf_path: Path) -> Dict[str, Any]:
    validator = ValidationRules()
    return {
        "confidence": validator.validate_confidence(ai_result.get("confidence")),
        "game_type": validator.validate_game_type(ai_result.get("game_type")),
        # ... other validations
    }
```

### 2. pdf_processor.py - Memory and Processing Issues

**Overall Stats:**
- **Lines:** 1,413
- **Methods:** 35+
- **Critical Issues:** Large file memory usage, complex categorization logic

#### **Critical Issue: _simple_categorize_content (Complexity: 21)**

**Location:** Lines 309-340 (~32 lines)
**Problem:** Complex content categorization with hardcoded rules

**Current Issues:**
1. **21 conditional branches** for content type detection
2. **Hardcoded pattern matching** for different content types
3. **No abstraction** for categorization rules
4. **Difficult to extend** for new content types

**Refactoring Strategy:**
```python
# Current approach:
def _simple_categorize_content(self, text: str, game_metadata: Dict[str, Any]) -> str:
    text_lower = text.lower()
    
    # Combat/mechanics patterns
    if any(term in text_lower for term in ["attack", "damage", "ac", "armor class"]):
        if "spell" in text_lower:
            return "spell"
        return "combat"
    
    # ... 20+ more conditions

# Proposed approach:
class ContentCategorizer:
    def __init__(self):
        self.rules = [
            SpellContentRule(),
            CombatContentRule(),
            LocationContentRule(),
            CharacterContentRule(),
            # ... extensible rules
        ]
    
    def categorize(self, text: str, metadata: Dict[str, Any]) -> str:
        for rule in self.rules:
            if rule.matches(text, metadata):
                return rule.category
        return "general"

class SpellContentRule(ContentRule):
    category = "spell"
    patterns = ["spell", "magic", "casting", "components"]
    
    def matches(self, text: str, metadata: Dict[str, Any]) -> bool:
        return any(pattern in text.lower() for pattern in self.patterns)
```

#### **Memory Management Issue: Large PDF Processing**

**Problem:** Entire PDF loaded into memory simultaneously

**Current Issues:**
1. **Full PDF in memory** for processing
2. **No streaming** for large files
3. **Memory spikes** with files >100MB
4. **No progressive processing**

**Refactoring Strategy:**
```python
# Current approach:
def extract_pdf(self, pdf_path: Path):
    doc = fitz.open(pdf_path)  # Loads entire PDF
    # Process all pages at once
    
# Proposed approach:
class StreamingPDFProcessor:
    def __init__(self, chunk_size: int = 10):
        self.chunk_size = chunk_size
    
    def extract_pdf_streaming(self, pdf_path: Path):
        with fitz.open(pdf_path) as doc:
            for page_chunk in self._chunk_pages(doc, self.chunk_size):
                yield self._process_page_chunk(page_chunk)
    
    def _chunk_pages(self, doc, chunk_size: int):
        for i in range(0, len(doc), chunk_size):
            yield doc[i:i + chunk_size]
```

### 3. ui/app.py - Flask Route Complexity

**Overall Stats:**
- **Lines:** 1,593
- **Routes:** 20+
- **Critical Issues:** Large route functions, mixed concerns

#### **Critical Issue: browse_mongodb_collection (Complexity: 21)**

**Location:** Lines 1194-1350 (~156 lines)
**Problem:** Complex database browsing with pagination and filtering

**Current Issues:**
1. **21 conditional branches** for different query types
2. **Mixed concerns** (route logic + database queries + pagination)
3. **Large function** (~156 lines)
4. **Complex parameter handling**

**Refactoring Strategy:**
```python
# Current approach:
@app.route('/browse/mongodb/<collection_name>')
def browse_mongodb_collection(collection_name):
    # 150+ lines of route logic
    # Database connection
    # Query building
    # Pagination logic
    # Response formatting

# Proposed approach:
@app.route('/browse/mongodb/<collection_name>')
def browse_mongodb_collection(collection_name):
    service = BrowsingService(mongodb_manager)
    request_params = BrowsingRequestParams.from_request(request)
    
    try:
        result = service.browse_collection(collection_name, request_params)
        return jsonify(result)
    except Exception as e:
        return error_handler.handle_error(e)

class BrowsingService:
    def browse_collection(self, collection_name: str, params: BrowsingRequestParams):
        query_builder = QueryBuilder(params)
        paginator = Paginator(params.page, params.per_page)
        
        documents = self.db.query_with_pagination(
            collection_name, 
            query_builder.build(), 
            paginator.get_skip(), 
            paginator.get_limit()
        )
        
        return BrowsingResponse(documents, paginator.metadata())
```

### 4. mongodb_manager.py - Database Operation Complexity

**Overall Stats:**
- **Lines:** 759
- **Methods:** 25+
- **Critical Issues:** Complex connection management, query building

#### **Connection Management Issue (Complexity: 11)**

**Location:** Lines 88-146 (~58 lines)
**Problem:** Complex connection establishment with multiple retry strategies

**Refactoring Strategy:**
```python
# Current approach:
def _connect(self) -> bool:
    # 50+ lines of connection logic
    # Multiple exception handling paths
    # Retry logic mixed with connection logic

# Proposed approach:
class DatabaseConnectionManager:
    def __init__(self, config: Dict[str, Any]):
        self.config = config
        self.retry_strategy = RetryStrategy(max_attempts=3, backoff=1.5)
    
    def connect(self) -> MongoClient:
        return self.retry_strategy.execute(self._establish_connection)
    
    def _establish_connection(self) -> MongoClient:
        # Clean connection logic
        return MongoClient(self.config["connection_string"])

class RetryStrategy:
    def execute(self, func: Callable) -> Any:
        # Reusable retry logic
        pass
```

## Summary of Refactoring Priorities

### **Immediate Actions (Week 1-2)**

| Module | Function | Current Complexity | Target Complexity | Effort |
|--------|----------|-------------------|-------------------|---------|
| `ai_game_detector.py` | `MockAIClient._analyze_content` | 45 → | 8-10 (rule-based) | 4 days |
| `ui/app.py` | `browse_mongodb_collection` | 21 → | 6-8 (service layer) | 2 days |
| `pdf_processor.py` | `_simple_categorize_content` | 21 → | 8-10 (rule-based) | 2 days |

### **Medium-term Actions (Week 3-6)**

| Module | Improvement | Expected Impact | Effort |
|--------|-------------|-----------------|---------|
| `pdf_processor.py` | Streaming processing | 60% memory reduction | 5 days |
| `ui/app.py` | Service layer extraction | 40% complexity reduction | 7 days |
| `mongodb_manager.py` | Repository pattern | Better testability | 4 days |

### **Success Metrics**

- **Average complexity reduction:** 15+ → 8-10
- **Memory usage reduction:** 60% for large files
- **Code duplication reduction:** 30%
- **Test coverage increase:** 14% → 25%

All refactoring maintains **100% test success rate** through incremental changes and comprehensive test updates.