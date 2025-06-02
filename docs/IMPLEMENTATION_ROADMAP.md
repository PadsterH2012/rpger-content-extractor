# Refactoring Implementation Roadmap

## Phase 1: Foundation - Week 1-2 Implementation Guide

### 1.1 Extract Common Utilities (2 days)

#### AI Error Handler Utility

**File:** `utils/ai_error_handler.py`
```python
"""Common AI provider error handling utilities"""
import logging
from typing import Dict, Any, Optional, Callable
from functools import wraps

class AIErrorHandler:
    """Centralized error handling for AI providers"""
    
    def __init__(self, logger: Optional[logging.Logger] = None):
        self.logger = logger or logging.getLogger(__name__)
    
    def with_fallback(self, fallback_func: Callable) -> Callable:
        """Decorator for AI calls with fallback handling"""
        def decorator(func):
            @wraps(func)
            def wrapper(*args, **kwargs):
                try:
                    return func(*args, **kwargs)
                except (ConnectionError, TimeoutError, Exception) as e:
                    self.logger.warning(f"AI call failed: {e}, using fallback")
                    return fallback_func()
            return wrapper
        return decorator
    
    def standard_fallback_response(self) -> Dict[str, Any]:
        """Standard fallback response for AI failures"""
        return {
            "game_type": "Unknown",
            "confidence": 0.0,
            "reasoning": "AI analysis failed, using fallback",
            "detection_method": "fallback"
        }
```

**Usage in ai_game_detector.py:**
```python
# Before refactoring (repeated in multiple methods):
try:
    response = self.ai_client.analyze(prompt)
    return self._parse_response(response)
except Exception as e:
    self.logger.error(f"AI analysis failed: {e}")
    return self._fallback_response()

# After refactoring:
from utils.ai_error_handler import AIErrorHandler

@AIErrorHandler().with_fallback(self._fallback_response)
def _perform_ai_analysis(self, content: Dict[str, Any]) -> Dict[str, Any]:
    response = self.ai_client.analyze(self._build_analysis_prompt(content))
    return self._parse_response(response)
```

#### PDF Content Extractor Utility

**File:** `utils/pdf_extractor.py`
```python
"""Common PDF content extraction utilities"""
import fitz
from pathlib import Path
from typing import Dict, Any, Optional

class PDFContentExtractor:
    """Centralized PDF content extraction logic"""
    
    @staticmethod
    def extract_sample_content(pdf_path: Path, max_pages: int = 3, 
                             max_chars: int = 3000) -> str:
        """Extract sample content from PDF for analysis"""
        try:
            doc = fitz.open(pdf_path)
            content_parts = []
            chars_collected = 0
            
            for page_num in range(min(len(doc), max_pages)):
                if chars_collected >= max_chars:
                    break
                    
                page = doc[page_num]
                text = page.get_text()
                remaining_chars = max_chars - chars_collected
                
                if len(text) > remaining_chars:
                    text = text[:remaining_chars] + "..."
                    
                content_parts.append(f"Page {page_num + 1}:\n{text}")
                chars_collected += len(text)
            
            doc.close()
            return "\n\n".join(content_parts)
            
        except Exception as e:
            raise PDFExtractionError(f"Failed to extract PDF content: {e}")
    
    @staticmethod
    def extract_metadata(pdf_path: Path) -> Dict[str, Any]:
        """Extract PDF metadata for analysis"""
        try:
            doc = fitz.open(pdf_path)
            metadata = doc.metadata
            doc.close()
            
            return {
                "title": metadata.get("title", ""),
                "author": metadata.get("author", ""),
                "subject": metadata.get("subject", ""),
                "creator": metadata.get("creator", ""),
                "page_count": len(doc) if doc else 0
            }
        except Exception as e:
            return {"error": str(e)}

class PDFExtractionError(Exception):
    """Custom exception for PDF extraction failures"""
    pass
```

#### Configuration Manager

