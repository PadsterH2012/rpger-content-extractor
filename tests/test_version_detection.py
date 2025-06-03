"""
Version Detection Tests

This module tests the dynamic version detection functionality that allows
the application to automatically detect its version from Docker container
metadata and environment variables.

Priority: 2 (Essential for deployment verification)
"""

import pytest
import os
import tempfile
from unittest.mock import patch, mock_open

# Import version module for testing
import sys
from pathlib import Path
sys.path.append(str(Path(__file__).parent.parent))

@pytest.mark.priority2
@pytest.mark.unit
class TestVersionDetection:
    """Test dynamic version detection functionality"""

    def test_environment_variable_detection(self):
        """Test version detection from environment variables"""
        # Test environment variables method
        with patch.dict(os.environ, {
            'BUILD_VERSION': '1.0.44',
            'BUILD_DATE': '2025-06-03T00:00:00Z',
            'GIT_COMMIT': 'abc123456',
            'ENVIRONMENT': 'production'
        }):
            # Import version module fresh to test detection
            import importlib
            import version
            importlib.reload(version)
            
            assert version.__version__ == '1.0.44'
            assert version.__environment__ == 'production'
            assert version.__commit_hash__ == 'abc123456'
            assert version.__detection_method__ == 'environment_variables'

    def test_version_file_detection(self):
        """Test version detection from VERSION file"""
        # Mock the VERSION file
        with patch('os.path.exists') as mock_exists:
            with patch('builtins.open', mock_open(read_data='1.0.44\n')):
                with patch.dict(os.environ, {
                    'ENVIRONMENT': 'production'
                }, clear=True):
                    # Mock file exists for /app/VERSION
                    mock_exists.side_effect = lambda path: path == '/app/VERSION'
                    
                    # Import version module fresh to test detection
                    import importlib
                    import version
                    importlib.reload(version)
                    
                    assert version.__version__ == '1.0.44'
                    assert version.__environment__ == 'production'
                    assert version.__detection_method__ == 'version_file'

    def test_fallback_to_hardcoded_version(self):
        """Test fallback to hardcoded version when no dynamic detection works"""
        # Clear environment variables and mock file not existing
        with patch.dict(os.environ, {}, clear=True):
            with patch('os.path.exists', return_value=False):
                # Import version module fresh to test detection
                import importlib
                import version
                importlib.reload(version)
                
                assert version.__version__ == '3.1.0'
                assert version.__environment__ == 'development'
                assert version.__detection_method__ == 'fallback_hardcoded'

    def test_get_version_info_structure(self):
        """Test that get_version_info returns expected structure"""
        import version
        
        version_info = version.get_version_info()
        
        # Check required fields
        required_fields = [
            'version', 'build_date', 'commit_hash', 
            'branch', 'environment', 'detection_method'
        ]
        
        for field in required_fields:
            assert field in version_info, f"Missing required field: {field}"
        
        # Check data types
        assert isinstance(version_info['version'], str)
        assert isinstance(version_info['build_date'], str)
        assert isinstance(version_info['commit_hash'], str)
        assert isinstance(version_info['branch'], str)
        assert isinstance(version_info['environment'], str)
        assert isinstance(version_info['detection_method'], str)

    def test_version_precedence(self):
        """Test that environment variables take precedence over version file"""
        with patch('os.path.exists', return_value=True):
            with patch('builtins.open', mock_open(read_data='1.0.99\n')):
                with patch.dict(os.environ, {
                    'BUILD_VERSION': '1.0.44',
                    'ENVIRONMENT': 'production'
                }):
                    # Import version module fresh to test detection
                    import importlib
                    import version
                    importlib.reload(version)
                    
                    # Environment variable should win over file
                    assert version.__version__ == '1.0.44'
                    assert version.__detection_method__ == 'environment_variables'

    def test_partial_environment_variables(self):
        """Test behavior with partial environment variables"""
        with patch.dict(os.environ, {
            'BUILD_VERSION': '1.0.44',
            'ENVIRONMENT': 'production'
            # Missing BUILD_DATE and GIT_COMMIT
        }):
            # Import version module fresh to test detection
            import importlib
            import version
            importlib.reload(version)
            
            assert version.__version__ == '1.0.44'
            assert version.__environment__ == 'production'
            assert version.__build_date__ == 'unknown'
            assert version.__commit_hash__ == 'unknown'
            assert version.__detection_method__ == 'environment_variables'

    def test_invalid_version_handling(self):
        """Test handling of invalid version values"""
        # Test with 'unknown' version (should fall back)
        with patch.dict(os.environ, {
            'BUILD_VERSION': 'unknown',
            'ENVIRONMENT': 'production'
        }):
            with patch('os.path.exists', return_value=False):
                # Import version module fresh to test detection
                import importlib
                import version
                importlib.reload(version)
                
                # Should fall back to hardcoded version
                assert version.__version__ == '3.1.0'
                assert version.__detection_method__ == 'fallback_hardcoded'


@pytest.mark.priority2
@pytest.mark.unit
@pytest.mark.integration
class TestVersionDetectionIntegration:
    """Test version detection integration with Flask app"""

    def test_flask_app_version_endpoint_with_environment(self):
        """Test Flask app version endpoint with environment variables"""
        with patch.dict(os.environ, {
            'BUILD_VERSION': '1.0.44',
            'BUILD_DATE': '2025-06-03T00:00:00Z', 
            'GIT_COMMIT': 'abc123456',
            'ENVIRONMENT': 'production'
        }):
            # Import Flask app fresh to test with new environment
            import importlib
            import sys
            if 'ui.app' in sys.modules:
                del sys.modules['ui.app']
            if 'version' in sys.modules:
                del sys.modules['version']
            
            sys.path.append('ui')
            from ui.app import app
            
            with app.test_client() as client:
                response = client.get('/api/version')
                
                assert response.status_code == 200
                data = response.get_json()
                
                assert data['version'] == '1.0.44'
                assert data['environment'] == 'production'
                assert data['commit_hash'] == 'abc123456'
                assert data['detection_method'] == 'environment_variables'

    def test_flask_app_version_endpoint_fallback(self):
        """Test Flask app version endpoint with fallback behavior"""
        with patch.dict(os.environ, {}, clear=True):
            with patch('os.path.exists', return_value=False):
                # Import Flask app fresh to test with clear environment
                import importlib
                import sys
                if 'ui.app' in sys.modules:
                    del sys.modules['ui.app']
                if 'version' in sys.modules:
                    del sys.modules['version']
                
                sys.path.append('ui')
                from ui.app import app
                
                with app.test_client() as client:
                    response = client.get('/api/version')
                    
                    assert response.status_code == 200
                    data = response.get_json()
                    
                    assert data['version'] == '3.1.0'
                    assert data['environment'] == 'development'
                    assert data['detection_method'] == 'fallback_hardcoded'