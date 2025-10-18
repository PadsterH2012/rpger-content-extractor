"""
Tests for Token Usage Tracker functionality.

This module tests the token usage tracking capabilities including:
- Session management
- API call recording
- Usage analytics
- Cost tracking

Priority: 3 (Supporting Modules)
"""

import pytest
from unittest.mock import Mock, patch
from datetime import datetime
from Modules.token_usage_tracker import TokenUsageTracker, APICallRecord, SessionUsage, get_tracker


@pytest.mark.unit
class TestTokenUsageTrackerInitialization:
    """Test token usage tracker initialization"""

    def test_basic_initialization(self):
        """Test basic initialization"""
        tracker = TokenUsageTracker()
        
        assert hasattr(tracker, '_sessions')
        assert hasattr(tracker, '_lock')
        assert len(tracker._sessions) == 0

    def test_global_tracker(self):
        """Test global tracker access"""
        global_tracker = get_tracker()
        
        assert isinstance(global_tracker, TokenUsageTracker)
        assert hasattr(global_tracker, '_sessions')



@pytest.mark.unit
class TestSessionManagement:
    """Test session management functionality"""

    def test_start_session(self):
        """Test starting a new session"""
        tracker = TokenUsageTracker()
        session_id = "test_session_123"
        
        tracker.start_session(session_id)
        
        # Should have the session
        assert session_id in tracker._sessions
        session = tracker._sessions[session_id]
        assert isinstance(session, SessionUsage)
        assert session.session_id == session_id
        assert session.total_tokens == 0
        assert session.total_cost == 0.0
        assert session.total_api_calls == 0
        assert len(session.api_calls) == 0

    def test_multiple_sessions(self):
        """Test managing multiple sessions"""
        tracker = TokenUsageTracker()
        
        session_ids = ["session_1", "session_2", "session_3"]
        
        for session_id in session_ids:
            tracker.start_session(session_id)
        
        # Should have all sessions
        assert len(tracker._sessions) == 3
        for session_id in session_ids:
            assert session_id in tracker._sessions

    def test_duplicate_session_start(self):
        """Test starting a session that already exists"""
        tracker = TokenUsageTracker()
        session_id = "duplicate_session"
        
        # Start twice
        tracker.start_session(session_id)
        tracker.start_session(session_id)
        
        # Should only have one session
        assert len(tracker._sessions) == 1
        assert session_id in tracker._sessions

    def test_clear_session(self):
        """Test clearing a session"""
        tracker = TokenUsageTracker()
        session_id = "test_session"
        
        # Start and then clear
        tracker.start_session(session_id)
        assert session_id in tracker._sessions
        
        tracker.clear_session(session_id)
        assert session_id not in tracker._sessions

    def test_clear_nonexistent_session(self):
        """Test clearing a non-existent session"""
        tracker = TokenUsageTracker()
        
        # Should handle gracefully
        tracker.clear_session("nonexistent_session")
        # No error should occur

    def test_list_active_sessions(self):
        """Test listing active sessions"""
        tracker = TokenUsageTracker()
        
        # Initially empty
        sessions = tracker.list_active_sessions()
        assert isinstance(sessions, list)
        assert len(sessions) == 0
        
        # Add some sessions
        session_ids = ["session_a", "session_b"]
        for session_id in session_ids:
            tracker.start_session(session_id)
        
        active_sessions = tracker.list_active_sessions()
        assert len(active_sessions) == 2
        for session_id in session_ids:
            assert session_id in active_sessions



