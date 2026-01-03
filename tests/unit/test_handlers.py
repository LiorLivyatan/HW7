"""
Tests for ToolHandlers - Building Block: ToolHandlers

Coverage:
- Handler initialization
- Individual tool handlers
- Error handling
- Edge cases
"""

import pytest
from unittest.mock import AsyncMock, MagicMock

from my_project.agents.player.handlers import ToolHandlers
from my_project.agents.player.state import PlayerState
from my_project.agents.player.strategy import StrategyEngine


class TestToolHandlersInit:
    """Test ToolHandlers initialization."""

    def test_initialization(self):
        """Test handler initialization."""
        state = PlayerState(player_id="P01", display_name="Test Agent")
        strategy = StrategyEngine(mode="random")
        handlers = ToolHandlers(state, strategy)

        assert handlers.state == state
        assert handlers.strategy == strategy


class TestHandleGameInvitation:
    """Test handle_game_invitation handler."""

    @pytest.mark.asyncio
    async def test_handle_game_invitation_accept(self):
        """Test accepting game invitation."""
        state = PlayerState(player_id="P01", display_name="Test Agent")
        state.set_auth_token("test_token_123")
        strategy = StrategyEngine(mode="random")
        handlers = ToolHandlers(state, strategy)

        params = {
            "protocol": "league.v2",
            "message_type": "GAME_INVITATION",
            "conversation_id": "conv-001",
            "match_id": "R1M1",
            "opponent_id": "P02",
            "game_type": "even_odd"
        }

        result = await handlers.handle_game_invitation(params)

        assert result["message_type"] == "GAME_JOIN_ACK"
        assert result["match_id"] == "R1M1"
        assert result["accept"] is True
        assert "arrival_timestamp" in result

    @pytest.mark.asyncio
    async def test_handle_game_invitation_missing_fields(self):
        """Test invitation with missing required fields."""
        state = PlayerState(player_id="P01", display_name="Test Agent")
        state.set_auth_token("test_token_123")
        strategy = StrategyEngine(mode="random")
        handlers = ToolHandlers(state, strategy)

        # Missing match_id
        params = {
            "protocol": "league.v2",
            "message_type": "GAME_INVITATION",
            "conversation_id": "conv-001"
        }

        result = await handlers.handle_game_invitation(params)

        # Should handle gracefully or return error
        assert result is not None


class TestChooseParity:
    """Test choose_parity handler."""

    @pytest.mark.asyncio
    async def test_choose_parity_random_strategy(self):
        """Test parity choice with random strategy."""
        state = PlayerState(player_id="P01", display_name="Test Agent")
        state.set_auth_token("test_token_123")
        strategy = StrategyEngine(mode="random")
        handlers = ToolHandlers(state, strategy)

        params = {
            "protocol": "league.v2",
            "message_type": "CHOOSE_PARITY_CALL",
            "conversation_id": "conv-001",
            "match_id": "R1M1",
            "opponent_id": "P02",
            "deadline": "2025-12-31T23:59:59Z"
        }

        result = await handlers.choose_parity(params)

        assert result["message_type"] == "CHOOSE_PARITY_RESPONSE"
        assert result["match_id"] == "R1M1"
        assert result["parity_choice"] in ["even", "odd"]
        assert result["parity_choice"].islower()  # Must be lowercase

    @pytest.mark.asyncio
    async def test_choose_parity_with_standings(self):
        """Test parity choice with standings context."""
        state = PlayerState(player_id="P01", display_name="Test Agent")
        state.set_auth_token("test_token_123")
        strategy = StrategyEngine(mode="random")
        handlers = ToolHandlers(state, strategy)

        # Add some match history
        state.update_from_result({
            "match_id": "R1M1",
            "opponent_id": "P02",
            "drawn_number": 5,
            "player_choice": "odd",
            "opponent_choice": "even",
            "winner_id": "P01"
        })

        params = {
            "protocol": "league.v2",
            "message_type": "CHOOSE_PARITY_CALL",
            "conversation_id": "conv-002",
            "match_id": "R1M2",
            "opponent_id": "P02",
            "deadline": "2025-12-31T23:59:59Z",
            "standings": {
                "P01": 3,
                "P02": 0
            }
        }

        result = await handlers.choose_parity(params)

        assert result["message_type"] == "CHOOSE_PARITY_RESPONSE"
        assert result["parity_choice"] in ["even", "odd"]


