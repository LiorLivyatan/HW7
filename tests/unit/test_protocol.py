"""
Unit Tests for ProtocolMessageBuilder

Tests construction of league.v2 protocol messages with exact JSON structure.
Ensures all messages include required fields and comply with protocol specs.

Coverage Target: 100% of protocol.py
"""

import pytest
from my_project.core.protocol import (
    ProtocolMessageBuilder,
    validate_parity_choice,
    normalize_parity_choice
)


class TestProtocolMessageBuilder:
    """Test suite for ProtocolMessageBuilder building block."""

    def test_initialization(self):
        """Test ProtocolMessageBuilder initialization."""
        builder = ProtocolMessageBuilder(player_id="P01")

        assert builder.player_id == "P01"
        assert builder.auth_token is None
        assert builder.PROTOCOL_VERSION == "league.v2"

    def test_initialization_empty_player_id_raises_error(self):
        """Test that empty player_id raises ValueError."""
        with pytest.raises(ValueError, match="player_id cannot be None or empty"):
            ProtocolMessageBuilder(player_id="")

        with pytest.raises(ValueError, match="player_id cannot be None or empty"):
            ProtocolMessageBuilder(player_id=None)

    def test_set_auth_token(self):
        """Test setting authentication token."""
        builder = ProtocolMessageBuilder(player_id="P01")
        builder.set_auth_token("test-token-12345")

        assert builder.auth_token == "test-token-12345"

    def test_build_league_register_request(self):
        """Test building LEAGUE_REGISTER_REQUEST message."""
        builder = ProtocolMessageBuilder(player_id="P01")

        message = builder.build_league_register_request(
            conversation_id="reg-001",
            display_name="Test Agent",
            callback_url="http://localhost:8101/mcp"
        )

        # Check required fields
        assert message["protocol"] == "league.v2"
        assert message["message_type"] == "LEAGUE_REGISTER_REQUEST"
        assert message["sender"] == "player:P01"
        assert message["conversation_id"] == "reg-001"
        assert message["player_id"] == "P01"
        assert message["display_name"] == "Test Agent"
        assert message["callback_url"] == "http://localhost:8101/mcp"

        # Check timestamp format
        assert "timestamp" in message
        assert message["timestamp"].endswith('Z')

        # Should NOT include auth_token (registration doesn't have it yet)
        assert "auth_token" not in message

    def test_build_game_join_ack(self):
        """Test building GAME_JOIN_ACK message."""
        builder = ProtocolMessageBuilder(player_id="P01")
        builder.set_auth_token("token-12345")

        message = builder.build_game_join_ack(
            conversation_id="conv-001",
            match_id="R1M1",
            accept=True
        )

        # Check required fields
        assert message["protocol"] == "league.v2"
        assert message["message_type"] == "GAME_JOIN_ACK"
        assert message["sender"] == "player:P01"
        assert message["conversation_id"] == "conv-001"
        assert message["auth_token"] == "token-12345"
        assert message["match_id"] == "R1M1"
        assert message["player_id"] == "P01"
        assert message["accept"] is True

        # Check timestamps (should have both timestamp and arrival_timestamp)
        assert "timestamp" in message
        assert "arrival_timestamp" in message
        assert message["timestamp"].endswith('Z')
        assert message["arrival_timestamp"].endswith('Z')

    def test_build_game_join_ack_without_auth_token_raises_error(self):
        """Test that build_game_join_ack raises error without auth_token."""
        builder = ProtocolMessageBuilder(player_id="P01")
        # Don't set auth_token

        with pytest.raises(ValueError, match="auth_token is required"):
            builder.build_game_join_ack(
                conversation_id="conv-001",
                match_id="R1M1",
                accept=True
            )

    def test_build_game_join_ack_reject(self):
        """Test building GAME_JOIN_ACK with accept=False."""
        builder = ProtocolMessageBuilder(player_id="P01")
        builder.set_auth_token("token-12345")

        message = builder.build_game_join_ack(
            conversation_id="conv-001",
            match_id="R1M1",
            accept=False  # Reject invitation
        )

        assert message["accept"] is False

    def test_build_choose_parity_response_even(self):
        """Test building CHOOSE_PARITY_RESPONSE with 'even'."""
        builder = ProtocolMessageBuilder(player_id="P01")
        builder.set_auth_token("token-12345")

        message = builder.build_choose_parity_response(
            conversation_id="conv-002",
            match_id="R1M1",
            parity_choice="even"
        )

        # Check required fields
        assert message["protocol"] == "league.v2"
        assert message["message_type"] == "CHOOSE_PARITY_RESPONSE"
        assert message["sender"] == "player:P01"
        assert message["conversation_id"] == "conv-002"
        assert message["auth_token"] == "token-12345"
        assert message["match_id"] == "R1M1"
        assert message["player_id"] == "P01"
        assert message["parity_choice"] == "even"  # Must be lowercase

        # Check timestamp
        assert "timestamp" in message
        assert message["timestamp"].endswith('Z')

    def test_build_choose_parity_response_odd(self):
        """Test building CHOOSE_PARITY_RESPONSE with 'odd'."""
        builder = ProtocolMessageBuilder(player_id="P01")
        builder.set_auth_token("token-12345")

        message = builder.build_choose_parity_response(
            conversation_id="conv-002",
            match_id="R1M1",
            parity_choice="odd"
        )

        assert message["parity_choice"] == "odd"

    def test_build_choose_parity_response_invalid_choice_raises_error(self):
        """Test that invalid parity choice raises ValueError."""
        builder = ProtocolMessageBuilder(player_id="P01")
        builder.set_auth_token("token-12345")

        # Capitalized (CRITICAL ERROR)
        with pytest.raises(ValueError, match="must be lowercase 'even' or 'odd'"):
            builder.build_choose_parity_response(
                conversation_id="conv-002",
                match_id="R1M1",
                parity_choice="Even"  # Capitalized!
            )

        # All caps
        with pytest.raises(ValueError, match="must be lowercase 'even' or 'odd'"):
            builder.build_choose_parity_response(
                conversation_id="conv-002",
                match_id="R1M1",
                parity_choice="EVEN"
            )

        # Invalid value
        with pytest.raises(ValueError, match="must be lowercase 'even' or 'odd'"):
            builder.build_choose_parity_response(
                conversation_id="conv-002",
                match_id="R1M1",
                parity_choice="invalid"
            )

    def test_build_choose_parity_response_without_auth_token_raises_error(self):
        """Test that build_choose_parity_response raises error without auth_token."""
        builder = ProtocolMessageBuilder(player_id="P01")

        with pytest.raises(ValueError, match="auth_token is required"):
            builder.build_choose_parity_response(
                conversation_id="conv-002",
                match_id="R1M1",
                parity_choice="even"
            )

    def test_build_result_acknowledgment(self):
        """Test building result acknowledgment message."""
        builder = ProtocolMessageBuilder(player_id="P01")
        builder.set_auth_token("token-12345")

        message = builder.build_result_acknowledgment(
            conversation_id="conv-003",
            match_id="R1M1",
            status="acknowledged"
        )

        # Check required fields
        assert message["protocol"] == "league.v2"
        assert message["message_type"] == "RESULT_ACKNOWLEDGMENT"
        assert message["sender"] == "player:P01"
        assert message["conversation_id"] == "conv-003"
        assert message["auth_token"] == "token-12345"
        assert message["match_id"] == "R1M1"
        assert message["status"] == "acknowledged"

        # Check timestamp
        assert "timestamp" in message
        assert message["timestamp"].endswith('Z')

    def test_sender_format(self):
        """Test that sender field follows 'player:<player_id>' format."""
        builder = ProtocolMessageBuilder(player_id="P99")
        builder.set_auth_token("token-12345")

        message = builder.build_game_join_ack(
            conversation_id="conv-001",
            match_id="R1M1"
        )

        assert message["sender"] == "player:P99"


