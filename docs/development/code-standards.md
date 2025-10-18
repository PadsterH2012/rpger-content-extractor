---
title: Code Standards
description: Coding standards and best practices for RPGer Content Extractor
tags: [development, standards, best-practices, code-quality]
last_updated: 2025-10-18
author: HL-Auggie Analysis System
---

# Code Standards

## Overview

This document outlines the coding standards, best practices, and conventions used in the RPGer Content Extractor project. Following these standards ensures code consistency, maintainability, and quality across the entire codebase.

## Python Code Standards

### Code Formatting

#### Black Formatter

All Python code must be formatted using Black with default settings:

```bash
# Format all Python files
black .

# Check formatting without making changes
black --check .

# Format specific directories
black Modules/ ui/ tests/
```

**Black Configuration** (pyproject.toml):
```toml
[tool.black]
line-length = 88
target-version = ['py311']
include = '\.pyi?$'
extend-exclude = '''
/(
  # directories
  \.eggs
  | \.git
  | \.hg
  | \.mypy_cache
  | \.tox
  | \.venv
  | build
  | dist
)/
'''
```

#### Line Length and Wrapping

- **Maximum line length**: 88 characters (Black default)
- **Docstring line length**: 72 characters
- **Long imports**: Use parentheses for multi-line imports

```python
# Good: Multi-line imports
from Modules.pdf_processor import (
    MultiGamePDFProcessor,
    PDFProcessingError,
    PDFValidationError
)

# Good: Long function calls
result = some_function(
    parameter_one="value",
    parameter_two="another_value",
    parameter_three="third_value"
)
```

### Naming Conventions

#### Variables and Functions

```python
# Variables: snake_case
user_name = "john_doe"
total_count = 42
is_valid = True

# Functions: snake_case
def process_pdf_file(file_path):
    pass

def calculate_confidence_score(data):
    pass

# Private functions: leading underscore
def _internal_helper_function():
    pass
```

#### Classes

```python
# Classes: PascalCase
class PDFProcessor:
    pass

class AIGameDetector:
    pass

class MongoDBManager:
    pass

# Private classes: leading underscore
class _InternalHelper:
    pass
```

#### Constants

```python
# Constants: UPPER_SNAKE_CASE
MAX_FILE_SIZE = 200 * 1024 * 1024  # 200MB
DEFAULT_AI_PROVIDER = "anthropic"
SUPPORTED_GAME_TYPES = ["D&D", "Pathfinder", "Call of Cthulhu"]

# Module-level constants
API_VERSION = "v1"
DEFAULT_TIMEOUT = 30
```

#### Files and Modules

```python
# Files: snake_case
pdf_processor.py
ai_game_detector.py
mongodb_manager.py

# Modules: snake_case
from Modules import pdf_processor
from Modules.ai_game_detector import AIGameDetector
```

### Documentation Standards

#### Docstrings

Use Google-style docstrings for all public functions, classes, and modules:

```python
def extract_pdf_content(file_path: str, game_type: str = None) -> dict:
    """Extract content from a PDF file with optional game type override.
    
    This function processes a PDF file and extracts structured content
    using AI-powered analysis and categorization.
    
    Args:
        file_path (str): Path to the PDF file to process
        game_type (str, optional): Override automatic game detection.
            Defaults to None for automatic detection.
    
    Returns:
        dict: Extraction results containing:
            - sections (list): Extracted content sections
            - metadata (dict): Game and processing metadata
            - summary (dict): Processing statistics
    
    Raises:
        FileNotFoundError: If the PDF file doesn't exist
        PDFProcessingError: If PDF processing fails
        AIProviderError: If AI analysis fails
    
    Example:
        >>> result = extract_pdf_content("dnd_phb.pdf")
        >>> print(result["metadata"]["game_type"])
        "D&D"
    """
    pass
```

#### Class Documentation