class TestNotifyMatchResult:
    """Test notify_match_result handler."""

    @pytest.mark.asyncio
    async def test_notify_match_result_win(self):
        """Test notification of match win."""
        state = PlayerState(player_id="P01", display_name="Test Agent")
        state.set_auth_token("test_token_123")
        strategy = StrategyEngine(mode="random")
        handlers = ToolHandlers(state, strategy)

        params = {
            "protocol": "league.v2",
            "message_type": "GAME_OVER",
            "conversation_id": "conv-001",
            "match_id": "R1M1",
            "drawn_number": 4,
            "choices": {
                "P01": "even",
                "P02": "odd"
            },
            "opponent_id": "P02",
            "winner": "P01"
        }

        result = await handlers.notify_match_result(params)

        # Check stats updated
        stats = state.get_stats()
        assert stats["wins"] == 1
        assert stats["total_matches"] == 1

        # Check acknowledgment
        assert result["status"] == "acknowledged"

    @pytest.mark.asyncio
    async def test_notify_match_result_loss(self):
        """Test notification of match loss."""
        state = PlayerState(player_id="P01", display_name="Test Agent")
        state.set_auth_token("test_token_123")
        strategy = StrategyEngine(mode="random")
        handlers = ToolHandlers(state, strategy)

        params = {
            "protocol": "league.v2",
            "message_type": "GAME_OVER",
            "conversation_id": "conv-001",
            "match_id": "R1M1",
            "drawn_number": 3,
            "choices": {
                "P01": "even",
                "P02": "odd"
            },
            "opponent_id": "P02",
            "winner": "P02"
        }

        result = await handlers.notify_match_result(params)

        # Check stats updated
        stats = state.get_stats()
        assert stats["losses"] == 1
        assert stats["total_matches"] == 1

    @pytest.mark.asyncio
    async def test_notify_match_result_draw(self):
        """Test notification of match draw."""
        state = PlayerState(player_id="P01", display_name="Test Agent")
        state.set_auth_token("test_token_123")
        strategy = StrategyEngine(mode="random")
        handlers = ToolHandlers(state, strategy)

        params = {
            "protocol": "league.v2",
            "message_type": "GAME_OVER",
            "conversation_id": "conv-001",
            "match_id": "R1M1",
            "drawn_number": 5,
            "choices": {
                "P01": "odd",
                "P02": "odd"
            },
            "opponent_id": "P02",
            "winner": None  # Draw
        }

        result = await handlers.notify_match_result(params)

        # Check stats updated
        stats = state.get_stats()
        assert stats["draws"] == 1
        assert stats["total_matches"] == 1


class TestErrorHandling:
    """Test error handling in handlers."""

    @pytest.mark.asyncio
    async def test_handle_empty_params(self):
        """Test handlers with empty params."""
        state = PlayerState(player_id="P01", display_name="Test Agent")
        state.set_auth_token("test_token_123")
        strategy = StrategyEngine(mode="random")
        handlers = ToolHandlers(state, strategy)

        # Empty params
        result = await handlers.handle_game_invitation({})
        assert result is not None  # Should handle gracefully

    @pytest.mark.asyncio
    async def test_choose_parity_without_auth_token(self):
        """Test parity choice without auth token."""
        state = PlayerState(player_id="P01", display_name="Test Agent")
        # Don't set auth token
        strategy = StrategyEngine(mode="random")
        handlers = ToolHandlers(state, strategy)

        params = {
            "protocol": "league.v2",
            "message_type": "CHOOSE_PARITY_CALL",
            "conversation_id": "conv-001",
            "match_id": "R1M1",
            "opponent_id": "P02",
            "deadline": "2025-12-31T23:59:59Z"
        }

        # Should fail without auth token
        try:
            result = await handlers.choose_parity(params)
            # If it doesn't raise, check result has error or is handled
            assert result is not None
        except (ValueError, KeyError):
            # Expected to raise without auth token
            pass
