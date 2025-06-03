"""
Tests for AI Usage Display feature
Testing the new AI model usage information display functionality
"""

import pytest
import json
from ui.app import app


class TestAIUsageAPI:
    """Test the new AI usage planning API endpoint"""
    
    @pytest.fixture
    def client(self):
        """Create test client"""
        app.config['TESTING'] = True
        with app.test_client() as client:
            yield client
    
    def test_planning_api_analysis_mock(self, client):
        """Test planning API for analysis with mock provider"""
        response = client.get('/api/processing/plan?step=analysis&ai_provider=mock&content_type=source_material')
        
        assert response.status_code == 200
        data = json.loads(response.data)
        
        assert data['step'] == 'analysis'
        assert data['ai_usage']['provider'] == 'mock'
        assert data['ai_usage']['fallback_mode'] is True
        assert data['ai_usage']['model'] == 'Mock AI (No real processing)'
        assert data['ai_usage']['purpose'] == 'Basic text extraction only'
        assert data['ai_usage']['estimated_tokens'] == 2000
    
    def test_planning_api_analysis_claude(self, client):
        """Test planning API for analysis with Claude provider"""
        response = client.get('/api/processing/plan?step=analysis&ai_provider=claude&content_type=source_material')
        
        assert response.status_code == 200
        data = json.loads(response.data)
        
        assert data['step'] == 'analysis'
        assert data['ai_usage']['provider'] == 'claude'
        assert data['ai_usage']['fallback_mode'] is False
        assert data['ai_usage']['model'] == 'Claude 3.5 Sonnet'
        assert data['ai_usage']['purpose'] == 'Content type detection & metadata extraction'
        assert data['ai_usage']['estimated_tokens'] == 2000
    
    def test_planning_api_extraction_openrouter(self, client):
        """Test planning API for extraction with OpenRouter"""
        response = client.get('/api/processing/plan?step=extraction&ai_provider=openrouter&ai_model=google/gemini-2.0-flash-exp&content_type=novel')
        
        assert response.status_code == 200
        data = json.loads(response.data)
        
        assert data['step'] == 'extraction'
        assert data['ai_usage']['provider'] == 'openrouter'
        assert data['ai_usage']['fallback_mode'] is False
        assert data['ai_usage']['model'] == 'google/gemini-2.0-flash-exp'
        assert data['ai_usage']['purpose'] == 'Content categorization & enhancement'
        assert data['ai_usage']['estimated_tokens'] == 5000
    
    def test_planning_api_openrouter_no_model(self, client):
        """Test planning API for OpenRouter without model selection"""
        response = client.get('/api/processing/plan?step=analysis&ai_provider=openrouter&content_type=source_material')
        
        assert response.status_code == 200
        data = json.loads(response.data)
        
        assert data['step'] == 'analysis'
        assert data['ai_usage']['provider'] == 'openrouter'
        assert data['ai_usage']['fallback_mode'] is True
        assert data['ai_usage']['model'] == 'OpenRouter (Model not selected)'
        assert data['ai_usage']['purpose'] == 'Please select a model first'
    
    def test_planning_api_missing_parameters(self, client):
        """Test planning API with missing parameters"""
        response = client.get('/api/processing/plan')
        
        assert response.status_code == 200
        data = json.loads(response.data)
        
        # Should use defaults
        assert data['step'] == 'analysis'
        assert data['ai_usage']['provider'] == 'mock'
        assert data['ai_usage']['fallback_mode'] is True
    
    def test_planning_api_invalid_step(self, client):
        """Test planning API with invalid step"""
        response = client.get('/api/processing/plan?step=invalid_step&ai_provider=mock')
        
        assert response.status_code == 200
        data = json.loads(response.data)
        
        # Should still work but with the invalid step name
        assert data['step'] == 'invalid_step'
        assert data['ai_usage']['provider'] == 'mock'


class TestAnalyzeEndpointEnhancement:
    """Test that analyze endpoint returns AI usage information"""
    
    @pytest.fixture
    def client(self):
        """Create test client"""
        app.config['TESTING'] = True
        with app.test_client() as client:
            yield client
    
    @pytest.fixture
    def sample_pdf_file(self):
        """Use existing test PDF file"""
        import os
        test_pdf = os.path.join(os.path.dirname(__file__), 'fixtures', 'pdfs', 'test.pdf')
        return test_pdf
    
    def test_analyze_returns_ai_usage(self, client, sample_pdf_file):
        """Test that analyze endpoint returns AI usage information"""
        response = client.post('/analyze', 
            json={
                'filepath': sample_pdf_file,
                'ai_provider': 'mock',
                'content_type': 'source_material'
            })
        
        assert response.status_code == 200
        data = json.loads(response.data)
        
        assert data['success'] is True
        assert 'ai_usage' in data
        assert data['ai_usage']['provider'] == 'mock'
        assert data['ai_usage']['fallback_used'] is True
        assert data['ai_usage']['model_used'] == 'Mock AI (No real processing)'
        assert 'tokens_consumed' in data['ai_usage']
        assert 'processing_time' in data['ai_usage']
        assert 'confidence' in data['ai_usage']


if __name__ == '__main__':
    pytest.main([__file__])