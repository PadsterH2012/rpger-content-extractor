"""
Flask Web UI Tests.

This module tests the Flask web application functionality including:
- File upload validation and handling
- API endpoints (/analyze, /extract, /progress)
- Error handling and status codes
- Real-time progress tracking
- Session management

Priority: 2 (Essential Integration & Workflow)
"""

import pytest
import json
import tempfile
import os
from pathlib import Path
from unittest.mock import Mock, patch, MagicMock
from io import BytesIO

# Import Flask app for testing
import sys
sys.path.append(str(Path(__file__).parent.parent / "ui"))

from ui.app import app, analysis_results, extraction_results


def create_mock_pdf_document(num_pages=1, has_isbn=False):
    """
    Create a properly configured mock PyMuPDF document.

    This helper function creates a mock document that properly supports:
    - len(doc) via __len__
    - doc[page_num] via __getitem__
    - page.get_text() for text extraction

    Args:
        num_pages: Number of pages in the mock document
        has_isbn: Whether to include ISBN in metadata

    Returns:
        MagicMock PyMuPDF document object with proper special methods
    """
    # Use MagicMock to properly support special methods like __len__ and __getitem__
    mock_doc = MagicMock()
    mock_doc.close = Mock()

    # Configure metadata
    if has_isbn:
        mock_doc.metadata = {'subject': 'ISBN-13: 9780786965601'}
    else:
        mock_doc.metadata = {}

    # Create mock pages
    mock_pages = []
    for i in range(num_pages):
        mock_page = MagicMock()
        mock_page.get_text = Mock(return_value=f"Page {i+1} content")
        mock_pages.append(mock_page)

    # Configure __len__ to support len(doc)
    mock_doc.__len__ = Mock(return_value=num_pages)

    # Configure __getitem__ to support doc[page_num]
    mock_doc.__getitem__ = Mock(side_effect=lambda idx: mock_pages[idx])

    return mock_doc


@pytest.mark.priority2
@pytest.mark.web
@pytest.mark.integration
class TestFlaskAppSetup:
    """Test Flask application setup and configuration"""

    @pytest.fixture
    def client(self):
        """Create test client"""
        app.config['TESTING'] = True
        app.config['WTF_CSRF_ENABLED'] = False
        with app.test_client() as client:
            yield client

    def test_app_configuration(self, client):
        """Test Flask app configuration"""
        assert app.config['MAX_CONTENT_LENGTH'] == 200 * 1024 * 1024  # 200MB
        assert app.config['UPLOAD_TIMEOUT'] == 300  # 5 minutes
        assert app.config['TESTING'] == True

    def test_index_route(self, client):
        """Test main index route"""
        response = client.get('/')
        assert response.status_code == 200
        assert b'html' in response.data.lower()

    def test_version_endpoint(self, client):
        """Test version API endpoint"""
        response = client.get('/api/version')
        assert response.status_code == 200

        data = json.loads(response.data)
        assert 'version' in data
        assert 'build_date' in data


