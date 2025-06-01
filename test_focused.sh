#!/bin/bash

# Focused Testing Strategy for Phase 2 Validation
# Skips known working modules to focus on remaining failures

echo "🎯 FOCUSED TESTING STRATEGY - PHASE 2 VALIDATION"
echo "=================================================="
echo ""

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

echo -e "${YELLOW}⚠️  CRITICAL REMINDER: This skips 35 validated tests temporarily${NC}"
echo -e "${YELLOW}   Must re-enable ALL tests when Phase 2 is complete!${NC}"
echo ""

echo -e "${BLUE}📊 Skipping Known Working Groups:${NC}"
echo "   ✅ Text Quality Enhancer: 14/14 tests fixed"
echo "   ✅ MongoDB Manager: 14/14 tests fixed"  
echo "   ✅ AI Game Detector: 7/7 tests fixed"
echo "   📈 Total Skipped: 35 tests"
echo ""

echo -e "${BLUE}🔍 Focusing on Remaining Problem Areas:${NC}"
echo "   🎯 PDF Processor edge cases"
echo "   🎯 Web UI functionality"
echo "   🎯 Integration issues"
echo ""

# Check if we're in the right directory
if [ ! -f "tests/test_pdf_processor.py" ]; then
    echo -e "${RED}❌ Error: Not in rpger-content-extractor directory${NC}"
    echo "Please run from project root"
    exit 1
fi

echo -e "${GREEN}🚀 Running Focused Test Suite...${NC}"
echo ""

# Run focused tests
python -m pytest \
    --ignore=tests/test_text_quality_enhancer.py \
    --ignore=tests/test_mongodb_manager.py \
    --ignore=tests/test_ai_game_detector.py \
    tests/test_pdf_processor.py \
    tests/test_web_ui.py \
    -v \
    --tb=short \
    --no-cov \
    2>&1 | tee focused_test_results.log

# Capture exit code
TEST_EXIT_CODE=${PIPESTATUS[0]}

echo ""
echo "=================================================="

if [ $TEST_EXIT_CODE -eq 0 ]; then
    echo -e "${GREEN}✅ FOCUSED TESTS PASSED!${NC}"
    echo -e "${GREEN}   All remaining issues resolved${NC}"
    echo -e "${YELLOW}   Ready to re-enable full test suite${NC}"
else
    echo -e "${RED}❌ FOCUSED TESTS FAILED${NC}"
    echo -e "${BLUE}   Check focused_test_results.log for details${NC}"
    echo -e "${BLUE}   Continue with Phase 2C fixes${NC}"
fi

echo ""
echo -e "${YELLOW}📋 Next Steps:${NC}"
echo "   1. Fix any remaining failures shown above"
echo "   2. Re-run focused tests until all pass"
echo "   3. Re-enable full test suite for final validation"
echo "   4. Commit and push for Build #20+"
echo ""

echo -e "${RED}⚠️  REMEMBER: Re-enable all tests when done!${NC}"
echo "   Remove --ignore flags for final validation"

exit $TEST_EXIT_CODE
