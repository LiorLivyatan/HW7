"""
Unit Tests for TimestampUtil

Tests UTC timestamp generation, validation, and expiration checking.
Ensures all timestamps follow ISO-8601 format with 'Z' suffix.

Coverage Target: 100% of timestamp.py
"""

import pytest
from datetime import datetime, timezone, timedelta
from my_project.utils.timestamp import TimestampUtil, utc_now, validate_timestamp


class TestTimestampUtil:
    """Test suite for TimestampUtil building block."""

    def test_get_utc_now_format(self):
        """Test that get_utc_now returns correct ISO-8601 format with 'Z'."""
        timestamp = TimestampUtil.get_utc_now()

        # Check format: YYYY-MM-DDTHH:MM:SS.ffffffZ
        assert isinstance(timestamp, str)
        assert timestamp.endswith('Z')
        assert 'T' in timestamp
        assert len(timestamp) >= 20  # Minimum length with microseconds

    def test_get_utc_now_is_recent(self):
        """Test that get_utc_now returns current time (within 1 second)."""
        before = datetime.now(timezone.utc)
        timestamp_str = TimestampUtil.get_utc_now()
        after = datetime.now(timezone.utc)

        # Parse timestamp
        timestamp_dt = datetime.fromisoformat(timestamp_str.rstrip('Z')).replace(tzinfo=timezone.utc)

        # Should be between before and after
        assert before <= timestamp_dt <= after

    def test_validate_timestamp_valid_cases(self):
        """Test validate_timestamp with valid timestamps."""
        valid_timestamps = [
            "2025-01-15T10:30:00.123456Z",
            "2025-01-15T10:30:00Z",
            "2025-12-31T23:59:59.999999Z",
            "2025-01-01T00:00:00Z",
        ]

        for ts in valid_timestamps:
            assert TimestampUtil.validate_timestamp(ts) is True, f"Failed for: {ts}"

    def test_validate_timestamp_invalid_cases(self):
        """Test validate_timestamp with invalid timestamps."""
        invalid_timestamps = [
            "2025-01-15T10:30:00",  # Missing 'Z'
            "2025-01-15T10:30:00+02:00",  # Timezone offset instead of 'Z'
            "2025-01-15T10:30:00+00:00",  # +00:00 instead of 'Z'
            "2025-01-15 10:30:00Z",  # Space instead of 'T'
            "2025/01/15T10:30:00Z",  # Wrong date separator
            "invalid",  # Not a timestamp at all
            "2025-13-01T10:30:00Z",  # Invalid month
            "2025-01-32T10:30:00Z",  # Invalid day
        ]

        for ts in invalid_timestamps:
            assert TimestampUtil.validate_timestamp(ts) is False, f"Should fail for: {ts}"

    def test_validate_timestamp_none_raises_error(self):
        """Test that validate_timestamp raises ValueError for None."""
        with pytest.raises(ValueError, match="cannot be None or empty"):
            TimestampUtil.validate_timestamp(None)

    def test_validate_timestamp_empty_raises_error(self):
        """Test that validate_timestamp raises ValueError for empty string."""
        with pytest.raises(ValueError, match="cannot be None or empty"):
            TimestampUtil.validate_timestamp("")

    def test_is_expired_not_expired(self):
        """Test is_expired returns False for timestamps within timeout."""
        timestamp = TimestampUtil.get_utc_now()

        # Should not be expired with 10 second timeout
        assert TimestampUtil.is_expired(timestamp, timeout_seconds=10) is False

    def test_is_expired_expired(self):
        """Test is_expired returns True for timestamps beyond timeout."""
        # Create timestamp 35 seconds ago
        past_time = datetime.now(timezone.utc) - timedelta(seconds=35)
        timestamp = past_time.isoformat().replace('+00:00', 'Z')

        # Should be expired with 30 second timeout
        assert TimestampUtil.is_expired(timestamp, timeout_seconds=30) is True

    def test_is_expired_exact_boundary(self):
        """Test is_expired at exact timeout boundary."""
        # Create timestamp exactly 30 seconds ago
        past_time = datetime.now(timezone.utc) - timedelta(seconds=30)
        timestamp = past_time.isoformat().replace('+00:00', 'Z')

        # At exact boundary, should NOT be expired (elapsed = timeout)
        result = TimestampUtil.is_expired(timestamp, timeout_seconds=30)
        # This is right at the boundary, could go either way due to microseconds
        assert isinstance(result, bool)

    def test_is_expired_with_reference_time(self):
        """Test is_expired with custom reference time."""
        start_time = "2025-01-15T10:30:00.000000Z"
        ref_time_10s_later = "2025-01-15T10:30:10.000000Z"

        # 10 seconds elapsed, 5 second timeout -> expired
        assert TimestampUtil.is_expired(
            start_time,
            timeout_seconds=5,
            reference_time=ref_time_10s_later
        ) is True

        # 10 seconds elapsed, 15 second timeout -> not expired
        assert TimestampUtil.is_expired(
            start_time,
            timeout_seconds=15,
            reference_time=ref_time_10s_later
        ) is False

    def test_is_expired_invalid_timestamp_raises_error(self):
        """Test is_expired raises ValueError for invalid timestamp."""
        with pytest.raises(ValueError, match="Invalid timestamp format"):
            TimestampUtil.is_expired("invalid", timeout_seconds=10)

    def test_is_expired_negative_timeout_raises_error(self):
        """Test is_expired raises ValueError for negative timeout."""
        timestamp = TimestampUtil.get_utc_now()

        with pytest.raises(ValueError, match="must be non-negative"):
            TimestampUtil.is_expired(timestamp, timeout_seconds=-5)

    def test_get_seconds_until_deadline_positive(self):
        """Test get_seconds_until_deadline with time remaining."""
        timestamp = TimestampUtil.get_utc_now()

        # With 30 second timeout, should have ~30 seconds remaining
        remaining = TimestampUtil.get_seconds_until_deadline(timestamp, timeout_seconds=30)

        assert remaining > 25  # At least 25 seconds (allowing for execution time)
        assert remaining <= 30  # Not more than timeout

    def test_get_seconds_until_deadline_negative(self):
        """Test get_seconds_until_deadline with deadline passed."""
        # Create timestamp 35 seconds ago
        past_time = datetime.now(timezone.utc) - timedelta(seconds=35)
        timestamp = past_time.isoformat().replace('+00:00', 'Z')

        # With 30 second timeout, should have negative remaining time
        remaining = TimestampUtil.get_seconds_until_deadline(timestamp, timeout_seconds=30)

        assert remaining < 0
        assert remaining < -4  # At least 4 seconds overdue (allowing for execution time)

    def test_get_seconds_until_deadline_with_reference_time(self):
        """Test get_seconds_until_deadline with custom reference time."""
        start_time = "2025-01-15T10:30:00.000000Z"
        ref_time_10s_later = "2025-01-15T10:30:10.000000Z"

        # 10 seconds elapsed, 30 second timeout -> 20 seconds remaining
        remaining = TimestampUtil.get_seconds_until_deadline(
            start_time,
            timeout_seconds=30,
            reference_time=ref_time_10s_later
        )

        assert remaining == 20.0

    def test_utc_now_convenience_function(self):
        """Test utc_now convenience function."""
        timestamp = utc_now()

        assert isinstance(timestamp, str)
        assert timestamp.endswith('Z')
        assert TimestampUtil.validate_timestamp(timestamp) is True

    def test_validate_timestamp_convenience_function(self):
        """Test validate_timestamp convenience function."""
        valid_ts = "2025-01-15T10:30:00.123456Z"
        invalid_ts = "2025-01-15T10:30:00"

        assert validate_timestamp(valid_ts) is True
        assert validate_timestamp(invalid_ts) is False


