# Test Suite Action Plan

## Current Status
- ✅ 251 tests passing (100% success rate)
- ✅ 45.21% coverage (exceeds 40% requirement)
- ⚠️ 6 modules with <30% coverage
- ⚠️ 4 fix-specific tests that should be removed
- ❌ 1 non-test file in test suite

---

## PHASE 1: CLEANUP (Immediate - 1 hour)

### Task 1.1: Remove test_manual_validation.py
**Status**: Ready to execute
**Reason**: Not a real pytest test, appears to be a manual validation script
**Action**: Delete file
```bash
rm tests/test_manual_validation.py
```

### Task 1.2: Document fix-specific tests for removal
**Status**: Ready to execute
**Reason**: These tests validate specific bug fixes, not core functionality
**Action**: Mark for removal after production verification
- test_token_tracking_fix.py
- test_recalculate_session_cost_fix.py
- test_ui_refresh_fix.py

---

## PHASE 2: CRITICAL COVERAGE GAPS (1-2 weeks)

### Task 2.1: Create test_ai_categorizer.py
**Current Coverage**: 17% (282 statements)
**Priority**: HIGH
**Modules to Test**: ai_categorizer.py
**Estimated Tests**: 15-20

### Task 2.2: Create test_game_detector.py
**Current Coverage**: 9% (141 statements)
**Priority**: CRITICAL
**Modules to Test**: game_detector.py
**Estimated Tests**: 10-15

### Task 2.3: Create test_multi_collection_manager.py
**Current Coverage**: 19% (449 statements)
**Priority**: HIGH
**Modules to Test**: multi_collection_manager.py
**Estimated Tests**: 20-25

### Task 2.4: Create test_novel_element_extractor.py
**Current Coverage**: 30% (627 statements)
**Priority**: HIGH
**Modules to Test**: novel_element_extractor.py
**Estimated Tests**: 25-30

### Task 2.5: Enhance test_openrouter_models.py
**Current Coverage**: 24% (118 statements)
**Priority**: MEDIUM
**Action**: Create or enhance existing tests
**Estimated Tests**: 10-15

### Task 2.6: Enhance test_categorizer.py
**Current Coverage**: 15% (93 statements)
**Priority**: MEDIUM
**Action**: Create or enhance existing tests
**Estimated Tests**: 8-12

---

## PHASE 3: MISSING FUNCTIONALITY TESTS (1-2 weeks)

### Task 3.1: Add Settings Management Tests
**What to Test**:
- `/get_settings` endpoint
- `/save_settings` endpoint
- MongoDB authentication configuration
- Settings persistence

**File**: Add to test_web_ui.py
**Estimated Tests**: 8-10

### Task 3.2: Add MongoDB Authentication Tests
**What to Test**:
- Username/password authentication
- Auth source configuration
- Connection with credentials
- Authentication failures

**File**: Add to test_mongodb_manager.py
**Estimated Tests**: 6-8

### Task 3.3: Add AI Provider Fallback Tests
**What to Test**:
- MockAIClient fallback behavior
- Low confidence scenarios (10% fallback)
- Provider switching
- Error recovery

**File**: Add to test_ai_game_detector.py
**Estimated Tests**: 5-8

### Task 3.4: Add Session Management Tests
**What to Test**:
- Session cleanup
- Concurrent session handling
- Session state persistence
- Session timeout

**File**: Add to test_web_ui.py or create test_session_management.py
**Estimated Tests**: 8-10

---

## PHASE 4: OPTIMIZATION (Ongoing)

### Task 4.1: Monitor Coverage
- Run full test suite weekly
- Track coverage trends
- Identify new gaps

### Task 4.2: Refactor Fix-Specific Tests
- After production verification, remove:
  - test_token_tracking_fix.py
  - test_recalculate_session_cost_fix.py
  - test_ui_refresh_fix.py

### Task 4.3: Maintain Test Quality
- Keep coverage >40% (current: 45.21%)
- Maintain 100% test success rate
- Add tests for new features

---

## Success Criteria

| Metric | Current | Target | Status |
|--------|---------|--------|--------|
| Total Tests | 251 | 280+ | 🟡 In Progress |
| Pass Rate | 100% | 100% | ✅ Met |
| Coverage | 45.21% | 50%+ | 🟡 In Progress |
| Untested Modules | 6 | 0 | 🔴 Critical |
| Fix-Specific Tests | 4 | 0 | 🟡 Pending |

---

## Timeline Estimate

- **Phase 1 (Cleanup)**: 1 hour
- **Phase 2 (Coverage Gaps)**: 1-2 weeks
- **Phase 3 (Missing Tests)**: 1-2 weeks
- **Phase 4 (Optimization)**: Ongoing

**Total**: 2-4 weeks to reach optimal test coverage

---

## Notes

- All current tests are passing ✅
- No breaking changes required
- Can be done incrementally
- Each phase can be executed independently
- Prioritize Phase 2 for maximum coverage improvement

