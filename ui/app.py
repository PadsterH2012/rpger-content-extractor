#!/usr/bin/env python3
"""
AI-Powered Extraction v3 Web UI
Modern web interface for PDF analysis and extraction
"""

import os
import sys
import json
import logging
import requests
import shutil
from pathlib import Path
from datetime import datetime
from flask import Flask, render_template, request, jsonify, send_file, flash, redirect, url_for
from werkzeug.utils import secure_filename
import tempfile

# Add parent directory to path to import extraction modules
sys.path.append(str(Path(__file__).parent.parent))

from Modules.ai_game_detector import AIGameDetector
from Modules.ai_categorizer import AICategorizer
from Modules.pdf_processor import MultiGamePDFProcessor
from Modules.multi_collection_manager import MultiGameCollectionManager
from Modules.mongodb_manager import MongoDBManager
from Modules.openrouter_models import openrouter_models
from version import __version__, __build_date__, __commit_hash__, __branch__, __environment__, get_version_info

app = Flask(__name__)
app.secret_key = 'extraction_v3_ui_secret_key_change_in_production'
app.config['MAX_CONTENT_LENGTH'] = 200 * 1024 * 1024  # 200MB max file size
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0  # Disable caching
app.config['UPLOAD_TIMEOUT'] = 300  # 5 minutes for upload timeout

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Global variables for session state
analysis_results = {}
extraction_results = {}
# Global storage for progress tracking
progress_tracking = {}

def progress_callback(session_id, stage, status, details=None):
    """Store progress updates for real-time tracking"""
    if session_id not in progress_tracking:
        progress_tracking[session_id] = {}

    progress_tracking[session_id][stage] = {
        'status': status,
        'details': details or {},
        'timestamp': datetime.now().isoformat()
    }

    logger.info(f"Progress update - Session: {session_id[:8]}, Stage: {stage}, Status: {status}")

def calculate_text_quality_metrics(sections):
    """Calculate aggregated text quality metrics from sections"""
    if not sections:
        return None

    enhanced_sections = [s for s in sections if s.get('text_quality_enhanced', False)]

    if not enhanced_sections:
        # Check if this is novel content (text enhancement disabled for memory optimization)
        is_novel = any(s.get('content_type') == 'novel' for s in sections)
        if is_novel:
            return {
                'enabled': False,
                'message': 'Text enhancement disabled for novels (memory optimization)'
            }
        else:
            return {
                'enabled': False,
                'message': 'Text quality enhancement was not enabled'
            }

    # Aggregate metrics
    total_sections = len(enhanced_sections)
    total_corrections = sum(s.get('corrections_made', 0) for s in enhanced_sections)

    # Calculate average scores
    before_scores = [s.get('text_quality_before', {}).get('score', 0) for s in enhanced_sections if s.get('text_quality_before')]
    after_scores = [s.get('text_quality_after', {}).get('score', 0) for s in enhanced_sections if s.get('text_quality_after')]

    if before_scores and after_scores:
        avg_before = sum(before_scores) / len(before_scores)
        avg_after = sum(after_scores) / len(after_scores)
        improvement = avg_after - avg_before

        # Get grade for average scores
        def get_grade(score):
            if score >= 90: return 'A'
            elif score >= 80: return 'B'
            elif score >= 70: return 'C'
            elif score >= 60: return 'D'
            else: return 'F'

        return {
            'enabled': True,
            'sections_enhanced': total_sections,
            'total_corrections': total_corrections,
            'average_before': round(avg_before, 1),
            'average_after': round(avg_after, 1),
            'improvement': round(improvement, 1),
            'grade_before': get_grade(avg_before),
            'grade_after': get_grade(avg_after),
            'aggressive_mode': enhanced_sections[0].get('cleanup_aggressive', False)
        }

    return {
        'enabled': True,
        'sections_enhanced': total_sections,
        'total_corrections': total_corrections,
        'message': 'Quality metrics calculated but scores unavailable'
    }

# Allowed file extensions
ALLOWED_EXTENSIONS = {'pdf'}

def allowed_file(filename):
    """Check if file extension is allowed"""
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/')
def index():
    """Main dashboard page"""
    version_info = get_version_info()
    return render_template('index.html', version_info=version_info)

@app.route('/api/version')
def get_version():
    """Get application version information"""
    return jsonify(get_version_info())