**File:** `utils/config_manager.py`
```python
"""Centralized configuration management"""
import os
from typing import Dict, Any, Optional
from pathlib import Path
import json

class ConfigurationManager:
    """Centralized configuration loading and validation"""
    
    def __init__(self, config_dir: Optional[Path] = None):
        self.config_dir = config_dir or Path(__file__).parent.parent / "config"
        self._cached_config = {}
    
    def load_ai_config(self, provider: str = None) -> Dict[str, Any]:
        """Load AI provider configuration"""
        provider = provider or os.getenv("DEFAULT_AI_PROVIDER", "mock")
        
        base_config = {
            "provider": provider,
            "debug": os.getenv("AI_DEBUG", "false").lower() == "true",
            "max_tokens": int(os.getenv("AI_MAX_TOKENS", "4000")),
            "timeout": int(os.getenv("AI_TIMEOUT", "30"))
        }
        
        # Provider-specific configuration
        if provider == "openai":
            base_config.update({
                "api_key": os.getenv("OPENAI_API_KEY"),
                "model": os.getenv("OPENAI_MODEL", "gpt-4")
            })
        elif provider == "anthropic":
            base_config.update({
                "api_key": os.getenv("ANTHROPIC_API_KEY"),
                "model": os.getenv("ANTHROPIC_MODEL", "claude-3-5-sonnet-20241022")
            })
        elif provider == "openrouter":
            base_config.update({
                "api_key": os.getenv("OPENROUTER_API_KEY"),
                "model": os.getenv("OPENROUTER_MODEL", "anthropic/claude-3.5-sonnet")
            })
        
        return self._validate_ai_config(base_config)
    
    def load_mongodb_config(self) -> Dict[str, Any]:
        """Load MongoDB configuration"""
        return {
            "connection_string": os.getenv("MONGODB_CONNECTION_STRING", "mongodb://localhost:27017"),
            "database_name": os.getenv("MONGODB_DATABASE", "rpg_content"),
            "timeout": int(os.getenv("MONGODB_TIMEOUT", "10")),
            "max_pool_size": int(os.getenv("MONGODB_POOL_SIZE", "10"))
        }
    
    def _validate_ai_config(self, config: Dict[str, Any]) -> Dict[str, Any]:
        """Validate AI configuration"""
        provider = config.get("provider")
        
        if provider in ["openai", "anthropic", "openrouter"]:
            if not config.get("api_key"):
                # Fallback to mock for missing keys
                config["provider"] = "mock"
        
        return config

# Global configuration instance
config_manager = ConfigurationManager()
```

### 1.2 Standardize Error Handling (3 days)

#### Custom Exception Hierarchy

**File:** `utils/exceptions.py`
```python
"""Custom exception hierarchy for the application"""

class RPGExtractorError(Exception):
    """Base exception for RPG content extractor"""
    pass

class AIProviderError(RPGExtractorError):
    """AI provider related errors"""
    pass

class PDFProcessingError(RPGExtractorError):
    """PDF processing related errors"""
    pass

class DatabaseError(RPGExtractorError):
    """Database operation related errors"""
    pass

class ConfigurationError(RPGExtractorError):
    """Configuration related errors"""
    pass

class ValidationError(RPGExtractorError):
    """Data validation related errors"""
    pass

# Specific AI provider errors
class AITimeoutError(AIProviderError):
    """AI API timeout error"""
    pass

class AIRateLimitError(AIProviderError):
    """AI API rate limit exceeded"""
    pass

class AIAuthenticationError(AIProviderError):
    """AI API authentication failed"""
    pass

# Specific database errors
class DatabaseConnectionError(DatabaseError):
    """Database connection failed"""
    pass

class DatabaseQueryError(DatabaseError):
    """Database query failed"""
    pass
```

#### Error Handler

**File:** `utils/error_handler.py`
```python
"""Centralized error handling and logging"""
import logging
from typing import Dict, Any, Optional
from utils.exceptions import *

class ErrorHandler:
    """Centralized error handling and response formatting"""
    
    def __init__(self, logger: Optional[logging.Logger] = None):
        self.logger = logger or logging.getLogger(__name__)
    
    def handle_ai_error(self, error: Exception, context: str = "") -> Dict[str, Any]:
        """Handle AI provider errors with appropriate response"""
        if isinstance(error, AITimeoutError):
            self.logger.warning(f"AI timeout in {context}: {error}")
            return {
                "success": False,
                "error": "AI_TIMEOUT",
                "message": "AI provider request timed out",
                "retryable": True
            }
        elif isinstance(error, AIRateLimitError):
            self.logger.warning(f"AI rate limit in {context}: {error}")
            return {
                "success": False,
                "error": "AI_RATE_LIMIT",
                "message": "AI provider rate limit exceeded",
                "retryable": True
            }
        else:
            self.logger.error(f"AI error in {context}: {error}")
            return {
                "success": False,
                "error": "AI_ERROR",
                "message": "AI provider error occurred",
                "retryable": False
            }
    
    def handle_database_error(self, error: Exception, context: str = "") -> Dict[str, Any]:
        """Handle database errors with appropriate response"""
        if isinstance(error, DatabaseConnectionError):
            self.logger.error(f"Database connection error in {context}: {error}")
            return {
                "success": False,
                "error": "DB_CONNECTION",
                "message": "Database connection failed",
                "retryable": True
            }
        else:
            self.logger.error(f"Database error in {context}: {error}")
            return {
                "success": False,
                "error": "DB_ERROR",
                "message": "Database operation failed",
                "retryable": False
            }
    
    def handle_pdf_error(self, error: Exception, context: str = "") -> Dict[str, Any]:
        """Handle PDF processing errors"""
        self.logger.error(f"PDF processing error in {context}: {error}")
        return {
            "success": False,
            "error": "PDF_PROCESSING",
            "message": "PDF processing failed",
            "retryable": False
        }

# Global error handler instance
error_handler = ErrorHandler()
```

### 1.3 Configuration Consolidation (2 days)

#### Base Configuration