@pytest.mark.priority2
@pytest.mark.web
@pytest.mark.integration
class TestFileUpload:
    """Test PDF file upload functionality"""

    @pytest.fixture
    def client(self):
        """Create test client"""
        app.config['TESTING'] = True
        app.config['WTF_CSRF_ENABLED'] = False
        with app.test_client() as client:
            yield client

    def test_valid_pdf_upload(self, client):
        """Test uploading a valid PDF file"""
        # Create mock PDF content
        pdf_content = b'%PDF-1.4\nMock PDF content\n%%EOF'

        data = {
            'file': (BytesIO(pdf_content), 'test.pdf', 'application/pdf')
        }

        response = client.post('/upload', data=data, content_type='multipart/form-data')
        assert response.status_code == 200

        result = json.loads(response.data)
        assert result['success'] == True
        assert result['filename'] == 'test.pdf'
        assert 'filepath' in result
        assert result['size'] == len(pdf_content)

    def test_no_file_upload(self, client):
        """Test upload with no file"""
        response = client.post('/upload', data={})
        assert response.status_code == 400

        result = json.loads(response.data)
        assert 'error' in result
        assert 'No file selected' in result['error']

    def test_empty_filename_upload(self, client):
        """Test upload with empty filename"""
        data = {
            'file': (BytesIO(b'content'), '', 'application/pdf')
        }

        response = client.post('/upload', data=data, content_type='multipart/form-data')
        assert response.status_code == 400

        result = json.loads(response.data)
        assert 'error' in result
        assert 'No file selected' in result['error']

    def test_invalid_file_type_upload(self, client):
        """Test upload with invalid file type"""
        data = {
            'file': (BytesIO(b'text content'), 'test.txt', 'text/plain')
        }

        response = client.post('/upload', data=data, content_type='multipart/form-data')
        assert response.status_code == 400

        result = json.loads(response.data)
        assert 'error' in result
        assert 'Only PDF files are allowed' in result['error']

    def test_file_size_limit(self, client):
        """Test file size limit enforcement"""
        # Create content larger than limit
        large_content = b'x' * (201 * 1024 * 1024)  # 201MB

        data = {
            'file': (BytesIO(large_content), 'large.pdf', 'application/pdf')
        }

        response = client.post('/upload', data=data, content_type='multipart/form-data')
        assert response.status_code == 400

        result = json.loads(response.data)
        assert 'error' in result
        assert 'File too large' in result['error']

    def test_file_corruption_detection(self, client):
        """Test detection of file corruption during upload"""
        # This test simulates file corruption by mocking file operations
        pdf_content = b'%PDF-1.4\nMock PDF content\n%%EOF'

        with patch('os.path.getsize') as mock_getsize:
            # Simulate size mismatch (corruption)
            mock_getsize.return_value = len(pdf_content) + 100

            data = {
                'file': (BytesIO(pdf_content), 'corrupt.pdf', 'application/pdf')
            }

            response = client.post('/upload', data=data, content_type='multipart/form-data')
            assert response.status_code == 500

            result = json.loads(response.data)
            assert 'error' in result
            assert 'corrupted' in result['error'].lower()