@app.route('/api/providers/available')
def get_available_providers():
    """Get list of AI providers that have API keys configured"""
    try:
        available_providers = []

        # Check each provider for API key availability
        if os.getenv('OPENROUTER_API_KEY'):
            available_providers.append('openrouter')

        if os.getenv('ANTHROPIC_API_KEY'):
            available_providers.append('anthropic')

        if os.getenv('OPENAI_API_KEY'):
            available_providers.append('openai')

        if os.getenv('LOCAL_LLM_URL'):
            available_providers.append('local')

        # Always include mock for testing
        available_providers.append('mock')

        return jsonify({
            'success': True,
            'available_providers': available_providers,
            'total_providers': len(available_providers)
        })

    except Exception as e:
        logger.error(f"Error checking available providers: {e}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/api/openrouter/models', methods=['GET'])
def get_openrouter_models():
    """Get available OpenRouter models for dropdown selection"""
    try:
        force_refresh = request.args.get('refresh', 'false').lower() == 'true'
        group_by_provider = request.args.get('group', 'true').lower() == 'true'

        # Initialize session tracking for UI API calls
        ui_session_id = "ui_session_" + str(hash("openrouter_models"))
        from Modules.token_usage_tracker import get_tracker
        tracker = get_tracker()

        # Check if UI session already exists
        existing_session = tracker.get_session_usage(ui_session_id)
        if not existing_session:
            tracker.start_session(ui_session_id)
            logger.info(f"🔧 UI session tracking started: {ui_session_id}")

        # Set session tracking for OpenRouter models (if it supports it)
        if hasattr(openrouter_models, 'set_session_tracking'):
            openrouter_models.set_session_tracking(ui_session_id)

        # Get models from OpenRouter
        if group_by_provider:
            models = openrouter_models.get_dropdown_options(group_by_provider=True)
        else:
            models = openrouter_models.get_dropdown_options(group_by_provider=False)

        # Get recommended models for character identification
        recommended = openrouter_models.get_recommended_models("character_identification")
        recommended_ids = [model["id"] for model in recommended]

        return jsonify({
            'success': True,
            'models': models,
            'recommended': recommended_ids,
            'total_models': len([m for m in models if m.get('type') == 'option']),
            'cache_info': {
                'cached': openrouter_models._is_cache_valid(),
                'cache_age': (datetime.now() - openrouter_models._cache_timestamp).total_seconds() if openrouter_models._cache_timestamp else None
            }
        })

    except Exception as e:
        logger.error(f"Error fetching OpenRouter models: {e}")

        # Return fallback models
        fallback_models = [
            {
                "type": "header",
                "label": "Anthropic",
                "value": "header_anthropic"
            },
            {
                "type": "option",
                "value": "anthropic/claude-3.5-sonnet",
                "label": "Claude 3.5 Sonnet (anthropic)",
                "description": "Anthropic's most capable model",
                "provider": "anthropic"
            },
            {
                "type": "header",
                "label": "OpenAI",
                "value": "header_openai"
            },
            {
                "type": "option",
                "value": "openai/gpt-4o",
                "label": "GPT-4o (openai)",
                "description": "OpenAI's flagship multimodal model",
                "provider": "openai"
            },
            {
                "type": "option",
                "value": "openai/gpt-4o-mini",
                "label": "GPT-4o Mini (openai)",
                "description": "Faster, cheaper GPT-4o",
                "provider": "openai"
            }
        ]

        return jsonify({
            'success': False,
            'error': str(e),
            'models': fallback_models,
            'recommended': ["anthropic/claude-3.5-sonnet", "openai/gpt-4o"],
            'fallback': True
        })

@app.route('/upload', methods=['POST'])
def upload_file():
    """Handle PDF file upload with improved timeout handling"""
    try:
        logger.info("📤 Upload request received")

        if 'file' not in request.files:
            logger.error("No file in request")
            return jsonify({'error': 'No file selected'}), 400

        file = request.files['file']
        if file.filename == '':
            logger.error("Empty filename")
            return jsonify({'error': 'No file selected'}), 400

        if not allowed_file(file.filename):
            logger.error(f"Invalid file type: {file.filename}")
            return jsonify({'error': 'Only PDF files are allowed'}), 400

        # Check file size before saving
        file.seek(0, os.SEEK_END)
        file_size = file.tell()
        file.seek(0)  # Reset to beginning

        if file_size > app.config['MAX_CONTENT_LENGTH']:
            logger.error(f"File too large: {file_size} bytes")
            return jsonify({'error': f'File too large. Maximum size is {app.config["MAX_CONTENT_LENGTH"] // (1024*1024)}MB'}), 400

        # Save uploaded file temporarily with better error handling
        filename = secure_filename(file.filename)
        temp_dir = tempfile.mkdtemp()
        filepath = os.path.join(temp_dir, filename)

        logger.info(f"💾 Saving file: {filename} ({file_size} bytes)")
        file.save(filepath)

        # Verify file was saved correctly
        if not os.path.exists(filepath):
            logger.error("File save failed")
            return jsonify({'error': 'Failed to save uploaded file'}), 500

        actual_size = os.path.getsize(filepath)
        if actual_size != file_size:
            logger.error(f"File size mismatch: expected {file_size}, got {actual_size}")
            return jsonify({'error': 'File upload corrupted'}), 500

        logger.info(f"✅ Upload successful: {filename}")
        return jsonify({
            'success': True,
            'filename': filename,
            'filepath': filepath,
            'size': actual_size
        })

    except Exception as e:
        logger.error(f"Upload error: {e}")
        import traceback
        logger.error(f"Full traceback: {traceback.format_exc()}")
        return jsonify({'error': f'Upload failed: {str(e)}'}), 500

@app.route('/analyze', methods=['POST'])
def analyze_pdf():
    """Analyze PDF content using AI with confidence testing"""
    try:
        data = request.get_json()
        filepath = data.get('filepath')
        ai_provider = data.get('ai_provider', 'mock')
        ai_model = data.get('ai_model')  # For OpenRouter model selection
        content_type = data.get('content_type', 'source_material')
        run_confidence_test = data.get('run_confidence_test', False)  # Disable by default for speed

        if not filepath or not os.path.exists(filepath):
            return jsonify({'error': 'File not found'}), 400

        # Run confidence test first if requested
        confidence_results = None
        if run_confidence_test:
            try:
                sys.path.append(str(Path(__file__).parent.parent / 'archive'))
                from confidence_tester import run_quick_test

                logger.info("Running confidence test...")
                confidence_results = run_quick_test(filepath, pages_to_test=3)
                logger.info(f"Confidence test complete: {confidence_results['quick_confidence']:.1f}%")
            except Exception as e:
                logger.warning(f"Confidence test failed: {e}")
                confidence_results = {
                    'quick_confidence': 75.0,  # Default assumption
                    'recommended_method': 'text',
                    'text_confidence': 75.0,
                    'layout_confidence': 75.0,
                    'issues': [f'Confidence test unavailable: {str(e)}']
                }

        # Initialize AI detector with enhanced analysis
        ai_config = {
            'provider': ai_provider,
            'debug': True,
            'analysis_pages': 25,  # Analyze more pages for better book identification
            'max_tokens': 4000     # Stay within Claude's limits (4096 max)
        }

        # Add model selection for OpenRouter
        if ai_model and ai_provider == 'openrouter':
            ai_config['model'] = ai_model
            logger.info(f"🔧 Analysis using OpenRouter model: {ai_model}")
        elif ai_provider == 'openrouter':
            logger.warning(f"🔧 OpenRouter selected but no model provided!")

        # Initialize session tracking for analysis phase
        session_id = str(hash(filepath))
        from Modules.token_usage_tracker import get_tracker
        tracker = get_tracker()
        tracker.start_session(session_id)
        logger.info(f"🔧 Analysis session tracking started: {session_id}")

        detector = AIGameDetector(ai_config)

        # CRITICAL: Set session tracking IMMEDIATELY after detector creation
        if hasattr(detector, 'set_session_tracking'):
            detector.set_session_tracking(session_id)
            logger.info(f"🔧 Analysis game detector session set: {session_id}")

        # Analyze the PDF
        logger.info(f"Analyzing PDF: {filepath} with provider: {ai_provider}")

        # Extract content for analysis (to store for copy functionality)
        extracted_content = detector.extract_analysis_content(Path(filepath))

        # Perform AI analysis (this should now be tracked)
        game_metadata = detector.analyze_game_metadata(Path(filepath))

        # Add content type to game metadata
        game_metadata['content_type'] = content_type

        # Extract ISBN during analysis phase for display in UI
        try:
            import fitz
            doc = fitz.open(filepath)

            # Use the same ISBN extraction logic as the PDF processor
            from Modules.pdf_processor import MultiGamePDFProcessor
            temp_processor = MultiGamePDFProcessor(debug=True)
            isbn_data = temp_processor._extract_isbn(doc, Path(filepath))

            # Add ISBN data to game metadata for UI display
            if isbn_data.get('isbn'):
                game_metadata['isbn'] = isbn_data['isbn']
            if isbn_data.get('isbn_10'):
                game_metadata['isbn_10'] = isbn_data['isbn_10']
            if isbn_data.get('isbn_13'):
                game_metadata['isbn_13'] = isbn_data['isbn_13']
            if isbn_data.get('source'):
                game_metadata['isbn_source'] = isbn_data['source']

            doc.close()

        except Exception as e:
            logger.warning(f"Failed to extract ISBN during analysis: {e}")
            # Continue without ISBN - not critical for analysis

        # Add confidence information to game metadata
        if confidence_results:
            game_metadata['extraction_confidence'] = confidence_results['quick_confidence']
            game_metadata['recommended_method'] = confidence_results['recommended_method']
            game_metadata['confidence_issues'] = confidence_results.get('issues', [])

        # Store results for later use (session_id already created above)
        analysis_results[session_id] = {
            'filepath': filepath,
            'filename': os.path.basename(filepath),
            'game_metadata': game_metadata,
            'ai_provider': ai_provider,
            'ai_model': ai_model,  # Store the model for extraction phase
            'content_type': content_type,
            'analysis_time': datetime.now().isoformat(),
            'extracted_text': extracted_content.get('combined_text', ''),  # Store extracted text for copy functionality
            'confidence_results': confidence_results
        }

        # Calculate estimated token usage (rough estimate)
        estimated_tokens = 0
        if extracted_content.get('combined_text'):
            # Rough estimate: 1 token per 4 characters
            estimated_tokens = len(extracted_content['combined_text']) // 4

        return jsonify({
            'success': True,
            'session_id': session_id,
            'analysis': game_metadata,
            'confidence': confidence_results,
            'tokens_used': estimated_tokens,
            'provider_used': ai_provider
        })

    except Exception as e:
        logger.error(f"Analysis error: {e}")
        return jsonify({'error': str(e)}), 500


@app.route('/get_extracted_text/<session_id>', methods=['GET'])
def get_extracted_text(session_id):
    """Get the extracted text content for a session"""
    try:
        if session_id not in analysis_results:
            return jsonify({'error': 'Session not found'}), 404

        extracted_text = analysis_results[session_id].get('extracted_text', '')
        if not extracted_text:
            return jsonify({'error': 'No extracted text available'}), 404

        return jsonify({
            'success': True,
            'extracted_text': extracted_text,
            'filename': analysis_results[session_id].get('filename', 'unknown.pdf')
        })

    except Exception as e:
        logger.error(f"Error retrieving extracted text: {e}")
        return jsonify({'error': str(e)}), 500

@app.route('/progress/<session_id>', methods=['GET'])
def get_progress(session_id):
    """Get real-time progress updates for a session"""
    try:
        logger.info(f"🔧 Progress request for session: {session_id}")
        logger.info(f"🔧 Available sessions: {list(progress_tracking.keys())}")

        if session_id not in progress_tracking:
            logger.warning(f"🔧 Session {session_id} not found in progress tracking")
            return jsonify({'error': 'Session not found', 'available_sessions': list(progress_tracking.keys())}), 404

        progress_data = progress_tracking[session_id]
        logger.info(f"🔧 Returning progress data: {progress_data}")

        return jsonify({
            'success': True,
            'progress': progress_data,
            'session_id': session_id
        })

    except Exception as e:
        logger.error(f"Error retrieving progress: {e}")
        return jsonify({'error': str(e)}), 500

@app.route('/extract', methods=['POST'])
def extract_pdf():
    """Extract content from analyzed PDF"""
    try:
        data = request.get_json()
        session_id = data.get('session_id')

        if session_id not in analysis_results:
            return jsonify({'error': 'Analysis session not found'}), 400

        analysis = analysis_results[session_id]
        filepath = analysis['filepath']
        game_metadata = analysis['game_metadata']

        # Text enhancement disabled - will be handled post-extraction in MongoDB
        enable_text_enhancement = data.get('enable_text_enhancement', False)
        aggressive_cleanup = data.get('aggressive_cleanup', False)

        # Initialize PDF processor with progress callback
        ai_config = {
            'provider': analysis['ai_provider'],
            'debug': True,
            'enable_text_enhancement': enable_text_enhancement,
            'aggressive_cleanup': aggressive_cleanup
        }

        # DEBUG: Log the analysis data
        logger.info(f"🔧 EXTRACTION DEBUG - Analysis data:")
        logger.info(f"   ai_provider: {analysis.get('ai_provider')}")
        logger.info(f"   ai_model: {analysis.get('ai_model')}")
        logger.info(f"   analysis keys: {list(analysis.keys())}")

        # CRITICAL: Pass the model and API configuration from analysis to extraction
        if 'ai_model' in analysis:
            ai_config['model'] = analysis['ai_model']
            logger.info(f"🔧 Using model from analysis: {analysis['ai_model']}")
        elif analysis['ai_provider'] == 'openrouter':
            logger.warning(f"🔧 No model found for OpenRouter in analysis session!")

        # Pass API key for OpenRouter
        if analysis['ai_provider'] == 'openrouter':
            import os
            api_key = os.getenv('OPENROUTER_API_KEY')
            if api_key:
                ai_config['api_key'] = api_key
                logger.info(f"🔧 OpenRouter API key configured for extraction")
            else:
                logger.warning(f"🔧 OpenRouter API key not found - extraction will use mock client")

        # DEBUG: Log the final AI config
        logger.info(f"🔧 EXTRACTION DEBUG - Final AI config:")
        logger.info(f"   provider: {ai_config.get('provider')}")
        logger.info(f"   model: {ai_config.get('model')}")
        logger.info(f"   api_key: {'***SET***' if ai_config.get('api_key') else 'NOT SET'}")
        logger.info(f"   config keys: {list(ai_config.keys())}")

        processor = MultiGamePDFProcessor(debug=True, ai_config=ai_config)

        # Set up progress tracking for this session
        progress_tracking[session_id] = {}
        logger.info(f"🔧 Progress tracking initialized for session: {session_id}")

        # Set up token tracking for the session (continue existing session if it exists)
        from Modules.token_usage_tracker import get_tracker
        tracker = get_tracker()

        # Check if session already exists (from analysis phase)
        existing_session = tracker.get_session_usage(session_id)
        if existing_session:
            logger.info(f"🔧 Continuing existing token tracking session: {session_id}")
        else:
            tracker.start_session(session_id)
            logger.info(f"🔧 Token tracking started for session: {session_id}")

        # Set session tracking for the processor
        processor.set_session_tracking(session_id)
        logger.info(f"🔧 Processor session tracking set for: {session_id}")

        # Create a progress callback function for this session
        def session_progress_callback(stage, status, details=None):
            logger.info(f"🔧 Progress callback: {session_id[:8]} - {stage} - {status}")
            progress_callback(session_id, stage, status, details)

        # Override the processor's progress callback to use our session tracking
        processor._character_progress_callback = session_progress_callback
        logger.info(f"🔧 Progress callback attached to processor")

        # Get content type
        content_type = analysis.get('content_type') or game_metadata.get('content_type', 'source_material')

        # Extract content
        logger.info(f"Extracting content from: {filepath} (Content Type: {content_type})")
        extraction_result = processor.extract_pdf(Path(filepath), content_type=content_type)

        # Get sections and summary from result
        sections = extraction_result['sections']
        summary = extraction_result['extraction_summary']

        # Calculate text quality metrics from sections
        text_quality_metrics = calculate_text_quality_metrics(sections)

        # Get token usage summary for this session
        token_summary = tracker.get_session_summary(session_id)
        active_sessions = tracker.list_active_sessions()
        logger.info(f"🔍 Looking for tokens in session: {session_id[:8]} (full: {session_id})")
        logger.info(f"🔍 Active sessions in tracker: {[s[:8] for s in active_sessions]}")

        # Also check for UI session data and combine it
        ui_session_id = "ui_session_" + str(hash("openrouter_models"))
        ui_token_summary = tracker.get_session_summary(ui_session_id)
        if ui_token_summary['found']:
            logger.info(f"🔍 Found UI session data: {ui_token_summary['total_api_calls']} calls")
            # Combine UI session data with extraction session data
            token_summary['total_api_calls'] += ui_token_summary['total_api_calls']
            token_summary['total_tokens'] += ui_token_summary['total_tokens']
            token_summary['total_cost'] += ui_token_summary['total_cost']
            token_summary['api_calls'].extend(ui_token_summary['api_calls'])

        # If no tokens tracked in this session, check if there's a different session ID format
        if token_summary['total_tokens'] == 0:
            # Try alternative session ID formats (the token tracker might be using truncated IDs)
            alt_session_ids = [
                session_id[:8],            # Truncated session ID (most likely)
                str(abs(hash(filepath))),  # Absolute hash
                str(hash(filepath)),       # Original hash
                session_id.split('-')[0] if '-' in session_id else session_id  # First part if hyphenated
            ]

            for alt_id in alt_session_ids:
                if alt_id != session_id:  # Don't try the same ID again
                    logger.info(f"🔍 Trying alternative session ID: {alt_id}")
                    alt_token_summary = tracker.get_session_summary(alt_id)
                    logger.info(f"🔍 Alternative session {alt_id} has {alt_token_summary['total_tokens']} tokens")
                    if alt_token_summary['total_tokens'] > 0:
                        token_summary = alt_token_summary
                        logger.info(f"📊 Found tokens in alternative session ID: {alt_id} (original: {session_id[:8]})")
                        break

        logger.info(f"📊 Session {session_id[:8]} token summary: {token_summary['total_api_calls']} calls, {token_summary['total_tokens']} tokens, ${token_summary['total_cost']:.4f}")

        # Store extraction results
        extraction_results[session_id] = {
            'sections': sections,
            'summary': summary,
            'game_metadata': game_metadata,
            'text_quality_metrics': text_quality_metrics,
            'extraction_time': datetime.now().isoformat(),
            'token_usage': token_summary
        }

        # Prepare response data
        response_data = {
            'success': True,
            'summary': summary,
            'sections_count': len(sections),
            'text_quality_metrics': text_quality_metrics,
            'ready_for_import': True,
            'token_usage': {
                'total_tokens': token_summary['total_tokens'],
                'total_cost': token_summary['total_cost'],
                'total_api_calls': token_summary['total_api_calls'],
                'api_calls': token_summary['api_calls']
            }
        }

        # Add character identification results for novels
        if game_metadata.get('content_type') == 'novel' and 'character_identification' in game_metadata:
            character_data = game_metadata['character_identification']
            response_data['character_identification'] = {
                'total_characters': character_data.get('total_characters', 0),
                'characters': character_data.get('characters', []),
                'processing_stages': character_data.get('processing_stages', {})
            }

        return jsonify(response_data)

    except Exception as e:
        logger.error(f"Extraction error: {e}")

        # Check if this is an ISBN duplicate error
        error_str = str(e)
        if error_str.startswith("ISBN_DUPLICATE:"):
            # Extract the duplicate information from the error message
            duplicate_info = error_str.replace("ISBN_DUPLICATE: ", "")
            return jsonify({
                'error': 'ISBN_DUPLICATE',
                'error_type': 'isbn_duplicate',
                'message': duplicate_info,
                'title': 'Novel Already Processed',
                'details': 'This novel has already been processed. Each novel can only be extracted once to prevent duplicate patterns in the database.'
            }), 409  # 409 Conflict status code
        else:
            return jsonify({'error': str(e)}), 500

@app.route('/import_chroma', methods=['POST'])
def import_to_chroma():
    """Import extracted content to ChromaDB"""
    try:
        data = request.get_json()
        session_id = data.get('session_id')
        # Get any metadata overrides from the UI
        metadata_overrides = data.get('metadata_overrides', {})

        if session_id not in extraction_results:
            return jsonify({'error': 'Extraction session not found'}), 400

        extraction = extraction_results[session_id]
        sections = extraction['sections']
        game_metadata = extraction['game_metadata'].copy()

        # Apply any metadata overrides
        game_metadata.update(metadata_overrides)

        # Initialize collection manager
        manager = MultiGameCollectionManager()

        # Create hierarchical collection path: {content_type}.{game_type}.{edition}.{book_type}.{collection_name}
        content_type = game_metadata.get('content_type', 'source_material') or 'source_material'

        # Safe string handling with None checks
        game_type = game_metadata.get('game_type') or 'unknown'
        game_type = str(game_type).lower().replace(' ', '_').replace('&', 'and')

        edition = game_metadata.get('edition') or 'unknown'
        edition = str(edition).lower().replace(' ', '_').replace('&', 'and')

        book_type = game_metadata.get('book_type') or 'unknown'
        book_type = str(book_type).lower().replace(' ', '_').replace('&', 'and')

        collection_base = game_metadata.get('collection_name') or 'unknown'

        collection_name = f"{content_type}.{game_type}.{edition}.{book_type}.{collection_base}"
        logger.info(f"Importing to ChromaDB collection: {collection_name}")

        # Convert sections to ChromaDB format
        documents = []
        metadatas = []
        ids = []

        for i, section in enumerate(sections):
            doc_id = f"{collection_name}_page_{section['page']}_{i}"
            documents.append(section['content'])
            metadatas.append({
                'title': section['title'],
                'page': section['page'],
                'category': section['category'],
                'content_type': game_metadata.get('content_type', 'source_material'),
                'game_type': game_metadata['game_type'],
                'edition': game_metadata['edition'],
                'book': game_metadata.get('book_type', 'Unknown'),
                'source': f"{game_metadata['game_type']} {game_metadata['edition']} Edition",
                'collection_name': collection_name
            })
            ids.append(doc_id)

        # Add to collection (use import method)
        success = manager.add_documents_to_collection(collection_name, documents, metadatas, ids)

        return jsonify({
            'success': True,
            'collection_name': collection_name,
            'documents_imported': len(documents),
            'message': f'Successfully imported {len(documents)} documents to ChromaDB'
        })

    except Exception as e:
        logger.error(f"ChromaDB import error: {e}")
        return jsonify({'error': str(e)}), 500

@app.route('/import_mongodb', methods=['POST'])
def import_to_mongodb():
    """Import extracted content to MongoDB"""
    try:
        data = request.get_json()
        session_id = data.get('session_id')
        split_sections = data.get('split_sections', False)  # New parameter
        # Get any metadata overrides from the UI
        metadata_overrides = data.get('metadata_overrides', {})

        if session_id not in extraction_results:
            return jsonify({'error': 'Extraction session not found'}), 400

        extraction = extraction_results[session_id]
        game_metadata = extraction['game_metadata'].copy()

        # Apply any metadata overrides
        game_metadata.update(metadata_overrides)

        # Debug: Log metadata values to identify None issues
        logger.info(f"🔧 MongoDB import metadata debug:")
        logger.info(f"   game_type: {repr(game_metadata.get('game_type'))}")
        logger.info(f"   edition: {repr(game_metadata.get('edition'))}")
        logger.info(f"   book_type: {repr(game_metadata.get('book_type'))}")
        logger.info(f"   collection_name: {repr(game_metadata.get('collection_name'))}")
        logger.info(f"   content_type: {repr(game_metadata.get('content_type'))}")

        # Initialize MongoDB manager
        mongodb_manager = MongoDBManager()

        # Check if MongoDB is available and connected
        if not mongodb_manager.connected:
            return jsonify({
                'success': False,
                'error': 'MongoDB not connected',
                'note': 'Check MongoDB configuration in .env file'
            }), 500

        # Option 1: Hierarchical collection names (current approach)
        # Creates separate collections: source_material.dand.1st_edition.core_rules.dmg
        use_hierarchical_collections = data.get('use_hierarchical_collections', True)

        if use_hierarchical_collections:
            # Create hierarchical collection path: rpger.source_material.{game_type}.{edition}.{book_type}.{collection_name}
            content_type = game_metadata.get('content_type', 'source_material') or 'source_material'

            # Safe string handling with None checks
            game_type = game_metadata.get('game_type') or 'unknown'
            game_type = str(game_type).lower().replace(' ', '_').replace('&', 'and')

            edition = game_metadata.get('edition') or 'unknown'
            edition = str(edition).lower().replace(' ', '_').replace('&', 'and')

            book_type = game_metadata.get('book_type') or 'unknown'
            book_type = str(book_type).lower().replace(' ', '_').replace('&', 'and')

            collection_base = game_metadata.get('collection_name') or 'unknown'

            collection_name = f"{content_type}.{game_type}.{edition}.{book_type}.{collection_base}"
        else:
            # Option 2: Single collection with hierarchical documents
            # All content goes in one collection with folder-like metadata
            content_type = game_metadata.get('content_type', 'source_material')
            collection_name = content_type

            # Add hierarchical metadata to each document
            hierarchical_path = {
                "content_type": content_type,
                "game_type": game_metadata.get('game_type', 'unknown'),
                "edition": game_metadata.get('edition', 'unknown'),
                "book_type": game_metadata.get('book_type', 'unknown'),
                "collection_name": game_metadata.get('collection_name', 'unknown'),
                "full_path": f"{game_metadata.get('game_type', 'unknown')}/{game_metadata.get('edition', 'unknown')}/{game_metadata.get('book_type', 'unknown')}/{game_metadata.get('collection_name', 'unknown')}"
            }

            # Update extraction data to include hierarchical metadata
            extraction['hierarchical_path'] = hierarchical_path
        logger.info(f"Importing to MongoDB collection: {collection_name} (split_sections: {split_sections})")

        success, message = mongodb_manager.import_extracted_content(
            extraction,
            collection_name,
            split_sections=split_sections
        )

        if success:
            # Get MongoDB connection details for display
            mongodb_info = mongodb_manager.get_status()
            return jsonify({
                'success': True,
                'message': f'Successfully imported to MongoDB collection: {collection_name}',
                'collection': collection_name,
                'document_id': message.split(': ')[-1] if ': ' in message else message,
                'database_info': {
                    'host': mongodb_info.get('host', 'Unknown'),
                    'port': mongodb_info.get('port', 'Unknown'),
                    'database': mongodb_info.get('database', 'Unknown'),
                    'full_location': f"{mongodb_info.get('host', 'Unknown')}:{mongodb_info.get('port', 'Unknown')}/{mongodb_info.get('database', 'Unknown')}.{collection_name}"
                }
            })
        else:
            return jsonify({
                'success': False,
                'error': message
            }), 500

    except Exception as e:
        logger.error(f"MongoDB import error: {e}")
        return jsonify({'error': str(e)}), 500

@app.route('/download_results/<session_id>')
def download_results(session_id):
    """Download extraction results as JSON"""
    try:
        if session_id not in extraction_results:
            return jsonify({'error': 'Session not found'}), 404

        extraction = extraction_results[session_id]

        # Create temporary file with results
        temp_file = tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False)
        json.dump(extraction, temp_file, indent=2, default=str)
        temp_file.close()

        filename = f"extraction_results_{session_id[:8]}.json"

        return send_file(
            temp_file.name,
            as_attachment=True,
            download_name=filename,
            mimetype='application/json'
        )

    except Exception as e:
        logger.error(f"Download error: {e}")
        return jsonify({'error': str(e)}), 500

