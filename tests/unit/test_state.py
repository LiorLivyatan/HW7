"""
Unit Tests for PlayerState

Tests state management including statistics, match history, and persistence.

Coverage Target: 100% of state.py
"""

import pytest
import json
from pathlib import Path
import tempfile
from my_project.agents.player.state import PlayerState, MatchResult


class TestPlayerState:
    """Test suite for PlayerState building block."""

    def test_initialization(self):
        """Test PlayerState initialization."""
        state = PlayerState(player_id="P01", display_name="Test Agent")

        assert state.player_id == "P01"
        assert state.display_name == "Test Agent"
        assert state.auth_token is None
        assert state.registered is False
        assert state.stats == {"wins": 0, "draws": 0, "losses": 0, "total_points": 0, "total_matches": 0}
        assert state.match_history == []

    def test_initialization_empty_player_id_raises_error(self):
        """Test that empty player_id raises ValueError."""
        with pytest.raises(ValueError, match="player_id cannot be None or empty"):
            PlayerState(player_id="")

        with pytest.raises(ValueError, match="player_id cannot be None or empty"):
            PlayerState(player_id=None)

    def test_set_auth_token(self):
        """Test setting authentication token."""
        state = PlayerState(player_id="P01")
        state.set_auth_token("test-token-12345")

        assert state.auth_token == "test-token-12345"
        assert state.registered is True

    def test_update_from_result_win(self):
        """Test updating state from a win result."""
        state = PlayerState(player_id="P01")

        game_over_msg = {
            "match_id": "R1M1",
            "winner": "P01",  # We won!
            "drawn_number": 4,
            "choices": {
                "P01": "even",
                "P02": "odd"
            },
            "opponent_id": "P02"
        }

        state.update_from_result(game_over_msg)

        # Check statistics
        assert state.stats["wins"] == 1
        assert state.stats["draws"] == 0
        assert state.stats["losses"] == 0
        assert state.stats["total_points"] == 3  # Win = 3 points
        assert state.stats["total_matches"] == 1

        # Check match history
        assert len(state.match_history) == 1
        match = state.match_history[0]
        assert match.match_id == "R1M1"
        assert match.opponent_id == "P02"
        assert match.player_choice == "even"
        assert match.opponent_choice == "odd"
        assert match.drawn_number == 4
        assert match.result == "win"
        assert match.points_earned == 3

    def test_update_from_result_loss(self):
        """Test updating state from a loss result."""
        state = PlayerState(player_id="P01")

        game_over_msg = {
            "match_id": "R1M2",
            "winner": "P02",  # Opponent won
            "drawn_number": 7,
            "choices": {
                "P01": "even",
                "P02": "odd"
            },
            "opponent_id": "P02"
        }

        state.update_from_result(game_over_msg)

        # Check statistics
        assert state.stats["wins"] == 0
        assert state.stats["draws"] == 0
        assert state.stats["losses"] == 1
        assert state.stats["total_points"] == 0  # Loss = 0 points
        assert state.stats["total_matches"] == 1

        # Check match history
        match = state.match_history[0]
        assert match.result == "loss"
        assert match.points_earned == 0

    def test_update_from_result_draw(self):
        """Test updating state from a draw result."""
        state = PlayerState(player_id="P01")

        game_over_msg = {
            "match_id": "R1M3",
            "winner": None,  # Draw (both chose same parity)
            "drawn_number": 5,
            "choices": {
                "P01": "odd",
                "P02": "odd"
            },
            "opponent_id": "P02"
        }

        state.update_from_result(game_over_msg)

        # Check statistics
        assert state.stats["wins"] == 0
        assert state.stats["draws"] == 1
        assert state.stats["losses"] == 0
        assert state.stats["total_points"] == 1  # Draw = 1 point
        assert state.stats["total_matches"] == 1

        # Check match history
        match = state.match_history[0]
        assert match.result == "draw"
        assert match.points_earned == 1

    def test_update_from_result_multiple_matches(self):
        """Test updating state from multiple match results."""
        state = PlayerState(player_id="P01")

        # Win
        state.update_from_result({
            "match_id": "R1M1",
            "winner": "P01",
            "drawn_number": 4,
            "choices": {"P01": "even", "P02": "odd"},
            "opponent_id": "P02"
        })

        # Loss
        state.update_from_result({
            "match_id": "R1M2",
            "winner": "P03",
            "drawn_number": 7,
            "choices": {"P01": "even", "P03": "odd"},
            "opponent_id": "P03"
        })

        # Draw
        state.update_from_result({
            "match_id": "R1M3",
            "winner": None,
            "drawn_number": 5,
            "choices": {"P01": "odd", "P04": "odd"},
            "opponent_id": "P04"
        })

        # Another win
        state.update_from_result({
            "match_id": "R1M4",
            "winner": "P01",
            "drawn_number": 2,
            "choices": {"P01": "even", "P02": "odd"},
            "opponent_id": "P02"
        })

        # Check cumulative statistics
        assert state.stats["wins"] == 2
        assert state.stats["draws"] == 1
        assert state.stats["losses"] == 1
        assert state.stats["total_points"] == 7  # 3 + 0 + 1 + 3
        assert state.stats["total_matches"] == 4

        # Check match history
        assert len(state.match_history) == 4

    def test_get_stats(self):
        """Test get_stats returns copy of statistics."""
        state = PlayerState(player_id="P01")
        state.stats["wins"] = 5
        state.stats["total_points"] = 15

        stats = state.get_stats()

        assert stats["wins"] == 5
        assert stats["total_points"] == 15

        # Modifying returned stats shouldn't affect internal state
        stats["wins"] = 999
        assert state.stats["wins"] == 5  # Unchanged

    def test_get_win_rate_with_matches(self):
        """Test win rate calculation."""
        state = PlayerState(player_id="P01")
        state.stats = {
            "wins": 7,
            "draws": 2,
            "losses": 1,
            "total_matches": 10,
            "total_points": 23
        }

        win_rate = state.get_win_rate()
        assert win_rate == 0.7  # 7 wins / 10 matches

    def test_get_win_rate_no_matches(self):
        """Test win rate when no matches played."""
        state = PlayerState(player_id="P01")

        win_rate = state.get_win_rate()
        assert win_rate == 0.0

    def test_get_match_history_all(self):
        """Test get_match_history returns all matches."""
        state = PlayerState(player_id="P01")

        # Add 5 matches
        for i in range(5):
            state.update_from_result({
                "match_id": f"R1M{i+1}",
                "winner": "P01" if i % 2 == 0 else "P02",
                "drawn_number": 4,
                "choices": {"P01": "even", "P02": "odd"},
                "opponent_id": "P02"
            })

        history = state.get_match_history()
        assert len(history) == 5

    def test_get_match_history_with_limit(self):
        """Test get_match_history with limit."""
        state = PlayerState(player_id="P01")

        # Add 10 matches
        for i in range(10):
            state.update_from_result({
                "match_id": f"R1M{i+1}",
                "winner": "P01",
                "drawn_number": 4,
                "choices": {"P01": "even", "P02": "odd"},
                "opponent_id": "P02"
            })

        # Get only last 3
        history = state.get_match_history(limit=3)
        assert len(history) == 3
        # Should be most recent (last 3)
        assert history[0]["match_id"] == "R1M8"
        assert history[1]["match_id"] == "R1M9"
        assert history[2]["match_id"] == "R1M10"

    def test_get_opponent_history(self):
        """Test get_opponent_history filters by opponent."""
        state = PlayerState(player_id="P01")

        # Matches against P02
        state.update_from_result({
            "match_id": "R1M1",
            "winner": "P01",
            "drawn_number": 4,
            "choices": {"P01": "even", "P02": "odd"},
            "opponent_id": "P02"
        })
        state.update_from_result({
            "match_id": "R1M3",
            "winner": "P02",
            "drawn_number": 7,
            "choices": {"P01": "even", "P02": "odd"},
            "opponent_id": "P02"
        })

        # Match against P03
        state.update_from_result({
            "match_id": "R1M2",
            "winner": "P03",
            "drawn_number": 5,
            "choices": {"P01": "odd", "P03": "even"},
            "opponent_id": "P03"
        })

        # Get P02 matches only
        p02_matches = state.get_opponent_history("P02")
        assert len(p02_matches) == 2
        assert all(m["opponent_id"] == "P02" for m in p02_matches)

        # Get P03 matches only
        p03_matches = state.get_opponent_history("P03")
        assert len(p03_matches) == 1
        assert p03_matches[0]["opponent_id"] == "P03"

    def test_max_history_entries_trimming(self):
        """Test that history is trimmed to max_history_entries."""
        state = PlayerState(player_id="P01", max_history_entries=5)

        # Add 10 matches
        for i in range(10):
            state.update_from_result({
                "match_id": f"R1M{i+1}",
                "winner": "P01",
                "drawn_number": 4,
                "choices": {"P01": "even", "P02": "odd"},
                "opponent_id": "P02"
            })

        # Should only keep last 5
        assert len(state.match_history) == 5
        # Should be matches 6-10
        assert state.match_history[0].match_id == "R1M6"
        assert state.match_history[-1].match_id == "R1M10"

    def test_to_dict(self):
        """Test serialization to dictionary."""
        state = PlayerState(player_id="P01", display_name="Test Agent")
        state.set_auth_token("token-12345")
        state.update_from_result({
            "match_id": "R1M1",
            "winner": "P01",
            "drawn_number": 4,
            "choices": {"P01": "even", "P02": "odd"},
            "opponent_id": "P02"
        })

        state_dict = state.to_dict()

        assert state_dict["player_id"] == "P01"
        assert state_dict["display_name"] == "Test Agent"
        assert state_dict["auth_token"] == "token-12345"
        assert state_dict["registered"] is True
        assert state_dict["stats"]["wins"] == 1
        assert len(state_dict["match_history"]) == 1
        assert "last_updated" in state_dict