```python
class AIGameDetector:
    """AI-powered game system and edition detection.
    
    This class uses various AI providers to analyze PDF content and
    determine the game system, edition, and content type. It supports
    multiple detection strategies and confidence scoring.
    
    Attributes:
        provider (str): Current AI provider name
        model (str): AI model being used
        confidence_threshold (float): Minimum confidence for detection
    
    Example:
        >>> detector = AIGameDetector(provider="anthropic")
        >>> result = detector.detect_game("sample_content")
        >>> print(result["game_type"])
        "D&D"
    """
    
    def __init__(self, provider: str = "anthropic"):
        """Initialize the game detector.
        
        Args:
            provider (str): AI provider to use. Defaults to "anthropic".
        """
        pass
```

#### Module Documentation

```python
"""PDF processing module for RPG content extraction.

This module provides the core PDF processing functionality including:
- Text extraction with layout preservation
- Table detection and extraction
- Multi-column layout handling
- Quality enhancement and cleanup

Classes:
    MultiGamePDFProcessor: Main PDF processing class
    PDFProcessingError: Custom exception for processing errors
    
Functions:
    validate_pdf_file: Validate PDF file before processing
    extract_text_from_page: Extract text from a single PDF page

Example:
    >>> from Modules.pdf_processor import MultiGamePDFProcessor
    >>> processor = MultiGamePDFProcessor()
    >>> result = processor.extract_pdf("sample.pdf")
"""
```

### Type Hints

#### Function Type Hints

```python
from typing import Dict, List, Optional, Union, Tuple, Any
from pathlib import Path

def process_sections(
    sections: List[Dict[str, Any]], 
    game_type: str,
    confidence_threshold: float = 0.8
) -> Tuple[List[Dict[str, Any]], Dict[str, int]]:
    """Process extracted sections with type hints."""
    pass

def get_collection_info(
    collection_name: str
) -> Optional[Dict[str, Union[str, int]]]:
    """Get collection information with optional return."""
    pass
```

#### Class Type Hints

```python
from typing import Protocol, TypeVar, Generic

class AIProvider(Protocol):
    """Protocol for AI provider implementations."""
    
    def analyze_content(self, content: str) -> Dict[str, Any]:
        """Analyze content and return results."""
        ...

T = TypeVar('T')

class GenericProcessor(Generic[T]):
    """Generic processor class."""
    
    def process(self, data: T) -> T:
        """Process data of generic type."""
        pass
```

### Error Handling

#### Custom Exceptions

```python
class RPGExtractorError(Exception):
    """Base exception for RPG Extractor errors."""
    pass

class PDFProcessingError(RPGExtractorError):
    """Raised when PDF processing fails."""
    
    def __init__(self, message: str, file_path: str = None):
        super().__init__(message)
        self.file_path = file_path

class AIProviderError(RPGExtractorError):
    """Raised when AI provider operations fail."""
    
    def __init__(self, message: str, provider: str = None, model: str = None):
        super().__init__(message)
        self.provider = provider
        self.model = model
```

#### Exception Handling Patterns

```python
def safe_pdf_processing(file_path: str) -> Optional[Dict[str, Any]]:
    """Process PDF with comprehensive error handling."""
    try:
        # Validate input
        if not Path(file_path).exists():
            raise FileNotFoundError(f"PDF file not found: {file_path}")
        
        # Process PDF
        result = process_pdf(file_path)
        return result
        
    except FileNotFoundError as e:
        logger.error(f"File error: {e}")
        return None
        
    except PDFProcessingError as e:
        logger.error(f"PDF processing failed: {e}")
        return None
        
    except Exception as e:
        logger.error(f"Unexpected error: {e}")
        raise  # Re-raise unexpected errors
```

### Logging Standards

#### Logger Configuration

```python
import logging
from pathlib import Path

# Configure module logger
logger = logging.getLogger(__name__)

# Log levels and usage
logger.debug("Detailed debugging information")
logger.info("General information about program execution")
logger.warning("Warning about potential issues")
logger.error("Error that doesn't stop execution")
logger.critical("Critical error that may stop execution")
```

#### Logging Best Practices

