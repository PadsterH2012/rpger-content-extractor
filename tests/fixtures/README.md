# Test Fixtures

This directory contains test fixtures used by the test suite.

## PDF Test Files (`pdfs/`)

The `pdfs/` directory contains sample PDF files used for testing various scenarios:

### Files:
- **`test.pdf`** - Basic D&D 5th Edition content for standard testing
- **`novel.pdf`** - Fantasy novel content (The Hobbit excerpt) for novel processing tests
- **`empty.pdf`** - Empty PDF file for edge case testing
- **`large.pdf`** - Large PDF file (Pathfinder content) for performance testing
- **`scanned.pdf`** - PDF with OCR artifacts for text quality enhancement testing
- **`special_chars.pdf`** - PDF with special characters and Unicode for encoding tests
- **`test_book.pdf`** - RPG source material with metadata for extraction testing

### Creating Test PDFs

To regenerate the test PDF files:

```bash
cd tests/fixtures
python create_test_pdfs.py
```

This will create all the test PDF files in the `pdfs/` subdirectory.

### Usage in Tests

Use the `test_pdf_fixtures` fixture to access these files in your tests:

```python
def test_something(test_pdf_fixtures):
    test_pdf_path = test_pdf_fixtures["test_pdf"]
    # Use the path in your test
```

### File Descriptions

#### `test.pdf`
Contains basic D&D 5th Edition content including:
- Player's Handbook reference
- Ability scores (Strength, Dexterity, etc.)
- Armor Class description
- Standard RPG terminology

#### `novel.pdf`
Contains fantasy novel content:
- The Hobbit opening passage
- Narrative text structure
- No game mechanics

#### `large.pdf`
Contains Pathfinder content repeated 1000 times to simulate a large document for:
- Performance testing
- Memory usage testing
- Large file handling

#### `scanned.pdf`
Contains text with OCR artifacts:
- Character substitutions (0 for o, 1 for l)
- Common OCR errors
- Text quality enhancement testing

#### `special_chars.pdf`
Contains various special characters:
- Unicode characters (café, naïve)
- Mathematical symbols (α, β, ∑)
- Currency symbols (€, £, ¥)
- Smart quotes and dashes

## Notes

- These files are simple text-based PDFs created without reportlab if not available
- They contain enough content to trigger proper game detection and processing
- Files are designed to be small and fast to process during testing
- Each file tests specific scenarios and edge cases