@app.route('/status')
def system_status():
    """Get system status and configuration"""
    try:
        # Check ChromaDB connection
        try:
            manager = MultiGameCollectionManager()
            collections = manager.collections
            chroma_status = 'Connected'
            chroma_collections = len(collections)
        except Exception as e:
            chroma_status = f'Error: {str(e)}'
            chroma_collections = 0

        # Check MongoDB connection
        try:
            mongodb_manager = MongoDBManager()
            mongodb_info = mongodb_manager.get_status()
            mongodb_status = mongodb_info['status']
            mongodb_collections = mongodb_info.get('collections', 0)
        except Exception as e:
            mongodb_status = f'Error: {str(e)}'
            mongodb_collections = 0

        # Check AI providers
        ai_providers = {
            'mock': 'Available',
            'claude': 'Available' if os.getenv('ANTHROPIC_API_KEY') else 'API key not set',
            'openai': 'Available' if os.getenv('OPENAI_API_KEY') else 'API key not set',
            'openrouter': 'Available' if os.getenv('OPENROUTER_API_KEY') else 'API key not set',
            'local': 'Available' if os.getenv('LOCAL_LLM_URL') else 'URL not set'
        }

        # Get current session token tracking if available
        session_id = request.args.get('session_id')
        from Modules.token_usage_tracker import get_tracker
        tracker = get_tracker()

        # Always check for UI session data first
        ui_session_id = "ui_session_" + str(hash("openrouter_models"))
        ui_token_summary = tracker.get_session_summary(ui_session_id)

        # Debug logging - ALWAYS print this
        active_sessions = tracker.list_active_sessions()
        print(f"🔍 STATUS DEBUG - UI session ID: {ui_session_id}")
        print(f"🔍 STATUS DEBUG - UI session found: {ui_token_summary['found']}")
        print(f"🔍 STATUS DEBUG - UI session calls: {ui_token_summary['total_api_calls']}")
        print(f"🔍 STATUS DEBUG - Active sessions: {[s[:8] for s in active_sessions]}")
        logger.info(f"🔍 Status endpoint - UI session ID: {ui_session_id}")
        logger.info(f"🔍 Status endpoint - UI session found: {ui_token_summary['found']}")
        logger.info(f"🔍 Status endpoint - UI session calls: {ui_token_summary['total_api_calls']}")
        logger.info(f"🔍 Status endpoint - Active sessions: {[s[:8] for s in active_sessions]}")

        # Initialize token summary with UI session data
        token_summary = {
            'session_id': session_id or 'ui_only',
            'found': ui_token_summary['found'],
            'total_tokens': ui_token_summary['total_tokens'],
            'total_cost': ui_token_summary['total_cost'],
            'total_api_calls': ui_token_summary['total_api_calls'],
            'api_calls': ui_token_summary['api_calls'].copy()
        }

        # If extraction session ID is provided, add its data
        if session_id:
            extraction_summary = tracker.get_session_summary(session_id)

            # If extraction session found, combine with UI session
            if extraction_summary['found']:
                token_summary['total_tokens'] += extraction_summary['total_tokens']
                token_summary['total_cost'] += extraction_summary['total_cost']
                token_summary['total_api_calls'] += extraction_summary['total_api_calls']
                token_summary['api_calls'].extend(extraction_summary['api_calls'])
                token_summary['found'] = True

            # If no extraction tokens found, try alternative session ID formats
            elif extraction_summary['total_tokens'] == 0:
                alt_session_ids = [
                    str(abs(hash(session_id))),  # Absolute hash
                    str(hash(session_id)),       # Original hash
                    session_id[:8],              # Truncated session ID
                    session_id.split('-')[0] if '-' in session_id else session_id  # First part if hyphenated
                ]

                for alt_id in alt_session_ids:
                    if alt_id != session_id:  # Don't try the same ID again
                        alt_token_summary = tracker.get_session_summary(alt_id)
                        if alt_token_summary['total_tokens'] > 0:
                            token_summary['total_tokens'] += alt_token_summary['total_tokens']
                            token_summary['total_cost'] += alt_token_summary['total_cost']
                            token_summary['total_api_calls'] += alt_token_summary['total_api_calls']
                            token_summary['api_calls'].extend(alt_token_summary['api_calls'])
                            token_summary['found'] = True
                            break

        token_info = {
            'session_id': session_id or 'ui_session',
            'total_tokens': token_summary['total_tokens'],
            'total_cost': token_summary['total_cost'],
            'total_api_calls': token_summary['total_api_calls']
        }

        return jsonify({
            'chroma_status': chroma_status,
            'chroma_collections': chroma_collections,
            'mongodb_status': mongodb_status,
            'mongodb_collections': mongodb_collections,
            'ai_providers': ai_providers,
            'active_sessions': len(analysis_results),
            'completed_extractions': len(extraction_results),
            'token_tracking': token_info,
            'version': get_version_info()
        })

    except Exception as e:
        logger.error(f"Status error: {e}")
        return jsonify({'error': str(e)}), 500

