#!/bin/bash
# Project Status Overview Script for RPGer Content Extractor
# Provides a comprehensive overview of project status and metrics

set -e

echo "📊 RPGer Content Extractor - Project Status Overview"
echo "===================================================="

# Colors for output
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Project Information
echo -e "\n${BLUE}📋 Project Information${NC}"
echo "======================"
if [ -f ".augment/project-config.json" ]; then
    echo "Project Name: $(grep -o '"name": "[^"]*"' .augment/project-config.json | cut -d'"' -f4)"
    echo "Version: $(grep -o '"version": "[^"]*"' .augment/project-config.json | cut -d'"' -f4)"
    echo "Status: $(grep -o '"status": "[^"]*"' .augment/project-config.json | cut -d'"' -f4)"
    echo "Type: $(grep -o '"type": "[^"]*"' .augment/project-config.json | cut -d'"' -f4)"
fi

# Documentation Status
echo -e "\n${BLUE}📚 Documentation Status${NC}"
echo "======================="
doc_count=$(find docs -name "*.md" 2>/dev/null | wc -l)
echo "Total Documentation Files: $doc_count"

if [ -f "docs/index.md" ]; then
    echo -e "${GREEN}✅ Documentation Index: Present${NC}"
else
    echo -e "${YELLOW}⚠️  Documentation Index: Missing${NC}"
fi

if [ -f "summary.md" ]; then
    echo -e "${GREEN}✅ Project Summary: Present${NC}"
else
    echo -e "${YELLOW}⚠️  Project Summary: Missing${NC}"
fi

# PRP Status
echo -e "\n${BLUE}📋 PRP (Project Requirements & Planning) Status${NC}"
echo "==============================================="
base_prp_count=$(find docs/prp/base -name "*.md" 2>/dev/null | wc -l)
feature_prp_count=$(find docs/prp/features -name "*.md" 2>/dev/null | wc -l)
echo "Base PRPs: $base_prp_count"
echo "Feature PRPs: $feature_prp_count"
echo "Total PRPs: $((base_prp_count + feature_prp_count))"

# Code Structure
echo -e "\n${BLUE}💻 Code Structure${NC}"
echo "=================="
if [ -d "Modules" ]; then
    module_count=$(find Modules -name "*.py" 2>/dev/null | wc -l)
    echo "Python Modules: $module_count"
fi

if [ -d "tests" ]; then
    test_count=$(find tests -name "test_*.py" 2>/dev/null | wc -l)
    echo "Test Files: $test_count"
fi

if [ -d "ui" ]; then
    echo -e "${GREEN}✅ Web UI: Present${NC}"
else
    echo -e "${YELLOW}⚠️  Web UI: Missing${NC}"
fi

# Docker Configuration
echo -e "\n${BLUE}🐳 Docker Configuration${NC}"
echo "======================="
if [ -f "Dockerfile" ]; then
    echo -e "${GREEN}✅ Dockerfile: Present${NC}"
else
    echo -e "${YELLOW}⚠️  Dockerfile: Missing${NC}"
fi

compose_count=$(find . -maxdepth 1 -name "docker-compose*.yml" 2>/dev/null | wc -l)
echo "Docker Compose Files: $compose_count"

# Dependencies
echo -e "\n${BLUE}📦 Dependencies${NC}"
echo "==============="
if [ -f "requirements.txt" ]; then
    dep_count=$(grep -c "^[^#]" requirements.txt 2>/dev/null || echo "0")
    echo "Python Dependencies: $dep_count"
fi

if [ -f "ui/requirements.txt" ]; then
    ui_dep_count=$(grep -c "^[^#]" ui/requirements.txt 2>/dev/null || echo "0")
    echo "UI Dependencies: $ui_dep_count"
fi

# Git Status (if available)
echo -e "\n${BLUE}📝 Repository Status${NC}"
echo "==================="
if [ -d ".git" ]; then
    current_branch=$(git branch --show-current 2>/dev/null || echo "unknown")
    echo "Current Branch: $current_branch"
    
    commit_count=$(git rev-list --count HEAD 2>/dev/null || echo "unknown")
    echo "Total Commits: $commit_count"
    
    last_commit=$(git log -1 --format="%h - %s (%cr)" 2>/dev/null || echo "unknown")
    echo "Last Commit: $last_commit"
else
    echo "Not a Git repository"
fi

# File Statistics
echo -e "\n${BLUE}📊 File Statistics${NC}"
echo "=================="
total_files=$(find . -type f ! -path "./.git/*" ! -path "./venv/*" ! -path "./__pycache__/*" ! -path "./htmlcov/*" 2>/dev/null | wc -l)
echo "Total Project Files: $total_files"

py_files=$(find . -name "*.py" ! -path "./venv/*" ! -path "./__pycache__/*" 2>/dev/null | wc -l)
echo "Python Files: $py_files"

md_files=$(find . -name "*.md" 2>/dev/null | wc -l)
echo "Markdown Files: $md_files"

# Project Health Check
echo -e "\n${BLUE}🏥 Project Health Check${NC}"
echo "======================="

# Check if validation script exists and run it
if [ -f "scripts/validate-project.sh" ]; then
    echo "Running project validation..."
    if ./scripts/validate-project.sh > /dev/null 2>&1; then
        echo -e "${GREEN}✅ Project Validation: PASSED${NC}"
    else
        echo -e "${YELLOW}⚠️  Project Validation: ISSUES FOUND${NC}"
    fi
else
    echo -e "${YELLOW}⚠️  Project Validation Script: Not Available${NC}"
fi

# Check documentation validation
if [ -f "docs/validate-documentation.py" ]; then
    if python3 docs/validate-documentation.py > /dev/null 2>&1; then
        echo -e "${GREEN}✅ Documentation Validation: PASSED${NC}"
    else
        echo -e "${YELLOW}⚠️  Documentation Validation: ISSUES FOUND${NC}"
    fi
else
    echo -e "${YELLOW}⚠️  Documentation Validation: Not Available${NC}"
fi

echo -e "\n${GREEN}📈 Project Status: Operational${NC}"
echo "================================"
echo "For detailed information, see:"
echo "• Project Summary: summary.md"
echo "• Documentation Index: docs/index.md"
echo "• Installation Guide: docs/Installation-Guide.md"
echo "• Quick Start: docs/Quick-Start.md"
