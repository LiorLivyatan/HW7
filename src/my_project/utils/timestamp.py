"""
Timestamp Utilities - Building Block: TimestampUtil

Purpose:
    Provides UTC timestamp generation and validation for MCP protocol compliance.
    Ensures all timestamps follow ISO-8601 format with 'Z' suffix as required by league.v2.

Input Data:
    - timestamp_str (str): Timestamp string to validate
    - timeout_seconds (int): Timeout duration for expiration checks

Output Data:
    - Formatted UTC timestamp strings in ISO-8601 format
    - Boolean validation results
    - Time difference calculations

Setup/Configuration:
    No configuration required - uses Python's datetime module

CRITICAL:
    - All timestamps MUST be in UTC timezone
    - Format MUST be ISO-8601 with 'Z' suffix: "2025-01-15T10:30:00.123456Z"
    - NEVER use local timezone or timezone offsets like "+02:00"

References:
    - CLAUDE.md: Line 1891-1913 (MCP Protocol Pitfalls - Timestamp Errors)
    - Assignment Chapter 2: General League Protocol
    - Assignment Chapter 4: JSON Message Structures
"""

from datetime import datetime, timezone
from typing import Optional
import re


class TimestampUtil:
    """
    Utility class for handling UTC timestamps in ISO-8601 format.

    This building block ensures protocol compliance by providing:
    1. Consistent UTC timestamp generation
    2. Timestamp validation against protocol requirements
    3. Expiration checking for deadline enforcement
    """

    # ISO-8601 format regex with 'Z' suffix
    ISO8601_PATTERN = re.compile(
        r'^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}(\.\d+)?Z$'
    )

    @staticmethod
    def get_utc_now() -> str:
        """
        Get current UTC timestamp in ISO-8601 format with 'Z' suffix.

        This is the ONLY correct way to generate timestamps for league.v2 protocol.

        Returns:
            str: Current UTC timestamp, e.g., "2025-01-15T10:30:00.123456Z"

        Example:
            >>> timestamp = TimestampUtil.get_utc_now()
            >>> print(timestamp)
            2025-01-15T10:30:00.123456Z

        Warning:
            NEVER use datetime.now() or datetime.now().isoformat()
            as they use local timezone which violates protocol!

        See Also:
            CLAUDE.md line 1891: Common Pitfall #1 - Timestamp Not UTC
        """
        return datetime.now(timezone.utc).isoformat().replace('+00:00', 'Z')

    @staticmethod
    def validate_timestamp(timestamp_str: str) -> bool:
        """
        Validate that timestamp string follows league.v2 protocol requirements.

        Checks:
        1. Matches ISO-8601 format with 'Z' suffix
        2. Can be parsed as a valid datetime
        3. Does not include timezone offset (only 'Z' allowed)

        Args:
            timestamp_str: Timestamp string to validate

        Returns:
            bool: True if valid, False otherwise

        Example:
            >>> TimestampUtil.validate_timestamp("2025-01-15T10:30:00.123456Z")
            True
            >>> TimestampUtil.validate_timestamp("2025-01-15T10:30:00+02:00")
            False  # Timezone offset not allowed
            >>> TimestampUtil.validate_timestamp("2025-01-15T10:30:00")
            False  # Missing 'Z' suffix

        Raises:
            ValueError: If timestamp_str is None or empty
        """
        if not timestamp_str:
            raise ValueError("Timestamp string cannot be None or empty")

        # Check format matches ISO-8601 with Z suffix
        if not TimestampUtil.ISO8601_PATTERN.match(timestamp_str):
            return False

        # Verify it's parseable as datetime
        try:
            TimestampUtil._parse_timestamp(timestamp_str)
            return True
        except (ValueError, TypeError):
            return False

    @staticmethod
    def is_expired(
        timestamp_str: str,
        timeout_seconds: int,
        reference_time: Optional[str] = None
    ) -> bool:
        """
        Check if timestamp has expired based on timeout duration.

        Used for enforcing protocol timeouts:
        - GAME_JOIN_ACK must be sent within 5 seconds
        - CHOOSE_PARITY_RESPONSE must be sent within 30 seconds
        - Result acknowledgment within 10 seconds

        Args:
            timestamp_str: The timestamp to check (start time)
            timeout_seconds: Maximum allowed duration in seconds
            reference_time: Optional reference time (default: current UTC time)

        Returns:
            bool: True if expired (exceeded timeout), False otherwise

        Example:
            >>> start = TimestampUtil.get_utc_now()
            >>> # After 35 seconds...
            >>> TimestampUtil.is_expired(start, timeout_seconds=30)
            True  # Exceeded 30-second timeout

        Raises:
            ValueError: If timestamp_str is invalid or timeout_seconds < 0

        See Also:
            config.yaml: timeouts section for protocol timeout values
        """
        if timeout_seconds < 0:
            raise ValueError(f"timeout_seconds must be non-negative, got {timeout_seconds}")

        if not TimestampUtil.validate_timestamp(timestamp_str):
            raise ValueError(f"Invalid timestamp format: {timestamp_str}")

        start_dt = TimestampUtil._parse_timestamp(timestamp_str)

        if reference_time:
            if not TimestampUtil.validate_timestamp(reference_time):
                raise ValueError(f"Invalid reference_time format: {reference_time}")
            current_dt = TimestampUtil._parse_timestamp(reference_time)
        else:
            current_dt = datetime.now(timezone.utc)

        elapsed = (current_dt - start_dt).total_seconds()
        return elapsed > timeout_seconds

    @staticmethod
    def get_seconds_until_deadline(
        start_timestamp: str,
        timeout_seconds: int,
        reference_time: Optional[str] = None
    ) -> float:
        """
        Calculate how many seconds remain until deadline.

        Useful for timeout management and fallback strategy triggers.

        Args:
            start_timestamp: When the operation started
            timeout_seconds: Maximum duration allowed
            reference_time: Optional reference time (default: current UTC time)

        Returns:
            float: Seconds remaining (negative if already expired)

        Example:
            >>> start = TimestampUtil.get_utc_now()
            >>> # After 5 seconds...
            >>> remaining = TimestampUtil.get_seconds_until_deadline(start, 30)
            >>> print(f"Remaining: {remaining:.2f}s")
            Remaining: 25.00s

        Raises:
            ValueError: If timestamps are invalid
        """
        if not TimestampUtil.validate_timestamp(start_timestamp):
            raise ValueError(f"Invalid start_timestamp: {start_timestamp}")

        start_dt = TimestampUtil._parse_timestamp(start_timestamp)

        if reference_time:
            if not TimestampUtil.validate_timestamp(reference_time):
                raise ValueError(f"Invalid reference_time: {reference_time}")
            current_dt = TimestampUtil._parse_timestamp(reference_time)
        else:
            current_dt = datetime.now(timezone.utc)

        elapsed = (current_dt - start_dt).total_seconds()
        return timeout_seconds - elapsed

    @staticmethod
    def _parse_timestamp(timestamp_str: str) -> datetime:
        """
        Internal method to parse ISO-8601 timestamp with 'Z' suffix.

        Args:
            timestamp_str: Timestamp string in ISO-8601 format

        Returns:
            datetime: Parsed datetime object with UTC timezone

        Raises:
            ValueError: If timestamp cannot be parsed
        """
        # Remove 'Z' and parse as ISO format, then attach UTC timezone
        dt_str = timestamp_str.rstrip('Z')
        dt = datetime.fromisoformat(dt_str)

        # Ensure timezone is UTC
        if dt.tzinfo is None:
            dt = dt.replace(tzinfo=timezone.utc)
        elif dt.tzinfo != timezone.utc:
            dt = dt.astimezone(timezone.utc)

        return dt


# Convenience functions for common use cases
def utc_now() -> str:
    """
    Convenience function to get current UTC timestamp.

    Returns:
        str: Current UTC timestamp in ISO-8601 format with 'Z'

    Example:
        >>> from my_project.utils.timestamp import utc_now
        >>> timestamp = utc_now()
    """
    return TimestampUtil.get_utc_now()


def validate_timestamp(timestamp_str: str) -> bool:
    """
    Convenience function to validate timestamp format.

    Args:
        timestamp_str: Timestamp to validate

    Returns:
        bool: True if valid ISO-8601 with 'Z', False otherwise
    """
    return TimestampUtil.validate_timestamp(timestamp_str)