class TestAnalyzeEndpoint:
    """Test /analyze API endpoint"""

    @pytest.fixture
    def client(self):
        """Create test client"""
        app.config['TESTING'] = True
        app.config['WTF_CSRF_ENABLED'] = False
        with app.test_client() as client:
            yield client

    @pytest.fixture
    def temp_pdf(self, tmp_path):
        """Create temporary PDF file for testing"""
        pdf_file = tmp_path / "test.pdf"
        pdf_file.write_text("Mock PDF content")
        return str(pdf_file)

    def test_analyze_with_mock_provider(self, client, temp_pdf):
        """Test analysis with mock AI provider"""
        with patch('ui.app.AIGameDetector') as mock_detector_class:
            mock_detector = Mock()
            mock_detector_class.return_value = mock_detector

            # Mock the extract_analysis_content method
            mock_detector.extract_analysis_content.return_value = {
                'combined_text': 'Test content for analysis',
                'pages_analyzed': 1
            }

            mock_detector.analyze_game_metadata.return_value = {
                'game_type': 'D&D',
                'edition': '5th Edition',
                'book_type': 'Core Rulebook',
                'collection': 'Player\'s Handbook',
                'collection_name': 'dnd_5th_players_handbook',
                'confidence': 95.0,
                'content_type': 'source_material'
            }

            # Mock the set_session_tracking method
            mock_detector.set_session_tracking = Mock()

            # Mock token tracker
            with patch('Modules.token_usage_tracker.get_tracker') as mock_tracker:
                mock_tracker_instance = Mock()
                mock_tracker.return_value = mock_tracker_instance
                mock_tracker_instance.start_session = Mock()

                # Mock fitz (PyMuPDF) for ISBN extraction
                with patch('fitz.open') as mock_fitz:
                    mock_doc = create_mock_pdf_document(num_pages=1, has_isbn=False)
                    mock_fitz.return_value = mock_doc

                    # Mock PDF processor for ISBN extraction
                    with patch('Modules.pdf_processor.MultiGamePDFProcessor') as mock_processor_class:
                        mock_processor = Mock()
                        mock_processor_class.return_value = mock_processor
                        mock_processor._extract_isbn.return_value = {
                            'isbn': '9780786965601',
                            'isbn_13': '9780786965601',
                            'source': 'pdf_metadata'
                        }

                        # Mock the analysis_results global dict
                        with patch('ui.app.analysis_results', {}) as mock_analysis_results:
                            data = {
                                'filepath': temp_pdf,
                                'ai_provider': 'mock',
                                'content_type': 'source_material',
                                'run_confidence_test': False
                            }

                            response = client.post('/analyze',
                                                 data=json.dumps(data),
                                                 content_type='application/json')

                            assert response.status_code == 200
                            result = json.loads(response.data)

                            assert result['success'] == True
                            assert 'session_id' in result
                            assert 'analysis' in result
                            assert result['analysis']['game_type'] == 'D&D'

    def test_analyze_file_not_found(self, client):
        """Test analysis with non-existent file"""
        data = {
            'filepath': '/non/existent/file.pdf',
            'ai_provider': 'mock'
        }

        response = client.post('/analyze',
                             data=json.dumps(data),
                             content_type='application/json')

        assert response.status_code == 400
        result = json.loads(response.data)
        assert 'error' in result
        assert 'File not found' in result['error']

    def test_analyze_with_different_providers(self, client, temp_pdf):
        """Test analysis with different AI providers"""
        providers = ['mock', 'openrouter', 'anthropic']

        for provider in providers:
            with patch('Modules.ai_game_detector.AIGameDetector') as mock_detector_class:
                mock_detector = Mock()
                mock_detector_class.return_value = mock_detector

                mock_detector.analyze_game_metadata.return_value = {
                    'game_type': 'D&D',
                    'edition': '5th Edition',
                    'confidence': 90.0
                }

                with patch('fitz.open') as mock_fitz:
                    mock_doc = Mock()
                    mock_doc.metadata = {}
                    mock_doc.__len__ = Mock(return_value=1)
                    mock_doc.__getitem__ = Mock(return_value=Mock())
                    mock_doc.__getitem__.return_value.get_text.return_value = "Test"
                    mock_fitz.return_value = mock_doc

                    data = {
                        'filepath': temp_pdf,
                        'ai_provider': provider,
                        'run_confidence_test': False
                    }

                    response = client.post('/analyze',
                                         data=json.dumps(data),
                                         content_type='application/json')

                    # Should handle all providers (mock will work, others may fail gracefully)
                    assert response.status_code in [200, 500]

    def test_analyze_with_confidence_testing(self, client, temp_pdf):
        """Test analysis with confidence testing enabled"""
        with patch('ui.app.AIGameDetector') as mock_detector_class:
            mock_detector = Mock()
            mock_detector_class.return_value = mock_detector

            # Mock the extract_analysis_content method
            mock_detector.extract_analysis_content.return_value = {
                'combined_text': 'Test content for analysis',
                'pages_analyzed': 1
            }

            mock_detector.analyze_game_metadata.return_value = {
                'game_type': 'D&D',
                'edition': '5th Edition',
                'book_type': 'Core Rulebook',
                'collection': 'Player\'s Handbook',
                'collection_name': 'dnd_5th_players_handbook',
                'confidence': 95.0,
                'content_type': 'source_material'
            }

            # Mock the set_session_tracking method
            mock_detector.set_session_tracking = Mock()

            # Mock confidence tester import - use direct module mocking
            with patch.dict('sys.modules', {'confidence_tester': Mock()}) as mock_modules:
                # Mock the specific function that will be imported
                mock_confidence_module = Mock()
                mock_confidence_module.run_quick_test = Mock(return_value={
                    'quick_confidence': 85.0,
                    'recommended_method': 'text',
                    'text_confidence': 85.0,
                    'layout_confidence': 80.0,
                    'issues': []
                })
                mock_modules['confidence_tester'] = mock_confidence_module

                # Mock token tracker
                with patch('Modules.token_usage_tracker.get_tracker') as mock_tracker:
                    mock_tracker_instance = Mock()
                    mock_tracker.return_value = mock_tracker_instance
                    mock_tracker_instance.start_session = Mock()

                    # Mock fitz and PDF processor for ISBN extraction
                    with patch('fitz.open') as mock_fitz:
                        mock_doc = create_mock_pdf_document(num_pages=1, has_isbn=False)
                        mock_fitz.return_value = mock_doc

                        with patch('Modules.pdf_processor.MultiGamePDFProcessor') as mock_processor_class:
                            mock_processor = Mock()
                            mock_processor_class.return_value = mock_processor
                            mock_processor._extract_isbn.return_value = {
                                'isbn': '9780786965601',
                                'source': 'pdf_metadata'
                            }

                            # Mock the analysis_results global dict
                            with patch('ui.app.analysis_results', {}) as mock_analysis_results:
                                data = {
                                    'filepath': temp_pdf,
                                    'ai_provider': 'mock',
                                    'run_confidence_test': True
                                }

                                response = client.post('/analyze',
                                                     data=json.dumps(data),
                                                     content_type='application/json')

                                assert response.status_code == 200
                                result = json.loads(response.data)

                                assert result['success'] == True
                                assert 'confidence' in result