```python
def process_with_logging(data: Dict[str, Any]) -> bool:
    """Example of proper logging usage."""
    logger.info(f"Starting processing for {len(data)} items")
    
    try:
        # Log important steps
        logger.debug(f"Processing data: {data.keys()}")
        
        # Process data
        result = perform_processing(data)
        
        # Log success
        logger.info(f"Processing completed successfully: {result}")
        return True
        
    except Exception as e:
        # Log errors with context
        logger.error(f"Processing failed: {e}", exc_info=True)
        return False
```

## Code Organization

### Module Structure

```
Modules/
├── __init__.py              # Module initialization
├── pdf_processor.py         # PDF processing functionality
├── ai_game_detector.py      # AI game detection
├── ai_categorizer.py        # Content categorization
├── mongodb_manager.py       # MongoDB operations
├── multi_collection_manager.py  # Collection management
├── text_quality_enhancer.py    # Text enhancement
├── token_usage_tracker.py      # Token tracking
├── game_configs.py             # Game configurations
└── openrouter_models.py        # OpenRouter model management
```

### Import Organization

```python
# Standard library imports
import os
import sys
import json
import logging
from pathlib import Path
from typing import Dict, List, Optional, Any
from datetime import datetime

# Third-party imports
import requests
import pymongo
from flask import Flask, request, jsonify

# Local imports
from Modules.pdf_processor import MultiGamePDFProcessor
from Modules.ai_game_detector import AIGameDetector
from Modules.mongodb_manager import MongoDBManager
```

### Class Organization

```python
class ExampleClass:
    """Example class showing proper organization."""
    
    # Class variables
    DEFAULT_TIMEOUT = 30
    SUPPORTED_FORMATS = ["pdf"]
    
    def __init__(self, config: Dict[str, Any]):
        """Initialize with configuration."""
        # Public attributes
        self.config = config
        self.is_initialized = False
        
        # Private attributes
        self._internal_state = {}
        self._logger = logging.getLogger(__name__)
    
    # Public methods
    def public_method(self) -> bool:
        """Public method for external use."""
        pass
    
    def another_public_method(self, param: str) -> Optional[str]:
        """Another public method."""
        pass
    
    # Private methods
    def _private_helper(self) -> None:
        """Private helper method."""
        pass
    
    def _another_private_method(self, data: Any) -> Any:
        """Another private method."""
        pass
    
    # Properties
    @property
    def status(self) -> str:
        """Get current status."""
        return "active" if self.is_initialized else "inactive"
    
    # Special methods
    def __str__(self) -> str:
        """String representation."""
        return f"ExampleClass(initialized={self.is_initialized})"
    
    def __repr__(self) -> str:
        """Developer representation."""
        return f"ExampleClass(config={self.config})"
```

## Testing Standards

### Test Organization

```python
import pytest
from unittest.mock import Mock, patch, MagicMock
from pathlib import Path

class TestPDFProcessor:
    """Test class for PDF processor functionality."""
    
    def setup_method(self):
        """Setup for each test method."""
        self.processor = PDFProcessor()
        self.test_data = {"sample": "data"}
    
    def teardown_method(self):
        """Cleanup after each test method."""
        # Clean up resources
        pass
    
    def test_valid_pdf_processing(self):
        """Test processing of valid PDF files."""
        # Arrange
        test_file = "test.pdf"
        expected_result = {"status": "success"}
        
        # Act
        result = self.processor.process(test_file)
        
        # Assert
        assert result["status"] == "success"
        assert "sections" in result
    
    @pytest.mark.parametrize("file_type,expected", [
        ("pdf", True),
        ("txt", False),
        ("doc", False),
    ])
    def test_file_type_validation(self, file_type, expected):
        """Test file type validation with parameters."""
        result = self.processor.is_valid_file_type(file_type)
        assert result == expected
    
    def test_error_handling(self):
        """Test error handling for invalid inputs."""
        with pytest.raises(FileNotFoundError):
            self.processor.process("nonexistent.pdf")
```

### Test Naming