class TestValidationUtilities:
    """Test validation utility functions."""

    def test_validate_parity_choice_valid(self):
        """Test validate_parity_choice with valid inputs."""
        assert validate_parity_choice("even") is True
        assert validate_parity_choice("odd") is True

    def test_validate_parity_choice_invalid(self):
        """Test validate_parity_choice with invalid inputs."""
        assert validate_parity_choice("Even") is False
        assert validate_parity_choice("ODD") is False
        assert validate_parity_choice("EVEN") is False
        assert validate_parity_choice("invalid") is False
        assert validate_parity_choice("") is False
        assert validate_parity_choice("0") is False
        assert validate_parity_choice("1") is False

    def test_normalize_parity_choice_valid(self):
        """Test normalize_parity_choice with valid inputs."""
        assert normalize_parity_choice("even") == "even"
        assert normalize_parity_choice("odd") == "odd"
        assert normalize_parity_choice("Even") == "even"
        assert normalize_parity_choice("ODD") == "odd"
        assert normalize_parity_choice("EVEN") == "even"
        assert normalize_parity_choice("Odd") == "odd"

    def test_normalize_parity_choice_invalid_raises_error(self):
        """Test normalize_parity_choice raises error for invalid inputs."""
        with pytest.raises(ValueError, match="Invalid parity choice"):
            normalize_parity_choice("invalid")

        with pytest.raises(ValueError, match="Invalid parity choice"):
            normalize_parity_choice("")

        with pytest.raises(ValueError, match="Invalid parity choice"):
            normalize_parity_choice("neither")


