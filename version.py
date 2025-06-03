#!/usr/bin/env python3
"""
Extraction v3 Version Information
Provides version details for the application with dynamic detection support
"""

import datetime
import os
import subprocess
import json

def detect_version_from_environment():
    """
    Dynamically detect version information from Docker environment.
    This enables automatic version detection from CI/CD builds.
    """
    try:
        # Method 1: Read from environment variables set during Docker build
        version = os.getenv('BUILD_VERSION')
        build_date = os.getenv('BUILD_DATE')
        commit_hash = os.getenv('GIT_COMMIT')
        environment = os.getenv('ENVIRONMENT', 'development')
        
        if version and version != 'unknown':
            return {
                'version': version,
                'build_date': build_date or 'unknown',
                'commit_hash': commit_hash or 'unknown',
                'environment': environment,
                'detection_method': 'environment_variables'
            }
            
        # Method 2: Read from version file created during Docker build
        version_file = '/app/VERSION'
        if os.path.exists(version_file):
            with open(version_file, 'r') as f:
                version = f.read().strip()
                if version and version != 'unknown':
                    return {
                        'version': version,
                        'build_date': build_date or 'unknown', 
                        'commit_hash': commit_hash or 'unknown',
                        'environment': environment,
                        'detection_method': 'version_file'
                    }
                    
        # Method 3: Try to read from Docker container metadata (if running in container)
        try:
            # Get container ID from /proc/self/cgroup (works in most container environments)
            with open('/proc/self/cgroup', 'r') as f:
                cgroup_content = f.read()
                if 'docker' in cgroup_content:
                    # We're in a container, try to inspect it
                    result = subprocess.run(
                        ['docker', 'inspect', 'self'], 
                        capture_output=True, text=True, timeout=5
                    )
                    if result.returncode == 0:
                        data = json.loads(result.stdout)[0]
                        labels = data.get('Config', {}).get('Labels', {})
                        version = labels.get('version')
                        if version:
                            return {
                                'version': version,
                                'build_date': labels.get('build.date', 'unknown'),
                                'commit_hash': labels.get('git.commit', 'unknown'),
                                'environment': environment,
                                'detection_method': 'docker_labels'
                            }
        except (FileNotFoundError, subprocess.TimeoutExpired, json.JSONDecodeError, IOError):
            # Docker command not available or container inspection failed
            pass
            
    except Exception as e:
        # Log error but don't fail - fall back to hardcoded values
        print(f"Version detection error: {e}")
        
    # Return None to indicate no dynamic version was detected
    return None

# Try to detect version dynamically first
dynamic_version = detect_version_from_environment()

if dynamic_version:
    # Use dynamically detected version
    __version__ = dynamic_version['version']
    __build_date__ = dynamic_version['build_date']
    __commit_hash__ = dynamic_version['commit_hash'] 
    __environment__ = dynamic_version['environment']
    __branch__ = "main"  # Default branch
    __detection_method__ = dynamic_version['detection_method']
else:
    # Fallback to hardcoded values for local development
    __version__ = "3.1.0"
    __build_date__ = datetime.datetime.now().strftime("%Y-%m-%dT%H:%M:%SZ")
    __commit_hash__ = "unknown"
    __branch__ = "main"
    __environment__ = "development"
    __detection_method__ = "fallback_hardcoded"

# Function to get version information as a dictionary
def get_version_info():
    """Return version information as a dictionary"""
    return {
        "version": __version__,
        "build_date": __build_date__,
        "commit_hash": __commit_hash__,
        "branch": __branch__,
        "environment": __environment__,
        "detection_method": __detection_method__
    }