```python
# Test function naming: test_[what]_[condition]_[expected]
def test_pdf_processing_valid_file_returns_success():
    pass

def test_ai_detection_unknown_content_returns_low_confidence():
    pass

def test_mongodb_connection_invalid_url_raises_error():
    pass

# Test class naming: Test[ClassName]
class TestAIGameDetector:
    pass

class TestMongoDBManager:
    pass
```

## Performance Standards

### Optimization Guidelines

#### Memory Management

```python
# Use generators for large datasets
def process_large_dataset(data):
    """Process large dataset efficiently."""
    for item in data:
        yield process_item(item)

# Context managers for resource cleanup
class DatabaseConnection:
    def __enter__(self):
        self.connection = create_connection()
        return self.connection
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        self.connection.close()

# Use with statement
with DatabaseConnection() as conn:
    result = conn.query("SELECT * FROM table")
```

#### Caching

```python
from functools import lru_cache
from typing import Dict, Any

class ConfigManager:
    """Configuration manager with caching."""
    
    @lru_cache(maxsize=128)
    def get_config(self, key: str) -> Any:
        """Get configuration value with caching."""
        return self._load_config(key)
    
    def _load_config(self, key: str) -> Any:
        """Load configuration from source."""
        # Expensive operation
        pass
```

## Security Standards

### Input Validation

```python
from pathlib import Path
import re

def validate_file_path(file_path: str) -> bool:
    """Validate file path for security."""
    path = Path(file_path)
    
    # Check for path traversal
    if ".." in str(path):
        return False
    
    # Check file extension
    if path.suffix.lower() not in [".pdf"]:
        return False
    
    # Check file exists and is readable
    if not path.exists() or not path.is_file():
        return False
    
    return True

def sanitize_input(user_input: str) -> str:
    """Sanitize user input."""
    # Remove potentially dangerous characters
    sanitized = re.sub(r'[<>"\']', '', user_input)
    
    # Limit length
    return sanitized[:1000]
```

### Environment Variables

```python
import os
from typing import Optional

def get_env_var(key: str, default: Optional[str] = None) -> str:
    """Safely get environment variable."""
    value = os.getenv(key, default)
    
    if value is None:
        raise ValueError(f"Required environment variable {key} not set")
    
    return value

# Usage
API_KEY = get_env_var("ANTHROPIC_API_KEY")
DEBUG_MODE = get_env_var("DEBUG", "false").lower() == "true"
```

## Code Review Guidelines

### Review Checklist

**Functionality**:
- [ ] Code works as intended
- [ ] Edge cases are handled
- [ ] Error handling is appropriate
- [ ] Performance is acceptable

**Code Quality**:
- [ ] Follows naming conventions
- [ ] Proper documentation
- [ ] Type hints where appropriate
- [ ] No code duplication

**Testing**:
- [ ] Tests cover new functionality
- [ ] Tests pass locally
- [ ] Edge cases are tested
- [ ] Mock objects used appropriately

**Security**:
- [ ] Input validation implemented
- [ ] No hardcoded secrets
- [ ] Proper error handling
- [ ] Security best practices followed

### Review Process

1. **Self Review**: Review your own code before submitting
2. **Automated Checks**: Ensure all CI checks pass
3. **Peer Review**: Get review from team member
4. **Address Feedback**: Make requested changes
5. **Final Approval**: Get approval before merging

## Continuous Integration

### Pre-commit Hooks

```bash
# Install pre-commit
pip install pre-commit

# Setup pre-commit hooks
pre-commit install

# Run manually
pre-commit run --all-files
```

### CI Pipeline

The project uses Jenkins for CI/CD with the following stages:
1. **Code Quality**: Black formatting, flake8 linting
2. **Testing**: Unit tests, integration tests, coverage
3. **Security**: Dependency scanning, security checks
4. **Build**: Docker image creation
5. **Deploy**: Automated deployment to staging

### Quality Gates

- **Test Coverage**: Minimum 40% coverage required
- **Code Quality**: All linting checks must pass
- **Security**: No high-severity vulnerabilities
- **Performance**: No significant performance regressions