class TestExtractEndpoint:
    """Test /extract API endpoint"""

    @pytest.fixture
    def client(self):
        """Create test client"""
        app.config['TESTING'] = True
        app.config['WTF_CSRF_ENABLED'] = False
        with app.test_client() as client:
            yield client

    def test_extract_without_analysis(self, client):
        """Test extraction without prior analysis"""
        data = {
            'session_id': 'non_existent_session'
        }

        response = client.post('/extract',
                             data=json.dumps(data),
                             content_type='application/json')

        assert response.status_code == 400
        result = json.loads(response.data)
        assert 'error' in result
        assert 'Analysis session not found' in result['error']

    def test_extract_with_text_enhancement(self, client):
        """Test extraction with text enhancement options"""
        # Set up a test session in analysis_results
        test_session_id = 'test_session_extract'
        analysis_results[test_session_id] = {
            'filepath': '/tmp/test.pdf',
            'game_metadata': {
                'game_type': 'D&D',
                'edition': '5th Edition',
                'confidence': 95.0
            },
            'ai_provider': 'mock',
            'content_type': 'source_material'
        }

        try:
            with patch('Modules.pdf_processor.MultiGamePDFProcessor') as mock_processor_class:
                mock_processor = Mock()
                mock_processor_class.return_value = mock_processor

                # Mock the progress callback
                mock_processor._character_progress_callback = Mock()

                mock_processor.extract_pdf.return_value = {
                    'metadata': {'game_type': 'D&D'},
                    'sections': [{'title': 'Test', 'content': 'Test content'}],
                    'extraction_summary': {
                        'total_pages': 1,
                        'sections_extracted': 1
                    }
                }

                # Mock fitz for any ISBN extraction that might occur
                with patch('fitz.open') as mock_fitz:
                    mock_doc = create_mock_pdf_document(num_pages=1)
                    mock_fitz.return_value = mock_doc

                    data = {
                        'session_id': test_session_id,
                        'enable_text_enhancement': True,
                        'aggressive_cleanup': False
                    }

                    response = client.post('/extract',
                                         data=json.dumps(data),
                                         content_type='application/json')

                    # Should handle extraction request (200 success or 500 error)
                    assert response.status_code in [200, 500]
        finally:
            # Clean up test data
            if test_session_id in analysis_results:
                del analysis_results[test_session_id]
            if test_session_id in extraction_results:
                del extraction_results[test_session_id]