@app.route('/browse_chromadb')
def browse_chromadb():
    """Browse ChromaDB collections and documents"""
    try:
        manager = MultiGameCollectionManager()
        collections = manager.collections

        # Get collection details
        collection_details = []
        for collection_name in collections:
            info = manager.get_collection_info(collection_name)
            if info:
                collection_details.append({
                    'name': collection_name,
                    'document_count': info.get('document_count', 0),
                    'game_type': manager.parse_collection_name(collection_name).get('game_type', 'Unknown')
                })

        return jsonify({
            'success': True,
            'collections': collection_details,
            'total_collections': len(collection_details)
        })

    except Exception as e:
        logger.error(f"ChromaDB browse error: {e}")
        return jsonify({'error': str(e)}), 500

@app.route('/browse_chromadb/<collection_name>')
def browse_chromadb_collection(collection_name):
    """Browse specific ChromaDB collection documents"""
    try:
        limit = int(request.args.get('limit', 10))
        offset = int(request.args.get('offset', 0))

        manager = MultiGameCollectionManager()

        # Get collection documents
        collection_uuid = manager._get_collection_uuid(collection_name)
        if not collection_uuid:
            return jsonify({'error': f'Collection {collection_name} not found'}), 404

        # Get documents from ChromaDB
        get_url = f"{manager.base_url}/collections/{collection_uuid}/get"
        params = {
            "limit": limit,
            "offset": offset
        }

        response = requests.post(get_url, json=params)
        if response.status_code != 200:
            return jsonify({'error': 'Failed to fetch documents'}), 500

        data = response.json()
        documents = data.get("documents", [])
        metadatas = data.get("metadatas", [])
        ids = data.get("ids", [])

        # Format documents for display
        formatted_docs = []
        for i, doc in enumerate(documents):
            formatted_docs.append({
                'id': ids[i] if i < len(ids) else f'doc_{i}',
                'content': doc[:200] + '...' if len(doc) > 200 else doc,  # Truncate for display
                'full_content': doc,
                'metadata': metadatas[i] if i < len(metadatas) else {},
                'word_count': len(doc.split()) if doc else 0
            })

        return jsonify({
            'success': True,
            'collection': collection_name,
            'documents': formatted_docs,
            'total_shown': len(formatted_docs),
            'offset': offset,
            'limit': limit
        })

    except Exception as e:
        logger.error(f"ChromaDB collection browse error: {e}")
        return jsonify({'error': str(e)}), 500