class TestPersistence:
    """Test state persistence to file."""

    def test_persistence_save_and_load(self):
        """Test saving and loading state from file."""
        with tempfile.TemporaryDirectory() as tmpdir:
            state_file = Path(tmpdir) / "state.json"

            # Create state with persistence enabled
            state1 = PlayerState(
                player_id="P01",
                display_name="Test Agent",
                persistence_enabled=True,
                state_file_path=str(state_file)
            )

            # Add some data
            state1.set_auth_token("token-12345")
            state1.update_from_result({
                "match_id": "R1M1",
                "winner": "P01",
                "drawn_number": 4,
                "choices": {"P01": "even", "P02": "odd"},
                "opponent_id": "P02"
            })

            # Create new state instance loading from same file
            state2 = PlayerState(
                player_id="P01",
                display_name="Test Agent",
                persistence_enabled=True,
                state_file_path=str(state_file)
            )

            # Should have loaded persisted data
            assert state2.auth_token == "token-12345"
            assert state2.stats["wins"] == 1
            assert len(state2.match_history) == 1

    def test_persistence_disabled_no_file_created(self):
        """Test that no file is created when persistence is disabled."""
        with tempfile.TemporaryDirectory() as tmpdir:
            state_file = Path(tmpdir) / "state.json"

            state = PlayerState(
                player_id="P01",
                persistence_enabled=False,  # Disabled
                state_file_path=str(state_file)
            )

            state.set_auth_token("token-12345")

            # File should NOT be created
            assert not state_file.exists()


class TestEdgeCases:
    """Test edge cases and boundary conditions."""

    def test_empty_match_history(self):
        """Test operations on empty match history."""
        state = PlayerState(player_id="P01")

        assert state.get_match_history() == []
        assert state.get_opponent_history("P02") == []
        assert state.get_win_rate() == 0.0

    def test_match_without_opponent_id(self):
        """Test handling match result without opponent_id."""
        state = PlayerState(player_id="P01")

        game_over_msg = {
            "match_id": "R1M1",
            "winner": "P01",
            "drawn_number": 4,
            "choices": {"P01": "even"},
            # Missing opponent_id
        }

        state.update_from_result(game_over_msg)

        # Should still work, using "unknown" opponent
        assert len(state.match_history) == 1
        assert state.match_history[0].opponent_id == "unknown"

    def test_very_long_player_id(self):
        """Test with very long player ID."""
        long_id = "P" + "0" * 100
        state = PlayerState(player_id=long_id)

        assert state.player_id == long_id
