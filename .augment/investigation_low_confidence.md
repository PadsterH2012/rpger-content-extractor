# Investigation: Low AI Confidence (10%) Issue

## Problem
When analyzing PDFs with AI, the confidence score is only 10% instead of the expected 80%+ for valid game books.

## Root Cause Analysis

### Issue Location
**File**: `Modules/ai_game_detector.py`

The confidence of 10% (0.1) is returned from the **fallback analysis** at **line 549**:

```python
def _fallback_analysis(self, content: Dict[str, Any]) -> Dict[str, Any]:
    # ... novel detection logic ...
    else:
        return {
            "game_type": "Unknown",
            # ...
            "confidence": 0.1,  # ← THIS IS THE 10% CONFIDENCE
            "reasoning": "AI analysis failed, using fallback",
            # ...
        }
```

### Why Fallback is Being Triggered

The fallback analysis is triggered when:

1. **AI Analysis Fails** (line 260-265 in `_perform_ai_analysis`):
   - Exception occurs during AI client call
   - JSON parsing fails
   - AI response is not a dictionary

2. **MockAIClient Raises Exception** (line 874):
   ```python
   def analyze(self, prompt: str) -> Dict[str, Any]:
       provider = self.ai_config.get("provider", "mock")
       if provider in ["openrouter", "anthropic", "openai"] and not self.ai_config.get("api_key"):
           raise Exception(f"Missing API key for {provider} provider")
   ```

### The Problem Chain

1. User configures AI provider (e.g., "openrouter", "anthropic", "openai")
2. No API key is provided in `ai_config`
3. MockAIClient detects this and raises an exception
4. Exception is caught in `_perform_ai_analysis`
5. `_fallback_analysis` is called
6. Returns confidence of 0.1 (10%)

### Expected Behavior

When using MockAIClient with a real provider name but no API key:
- Should either use mock analysis (confidence 0.8)
- OR provide a clear error message
- NOT silently fall back to 0.1 confidence

## Solution Options

### Option 1: Use Mock Analysis When No API Key
Modify MockAIClient to return mock analysis instead of raising exception:
```python
def analyze(self, prompt: str) -> Dict[str, Any]:
    # Don't raise exception, just use mock analysis
    return self._analyze_content(prompt)
```

### Option 2: Initialize Correct Provider
Ensure the correct AI provider is initialized based on available credentials:
- Check for API keys before initializing
- Fall back to "mock" provider if no keys available

### Option 3: Improve Error Handling
Provide better logging/warnings when falling back to 0.1 confidence

## Recommendation

**Option 1** is best because:
- MockAIClient should be a true fallback
- Returns reasonable confidence (0.8) for mock analysis
- Allows testing without API keys
- Maintains backward compatibility

## Files to Modify

1. `Modules/ai_game_detector.py` - MockAIClient.analyze() method (line 869-876)