@app.route('/browse_mongodb')
def browse_mongodb():
    """Browse MongoDB collections and documents"""
    try:
        mongodb_manager = MongoDBManager()

        if not mongodb_manager.connected:
            return jsonify({'error': 'MongoDB not connected'}), 500

        # Get collection names
        collection_names = mongodb_manager.database.list_collection_names()

        # Get collection details
        collection_details = []
        for collection_name in collection_names:
            try:
                collection = mongodb_manager.database[collection_name]
                doc_count = collection.count_documents({})

                # Get sample document to show structure
                sample_doc = collection.find_one()
                sample_fields = list(sample_doc.keys()) if sample_doc else []

                collection_details.append({
                    'name': collection_name,
                    'document_count': doc_count,
                    'sample_fields': sample_fields[:10]  # First 10 fields
                })
            except Exception as e:
                logger.warning(f"Error getting info for collection {collection_name}: {e}")

        return jsonify({
            'success': True,
            'collections': collection_details,
            'total_collections': len(collection_details),
            'database_info': mongodb_manager.get_status()
        })

    except Exception as e:
        logger.error(f"MongoDB browse error: {e}")
        return jsonify({'error': str(e)}), 500

@app.route('/browse_mongodb/<path:collection_name>')
def browse_mongodb_collection(collection_name):
    """Browse specific MongoDB collection documents"""
    try:
        # URL decode the collection name to handle special characters
        from urllib.parse import unquote
        decoded_collection_name = unquote(collection_name)

        logger.info(f"Browsing MongoDB collection: {decoded_collection_name} (original: {collection_name})")

        limit = int(request.args.get('limit', 10))
        skip = int(request.args.get('skip', 0))

        mongodb_manager = MongoDBManager()

        if not mongodb_manager.connected:
            return jsonify({'error': 'MongoDB not connected'}), 500

        collection = mongodb_manager.database[decoded_collection_name]

        # Get documents
        cursor = collection.find().skip(skip).limit(limit)
        documents = []

        for doc in cursor:
            # Convert ObjectId to string for JSON serialization
            if '_id' in doc:
                doc['_id'] = str(doc['_id'])

            # Handle different content field names and structures
            content_text = ""

            # Check for various content fields
            if 'content' in doc:
                content_text = str(doc['content'])
            elif 'sections' in doc and isinstance(doc['sections'], list):
                # Extract content from sections array (AI extraction format)
                section_texts = []
                for section in doc['sections'][:3]:  # First 3 sections for preview
                    if isinstance(section, dict) and 'content' in section:
                        section_texts.append(str(section['content'])[:100])
                    elif isinstance(section, str):
                        section_texts.append(section[:100])
                content_text = " | ".join(section_texts)
            elif 'description' in doc:
                content_text = str(doc['description'])
            elif 'text' in doc:
                content_text = str(doc['text'])
            else:
                # Try to find any text-like field
                for key, value in doc.items():
                    if key not in ['_id', 'import_date', 'created_at', 'metadata'] and isinstance(value, str) and len(value) > 20:
                        content_text = str(value)
                        break

            # Truncate content for display
            if content_text and len(content_text) > 200:
                doc['content_preview'] = content_text[:200] + '...'
                doc['content_full'] = content_text
                doc['content'] = doc['content_preview']
            elif content_text:
                doc['content'] = content_text
            else:
                doc['content'] = "No content available"

            documents.append(doc)

        # Get total count
        total_count = collection.count_documents({})

        return jsonify({
            'success': True,
            'collection': decoded_collection_name,
            'documents': documents,
            'total_shown': len(documents),
            'total_count': total_count,
            'skip': skip,
            'limit': limit
        })

    except Exception as e:
        logger.error(f"MongoDB collection browse error: {e}")
        return jsonify({'error': str(e)}), 500

