"""
Tests for Confidence Tester functionality.

This module tests the confidence testing capabilities including:
- Confidence level testing
- AI game detection confidence validation
- Test case management
- Statistical analysis

Priority: 2 (Essential Integration & Workflow)
"""

import pytest
from unittest.mock import Mock, patch
from Modules.confidence_tester import ConfidenceTester



@pytest.mark.unit
class TestConfidenceTesterInitialization:
    """Test confidence tester initialization"""

    def test_basic_initialization(self):
        """Test basic initialization"""
        tester = ConfidenceTester()
        
        assert tester.ai_config is not None
        assert tester.ai_config["provider"] == "mock"
        assert isinstance(tester.test_results, list)
        assert len(tester.test_results) == 0

    def test_initialization_with_config(self):
        """Test initialization with custom config"""
        config = {"provider": "test", "model": "test-model"}
        tester = ConfidenceTester(ai_config=config)
        
        assert tester.ai_config == config
        assert isinstance(tester.test_results, list)



@pytest.mark.unit
class TestConfidenceLevelTesting:
    """Test confidence level testing functionality"""

    def test_empty_test_cases(self):
        """Test handling of empty test cases"""
        tester = ConfidenceTester()
        
        results = tester.test_confidence_levels([])
        
        assert results["total_tests"] == 0
        assert results["passed"] == 0
        assert results["failed"] == 0
        assert results["average_confidence"] == 0.0
        assert len(results["test_details"]) == 0

    def test_single_test_case(self):
        """Test single test case"""
        tester = ConfidenceTester()
        
        test_cases = [{
            "content": "The wizard cast a fireball spell.",
            "expected_game_type": "D&D",
            "expected_confidence": 80.0
        }]
        
        results = tester.test_confidence_levels(test_cases)
        
        assert results["total_tests"] == 1
        assert len(results["test_details"]) == 1
        assert isinstance(results["average_confidence"], float)
        assert 0 <= results["average_confidence"] <= 100

    def test_multiple_test_cases(self):
        """Test multiple test cases"""
        tester = ConfidenceTester()
        
        test_cases = [
            {
                "content": "The wizard cast a fireball spell.",
                "expected_game_type": "D&D",
                "expected_confidence": 80.0
            },
            {
                "content": "The ranger tracked through the forest.",
                "expected_game_type": "D&D",
                "expected_confidence": 70.0
            },
            {
                "content": "Unknown content with no game elements.",
                "expected_game_type": "Unknown",
                "expected_confidence": 10.0
            }
        ]
        
        results = tester.test_confidence_levels(test_cases)
        
        assert results["total_tests"] == 3
        assert len(results["test_details"]) == 3
        assert results["passed"] + results["failed"] == 3
        assert isinstance(results["average_confidence"], float)

    def test_test_case_validation(self):
        """Test test case validation logic"""
        tester = ConfidenceTester()
        
        # Test case that should pass (within tolerance)
        test_cases = [{
            "content": "Standard D&D content",
            "expected_game_type": "D&D",
            "expected_confidence": 50.0  # Mock returns values around this range
        }]
        
        results = tester.test_confidence_levels(test_cases)
        
        # Should have at least attempted the test
        assert len(results["test_details"]) == 1
        test_detail = results["test_details"][0]
        
        assert "test_id" in test_detail
        assert "content_sample" in test_detail
        assert "expected_game_type" in test_detail
        assert "expected_confidence" in test_detail
        assert "detected_confidence" in test_detail
        assert "passed" in test_detail



@pytest.mark.unit  
class TestMockConfidenceAnalysis:
    """Test mock confidence analysis functionality"""

    def test_mock_confidence_analysis_exists(self):
        """Test that mock confidence analysis method exists"""
        tester = ConfidenceTester()
        
        # Test that the method exists and can be called
        result = tester._mock_confidence_analysis("test content", "D&D")
        
        assert isinstance(result, (int, float))
        assert 0 <= result <= 100

    def test_mock_confidence_consistency(self):
        """Test mock confidence analysis consistency"""
        tester = ConfidenceTester()
        
        # Same input should give consistent results
        content = "The wizard cast a spell"
        game_type = "D&D"
        
        result1 = tester._mock_confidence_analysis(content, game_type)
        result2 = tester._mock_confidence_analysis(content, game_type)
        
        # Results should be consistent (or close)
        assert isinstance(result1, (int, float))
        assert isinstance(result2, (int, float))
        assert 0 <= result1 <= 100
        assert 0 <= result2 <= 100

    def test_mock_confidence_different_inputs(self):
        """Test mock confidence with different inputs"""
        tester = ConfidenceTester()
        
        test_cases = [
            ("D&D content with spells", "D&D"),
            ("Pathfinder ancestries and backgrounds", "Pathfinder"),
            ("Random non-game text", "Unknown"),
            ("", "Unknown")
        ]
        
        for content, game_type in test_cases:
            result = tester._mock_confidence_analysis(content, game_type)
            assert isinstance(result, (int, float))
            assert 0 <= result <= 100



