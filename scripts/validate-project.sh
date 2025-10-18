#!/bin/bash
# Project Validation Script for RPGer Content Extractor
# Validates project structure, documentation, and compliance

set -e

echo "🔍 RPGer Content Extractor - Project Validation"
echo "=============================================="

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Validation results
ERRORS=0
WARNINGS=0

# Function to print status
print_status() {
    local status=$1
    local message=$2
    case $status in
        "OK")
            echo -e "${GREEN}✅ $message${NC}"
            ;;
        "WARNING")
            echo -e "${YELLOW}⚠️  $message${NC}"
            ((WARNINGS++))
            ;;
        "ERROR")
            echo -e "${RED}❌ $message${NC}"
            ((ERRORS++))
            ;;
        "INFO")
            echo -e "${BLUE}ℹ️  $message${NC}"
            ;;
    esac
}

# Check project structure
echo -e "\n${BLUE}📁 Checking Project Structure...${NC}"

# Check for required directories
required_dirs=("docs" "docs/prp" "docs/prp/base" "docs/prp/features" "Modules" "tests" "ui")
for dir in "${required_dirs[@]}"; do
    if [ -d "$dir" ]; then
        print_status "OK" "Directory exists: $dir"
    else
        print_status "ERROR" "Missing required directory: $dir"
    fi
done

# Check for required files
required_files=("summary.md" "docs/index.md" "README.md" "requirements.txt" "Dockerfile")
for file in "${required_files[@]}"; do
    if [ -f "$file" ]; then
        print_status "OK" "File exists: $file"
    else
        print_status "ERROR" "Missing required file: $file"
    fi
done

# Check .augment directory
echo -e "\n${BLUE}⚙️  Checking Project Configuration...${NC}"
if [ -d ".augment" ]; then
    print_status "OK" ".augment directory exists"
    if [ -f ".augment/project-config.json" ]; then
        print_status "OK" "Project configuration file exists"
    else
        print_status "WARNING" "Missing project configuration file"
    fi
else
    print_status "WARNING" "Missing .augment directory for project configuration"
fi

# Validate documentation
echo -e "\n${BLUE}📚 Validating Documentation...${NC}"
if [ -f "docs/validate-documentation.py" ]; then
    print_status "INFO" "Running documentation validation..."
    if python3 docs/validate-documentation.py > /dev/null 2>&1; then
        print_status "OK" "Documentation validation passed"
    else
        print_status "ERROR" "Documentation validation failed"
    fi
else
    print_status "WARNING" "Documentation validation script not found"
fi

# Check PRP structure
echo -e "\n${BLUE}📋 Checking PRP Structure...${NC}"
prp_base_files=("base-requirements.md" "architecture-requirements.md" "quality-requirements.md")
for file in "${prp_base_files[@]}"; do
    if [ -f "docs/prp/base/$file" ]; then
        print_status "OK" "Base PRP exists: $file"
    else
        print_status "ERROR" "Missing base PRP: $file"
    fi
done

# Check for feature PRPs
feature_count=$(find docs/prp/features -name "*.md" 2>/dev/null | wc -l)
if [ "$feature_count" -gt 0 ]; then
    print_status "OK" "Found $feature_count feature PRP(s)"
else
    print_status "WARNING" "No feature PRPs found"
fi

# Check Docker configuration
echo -e "\n${BLUE}🐳 Checking Docker Configuration...${NC}"
docker_files=("Dockerfile" "docker-compose.yml")
for file in "${docker_files[@]}"; do
    if [ -f "$file" ]; then
        print_status "OK" "Docker file exists: $file"
    else
        print_status "ERROR" "Missing Docker file: $file"
    fi
done

# Check test structure
echo -e "\n${BLUE}🧪 Checking Test Structure...${NC}"
if [ -d "tests" ]; then
    test_count=$(find tests -name "test_*.py" 2>/dev/null | wc -l)
    if [ "$test_count" -gt 0 ]; then
        print_status "OK" "Found $test_count test file(s)"
    else
        print_status "WARNING" "No test files found"
    fi
    
    if [ -f "pytest.ini" ]; then
        print_status "OK" "pytest configuration exists"
    else
        print_status "WARNING" "Missing pytest configuration"
    fi
else
    print_status "ERROR" "Missing tests directory"
fi

# Final results
echo -e "\n${BLUE}📊 Validation Results${NC}"
echo "===================="

if [ $ERRORS -eq 0 ] && [ $WARNINGS -eq 0 ]; then
    print_status "OK" "All validation checks passed!"
    echo -e "\n${GREEN}✅ Project is fully compliant${NC}"
    exit 0
elif [ $ERRORS -eq 0 ]; then
    print_status "WARNING" "Validation passed with $WARNINGS warning(s)"
    echo -e "\n${YELLOW}⚠️  Project is compliant with minor issues${NC}"
    exit 0
else
    print_status "ERROR" "Validation failed with $ERRORS error(s) and $WARNINGS warning(s)"
    echo -e "\n${RED}❌ Project has compliance issues that need to be addressed${NC}"
    exit 1
fi