@app.route('/query_game_edition', methods=['POST'])
def query_game_edition():
    """Query content across collections for a specific game/edition"""
    try:
        data = request.get_json()
        game_type = data.get('game_type')
        edition = data.get('edition')
        book_type = data.get('book_type')

        if not game_type:
            return jsonify({'error': 'game_type is required'}), 400

        mongodb_manager = MongoDBManager()

        if not mongodb_manager.connected:
            return jsonify({'error': 'MongoDB not connected'}), 500

        # Query across collections
        results = mongodb_manager.query_by_game_edition(game_type, edition, book_type)

        # Format results for display
        formatted_results = []
        for doc in results:
            # Convert ObjectId to string for JSON serialization
            if '_id' in doc:
                doc['_id'] = str(doc['_id'])

            # Extract content preview
            content_preview = ""
            if 'content' in doc:
                content_preview = str(doc['content'])[:200] + '...' if len(str(doc['content'])) > 200 else str(doc['content'])
            elif 'sections' in doc and isinstance(doc['sections'], list) and doc['sections']:
                # Get content from first section
                first_section = doc['sections'][0]
                if isinstance(first_section, dict) and 'content' in first_section:
                    content_preview = str(first_section['content'])[:200] + '...'

            formatted_results.append({
                'id': doc.get('_id', 'unknown'),
                'source_collection': doc.get('_source_collection', 'unknown'),
                'collection_parts': doc.get('_collection_parts', {}),
                'content_preview': content_preview,
                'sections_count': len(doc.get('sections', [])) if 'sections' in doc else 0,
                'title': doc.get('title', 'Untitled'),
                'category': doc.get('category', 'Unknown')
            })

        return jsonify({
            'success': True,
            'query': {
                'game_type': game_type,
                'edition': edition,
                'book_type': book_type
            },
            'results': formatted_results,
            'total_results': len(formatted_results),
            'collections_searched': len(set(r['source_collection'] for r in formatted_results))
        })

    except Exception as e:
        logger.error(f"Game edition query error: {e}")
        return jsonify({'error': str(e)}), 500