@pytest.mark.unit
class TestAPICallRecording:
    """Test API call recording functionality"""

    def test_record_api_call_basic(self):
        """Test basic API call recording"""
        tracker = TokenUsageTracker()
        session_id = "test_session"
        
        # Record an API call (should auto-create session)
        tracker.record_api_call(
            session_id=session_id,
            provider="openai",
            model="gpt-3.5-turbo",
            operation="chat_completion",
            prompt_tokens=100,
            completion_tokens=50,
            cost=0.0015
        )
        
        # Should have created session and recorded call
        assert session_id in tracker._sessions
        session = tracker._sessions[session_id]
        assert session.total_tokens == 150  # 100 + 50
        assert session.total_cost == 0.0015
        assert session.total_api_calls == 1
        assert len(session.api_calls) == 1
        
        api_call = session.api_calls[0]
        assert isinstance(api_call, APICallRecord)
        assert api_call.provider == "openai"
        assert api_call.model == "gpt-3.5-turbo"
        assert api_call.operation == "chat_completion"
        assert api_call.prompt_tokens == 100
        assert api_call.completion_tokens == 50
        assert api_call.total_tokens == 150
        assert api_call.cost == 0.0015
        assert api_call.session_id == session_id

    def test_record_multiple_api_calls(self):
        """Test recording multiple API calls"""
        tracker = TokenUsageTracker()
        session_id = "multi_call_session"
        
        # Record multiple calls
        calls = [
            {"prompt_tokens": 100, "completion_tokens": 50, "cost": 0.001},
            {"prompt_tokens": 200, "completion_tokens": 75, "cost": 0.002},
            {"prompt_tokens": 150, "completion_tokens": 25, "cost": 0.0015}
        ]
        
        for call in calls:
            tracker.record_api_call(
                session_id=session_id,
                provider="anthropic",
                model="claude-3",
                operation="completion",
                **call
            )
        
        session = tracker._sessions[session_id]
        assert session.total_tokens == 600  # Sum of all tokens
        assert abs(session.total_cost - 0.0045) < 1e-10  # Sum of all costs (with floating point tolerance)
        assert session.total_api_calls == 3
        assert len(session.api_calls) == 3

    def test_record_api_call_existing_session(self):
        """Test recording API call to existing session"""
        tracker = TokenUsageTracker()
        session_id = "existing_session"
        
        # Start session first
        tracker.start_session(session_id)
        
        # Record API call
        tracker.record_api_call(
            session_id=session_id,
            provider="mock",
            model="mock-model",
            operation="test",
            prompt_tokens=50,
            completion_tokens=25,
            cost=0.0005
        )
        
        session = tracker._sessions[session_id]
        assert session.total_tokens == 75
        assert session.total_cost == 0.0005
        assert session.total_api_calls == 1

    def test_api_call_timestamp(self):
        """Test that API calls have timestamps"""
        tracker = TokenUsageTracker()
        session_id = "timestamp_test"
        
        before_time = datetime.now()
        
        tracker.record_api_call(
            session_id=session_id,
            provider="test",
            model="test-model",
            operation="test",
            prompt_tokens=10,
            completion_tokens=5,
            cost=0.0001
        )
        
        after_time = datetime.now()
        
        session = tracker._sessions[session_id]
        api_call = session.api_calls[0]
        
        # Should have a timestamp
        assert hasattr(api_call, 'timestamp')
        assert isinstance(api_call.timestamp, str)
        
        # Parse timestamp to verify it's valid
        call_time = datetime.fromisoformat(api_call.timestamp)
        assert before_time <= call_time <= after_time



@pytest.mark.unit
class TestSessionUsageRetrieval:
    """Test session usage retrieval"""

    def test_get_session_usage_existing(self):
        """Test getting usage for existing session"""
        tracker = TokenUsageTracker()
        session_id = "existing_session"
        
        # Create session with data
        tracker.record_api_call(
            session_id=session_id,
            provider="test",
            model="test-model",
            operation="test",
            prompt_tokens=100,
            completion_tokens=50,
            cost=0.001
        )
        
        usage = tracker.get_session_usage(session_id)
        
        assert usage is not None
        assert isinstance(usage, SessionUsage)
        assert usage.session_id == session_id
        assert usage.total_tokens == 150
        assert usage.total_cost == 0.001
        assert usage.total_api_calls == 1

    def test_get_session_usage_nonexistent(self):
        """Test getting usage for non-existent session"""
        tracker = TokenUsageTracker()
        
        usage = tracker.get_session_usage("nonexistent_session")
        
        assert usage is None

    def test_get_session_summary_existing(self):
        """Test getting session summary for existing session"""
        tracker = TokenUsageTracker()
        session_id = "summary_test"
        
        # Create session with data
        tracker.record_api_call(
            session_id=session_id,
            provider="openai",
            model="gpt-4",
            operation="chat",
            prompt_tokens=200,
            completion_tokens=100,
            cost=0.005
        )
        
        summary = tracker.get_session_summary(session_id)
        
        assert isinstance(summary, dict)
        assert summary['session_id'] == session_id
        assert summary['found'] is True
        assert summary['total_tokens'] == 300
        assert summary['total_cost'] == 0.005
        assert summary['total_api_calls'] == 1
        assert 'start_time' in summary
        assert isinstance(summary['api_calls'], list)
        assert len(summary['api_calls']) == 1
        
        api_call_summary = summary['api_calls'][0]
        assert 'timestamp' in api_call_summary
        assert api_call_summary['provider'] == "openai"
        assert api_call_summary['model'] == "gpt-4"
        assert api_call_summary['tokens'] == 300
        assert api_call_summary['cost'] == 0.005

    def test_get_session_summary_nonexistent(self):
        """Test getting session summary for non-existent session"""
        tracker = TokenUsageTracker()
        
        summary = tracker.get_session_summary("nonexistent_session")
        
        assert isinstance(summary, dict)
        assert summary['session_id'] == "nonexistent_session"
        assert summary['found'] is False
        assert summary['total_tokens'] == 0
        assert summary['total_cost'] == 0.0
        assert summary['total_api_calls'] == 0
        assert summary['api_calls'] == []



