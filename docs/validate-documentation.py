#!/usr/bin/env python3
"""
Documentation Validation Script for RPGer Content Extractor

This script validates all documentation links and ensures the documentation
structure is complete and consistent.
"""

import os
import re
import sys
from pathlib import Path
from typing import List, Dict, Set, Tuple

class DocumentationValidator:
    """Validate documentation structure and links."""
    
    def __init__(self, docs_root: str = "docs"):
        self.docs_root = Path(docs_root)
        self.project_root = self.docs_root.parent
        self.errors: List[str] = []
        self.warnings: List[str] = []
        self.found_files: Set[Path] = set()
        self.referenced_files: Set[str] = set()
    
    def validate_all(self) -> bool:
        """Run all validation checks."""
        print("🔍 Validating RPGer Content Extractor Documentation...")
        print(f"📁 Documentation root: {self.docs_root.absolute()}")
        print()
        
        # Discover all documentation files
        self._discover_files()
        
        # Validate file structure
        self._validate_structure()
        
        # Validate links in all markdown files
        self._validate_links()
        
        # Check for orphaned files
        self._check_orphaned_files()
        
        # Print results
        self._print_results()
        
        return len(self.errors) == 0
    
    def _discover_files(self):
        """Discover all documentation files."""
        print("📋 Discovering documentation files...")
        
        # Find all markdown files
        for md_file in self.docs_root.rglob("*.md"):
            self.found_files.add(md_file)
        
        # Also check project root for key files
        for file_name in ["summary.md", "README.md", "issues.md"]:
            file_path = self.project_root / file_name
            if file_path.exists():
                self.found_files.add(file_path)
        
        print(f"   Found {len(self.found_files)} documentation files")
    
    def _validate_structure(self):
        """Validate expected documentation structure."""
        print("🏗️  Validating documentation structure...")
        
        required_dirs = [
            "api",
            "architecture", 
            "deployment",
            "development",
            "operations",
            "reference",
            "user-guides",
            "prp/base",
            "prp/features"
        ]
        
        for dir_name in required_dirs:
            dir_path = self.docs_root / dir_name
            if not dir_path.exists():
                self.errors.append(f"Missing required directory: {dir_path}")
            else:
                print(f"   ✅ {dir_name}/")
        
        # Check for key files
        required_files = [
            "index.md",
            "api/api-reference.md",
            "architecture/architecture-overview.md",
            "user-guides/web-interface-guide.md"
        ]
        
        for file_name in required_files:
            file_path = self.docs_root / file_name
            if not file_path.exists():
                self.errors.append(f"Missing required file: {file_path}")
            else:
                print(f"   ✅ {file_name}")
    
    def _validate_links(self):
        """Validate all markdown links."""
        print("🔗 Validating documentation links...")
        
        link_pattern = re.compile(r'\[([^\]]+)\]\(([^)]+)\)')
        
        for md_file in self.found_files:
            if md_file.suffix != '.md':
                continue
                
            try:
                content = md_file.read_text(encoding='utf-8')
                links = link_pattern.findall(content)
                
                for link_text, link_url in links:
                    self._validate_single_link(md_file, link_text, link_url)
                    
            except Exception as e:
                self.errors.append(f"Error reading {md_file}: {e}")
    
    def _validate_single_link(self, source_file: Path, link_text: str, link_url: str):
        """Validate a single markdown link."""
        # Skip external URLs
        if link_url.startswith(('http://', 'https://', 'mailto:')):
            return
        
        # Skip anchors
        if link_url.startswith('#'):
            return
        
        # Record referenced file
        self.referenced_files.add(link_url)
        
        # Resolve relative path
        if link_url.startswith('../'):
            # Link goes up from docs directory
            target_path = source_file.parent / link_url
        elif link_url.startswith('./'):
            # Link is relative to current directory
            target_path = source_file.parent / link_url[2:]
        elif '/' in link_url:
            # Link is relative to docs root
            target_path = self.docs_root / link_url
        else:
            # Link is in same directory
            target_path = source_file.parent / link_url
        
        # Resolve and normalize path
        try:
            target_path = target_path.resolve()
        except Exception:
            self.errors.append(f"Invalid link path in {source_file.name}: {link_url}")
            return
        
        # Check if target exists
        if not target_path.exists():
            self.errors.append(f"Broken link in {source_file.name}: '{link_text}' -> {link_url}")
        else:
            print(f"   ✅ {source_file.name}: {link_text}")
    
    def _check_orphaned_files(self):
        """Check for orphaned documentation files."""
        print("🔍 Checking for orphaned files...")
        
        # Files that should be referenced
        important_files = [
            "api/api-reference.md",
            "api/api-examples.md", 
            "architecture/architecture-overview.md",
            "user-guides/web-interface-guide.md",
            "development/development-setup.md"
        ]
        
        for file_path in important_files:
            if file_path not in self.referenced_files:
                # Check if it's referenced with different path formats
                file_name = Path(file_path).name
                if not any(file_name in ref for ref in self.referenced_files):
                    self.warnings.append(f"Important file may be orphaned: {file_path}")
    
    def _print_results(self):
        """Print validation results."""
        print("\n" + "="*60)
        print("📊 VALIDATION RESULTS")
        print("="*60)
        
        if self.errors:
            print(f"\n❌ ERRORS ({len(self.errors)}):")
            for error in self.errors:
                print(f"   • {error}")
        
        if self.warnings:
            print(f"\n⚠️  WARNINGS ({len(self.warnings)}):")
            for warning in self.warnings:
                print(f"   • {warning}")
        
        if not self.errors and not self.warnings:
            print("\n✅ ALL VALIDATION CHECKS PASSED!")
            print("   Documentation structure is complete and all links are valid.")
        elif not self.errors:
            print(f"\n✅ VALIDATION PASSED with {len(self.warnings)} warnings")
            print("   All critical checks passed, warnings are informational.")
        else:
            print(f"\n❌ VALIDATION FAILED with {len(self.errors)} errors")
            print("   Please fix the errors above before proceeding.")
        
        print(f"\n📈 STATISTICS:")
        print(f"   • Documentation files found: {len(self.found_files)}")
        print(f"   • Links validated: {len(self.referenced_files)}")
        print(f"   • Errors: {len(self.errors)}")
        print(f"   • Warnings: {len(self.warnings)}")

def main():
    """Main validation function."""
    # Change to script directory
    script_dir = Path(__file__).parent
    os.chdir(script_dir.parent)
    
    # Run validation
    validator = DocumentationValidator()
    success = validator.validate_all()
    
    # Exit with appropriate code
    sys.exit(0 if success else 1)

if __name__ == "__main__":
    main()