@app.route('/api/mongodb/collections/<path:collection_name>/deletion-info', methods=['GET'])
def get_collection_deletion_info(collection_name):
    """Get information needed for safe collection deletion"""
    try:
        # URL decode the collection name to handle special characters
        from urllib.parse import unquote
        decoded_collection_name = unquote(collection_name)

        logger.info(f"Getting deletion info for MongoDB collection: {decoded_collection_name}")

        mongodb_manager = MongoDBManager()

        if not mongodb_manager.connected:
            return jsonify({'success': False, 'error': 'MongoDB not connected'}), 500

        # Get collection metadata
        collection_info = mongodb_manager.get_collection_info(decoded_collection_name)
        if not collection_info:
            return jsonify({'success': False, 'error': 'Collection not found'}), 404

        # Check safety constraints
        safety_check = mongodb_manager.check_deletion_safety(decoded_collection_name)

        # Get recent activity (simplified - just document count for now)
        recent_activity = {
            'last_modified': 'Unknown',  # MongoDB doesn't easily track this
            'recent_changes': 0
        }

        return jsonify({
            'success': True,
            'collection_info': {
                'name': collection_info['name'],
                'document_count': collection_info['document_count'],
                'size_bytes': collection_info['size'],
                'storage_size': collection_info['storage_size'],
                'indexes': collection_info['indexes']
            },
            'safety_check': safety_check,
            'recent_activity': recent_activity,
            'estimated_backup_size': collection_info['size']
        })

    except Exception as e:
        logger.error(f"Error getting collection deletion info: {e}")
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/mongodb/collections/<path:collection_name>/delete', methods=['POST'])
def delete_mongodb_collection(collection_name):
    """Delete a MongoDB collection with safety checks"""
    try:
        # URL decode the collection name to handle special characters
        from urllib.parse import unquote
        decoded_collection_name = unquote(collection_name)

        logger.info(f"Deleting MongoDB collection: {decoded_collection_name}")

        data = request.get_json()
        confirmation_name = data.get('confirmation_name', '')
        create_backup = data.get('create_backup', True)
        admin_password = data.get('admin_password', '')

        # Validate request (compare with decoded name)
        if not confirmation_name or confirmation_name != decoded_collection_name:
            return jsonify({
                'success': False,
                'error': 'Collection name confirmation does not match'
            }), 400

        # TODO: Check admin privileges (if implemented)
        # For now, we'll skip admin password validation

        mongodb_manager = MongoDBManager()

        if not mongodb_manager.connected:
            return jsonify({'success': False, 'error': 'MongoDB not connected'}), 500

        # Safety checks
        safety_result = mongodb_manager.check_deletion_safety(collection_name)
        if not safety_result['safe_to_delete']:
            return jsonify({
                'success': False,
                'error': f'Collection deletion blocked: {safety_result["reason"]}'
            }), 400

        # Create backup if requested
        backup_path = None
        if create_backup:
            backup_result = mongodb_manager.create_collection_backup(collection_name)
            if backup_result['success']:
                backup_path = backup_result['backup_path']
                logger.info(f"Backup created: {backup_path}")
            else:
                return jsonify({
                    'success': False,
                    'error': f'Backup creation failed: {backup_result["error"]}'
                }), 500

        # Perform deletion
        deletion_result = mongodb_manager.delete_collection_safe(collection_name)

        if not deletion_result['success']:
            return jsonify({
                'success': False,
                'error': f'Deletion failed: {deletion_result["error"]}'
            }), 500

        # Log the deletion
        log_collection_deletion(collection_name, backup_path, request.remote_addr)

        return jsonify({
            'success': True,
            'message': f'Collection "{collection_name}" deleted successfully',
            'backup_created': backup_path is not None,
            'backup_path': backup_path,
            'documents_deleted': deletion_result['documents_deleted']
        })

    except Exception as e:
        logger.error(f"Error deleting collection {collection_name}: {e}")
        return jsonify({
            'success': False,
            'error': f'Deletion failed: {str(e)}'
        }), 500