@pytest.mark.unit
class TestThreadSafety:
    """Test thread safety features"""

    def test_lock_exists(self):
        """Test that threading lock exists"""
        tracker = TokenUsageTracker()
        
        assert hasattr(tracker, '_lock')
        # Lock should be usable in context manager
        with tracker._lock:
            pass  # Should not raise error

    def test_concurrent_session_operations(self):
        """Test concurrent session operations"""
        tracker = TokenUsageTracker()
        
        # Simulate concurrent operations
        session_ids = ["concurrent_1", "concurrent_2", "concurrent_3"]
        
        # Start multiple sessions
        for session_id in session_ids:
            tracker.start_session(session_id)
        
        # Record calls to multiple sessions
        for i, session_id in enumerate(session_ids):
            tracker.record_api_call(
                session_id=session_id,
                provider="test",
                model="test-model",
                operation="test",
                prompt_tokens=10 * (i + 1),
                completion_tokens=5 * (i + 1),
                cost=0.001 * (i + 1)
            )
        
        # Verify all sessions exist and have correct data
        assert len(tracker._sessions) == 3
        for i, session_id in enumerate(session_ids):
            session = tracker._sessions[session_id]
            expected_tokens = 15 * (i + 1)  # prompt + completion
            assert session.total_tokens == expected_tokens



@pytest.mark.unit
class TestErrorHandling:
    """Test error handling scenarios"""

    def test_invalid_session_id_types(self):
        """Test handling of invalid session ID types"""
        tracker = TokenUsageTracker()
        
        # Test with None (should handle gracefully)
        try:
            tracker.start_session(None)
            # If it doesn't raise, check it was handled
            assert None in tracker._sessions or len(tracker._sessions) == 0
        except (TypeError, ValueError):
            # Expected behavior for invalid input
            pass

    def test_negative_token_counts(self):
        """Test handling of negative token counts"""
        tracker = TokenUsageTracker()
        session_id = "negative_test"
        
        # Record call with negative tokens
        tracker.record_api_call(
            session_id=session_id,
            provider="test",
            model="test-model",
            operation="test",
            prompt_tokens=-10,  # Negative
            completion_tokens=5,
            cost=0.001
        )
        
        # Should handle gracefully
        if session_id in tracker._sessions:
            session = tracker._sessions[session_id]
            # Verify it recorded something (even if adjusted)
            assert isinstance(session.total_tokens, int)

    def test_zero_cost_calls(self):
        """Test handling of zero-cost API calls"""
        tracker = TokenUsageTracker()
        session_id = "zero_cost_test"
        
        tracker.record_api_call(
            session_id=session_id,
            provider="free_tier",
            model="free-model",
            operation="test",
            prompt_tokens=100,
            completion_tokens=50,
            cost=0.0  # Zero cost
        )
        
        # Should handle gracefully
        session = tracker._sessions[session_id]
        assert session.total_cost == 0.0
        assert session.total_tokens == 150



@pytest.mark.unit
class TestDataStructures:
    """Test data structure functionality"""

    def test_api_call_record_creation(self):
        """Test APICallRecord creation"""
        record = APICallRecord(
            timestamp="2024-01-01T12:00:00",
            provider="test",
            model="test-model",
            operation="test_op",
            prompt_tokens=100,
            completion_tokens=50,
            total_tokens=150,
            cost=0.002,
            session_id="test_session"
        )
        
        assert record.timestamp == "2024-01-01T12:00:00"
        assert record.provider == "test"
        assert record.model == "test-model"
        assert record.operation == "test_op"
        assert record.prompt_tokens == 100
        assert record.completion_tokens == 50
        assert record.total_tokens == 150
        assert record.cost == 0.002
        assert record.session_id == "test_session"

    def test_session_usage_creation(self):
        """Test SessionUsage creation"""
        session = SessionUsage(
            session_id="test_session",
            start_time="2024-01-01T12:00:00",
            total_tokens=0,
            total_cost=0.0,
            total_api_calls=0,
            api_calls=[]
        )
        
        assert session.session_id == "test_session"
        assert session.start_time == "2024-01-01T12:00:00"
        assert session.total_tokens == 0
        assert session.total_cost == 0.0
        assert session.total_api_calls == 0
        assert isinstance(session.api_calls, list)
        assert len(session.api_calls) == 0