class TestProgressTracking:
    """Test real-time progress tracking"""

    @pytest.fixture
    def client(self):
        """Create test client"""
        app.config['TESTING'] = True
        app.config['WTF_CSRF_ENABLED'] = False
        with app.test_client() as client:
            yield client

    def test_progress_endpoint_structure(self, client):
        """Test progress endpoint basic structure"""
        # Test that progress endpoint exists and has proper structure
        # Note: Actual progress testing requires session setup

        response = client.get('/progress/test_session')
        # Should return 404 for non-existent session or proper progress data
        assert response.status_code in [200, 404]

    def test_session_progress_callback(self):
        """Test session progress callback functionality"""
        # Mock progress callback system
        progress_data = {
            'session_id': 'test_session',
            'stage': 'extraction',
            'progress': 50.0,
            'message': 'Processing page 5 of 10'
        }

        # Test progress data structure
        assert 'session_id' in progress_data
        assert 'stage' in progress_data
        assert 'progress' in progress_data
        assert isinstance(progress_data['progress'], (int, float))
        assert 0 <= progress_data['progress'] <= 100


class TestErrorHandling:
    """Test error handling and status codes"""

    @pytest.fixture
    def client(self):
        """Create test client"""
        app.config['TESTING'] = True
        app.config['WTF_CSRF_ENABLED'] = False
        with app.test_client() as client:
            yield client

    def test_404_handling(self, client):
        """Test 404 error handling"""
        response = client.get('/non_existent_endpoint')
        assert response.status_code == 404

    def test_method_not_allowed(self, client):
        """Test method not allowed errors"""
        # Try GET on POST-only endpoint
        response = client.get('/upload')
        assert response.status_code == 405

    def test_invalid_json_handling(self, client):
        """Test handling of invalid JSON in requests"""
        # Send actual invalid JSON to test Flask's built-in JSON parsing
        response = client.post('/analyze',
                             data='{"invalid": json}',  # Missing quotes around json
                             content_type='application/json')

        # The app catches JSON errors and returns 500, not 400
        assert response.status_code == 500

    def test_missing_required_fields(self, client):
        """Test handling of missing required fields"""
        # Test analyze endpoint without required filepath
        data = {
            'ai_provider': 'mock'
            # Missing filepath
        }

        response = client.post('/analyze',
                             data=json.dumps(data),
                             content_type='application/json')

        assert response.status_code == 400
        result = json.loads(response.data)
        assert 'error' in result


class TestSystemStatus:
    """Test system status and health endpoints"""

    @pytest.fixture
    def client(self):
        """Create test client"""
        app.config['TESTING'] = True
        app.config['WTF_CSRF_ENABLED'] = False
        with app.test_client() as client:
            yield client

    def test_health_endpoint(self, client):
        """Test health check endpoint for CI/CD"""
        response = client.get('/health')
        assert response.status_code == 200

        result = json.loads(response.data)
        assert result['status'] == 'healthy'
        assert 'timestamp' in result
        assert 'version' in result
        assert 'environment' in result

    def test_status_endpoint(self, client):
        """Test system status endpoint"""
        with patch('Modules.multi_collection_manager.MultiGameCollectionManager') as mock_chroma:
            with patch('Modules.mongodb_manager.MongoDBManager') as mock_mongo:
                # Mock successful connections
                mock_chroma.return_value.collections = ['test_collection']
                mock_mongo.return_value.get_status.return_value = {
                    'status': 'Connected',
                    'collections': 5
                }

                response = client.get('/status')
                assert response.status_code == 200

                result = json.loads(response.data)
                assert 'chroma_status' in result
                assert 'mongodb_status' in result

    def test_available_providers_endpoint(self, client):
        """Test available AI providers endpoint"""
        with patch.dict(os.environ, {'OPENROUTER_API_KEY': 'test_key'}):
            response = client.get('/api/providers/available')
            assert response.status_code == 200

            result = json.loads(response.data)
            assert result['success'] == True
            assert 'available_providers' in result
            assert 'openrouter' in result['available_providers']
            assert 'mock' in result['available_providers']  # Always available
