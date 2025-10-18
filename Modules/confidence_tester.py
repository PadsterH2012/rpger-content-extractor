#!/usr/bin/env python3
"""
Confidence Tester Module
Provides confidence testing functionality for AI game detection
"""

from typing import Dict, Any, List
from pathlib import Path


class ConfidenceTester:
    """Test confidence levels of AI game detection"""
    
    def __init__(self, ai_config: Dict[str, Any] = None):
        self.ai_config = ai_config or {"provider": "mock"}
        self.test_results = []
    
    def test_confidence_levels(self, test_cases: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Test confidence levels across multiple test cases"""
        results = {
            "total_tests": len(test_cases),
            "passed": 0,
            "failed": 0,
            "average_confidence": 0.0,
            "test_details": []
        }
        
        total_confidence = 0.0
        
        for i, test_case in enumerate(test_cases):
            content = test_case.get("content", "")
            expected_game_type = test_case.get("expected_game_type", "Unknown")
            expected_confidence = test_case.get("expected_confidence", 50.0)
            
            # Mock confidence testing
            detected_confidence = self._mock_confidence_analysis(content, expected_game_type)
            
            test_result = {
                "test_id": i + 1,
                "content_sample": content[:100] + "..." if len(content) > 100 else content,
                "expected_game_type": expected_game_type,
                "expected_confidence": expected_confidence,
                "detected_confidence": detected_confidence,
                "passed": abs(detected_confidence - expected_confidence) <= 20.0
            }
            
            results["test_details"].append(test_result)
            total_confidence += detected_confidence
            
            if test_result["passed"]:
                results["passed"] += 1
            else:
                results["failed"] += 1
        
        if test_cases:
            results["average_confidence"] = total_confidence / len(test_cases)
        
        return results
    
    def _mock_confidence_analysis(self, content: str, expected_game_type: str) -> float:
        """Mock confidence analysis for testing"""
        content_lower = content.lower()
        
        # Simple keyword-based confidence scoring
        confidence = 50.0  # Base confidence
        
        if expected_game_type.lower() == "d&d":
            if any(keyword in content_lower for keyword in ["dungeons", "dragons", "d&d", "dnd"]):
                confidence += 30.0
            if any(keyword in content_lower for keyword in ["armor class", "hit points", "saving throw"]):
                confidence += 15.0
        
        elif expected_game_type.lower() == "pathfinder":
            if any(keyword in content_lower for keyword in ["pathfinder", "paizo"]):
                confidence += 30.0
            if any(keyword in content_lower for keyword in ["ancestry", "heritage", "feat"]):
                confidence += 15.0
        
        elif expected_game_type.lower() == "unknown":
            confidence = max(20.0, confidence - 20.0)
        
        # Add some randomness to simulate real AI behavior
        import random
        confidence += random.uniform(-5.0, 5.0)
        
        return min(100.0, max(0.0, confidence))
    
    def generate_confidence_report(self, results: Dict[str, Any]) -> str:
        """Generate a human-readable confidence test report"""
        report = []
        report.append("=== CONFIDENCE TESTING REPORT ===")
        report.append(f"Total Tests: {results['total_tests']}")
        report.append(f"Passed: {results['passed']}")
        report.append(f"Failed: {results['failed']}")
        report.append(f"Success Rate: {(results['passed'] / results['total_tests'] * 100):.1f}%")
        report.append(f"Average Confidence: {results['average_confidence']:.1f}%")
        report.append("")
        
        report.append("=== TEST DETAILS ===")
        for test in results["test_details"]:
            status = "✅ PASS" if test["passed"] else "❌ FAIL"
            report.append(f"Test {test['test_id']}: {status}")
            report.append(f"  Expected: {test['expected_game_type']} ({test['expected_confidence']:.1f}%)")
            report.append(f"  Detected: {test['detected_confidence']:.1f}%")
            report.append(f"  Content: {test['content_sample']}")
            report.append("")
        
        return "\n".join(report)


def run_confidence_tests(test_cases: List[Dict[str, Any]], ai_config: Dict[str, Any] = None) -> Dict[str, Any]:
    """Convenience function to run confidence tests"""
    tester = ConfidenceTester(ai_config)
    return tester.test_confidence_levels(test_cases)