class TestProtocolCompliance:
    """Test compliance with league.v2 protocol requirements."""

    def test_all_messages_have_protocol_field(self):
        """Test that all messages include protocol field."""
        builder = ProtocolMessageBuilder(player_id="P01")
        builder.set_auth_token("token-12345")

        messages = [
            builder.build_league_register_request("conv-1", "Agent", "http://localhost:8101/mcp"),
            builder.build_game_join_ack("conv-2", "R1M1"),
            builder.build_choose_parity_response("conv-3", "R1M1", "even"),
            builder.build_result_acknowledgment("conv-4", "R1M1"),
        ]

        for msg in messages:
            assert "protocol" in msg
            assert msg["protocol"] == "league.v2"

    def test_all_messages_have_utc_timestamps(self):
        """Test that all messages have UTC timestamps with 'Z' suffix."""
        builder = ProtocolMessageBuilder(player_id="P01")
        builder.set_auth_token("token-12345")

        messages = [
            builder.build_league_register_request("conv-1", "Agent", "http://localhost:8101/mcp"),
            builder.build_game_join_ack("conv-2", "R1M1"),
            builder.build_choose_parity_response("conv-3", "R1M1", "even"),
            builder.build_result_acknowledgment("conv-4", "R1M1"),
        ]

        for msg in messages:
            assert "timestamp" in msg
            assert msg["timestamp"].endswith('Z')

    def test_parity_choice_must_be_lowercase(self):
        """Test critical requirement: parity_choice MUST be lowercase."""
        builder = ProtocolMessageBuilder(player_id="P01")
        builder.set_auth_token("token-12345")

        # Lowercase should work
        msg = builder.build_choose_parity_response("conv-1", "R1M1", "even")
        assert msg["parity_choice"] == "even"

        msg = builder.build_choose_parity_response("conv-2", "R1M1", "odd")
        assert msg["parity_choice"] == "odd"

        # Capitalized should fail
        with pytest.raises(ValueError):
            builder.build_choose_parity_response("conv-3", "R1M1", "Even")

        with pytest.raises(ValueError):
            builder.build_choose_parity_response("conv-4", "R1M1", "ODD")

    def test_auth_token_included_after_registration(self):
        """Test that auth_token is included in all messages after registration."""
        builder = ProtocolMessageBuilder(player_id="P01")
        builder.set_auth_token("test-token-abc")

        # Messages that require auth_token
        msg1 = builder.build_game_join_ack("conv-1", "R1M1")
        assert "auth_token" in msg1
        assert msg1["auth_token"] == "test-token-abc"

        msg2 = builder.build_choose_parity_response("conv-2", "R1M1", "even")
        assert "auth_token" in msg2
        assert msg2["auth_token"] == "test-token-abc"

        msg3 = builder.build_result_acknowledgment("conv-3", "R1M1")
        assert "auth_token" in msg3
        assert msg3["auth_token"] == "test-token-abc"

    def test_conversation_id_echoed_correctly(self):
        """Test that conversation_id is echoed from incoming messages."""
        builder = ProtocolMessageBuilder(player_id="P01")
        builder.set_auth_token("token-12345")

        unique_convs = [
            "conv-invitation-001",
            "conv-parity-002",
            "conv-result-003",
        ]

        msg1 = builder.build_game_join_ack(unique_convs[0], "R1M1")
        assert msg1["conversation_id"] == unique_convs[0]

        msg2 = builder.build_choose_parity_response(unique_convs[1], "R1M1", "even")
        assert msg2["conversation_id"] == unique_convs[1]

        msg3 = builder.build_result_acknowledgment(unique_convs[2], "R1M1")
        assert msg3["conversation_id"] == unique_convs[2]