def log_collection_deletion(collection_name: str, backup_path: str, user_ip: str):
    """Log collection deletion for audit purposes"""
    try:
        log_entry = {
            'action': 'collection_deletion',
            'collection_name': collection_name,
            'timestamp': datetime.now().isoformat() + 'Z',
            'backup_created': backup_path is not None,
            'backup_path': backup_path,
            'user_ip': user_ip,
            'user_agent': request.headers.get('User-Agent', '')
        }

        # Store in audit log collection
        mongodb_manager = MongoDBManager()
        if mongodb_manager.connected:
            audit_collection = mongodb_manager.database['system.audit_log']
            audit_collection.insert_one(log_entry)
            logger.info(f"Logged collection deletion: {collection_name}")
    except Exception as e:
        logger.error(f"Failed to log collection deletion: {e}")

@app.route('/get_settings', methods=['GET'])
def get_settings():
    """Get current settings from .env file"""
    try:
        env_path = Path(__file__).parent.parent / '.env'
        env_sample_path = Path(__file__).parent.parent / '.env.sample'

        # If .env doesn't exist, copy from .env.sample
        if not env_path.exists() and env_sample_path.exists():
            shutil.copy2(env_sample_path, env_path)
            logger.info("Created .env file from .env.sample")

        settings = {}

        # Read .env file if it exists
        if env_path.exists():
            with open(env_path, 'r') as f:
                for line in f:
                    line = line.strip()
                    if line and not line.startswith('#') and '=' in line:
                        key, value = line.split('=', 1)
                        # Remove quotes if present
                        value = value.strip('"\'')
                        settings[key.strip()] = value

        return jsonify({
            'success': True,
            'settings': settings
        })

    except Exception as e:
        logger.error(f"Settings load error: {e}")
        return jsonify({'error': str(e)}), 500

@app.route('/save_settings', methods=['POST'])
def save_settings():
    """Save settings to .env file"""
    try:
        data = request.get_json()
        new_settings = data.get('settings', {})

        env_path = Path(__file__).parent.parent / '.env'
        env_sample_path = Path(__file__).parent.parent / '.env.sample'

        # If .env doesn't exist, copy from .env.sample
        if not env_path.exists() and env_sample_path.exists():
            shutil.copy2(env_sample_path, env_path)
            logger.info("Created .env file from .env.sample")

        # Read existing settings
        if env_path.exists():
            with open(env_path, 'r') as f:
                lines = f.readlines()
        else:
            lines = []

        # Parse existing lines
        updated_lines = []
        updated_keys = set()

        for line in lines:
            stripped = line.strip()
            if stripped and not stripped.startswith('#') and '=' in stripped:
                key = stripped.split('=', 1)[0].strip()
                if key in new_settings:
                    # Update existing setting
                    value = new_settings[key]
                    # Add quotes if value contains spaces or special characters
                    if ' ' in value or any(char in value for char in ['$', '&', '|', ';']):
                        value = f'"{value}"'
                    updated_lines.append(f"{key}={value}\n")
                    updated_keys.add(key)
                else:
                    # Keep existing line
                    updated_lines.append(line)
            else:
                # Keep comments and empty lines
                updated_lines.append(line)

        # Add new settings that weren't in the file
        for key, value in new_settings.items():
            if key not in updated_keys and value:  # Only add non-empty values
                # Add quotes if value contains spaces or special characters
                if ' ' in value or any(char in value for char in ['$', '&', '|', ';']):
                    value = f'"{value}"'
                updated_lines.append(f"{key}={value}\n")

        # Write updated .env file
        with open(env_path, 'w') as f:
            f.writelines(updated_lines)

        logger.info("Settings saved to .env file")

        return jsonify({
            'success': True,
            'message': 'Settings saved successfully'
        })

    except Exception as e:
        logger.error(f"Settings save error: {e}")
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    import os
    port = int(os.environ.get('PORT', 5001))
    print(f"🌐 Starting UI on http://localhost:{port}")
    app.run(debug=True, host='0.0.0.0', port=port)