**File:** `config/base_config.py`
```python
"""Base configuration for all environments"""
import os
from pathlib import Path

class BaseConfig:
    """Base configuration class"""
    
    # Application settings
    APP_NAME = "RPG Content Extractor"
    VERSION = "3.0.0"
    DEBUG = False
    
    # File handling
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16MB
    UPLOAD_FOLDER = Path("uploads")
    ALLOWED_EXTENSIONS = {"pdf"}
    
    # AI settings
    AI_DEFAULT_PROVIDER = "mock"
    AI_MAX_TOKENS = 4000
    AI_TIMEOUT = 30
    AI_ANALYSIS_PAGES = 25
    
    # Database settings
    MONGODB_DATABASE = "rpg_content"
    MONGODB_TIMEOUT = 10
    MONGODB_POOL_SIZE = 10
    
    # Text processing
    TEXT_QUALITY_AGGRESSIVE = False
    TEXT_MAX_CHUNK_SIZE = 1000
    
    # Logging
    LOG_LEVEL = "INFO"
    LOG_FORMAT = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    
    @classmethod
    def from_env(cls):
        """Create configuration from environment variables"""
        config = cls()
        
        # Override with environment variables
        config.DEBUG = os.getenv("DEBUG", "false").lower() == "true"
        config.AI_DEFAULT_PROVIDER = os.getenv("DEFAULT_AI_PROVIDER", config.AI_DEFAULT_PROVIDER)
        config.AI_MAX_TOKENS = int(os.getenv("AI_MAX_TOKENS", config.AI_MAX_TOKENS))
        config.MONGODB_DATABASE = os.getenv("MONGODB_DATABASE", config.MONGODB_DATABASE)
        
        return config
```

**File:** `config/production_config.py`
```python
"""Production-specific configuration"""
from .base_config import BaseConfig

class ProductionConfig(BaseConfig):
    """Production configuration"""
    
    DEBUG = False
    LOG_LEVEL = "WARNING"
    
    # Production AI settings
    AI_DEFAULT_PROVIDER = "claude"  # Use Claude in production
    AI_TIMEOUT = 60  # Longer timeout for production
    
    # Production database settings
    MONGODB_POOL_SIZE = 50  # Larger pool for production
    MONGODB_TIMEOUT = 30
```

**File:** `config/test_config.py`
```python
"""Test-specific configuration"""
from .base_config import BaseConfig

class TestConfig(BaseConfig):
    """Test configuration"""
    
    DEBUG = True
    
    # Test AI settings
    AI_DEFAULT_PROVIDER = "mock"  # Always use mock in tests
    AI_TIMEOUT = 5  # Short timeout for tests
    
    # Test database settings
    MONGODB_DATABASE = "rpg_content_test"
    MONGODB_POOL_SIZE = 5
    
    # Test file settings
    MAX_CONTENT_LENGTH = 1024 * 1024  # 1MB for tests
```

### Implementation Strategy for Phase 1

#### Modified Files List
```
Files to Create:
+ utils/__init__.py
+ utils/ai_error_handler.py
+ utils/pdf_extractor.py
+ utils/config_manager.py
+ utils/exceptions.py
+ utils/error_handler.py
+ config/__init__.py
+ config/base_config.py
+ config/production_config.py
+ config/test_config.py

Files to Modify:
~ Modules/ai_game_detector.py (remove ~40 lines, add imports)
~ Modules/ai_categorizer.py (remove ~30 lines, add imports)
~ Modules/novel_element_extractor.py (remove ~35 lines, add imports)
~ Modules/pdf_processor.py (remove ~25 lines, add imports)
~ Modules/mongodb_manager.py (add error handling, ~10 lines)
~ ui/app.py (add configuration, error handling)
```

#### Testing Strategy
1. **Create tests for new utilities**
2. **Modify existing tests to use new patterns**
3. **Ensure 100% test pass rate maintained**

#### Rollback Plan
- Each utility can be independently reverted
- Original functionality preserved through imports
- No breaking changes to public interfaces

## Phase 2: Core Refactoring Preview

### AI Provider Strategy Pattern (5 days)

```python
# providers/base_provider.py
from abc import ABC, abstractmethod
from typing import Dict, Any

class AIProvider(ABC):
    """Abstract base class for AI providers"""
    
    @abstractmethod
    def analyze(self, prompt: str) -> Dict[str, Any]:
        """Analyze content and return structured response"""
        pass
    
    @abstractmethod
    def categorize(self, prompt: str) -> Dict[str, Any]:
        """Categorize content and return categories"""
        pass

# providers/provider_factory.py
class AIProviderFactory:
    """Factory for creating AI providers"""
    
    @staticmethod
    def create_provider(config: Dict[str, Any]) -> AIProvider:
        provider_type = config.get("provider", "mock")
        
        if provider_type == "openai":
            return OpenAIProvider(config)
        elif provider_type == "anthropic":
            return AnthropicProvider(config)
        elif provider_type == "openrouter":
            return OpenRouterProvider(config)
        else:
            return MockProvider(config)
```

This roadmap provides concrete implementation details for the first phase of refactoring, focusing on low-risk, high-impact changes that establish a foundation for future improvements while maintaining the 100% test success rate.