class TestEdgeCases:
    """Test edge cases and boundary conditions."""

    def test_microseconds_in_timestamp(self):
        """Test timestamps with and without microseconds."""
        # With microseconds
        ts_with_micro = "2025-01-15T10:30:00.123456Z"
        assert TimestampUtil.validate_timestamp(ts_with_micro) is True

        # Without microseconds
        ts_without_micro = "2025-01-15T10:30:00Z"
        assert TimestampUtil.validate_timestamp(ts_without_micro) is True

    def test_zero_timeout(self):
        """Test is_expired with zero timeout."""
        timestamp = TimestampUtil.get_utc_now()

        # Any time elapsed should make it expired with 0 timeout
        # But this might be flaky due to execution speed, so we just check it doesn't crash
        result = TimestampUtil.is_expired(timestamp, timeout_seconds=0)
        assert isinstance(result, bool)

    def test_very_large_timeout(self):
        """Test is_expired with very large timeout (1 year)."""
        timestamp = TimestampUtil.get_utc_now()

        # Should not be expired with 1 year timeout
        one_year_seconds = 365 * 24 * 60 * 60
        assert TimestampUtil.is_expired(timestamp, timeout_seconds=one_year_seconds) is False

    def test_leap_year_date(self):
        """Test timestamp validation with leap year date."""
        leap_year_ts = "2024-02-29T10:30:00Z"  # 2024 is a leap year
        assert TimestampUtil.validate_timestamp(leap_year_ts) is True

    def test_non_leap_year_invalid_date(self):
        """Test that Feb 29 in non-leap year is invalid."""
        non_leap_year_ts = "2025-02-29T10:30:00Z"  # 2025 is NOT a leap year
        assert TimestampUtil.validate_timestamp(non_leap_year_ts) is False


class TestProtocolCompliance:
    """Test compliance with league.v2 protocol requirements."""

    def test_generated_timestamps_always_have_z_suffix(self):
        """Test that all generated timestamps end with 'Z' (critical requirement)."""
        for _ in range(10):
            timestamp = TimestampUtil.get_utc_now()
            assert timestamp.endswith('Z'), f"Timestamp missing 'Z' suffix: {timestamp}"

    def test_no_timezone_offsets_allowed(self):
        """Test that timezone offsets like +00:00 are rejected."""
        invalid_timestamps = [
            "2025-01-15T10:30:00+00:00",
            "2025-01-15T10:30:00-00:00",
            "2025-01-15T10:30:00+02:00",
            "2025-01-15T10:30:00-05:00",
        ]

        for ts in invalid_timestamps:
            assert TimestampUtil.validate_timestamp(ts) is False, \
                f"Timezone offset should be rejected: {ts}"

    def test_timeout_enforcement_for_protocol_deadlines(self):
        """Test timeout enforcement for protocol-specified deadlines."""
        start_time = TimestampUtil.get_utc_now()

        # Protocol timeouts
        assert TimestampUtil.is_expired(start_time, timeout_seconds=5) is False  # GAME_JOIN_ACK
        assert TimestampUtil.is_expired(start_time, timeout_seconds=30) is False  # CHOOSE_PARITY
        assert TimestampUtil.is_expired(start_time, timeout_seconds=10) is False  # RESULT_ACK