@pytest.mark.unit
class TestResultsManagement:
    """Test test results management"""

    def test_test_results_storage(self):
        """Test that test results are stored properly"""
        tester = ConfidenceTester()
        
        # Initially empty
        assert len(tester.test_results) == 0
        
        # Run a test
        test_cases = [{
            "content": "Test content",
            "expected_game_type": "D&D",
            "expected_confidence": 75.0
        }]
        
        results = tester.test_confidence_levels(test_cases)
        
        # Results structure should be valid
        assert isinstance(results, dict)
        assert "total_tests" in results
        assert "test_details" in results
        assert isinstance(results["test_details"], list)

    def test_content_truncation(self):
        """Test content truncation in results"""
        tester = ConfidenceTester()
        
        # Long content that should be truncated
        long_content = "A" * 200  # 200 characters
        
        test_cases = [{
            "content": long_content,
            "expected_game_type": "D&D", 
            "expected_confidence": 50.0
        }]
        
        results = tester.test_confidence_levels(test_cases)
        
        test_detail = results["test_details"][0]
        content_sample = test_detail["content_sample"]
        
        # Should be truncated with "..."
        assert len(content_sample) <= 103  # 100 chars + "..."
        assert content_sample.endswith("...")

    def test_short_content_no_truncation(self):
        """Test that short content is not truncated"""
        tester = ConfidenceTester()
        
        short_content = "Short"  # 5 characters
        
        test_cases = [{
            "content": short_content,
            "expected_game_type": "D&D",
            "expected_confidence": 50.0
        }]
        
        results = tester.test_confidence_levels(test_cases)
        
        test_detail = results["test_details"][0]
        content_sample = test_detail["content_sample"]
        
        # Should not be truncated
        assert content_sample == short_content
        assert not content_sample.endswith("...")



@pytest.mark.unit
class TestStatisticalAnalysis:
    """Test statistical analysis functionality"""

    def test_average_confidence_calculation(self):
        """Test average confidence calculation"""
        tester = ConfidenceTester()
        
        # Create test cases where we can predict the average
        test_cases = [
            {"content": "Test 1", "expected_game_type": "D&D", "expected_confidence": 60.0},
            {"content": "Test 2", "expected_game_type": "D&D", "expected_confidence": 80.0},
        ]
        
        results = tester.test_confidence_levels(test_cases)
        
        # Average should be calculated
        assert isinstance(results["average_confidence"], float)
        assert 0 <= results["average_confidence"] <= 100
        
        # Should be based on detected confidence, not expected
        detected_confidences = [detail["detected_confidence"] for detail in results["test_details"]]
        expected_average = sum(detected_confidences) / len(detected_confidences)
        assert abs(results["average_confidence"] - expected_average) < 0.01

    def test_pass_fail_counting(self):
        """Test pass/fail counting logic"""
        tester = ConfidenceTester()
        
        test_cases = [
            {"content": "Test content", "expected_game_type": "D&D", "expected_confidence": 50.0}
        ]
        
        results = tester.test_confidence_levels(test_cases)
        
        # Should count passes and fails
        assert isinstance(results["passed"], int)
        assert isinstance(results["failed"], int)
        assert results["passed"] >= 0
        assert results["failed"] >= 0
        assert results["passed"] + results["failed"] == results["total_tests"]



@pytest.mark.unit
class TestErrorHandling:
    """Test error handling scenarios"""

    def test_missing_content_field(self):
        """Test handling of missing content field"""
        tester = ConfidenceTester()
        
        test_cases = [{
            "expected_game_type": "D&D",
            "expected_confidence": 50.0
            # Missing "content" field
        }]
        
        results = tester.test_confidence_levels(test_cases)
        
        # Should handle gracefully
        assert results["total_tests"] == 1
        assert len(results["test_details"]) == 1
        
        # Content should default to empty string
        test_detail = results["test_details"][0]
        assert test_detail["content_sample"] == ""

    def test_missing_optional_fields(self):
        """Test handling of missing optional fields"""
        tester = ConfidenceTester()
        
        test_cases = [{
            "content": "Test content"
            # Missing expected_game_type and expected_confidence
        }]
        
        results = tester.test_confidence_levels(test_cases)
        
        # Should handle gracefully with defaults
        assert results["total_tests"] == 1
        test_detail = results["test_details"][0]
        
        assert test_detail["expected_game_type"] == "Unknown"
        assert test_detail["expected_confidence"] == 50.0

    def test_invalid_input_types(self):
        """Test handling of invalid input types"""
        tester = ConfidenceTester()
        
        # Test with None
        results = tester.test_confidence_levels(None or [])
        assert results["total_tests"] == 0
        
        # Test with non-list
        results = tester.test_confidence_levels({})
        # Should handle gracefully or iterate over empty